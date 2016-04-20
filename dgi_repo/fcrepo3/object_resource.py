"""
Class file for the implementation of the object resource.
"""
import logging

import dateutil.parser
import falcon
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
from dgi_repo.fcrepo3.exceptions import ObjectExistsError
from dgi_repo.database.utilities import get_connection
from dgi_repo.fcrepo3 import api, foxml, relations
from dgi_repo.fcrepo3.utilities import resolve_log

logger = logging.getLogger(__name__)


class ObjectResource(api.ObjectResource):
    """
    Provide the object endpoint.
    """

    def on_post(self, req, resp, pid):
        """
        Create the new object.
        """
        super().on_post(req, resp, pid)
        with get_connection(ISOLATION_LEVEL_READ_COMMITTED) as conn:
            with conn.cursor() as cursor:
                xml = req.get_param('file')
                if xml is not None:
                    try:
                        # Import FOXML, getting PID.
                        pid = foxml.import_foxml(
                            xml.file,
                            req.env['wsgi.identity'].source_id,
                            cursor=cursor
                        )
                        logger.info('Imported %s', pid)
                    except ObjectExistsError as e:
                        self._send_500(e.pid, resp)
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
                    except IntegrityError:
                        self._send_500()
                    if log is not None:
                        logger.info('Ingested %s with log: "%s".', pid, log)
                    foxml.create_default_dc_ds(cursor.fetchone()[0], pid,
                                               cursor=cursor)

                resp.body = 'Ingested {}'.format(pid)
        return

    def on_get(self, req, resp, pid):
        """
        Generate the object profile XML.

        This does not respect asOfDateTime from Fedora.
        """
        super().on_get(req, resp, pid)

        with get_connection() as conn:
            with conn.cursor() as cursor:
                try:
                    object_reader.object_info_from_raw(pid, cursor=cursor)
                except TypeError:
                    self._send_404(pid, resp)

                # Get object info.
                object_info = cursor.fetchone()
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
                owner = cursor.fetchone()['username']

                resp.body = self._get_object_profile(
                    pid,
                    object_info['label'],
                    models,
                    object_info['created'],
                    object_info['modified'],
                    object_info['state'],
                    owner
                )

                logger.info('Retrieved object: %s.', pid)
        return

    def on_put(self, req, resp, pid):
        """
        Commit the object modification.
        """
        super().on_put(req, resp, pid)
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # Get current object info.
                try:
                    object_reader.object_info_from_raw(pid, cursor=cursor)
                except TypeError:
                    self._send_404(pid, resp)

                object_info = dict(cursor.fetchone())

                # Check modified date param, exiting if needed.
                modified_date = req.get_param('lastModifiedDate')
                if modified_date is not None:
                    modified_date = utils.check_datetime_timezone(
                        dateutil.parser.parse(modified_date)
                    )

                    if object_info['modified'] > modified_date:
                        logger.info(('{} lastModifiedDate ({}) is more recent '
                                    'than the request ({})').format(
                                        pid,
                                        object_info['modified'].isoformat(),
                                        modified_date.isoformat()
                        ))
                        # @XXX Raising HTTPError over HTTPConflict because we
                        # don't have  a title and description for HTTPConflict.
                        raise falcon.HTTPError('409 Conflict')

                # Create old version of object.
                if object_info['versioned']:
                    old_object_info = object_info
                    old_object_info['committed'] = object_info['modified']
                    old_object_info['object'] = object_info['id']
                    del old_object_info['id']
                    object_writer.upsert_old_object(
                        old_object_info,
                        cursor=cursor
                    )
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
                if modified_date is not None:
                    resp.body = modified_date.isoformat()
                    new_object_info['modified'] = req.get_param(
                        'lastModifiedDate',
                        default=object_info['modified']
                    )
                else:
                    del new_object_info['modified']
                object_writer.upsert_object(
                    new_object_info,
                    cursor=cursor
                )

                logger.info('Modified %s', pid)

    def on_delete(self, req, resp, pid):
        """
        Purge the object.

        @TODO: handle logMessage when audit is dealt with.
        """
        super().on_delete(req, resp, pid)
        with get_connection() as conn:
            with conn.cursor() as cursor:
                try:
                    object_reader.object_info_from_raw(pid, cursor)
                    object_id = cursor.fetchone()['id']
                    object_purger.delete_object(object_id, cursor)
                except TypeError:
                    self._send_404(pid, resp)

                resp.body = 'Purged {}'.format(pid)
                logger.info('Purged %s', pid)

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
