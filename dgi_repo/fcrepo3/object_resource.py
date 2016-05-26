"""
Class file for the implementation of the object resource.
"""
from psycopg2 import IntegrityError
from psycopg2.extensions import ISOLATION_LEVEL_READ_COMMITTED

import dgi_repo.database.write.repo_objects as object_writer
import dgi_repo.database.read.object_relations as object_relation_reader
import dgi_repo.database.delete.repo_objects as object_purger
import dgi_repo.database.read.repo_objects as object_reader
import dgi_repo.database.write.sources as source_writer
import dgi_repo.database.read.sources as source_reader
from dgi_repo import utilities as utils
from dgi_repo.configuration import configuration as _config
from dgi_repo.exceptions import (ObjectExistsError, ObjectDoesNotExistError,
                                 ObjectConflictsError)
from dgi_repo.database.utilities import get_connection
from dgi_repo.fcrepo3 import api, foxml, relations
from dgi_repo.fcrepo3.utilities import resolve_log


class ObjectResource(api.ObjectResource):
    """
    Provide the object endpoint.
    """

    def _create_object(self, req, pid):
        """
        Create the new object.
        """
        conn = get_connection(ISOLATION_LEVEL_READ_COMMITTED)
        with conn, conn.cursor() as cursor:
            if not pid or pid == 'new':
                import_pid = None
            else:
                import_pid = pid
            try:
                # Import FOXML, getting PID.
                pid = foxml.import_foxml(
                    req.get_param('file').file,
                    req.env['wsgi.identity'].source_id,
                    pid=import_pid,
                    cursor=cursor
                )
            except AttributeError:
                if req.content_length:
                    # Try to import FOXML from request body.
                    pid = foxml.import_foxml(
                        req.stream,
                        req.env['wsgi.identity'].source_id,
                        pid=import_pid,
                        cursor=cursor
                    )
                else:
                    if not pid or pid == 'new':
                        # Generate PID.
                        raw_namespace = req.get_param(
                            'namespace',
                            default=_config['default_namespace']
                        )
                        object_writer.get_pid_id(raw_namespace, cursor=cursor)
                        pid_id, namespace = cursor.fetchone()
                        pid = utils.make_pid(raw_namespace, pid_id)
                    else:
                        # Reserve given PID in namespace.
                        raw_namespace, pid_id = utils.break_pid(pid)
                        object_reader.namespace_id(raw_namespace,
                                                   cursor=cursor)
                        try:
                            namespace = cursor.fetchone()[0]
                        except TypeError:
                            # @XXX burns the first PID in a namespace.
                            object_writer.get_pid_id(raw_namespace,
                                                     cursor=cursor)
                            namespace = cursor.fetchone()[1]

                        # Jump up PIDs if needed.
                        object_writer.jump_pids(namespace, pid_id,
                                                cursor=cursor)

                    # Figure out the owner's DB ID.
                    owner = self._resolve_owner(req, cursor)

                    # Figure out the log's DB ID.
                    log = resolve_log(req, cursor)

                    try:
                        object_writer.write_object(
                            {
                                'namespace': namespace,
                                'state': req.get_param('state', default='A'),
                                'label': req.get_param('label'),
                                'log': log,
                                'pid_id': pid_id,
                                'owner': owner,
                            },
                            cursor=cursor
                        )
                    except IntegrityError as e:
                        raise ObjectExistsError(pid) from e
                    foxml.create_default_dc_ds(cursor.fetchone()[0], pid,
                                               cursor=cursor)
        conn.close()

        return pid

    def _get_object(self, req, pid):
        """
        Generate the object profile XML.

        This does not respect asOfDateTime from Fedora.
        """
        with get_connection() as conn, conn.cursor() as cursor:
            # Get object info.
            object_info = object_reader.object_info_from_raw(
                pid,
                cursor=cursor
            ).fetchone()
            if object_info is None:
                raise ObjectDoesNotExistError(pid)
            object_relation_reader.read_relationship(
                relations.FEDORA_MODEL_NAMESPACE,
                relations.HAS_MODEL_PREDICATE,
                object_info['id'],
                cursor=cursor
            )
            model_info = cursor.fetchall()
            models = set()
            for rdf_object_info in model_info:
                cursor = object_reader.object_info(
                    rdf_object_info['rdf_object'],
                    cursor=cursor
                )
                model_object_info = cursor.fetchone()

                object_reader.namespace_info(
                    model_object_info['namespace'],
                    cursor=cursor
                )
                namespace = cursor.fetchone()['namespace']

                model_pid = utils.make_pid(namespace,
                                           model_object_info['pid_id'])
                models.add('info:fedora/{}'.format(model_pid))
            source_reader.user(object_info['owner'], cursor=cursor)
            owner = cursor.fetchone()['name']

            return (
                pid,
                object_info['label'],
                models,
                object_info['created'],
                object_info['modified'],
                object_info['state'],
                owner
            )

    def _update_object(self, req, pid):
        """
        Commit the object modification.
        """
        modified = None
        with get_connection() as conn, conn.cursor() as cursor:
            # Get current object info.
            object_info = object_reader.object_info_from_raw(pid, cursor=cursor
                                                             ).fetchone()
            if not object_info:
                raise ObjectDoesNotExistError(pid)

            object_info = dict(object_info)

            # Check modified date param, exiting if needed.
            modified_date = req.get_param('lastModifiedDate')
            if modified_date is not None:
                modified_date = utils.iso8601_to_datetime(modified_date)
                if object_info['modified'] > modified_date:
                    raise ObjectConflictsError(pid, object_info['modified'],
                                               modified_date)

            # Create old version of object.
            if object_info['versioned']:
                old_object_info = object_info
                old_object_info['committed'] = object_info['modified']
                old_object_info['object'] = object_info['id']
                del old_object_info['id']
                object_writer.upsert_old_object(old_object_info, cursor=cursor)
                cursor.fetchone()

            # Update object info.
            new_object_info = object_info
            new_object_info['label'] = req.get_param(
                'label',
                default=object_info['label']
            )
            new_object_info['state'] = req.get_param(
                'state',
                default=object_info['state']
            )
            if req.get_param('ownerId') is not None:
                new_object_info['owner'] = self._resolve_owner(req, cursor)
            if req.get_param('logMessage') is not None:
                new_object_info['log'] = resolve_log(req, cursor)
            del new_object_info['modified']
            object_id = object_writer.upsert_object(new_object_info,
                                                    cursor=cursor
                                                    ).fetchone()['id']
            return object_reader.object_info(object_id, cursor=cursor
                                             ).fetchone()['modified']

    def _purge_object(self, req, pid):
        """
        Purge the object.

        @TODO: handle logMessage when audit is dealt with.
        """
        with get_connection() as conn, conn.cursor() as cursor:
            object_info = object_reader.object_info_from_raw(pid,
                                                             cursor).fetchone()

            if object_info is None:
                raise ObjectDoesNotExistError(pid)
            if object_relation_reader.is_object_referenced(object_info['id'],
                                                           cursor):
                raise ValueError('Not purging {} as it is referenced.'
                                 .format(pid))

            object_purger.delete_object(object_info['id'], cursor)

    def _resolve_owner(self, req, cursor):
        """
        Get the DB owner from the req.
        """
        raw_owner = req.get_param('ownerId')
        if raw_owner:
            source_writer.upsert_user(
                {'name': raw_owner,
                 'source': req.env['wsgi.identity'].source_id},
                cursor=cursor
            )
            owner = cursor.fetchone()[0]
        else:
            owner = req.env['wsgi.identity'].user_id
        return owner
