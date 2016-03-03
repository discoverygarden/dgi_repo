--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.1
-- Dumped by pg_dump version 9.5.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

SET search_path = public, pg_catalog;

--
-- Name: checksum_algorithims; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE checksum_algorithims AS ENUM (
    'MD5',
    'SHA-1',
    'SHA-256',
    'SHA-512'
);


--
-- Name: TYPE checksum_algorithims; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TYPE checksum_algorithims IS 'Types of checksums.';


--
-- Name: datastream_control_group; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE datastream_control_group AS ENUM (
    'R',
    'E',
    'I',
    'M'
);


--
-- Name: TYPE datastream_control_group; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TYPE datastream_control_group IS 'Control group for datastreams. Legacy from Fedora.';


--
-- Name: state; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE state AS ENUM (
    'I',
    'A',
    'D'
);


--
-- Name: TYPE state; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TYPE state IS 'State of the object or datastream.  This is legacy from Fedora.';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: checksums; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE checksums (
    checksum character(128) NOT NULL,
    id bigint NOT NULL,
    uri bigint NOT NULL,
    type checksum_algorithims NOT NULL
);


--
-- Name: TABLE checksums; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE checksums IS 'All checksums stored by the system.';


--
-- Name: COLUMN checksums.checksum; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN checksums.checksum IS 'The stored checksum.';


--
-- Name: COLUMN checksums.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN checksums.id IS 'The database ID for the checksum';


--
-- Name: COLUMN checksums.uri; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN checksums.uri IS 'The database id of the URI that the checksum belongs to.';


--
-- Name: COLUMN checksums.type; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN checksums.type IS 'The type of checksum.';


--
-- Name: checksums_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE checksums_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: checksums_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE checksums_id_seq OWNED BY checksums.id;


--
-- Name: datastream_is_manageable_by_role_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE datastream_is_manageable_by_role_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: datastream_is_manageable_by_role; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE datastream_is_manageable_by_role (
    id bigint DEFAULT nextval('datastream_is_manageable_by_role_id_seq'::regclass) NOT NULL,
    rdf_subject bigint NOT NULL,
    rdf_object bigint NOT NULL
);


--
-- Name: TABLE datastream_is_manageable_by_role; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE datastream_is_manageable_by_role IS 'Maps what roles can manage a datastream.';


--
-- Name: COLUMN datastream_is_manageable_by_role.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN datastream_is_manageable_by_role.id IS 'The database ID of the security rule.';


--
-- Name: COLUMN datastream_is_manageable_by_role.rdf_subject; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN datastream_is_manageable_by_role.rdf_subject IS 'Database ID of the datastream.';


--
-- Name: COLUMN datastream_is_manageable_by_role.rdf_object; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN datastream_is_manageable_by_role.rdf_object IS 'Role that can manage the datastream.';


--
-- Name: datastream_is_manageable_by_user; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE datastream_is_manageable_by_user (
    id bigint DEFAULT nextval('datastream_is_manageable_by_role_id_seq'::regclass) NOT NULL,
    rdf_subject bigint NOT NULL,
    rdf_object bigint NOT NULL
);


--
-- Name: TABLE datastream_is_manageable_by_user; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE datastream_is_manageable_by_user IS 'Maps what users can manage a datastream.';


--
-- Name: COLUMN datastream_is_manageable_by_user.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN datastream_is_manageable_by_user.id IS 'The database ID of the security rule.';


--
-- Name: COLUMN datastream_is_manageable_by_user.rdf_subject; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN datastream_is_manageable_by_user.rdf_subject IS 'Database ID of the datastream.';


--
-- Name: COLUMN datastream_is_manageable_by_user.rdf_object; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN datastream_is_manageable_by_user.rdf_object IS 'User that can manage the datastream.';


--
-- Name: datastream_is_manageable_by_user_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE datastream_is_manageable_by_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: datastream_is_viewable_by_role_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE datastream_is_viewable_by_role_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: datastream_is_viewable_by_role; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE datastream_is_viewable_by_role (
    id bigint DEFAULT nextval('datastream_is_viewable_by_role_id_seq'::regclass) NOT NULL,
    rdf_subject bigint NOT NULL,
    rdf_object bigint NOT NULL
);


--
-- Name: TABLE datastream_is_viewable_by_role; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE datastream_is_viewable_by_role IS 'Maps what roles can view a datastream.';


--
-- Name: COLUMN datastream_is_viewable_by_role.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN datastream_is_viewable_by_role.id IS 'The database ID of the security rule.';


--
-- Name: COLUMN datastream_is_viewable_by_role.rdf_subject; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN datastream_is_viewable_by_role.rdf_subject IS 'Database ID of the datastream.';


--
-- Name: COLUMN datastream_is_viewable_by_role.rdf_object; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN datastream_is_viewable_by_role.rdf_object IS 'Role that can view the datastream.';


--
-- Name: datastream_is_viewable_by_user_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE datastream_is_viewable_by_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: datastream_is_viewable_by_user; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE datastream_is_viewable_by_user (
    id bigint DEFAULT nextval('datastream_is_viewable_by_user_id_seq'::regclass) NOT NULL,
    rdf_subject bigint NOT NULL,
    rdf_object bigint NOT NULL
);


--
-- Name: TABLE datastream_is_viewable_by_user; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE datastream_is_viewable_by_user IS 'Maps what users can view a datastream.';


--
-- Name: COLUMN datastream_is_viewable_by_user.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN datastream_is_viewable_by_user.id IS 'The database ID of the security rule.';


--
-- Name: COLUMN datastream_is_viewable_by_user.rdf_subject; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN datastream_is_viewable_by_user.rdf_subject IS 'Database ID of the datastream.';


--
-- Name: COLUMN datastream_is_viewable_by_user.rdf_object; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN datastream_is_viewable_by_user.rdf_object IS 'User that can view the datastream.';


--
-- Name: datastream_relationships; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE datastream_relationships (
    id bigint NOT NULL,
    subject bigint NOT NULL,
    predicate_id bigint NOT NULL,
    rdf_object character varying(1024)
);


--
-- Name: TABLE datastream_relationships; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE datastream_relationships IS 'Datastream relations not captured in other tables.';


--
-- Name: COLUMN datastream_relationships.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN datastream_relationships.id IS 'Database ID of the datastream relationship.';


--
-- Name: COLUMN datastream_relationships.subject; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN datastream_relationships.subject IS 'The subject of the relationship.';


--
-- Name: COLUMN datastream_relationships.predicate_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN datastream_relationships.predicate_id IS 'The predicate of the relationship.';


--
-- Name: COLUMN datastream_relationships.rdf_object; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN datastream_relationships.rdf_object IS 'The object of the relationship.';


--
-- Name: datastream_relationships_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE datastream_relationships_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: datastream_relationships_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE datastream_relationships_id_seq OWNED BY datastream_relationships.id;


--
-- Name: datastreams; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE datastreams (
    id bigint NOT NULL,
    object_id bigint NOT NULL,
    label text,
    dsid character varying(255) NOT NULL,
    resource_id bigint,
    versioned boolean DEFAULT false NOT NULL,
    archival boolean DEFAULT false NOT NULL,
    control_group datastream_control_group NOT NULL,
    state state NOT NULL,
    log bigint,
    modified timestamp with time zone,
    created timestamp with time zone NOT NULL
);


--
-- Name: TABLE datastreams; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE datastreams IS 'File containers.';


--
-- Name: COLUMN datastreams.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN datastreams.id IS 'Database id for datastreams.';


--
-- Name: COLUMN datastreams.object_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN datastreams.object_id IS 'The database ID of the object that the datastream belongs to.';


--
-- Name: COLUMN datastreams.label; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN datastreams.label IS 'Human readable label for the datastream.';


--
-- Name: COLUMN datastreams.dsid; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN datastreams.dsid IS 'Machine name for the datastream.';


--
-- Name: COLUMN datastreams.resource_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN datastreams.resource_id IS 'The URI to the datastream content.';


--
-- Name: COLUMN datastreams.versioned; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN datastreams.versioned IS 'Whether or not the datstream should be versioned.';


--
-- Name: COLUMN datastreams.archival; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN datastreams.archival IS 'Whether or not a datastream is necessary for archival purposes.';


--
-- Name: COLUMN datastreams.control_group; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN datastreams.control_group IS 'Control goup of the datastream.';


--
-- Name: COLUMN datastreams.state; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN datastreams.state IS 'State of the datastream.';


--
-- Name: COLUMN datastreams.log; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN datastreams.log IS 'Current log entry.';


--
-- Name: COLUMN datastreams.modified; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN datastreams.modified IS 'Time the datastream was last modified.';


--
-- Name: COLUMN datastreams.created; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN datastreams.created IS 'Time the datastream was created.';


--
-- Name: datastreams_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE datastreams_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: datastreams_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE datastreams_id_seq OWNED BY datastreams.id;


--
-- Name: date_issued; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE date_issued (
    id bigint NOT NULL,
    rdf_subject bigint NOT NULL,
    rdf_object timestamp with time zone NOT NULL
);


--
-- Name: TABLE date_issued; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE date_issued IS 'Table to represent date issued relations.';


--
-- Name: COLUMN date_issued.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN date_issued.id IS 'Database ID of the relation.';


--
-- Name: COLUMN date_issued.rdf_subject; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN date_issued.rdf_subject IS 'Subject of the relation.';


--
-- Name: COLUMN date_issued.rdf_object; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN date_issued.rdf_object IS 'The date the item was issued.';


--
-- Name: date_issued_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE date_issued_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: date_issued_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE date_issued_id_seq OWNED BY date_issued.id;


--
-- Name: dc_contributor_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE dc_contributor_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: dc_contributor; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE dc_contributor (
    id bigint DEFAULT nextval('dc_contributor_id_seq'::regclass) NOT NULL,
    rdf_subject bigint NOT NULL,
    rdf_object character varying(1024) NOT NULL
);


--
-- Name: TABLE dc_contributor; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE dc_contributor IS 'Table to represent DC contributor relations.';


--
-- Name: COLUMN dc_contributor.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN dc_contributor.id IS 'Database ID of the relation.';


--
-- Name: COLUMN dc_contributor.rdf_subject; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN dc_contributor.rdf_subject IS 'Subject of the relation.';


--
-- Name: COLUMN dc_contributor.rdf_object; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN dc_contributor.rdf_object IS 'The subject of the relation.';


--
-- Name: dc_coverage_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE dc_coverage_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: dc_coverage; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE dc_coverage (
    id bigint DEFAULT nextval('dc_coverage_id_seq'::regclass) NOT NULL,
    rdf_subject bigint NOT NULL,
    rdf_object character varying(1024) NOT NULL
);


--
-- Name: TABLE dc_coverage; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE dc_coverage IS 'Table to represent DC coverage relations.';


--
-- Name: COLUMN dc_coverage.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN dc_coverage.id IS 'Database ID of the relation.';


--
-- Name: COLUMN dc_coverage.rdf_subject; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN dc_coverage.rdf_subject IS 'Subject of the relation.';


--
-- Name: COLUMN dc_coverage.rdf_object; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN dc_coverage.rdf_object IS 'The subject of the relation.';


--
-- Name: dc_creator_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE dc_creator_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: dc_creator; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE dc_creator (
    id bigint DEFAULT nextval('dc_creator_id_seq'::regclass) NOT NULL,
    rdf_subject bigint NOT NULL,
    rdf_object character varying(1024) NOT NULL
);


--
-- Name: TABLE dc_creator; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE dc_creator IS 'Table to represent DC creator relations.';


--
-- Name: COLUMN dc_creator.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN dc_creator.id IS 'Database ID of the relation.';


--
-- Name: COLUMN dc_creator.rdf_subject; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN dc_creator.rdf_subject IS 'Subject of the relation.';


--
-- Name: COLUMN dc_creator.rdf_object; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN dc_creator.rdf_object IS 'The subject of the relation.';


--
-- Name: dc_date_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE dc_date_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: dc_date; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE dc_date (
    id bigint DEFAULT nextval('dc_date_id_seq'::regclass) NOT NULL,
    rdf_subject bigint NOT NULL,
    rdf_object character varying(1024) NOT NULL
);


--
-- Name: TABLE dc_date; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE dc_date IS 'Table to represent DC date relations.';


--
-- Name: COLUMN dc_date.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN dc_date.id IS 'Database ID of the relation.';


--
-- Name: COLUMN dc_date.rdf_subject; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN dc_date.rdf_subject IS 'Subject of the relation.';


--
-- Name: COLUMN dc_date.rdf_object; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN dc_date.rdf_object IS 'The subject of the relation.';


--
-- Name: dc_description_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE dc_description_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: dc_description; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE dc_description (
    id bigint DEFAULT nextval('dc_description_id_seq'::regclass) NOT NULL,
    rdf_subject bigint NOT NULL,
    rdf_object character varying(1024) NOT NULL
);


--
-- Name: TABLE dc_description; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE dc_description IS 'Table to represent DC description relations.';


--
-- Name: COLUMN dc_description.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN dc_description.id IS 'Database ID of the relation.';


--
-- Name: COLUMN dc_description.rdf_subject; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN dc_description.rdf_subject IS 'Subject of the relation.';


--
-- Name: COLUMN dc_description.rdf_object; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN dc_description.rdf_object IS 'The subject of the relation.';


--
-- Name: dc_format_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE dc_format_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: dc_format; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE dc_format (
    id bigint DEFAULT nextval('dc_format_id_seq'::regclass) NOT NULL,
    rdf_subject bigint NOT NULL,
    rdf_object character varying(1024) NOT NULL
);


--
-- Name: TABLE dc_format; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE dc_format IS 'Table to represent DC format relations.';


--
-- Name: COLUMN dc_format.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN dc_format.id IS 'Database ID of the relation.';


--
-- Name: COLUMN dc_format.rdf_subject; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN dc_format.rdf_subject IS 'Subject of the relation.';


--
-- Name: COLUMN dc_format.rdf_object; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN dc_format.rdf_object IS 'The subject of the relation.';


--
-- Name: dc_identifier_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE dc_identifier_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: dc_identifier; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE dc_identifier (
    id bigint DEFAULT nextval('dc_identifier_id_seq'::regclass) NOT NULL,
    rdf_subject bigint NOT NULL,
    rdf_object character varying(1024) NOT NULL
);


--
-- Name: TABLE dc_identifier; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE dc_identifier IS 'Table to represent DC identifier relations.';


--
-- Name: COLUMN dc_identifier.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN dc_identifier.id IS 'Database ID of the relation.';


--
-- Name: COLUMN dc_identifier.rdf_subject; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN dc_identifier.rdf_subject IS 'Subject of the relation.';


--
-- Name: COLUMN dc_identifier.rdf_object; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN dc_identifier.rdf_object IS 'The subject of the relation.';


--
-- Name: dc_language_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE dc_language_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: dc_language; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE dc_language (
    id bigint DEFAULT nextval('dc_language_id_seq'::regclass) NOT NULL,
    rdf_subject bigint NOT NULL,
    rdf_object character varying(1024) NOT NULL
);


--
-- Name: TABLE dc_language; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE dc_language IS 'Table to represent DC language relations.';


--
-- Name: COLUMN dc_language.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN dc_language.id IS 'Database ID of the relation.';


--
-- Name: COLUMN dc_language.rdf_subject; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN dc_language.rdf_subject IS 'Subject of the relation.';


--
-- Name: COLUMN dc_language.rdf_object; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN dc_language.rdf_object IS 'The subject of the relation.';


--
-- Name: dc_publisher_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE dc_publisher_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: dc_publisher; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE dc_publisher (
    id bigint DEFAULT nextval('dc_publisher_id_seq'::regclass) NOT NULL,
    rdf_subject bigint NOT NULL,
    rdf_object character varying(1024) NOT NULL
);


--
-- Name: TABLE dc_publisher; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE dc_publisher IS 'Table to represent DC publisher relations.';


--
-- Name: COLUMN dc_publisher.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN dc_publisher.id IS 'Database ID of the relation.';


--
-- Name: COLUMN dc_publisher.rdf_subject; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN dc_publisher.rdf_subject IS 'Subject of the relation.';


--
-- Name: COLUMN dc_publisher.rdf_object; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN dc_publisher.rdf_object IS 'The subject of the relation.';


--
-- Name: dc_relation_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE dc_relation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: dc_relation; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE dc_relation (
    id bigint DEFAULT nextval('dc_relation_id_seq'::regclass) NOT NULL,
    rdf_subject bigint NOT NULL,
    rdf_object character varying(1024) NOT NULL
);


--
-- Name: TABLE dc_relation; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE dc_relation IS 'Table to represent DC relation relations.';


--
-- Name: COLUMN dc_relation.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN dc_relation.id IS 'Database ID of the relation.';


--
-- Name: COLUMN dc_relation.rdf_subject; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN dc_relation.rdf_subject IS 'Subject of the relation.';


--
-- Name: COLUMN dc_relation.rdf_object; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN dc_relation.rdf_object IS 'The subject of the relation.';


--
-- Name: dc_rights_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE dc_rights_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: dc_rights; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE dc_rights (
    id bigint DEFAULT nextval('dc_rights_id_seq'::regclass) NOT NULL,
    rdf_subject bigint NOT NULL,
    rdf_object character varying(1024) NOT NULL
);


--
-- Name: TABLE dc_rights; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE dc_rights IS 'Table to represent DC rights relations.';


--
-- Name: COLUMN dc_rights.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN dc_rights.id IS 'Database ID of the relation.';


--
-- Name: COLUMN dc_rights.rdf_subject; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN dc_rights.rdf_subject IS 'Subject of the relation.';


--
-- Name: COLUMN dc_rights.rdf_object; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN dc_rights.rdf_object IS 'The subject of the relation.';


--
-- Name: dc_source_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE dc_source_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: dc_source; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE dc_source (
    id bigint DEFAULT nextval('dc_source_id_seq'::regclass) NOT NULL,
    rdf_subject bigint NOT NULL,
    rdf_object character varying(1024) NOT NULL
);


--
-- Name: TABLE dc_source; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE dc_source IS 'Table to represent DC source relations.';


--
-- Name: COLUMN dc_source.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN dc_source.id IS 'Database ID of the relation.';


--
-- Name: COLUMN dc_source.rdf_subject; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN dc_source.rdf_subject IS 'Subject of the relation.';


--
-- Name: COLUMN dc_source.rdf_object; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN dc_source.rdf_object IS 'The subject of the relation.';


--
-- Name: dc_subject_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE dc_subject_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: dc_subject; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE dc_subject (
    id bigint DEFAULT nextval('dc_subject_id_seq'::regclass) NOT NULL,
    rdf_subject bigint NOT NULL,
    rdf_object character varying(1024) NOT NULL
);


--
-- Name: TABLE dc_subject; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE dc_subject IS 'Table to represent DC subject relations.';


--
-- Name: COLUMN dc_subject.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN dc_subject.id IS 'Database ID of the relation.';


--
-- Name: COLUMN dc_subject.rdf_subject; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN dc_subject.rdf_subject IS 'Subject of the relation.';


--
-- Name: COLUMN dc_subject.rdf_object; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN dc_subject.rdf_object IS 'The subject of the relation.';


--
-- Name: dc_title_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE dc_title_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: dc_title; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE dc_title (
    id bigint DEFAULT nextval('dc_title_id_seq'::regclass) NOT NULL,
    rdf_subject bigint NOT NULL,
    rdf_object character varying(1024) NOT NULL
);


--
-- Name: TABLE dc_title; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE dc_title IS 'Table to represent DC title relations.';


--
-- Name: COLUMN dc_title.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN dc_title.id IS 'Database ID of the relation.';


--
-- Name: COLUMN dc_title.rdf_subject; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN dc_title.rdf_subject IS 'Subject of the relation.';


--
-- Name: COLUMN dc_title.rdf_object; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN dc_title.rdf_object IS 'The subject of the relation.';


--
-- Name: dc_type_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE dc_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: dc_type; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE dc_type (
    id bigint DEFAULT nextval('dc_type_id_seq'::regclass) NOT NULL,
    rdf_subject bigint NOT NULL,
    rdf_object character varying(1024) NOT NULL
);


--
-- Name: TABLE dc_type; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE dc_type IS 'Table to represent DC type relations.';


--
-- Name: COLUMN dc_type.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN dc_type.id IS 'Database ID of the relation.';


--
-- Name: COLUMN dc_type.rdf_subject; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN dc_type.rdf_subject IS 'Subject of the relation.';


--
-- Name: COLUMN dc_type.rdf_object; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN dc_type.rdf_object IS 'The subject of the relation.';


--
-- Name: generate_ocr; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE generate_ocr (
    id bigint NOT NULL,
    rdf_subject bigint NOT NULL,
    rdf_object boolean NOT NULL
);


--
-- Name: TABLE generate_ocr; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE generate_ocr IS 'Table to represent generate OCR relations.';


--
-- Name: COLUMN generate_ocr.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN generate_ocr.id IS 'Database ID of the relation.';


--
-- Name: COLUMN generate_ocr.rdf_subject; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN generate_ocr.rdf_subject IS 'Subject of the relation.';


--
-- Name: COLUMN generate_ocr.rdf_object; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN generate_ocr.rdf_object IS 'Whether or not the item should compute OCR.';


--
-- Name: generate_ocr_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE generate_ocr_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: generate_ocr_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE generate_ocr_id_seq OWNED BY generate_ocr.id;


--
-- Name: has_language; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE has_language (
    id bigint NOT NULL,
    rdf_subject bigint NOT NULL,
    rdf_object character varying(1024) NOT NULL
);


--
-- Name: TABLE has_language; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE has_language IS 'Table to represent has language relations.';


--
-- Name: COLUMN has_language.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN has_language.id IS 'Database ID of the relation.';


--
-- Name: COLUMN has_language.rdf_subject; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN has_language.rdf_subject IS 'Subject of the relation.';


--
-- Name: COLUMN has_language.rdf_object; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN has_language.rdf_object IS 'The subject of the relation.';


--
-- Name: has_language_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE has_language_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: has_language_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE has_language_id_seq OWNED BY has_language.id;


--
-- Name: has_model; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE has_model (
    id bigint NOT NULL,
    rdf_subject bigint NOT NULL,
    rdf_object bigint NOT NULL
);


--
-- Name: TABLE has_model; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE has_model IS 'Table to represent has model relations.';


--
-- Name: COLUMN has_model.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN has_model.id IS 'Database ID of the relation.';


--
-- Name: COLUMN has_model.rdf_subject; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN has_model.rdf_subject IS 'Subject of the relation.';


--
-- Name: COLUMN has_model.rdf_object; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN has_model.rdf_object IS 'Object of the relation.';


--
-- Name: has_model_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE has_model_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: has_model_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE has_model_id_seq OWNED BY has_model.id;


--
-- Name: image_height; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE image_height (
    id bigint NOT NULL,
    rdf_subject bigint NOT NULL,
    rdf_object integer NOT NULL
);


--
-- Name: TABLE image_height; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE image_height IS 'Table to represent height relations.';


--
-- Name: COLUMN image_height.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN image_height.id IS 'Database ID of the relation.';


--
-- Name: COLUMN image_height.rdf_subject; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN image_height.rdf_subject IS 'The subject of the relation.';


--
-- Name: COLUMN image_height.rdf_object; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN image_height.rdf_object IS 'The height of the image.';


--
-- Name: image_height_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE image_height_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: image_height_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE image_height_id_seq OWNED BY image_height.id;


--
-- Name: image_width; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE image_width (
    id bigint NOT NULL,
    rdf_subject bigint NOT NULL,
    rdf_object integer NOT NULL
);


--
-- Name: TABLE image_width; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE image_width IS 'Table to represent width relations.';


--
-- Name: COLUMN image_width.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN image_width.id IS 'Database ID of the relation.';


--
-- Name: COLUMN image_width.rdf_subject; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN image_width.rdf_subject IS 'The subject of the relation.';


--
-- Name: COLUMN image_width.rdf_object; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN image_width.rdf_object IS 'The width of the image.';


--
-- Name: image_width_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE image_width_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: image_width_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE image_width_id_seq OWNED BY image_width.id;


--
-- Name: is_constituent_of; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE is_constituent_of (
    id bigint NOT NULL,
    rdf_subject bigint NOT NULL,
    rdf_object bigint NOT NULL
);


--
-- Name: TABLE is_constituent_of; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE is_constituent_of IS 'Table to represent is constituent of relations.';


--
-- Name: COLUMN is_constituent_of.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN is_constituent_of.id IS 'Database ID of the relation.';


--
-- Name: COLUMN is_constituent_of.rdf_subject; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN is_constituent_of.rdf_subject IS 'Subject of the relation.';


--
-- Name: COLUMN is_constituent_of.rdf_object; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN is_constituent_of.rdf_object IS 'Object of the relation.';


--
-- Name: is_constituent_of_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE is_constituent_of_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: is_constituent_of_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE is_constituent_of_id_seq OWNED BY is_constituent_of.id;


--
-- Name: is_member_of; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE is_member_of (
    id bigint NOT NULL,
    rdf_subject bigint NOT NULL,
    rdf_object bigint NOT NULL
);


--
-- Name: TABLE is_member_of; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE is_member_of IS 'Table to represent is member of relations.';


--
-- Name: COLUMN is_member_of.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN is_member_of.id IS 'Database ID of the relation.';


--
-- Name: COLUMN is_member_of.rdf_subject; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN is_member_of.rdf_subject IS 'Subject of the relation.';


--
-- Name: COLUMN is_member_of.rdf_object; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN is_member_of.rdf_object IS 'Object of the relation.';


--
-- Name: is_member_of_collection; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE is_member_of_collection (
    id bigint NOT NULL,
    rdf_subject bigint NOT NULL,
    rdf_object bigint NOT NULL
);


--
-- Name: TABLE is_member_of_collection; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE is_member_of_collection IS 'Table to represent is member of collection relations.';


--
-- Name: COLUMN is_member_of_collection.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN is_member_of_collection.id IS 'Database ID of the relation.';


--
-- Name: COLUMN is_member_of_collection.rdf_subject; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN is_member_of_collection.rdf_subject IS 'Subject of the relation.';


--
-- Name: COLUMN is_member_of_collection.rdf_object; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN is_member_of_collection.rdf_object IS 'Object of the relation.';


--
-- Name: is_member_of_collection_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE is_member_of_collection_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: is_member_of_collection_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE is_member_of_collection_id_seq OWNED BY is_member_of_collection.id;


--
-- Name: is_member_of_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE is_member_of_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: is_member_of_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE is_member_of_id_seq OWNED BY is_member_of.id;


--
-- Name: is_page_number; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE is_page_number (
    id bigint NOT NULL,
    rdf_subject bigint NOT NULL,
    rdf_object integer NOT NULL
);


--
-- Name: TABLE is_page_number; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE is_page_number IS 'Table to represent is page number relations.';


--
-- Name: COLUMN is_page_number.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN is_page_number.id IS 'Database ID of the relation.';


--
-- Name: COLUMN is_page_number.rdf_subject; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN is_page_number.rdf_subject IS 'Subject of the relation.';


--
-- Name: COLUMN is_page_number.rdf_object; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN is_page_number.rdf_object IS 'The object of the relation.';


--
-- Name: is_page_number_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE is_page_number_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: is_page_number_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE is_page_number_id_seq OWNED BY is_page_number.id;


--
-- Name: is_page_of; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE is_page_of (
    id bigint NOT NULL,
    rdf_subject bigint NOT NULL,
    rdf_object bigint NOT NULL
);


--
-- Name: TABLE is_page_of; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE is_page_of IS 'Table to represent is page of relations.';


--
-- Name: COLUMN is_page_of.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN is_page_of.id IS 'Database ID of the relation.';


--
-- Name: COLUMN is_page_of.rdf_subject; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN is_page_of.rdf_subject IS 'Subject of the relation.';


--
-- Name: COLUMN is_page_of.rdf_object; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN is_page_of.rdf_object IS 'Object of the relation.';


--
-- Name: is_page_of_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE is_page_of_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: is_page_of_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE is_page_of_id_seq OWNED BY is_page_of.id;


--
-- Name: is_section; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE is_section (
    id bigint NOT NULL,
    rdf_subject bigint NOT NULL,
    rdf_object integer NOT NULL
);


--
-- Name: TABLE is_section; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE is_section IS 'Table to represent is section relations.';


--
-- Name: COLUMN is_section.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN is_section.id IS 'Database ID of the relation.';


--
-- Name: COLUMN is_section.rdf_subject; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN is_section.rdf_subject IS 'Subject of the relation.';


--
-- Name: COLUMN is_section.rdf_object; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN is_section.rdf_object IS 'The object of the relation.';


--
-- Name: is_section_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE is_section_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: is_section_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE is_section_id_seq OWNED BY is_section.id;


--
-- Name: is_sequence_number; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE is_sequence_number (
    id bigint NOT NULL,
    rdf_subject bigint NOT NULL,
    rdf_object integer NOT NULL
);


--
-- Name: TABLE is_sequence_number; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE is_sequence_number IS 'Table to represent sequence number relations. Do not confuse with is_squence_number_of.';


--
-- Name: COLUMN is_sequence_number.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN is_sequence_number.id IS 'Database ID of the relation.';


--
-- Name: COLUMN is_sequence_number.rdf_subject; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN is_sequence_number.rdf_subject IS 'Subject of the relation.';


--
-- Name: COLUMN is_sequence_number.rdf_object; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN is_sequence_number.rdf_object IS 'The object of the relation.';


--
-- Name: is_sequence_number_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE is_sequence_number_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: is_sequence_number_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE is_sequence_number_id_seq OWNED BY is_sequence_number.id;


--
-- Name: is_sequence_number_of; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE is_sequence_number_of (
    id bigint NOT NULL,
    rdf_subject bigint NOT NULL,
    rdf_object bigint NOT NULL,
    sequence_number smallint NOT NULL
);


--
-- Name: TABLE is_sequence_number_of; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE is_sequence_number_of IS 'Tabel to map the isSequenceNumberOf relation. This is a strange relation in Islandora. Do not confuse with is_sequence_number.';


--
-- Name: COLUMN is_sequence_number_of.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN is_sequence_number_of.id IS 'Database ID of the relation.';


--
-- Name: COLUMN is_sequence_number_of.rdf_subject; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN is_sequence_number_of.rdf_subject IS 'The subject of the relation.';


--
-- Name: COLUMN is_sequence_number_of.rdf_object; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN is_sequence_number_of.rdf_object IS 'The object of the relationship.';


--
-- Name: COLUMN is_sequence_number_of.sequence_number; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN is_sequence_number_of.sequence_number IS 'The sequence number of the subject in the object.';


--
-- Name: is_sequence_number_of_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE is_sequence_number_of_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: is_sequence_number_of_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE is_sequence_number_of_id_seq OWNED BY is_sequence_number_of.id;


--
-- Name: log; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE log (
    id bigint NOT NULL,
    log_entry text NOT NULL
);


--
-- Name: TABLE log; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE log IS 'Log entries for chages to the repository.';


--
-- Name: COLUMN log.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN log.id IS 'Database ID of the log entry.';


--
-- Name: COLUMN log.log_entry; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN log.log_entry IS 'Text of the log entry.';


--
-- Name: log_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE log_id_seq OWNED BY log.id;


--
-- Name: mimes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE mimes (
    id bigint NOT NULL,
    mime text NOT NULL
);


--
-- Name: TABLE mimes; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE mimes IS 'Mimes of URIs in the repository.';


--
-- Name: COLUMN mimes.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN mimes.id IS 'Database ID for mime.';


--
-- Name: COLUMN mimes.mime; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN mimes.mime IS 'Mimetype string.';


--
-- Name: mimes_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE mimes_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: mimes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE mimes_id_seq OWNED BY mimes.id;


--
-- Name: pid_namespaces; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE pid_namespaces (
    namespace character varying(1024) NOT NULL,
    highest_id bigint DEFAULT 0 NOT NULL,
    id bigint NOT NULL
);


--
-- Name: TABLE pid_namespaces; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE pid_namespaces IS 'A table used to track the highest used PID.';


--
-- Name: COLUMN pid_namespaces.namespace; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN pid_namespaces.namespace IS 'The PID namespace being tracked.';


--
-- Name: COLUMN pid_namespaces.highest_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN pid_namespaces.highest_id IS 'The highest used integer for an object in the given Namespace.';


--
-- Name: COLUMN pid_namespaces.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN pid_namespaces.id IS 'Database ID of the namespace.';


--
-- Name: namespaces_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE namespaces_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: namespaces_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE namespaces_id_seq OWNED BY pid_namespaces.id;


--
-- Name: object_is_manageable_by_role_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE object_is_manageable_by_role_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: object_is_manageable_by_role; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE object_is_manageable_by_role (
    id bigint DEFAULT nextval('object_is_manageable_by_role_id_seq'::regclass) NOT NULL,
    rdf_subject bigint NOT NULL,
    rdf_object bigint NOT NULL
);


--
-- Name: TABLE object_is_manageable_by_role; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE object_is_manageable_by_role IS 'Maps what roles can manage a object.';


--
-- Name: COLUMN object_is_manageable_by_role.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN object_is_manageable_by_role.id IS 'The database ID of the security rule.';


--
-- Name: COLUMN object_is_manageable_by_role.rdf_subject; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN object_is_manageable_by_role.rdf_subject IS 'Database ID of the object.';


--
-- Name: COLUMN object_is_manageable_by_role.rdf_object; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN object_is_manageable_by_role.rdf_object IS 'Role that can manage the object.';


--
-- Name: object_is_manageable_by_user_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE object_is_manageable_by_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: object_is_manageable_by_user; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE object_is_manageable_by_user (
    id bigint DEFAULT nextval('object_is_manageable_by_user_id_seq'::regclass) NOT NULL,
    rdf_subject bigint NOT NULL,
    rdf_object bigint NOT NULL
);


--
-- Name: TABLE object_is_manageable_by_user; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE object_is_manageable_by_user IS 'Maps what users can manage a object.';


--
-- Name: COLUMN object_is_manageable_by_user.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN object_is_manageable_by_user.id IS 'The database ID of the security rule.';


--
-- Name: COLUMN object_is_manageable_by_user.rdf_subject; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN object_is_manageable_by_user.rdf_subject IS 'Database ID of the object.';


--
-- Name: COLUMN object_is_manageable_by_user.rdf_object; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN object_is_manageable_by_user.rdf_object IS 'User that can manage the object.';


--
-- Name: object_is_viewable_by_role_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE object_is_viewable_by_role_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: object_is_viewable_by_role; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE object_is_viewable_by_role (
    id bigint DEFAULT nextval('object_is_viewable_by_role_id_seq'::regclass) NOT NULL,
    rdf_subject bigint NOT NULL,
    rdf_object bigint NOT NULL
);


--
-- Name: TABLE object_is_viewable_by_role; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE object_is_viewable_by_role IS 'Maps what roles can view a object.';


--
-- Name: COLUMN object_is_viewable_by_role.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN object_is_viewable_by_role.id IS 'The database ID of the security rule.';


--
-- Name: COLUMN object_is_viewable_by_role.rdf_subject; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN object_is_viewable_by_role.rdf_subject IS 'Database ID of the object.';


--
-- Name: COLUMN object_is_viewable_by_role.rdf_object; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN object_is_viewable_by_role.rdf_object IS 'Role that can view the object.';


--
-- Name: object_is_viewable_by_user_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE object_is_viewable_by_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: object_is_viewable_by_user; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE object_is_viewable_by_user (
    id bigint DEFAULT nextval('object_is_viewable_by_user_id_seq'::regclass) NOT NULL,
    rdf_subject bigint NOT NULL,
    rdf_object bigint NOT NULL
);


--
-- Name: TABLE object_is_viewable_by_user; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE object_is_viewable_by_user IS 'Maps what users can view a object.';


--
-- Name: COLUMN object_is_viewable_by_user.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN object_is_viewable_by_user.id IS 'The database ID of the security rule.';


--
-- Name: COLUMN object_is_viewable_by_user.rdf_subject; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN object_is_viewable_by_user.rdf_subject IS 'Database ID of the object.';


--
-- Name: COLUMN object_is_viewable_by_user.rdf_object; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN object_is_viewable_by_user.rdf_object IS 'User that can view the object.';


--
-- Name: object_relationships; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE object_relationships (
    id bigint NOT NULL,
    subject bigint NOT NULL,
    predicate_id bigint NOT NULL,
    rdf_object character varying(1024)
);


--
-- Name: TABLE object_relationships; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE object_relationships IS 'Object relations not in other tables.';


--
-- Name: COLUMN object_relationships.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN object_relationships.id IS 'Database ID of the object relationship.';


--
-- Name: COLUMN object_relationships.subject; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN object_relationships.subject IS 'The subject of the relationship.';


--
-- Name: COLUMN object_relationships.predicate_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN object_relationships.predicate_id IS 'Predicate of the relationship.';


--
-- Name: COLUMN object_relationships.rdf_object; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN object_relationships.rdf_object IS 'The RDF object in string format.';


--
-- Name: object_relationships_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE object_relationships_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: object_relationships_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE object_relationships_id_seq OWNED BY object_relationships.id;


--
-- Name: objects; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE objects (
    id bigint NOT NULL,
    pid_id character varying(1024) NOT NULL,
    namespace bigint NOT NULL,
    state state NOT NULL,
    owner bigint NOT NULL,
    label character varying(1024),
    log bigint,
    versioned boolean DEFAULT true NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone
);


--
-- Name: TABLE objects; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE objects IS 'All objects in the repository.';


--
-- Name: COLUMN objects.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN objects.id IS 'Database ID of the object.';


--
-- Name: COLUMN objects.pid_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN objects.pid_id IS 'ID part of the PID of the object.';


--
-- Name: COLUMN objects.namespace; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN objects.namespace IS 'Database ID of namespace.';


--
-- Name: COLUMN objects.state; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN objects.state IS 'State of the object.';


--
-- Name: COLUMN objects.owner; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN objects.owner IS 'The owner of the object.';


--
-- Name: COLUMN objects.label; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN objects.label IS 'The human readable label of the object.';


--
-- Name: COLUMN objects.log; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN objects.log IS 'Current log entry.';


--
-- Name: COLUMN objects.versioned; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN objects.versioned IS 'Whether or not the object should be versioned.';


--
-- Name: COLUMN objects.created; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN objects.created IS 'Time the object was created.';


--
-- Name: COLUMN objects.modified; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN objects.modified IS 'Time the object was modified.';


--
-- Name: objects_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE objects_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: objects_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE objects_id_seq OWNED BY objects.id;


--
-- Name: objects_owner_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE objects_owner_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: objects_owner_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE objects_owner_seq OWNED BY objects.owner;


--
-- Name: old_datastreams; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE old_datastreams (
    id bigint NOT NULL,
    current_datastream bigint NOT NULL,
    log bigint,
    state state NOT NULL,
    label text,
    uri_id bigint,
    committed timestamp with time zone NOT NULL
);


--
-- Name: TABLE old_datastreams; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE old_datastreams IS 'Old versions of datastreams.';


--
-- Name: COLUMN old_datastreams.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN old_datastreams.id IS 'Database ID of the old datastream version.';


--
-- Name: COLUMN old_datastreams.current_datastream; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN old_datastreams.current_datastream IS 'Current version of the datastream.';


--
-- Name: COLUMN old_datastreams.log; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN old_datastreams.log IS 'Log entry for the datastream version.';


--
-- Name: COLUMN old_datastreams.state; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN old_datastreams.state IS 'State of the datastream at the version.';


--
-- Name: COLUMN old_datastreams.label; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN old_datastreams.label IS 'Label of the datastream at the version.';


--
-- Name: COLUMN old_datastreams.uri_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN old_datastreams.uri_id IS 'URI to the resource at the version.';


--
-- Name: COLUMN old_datastreams.committed; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN old_datastreams.committed IS 'The point in time that this datastream version became the current version.';


--
-- Name: old_datastreams_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE old_datastreams_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: old_datastreams_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE old_datastreams_id_seq OWNED BY old_datastreams.id;


--
-- Name: old_objects; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE old_objects (
    id bigint NOT NULL,
    current_object bigint NOT NULL,
    log bigint,
    state state NOT NULL,
    owner bigint,
    label text,
    committed timestamp with time zone NOT NULL
);


--
-- Name: TABLE old_objects; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE old_objects IS 'Old versions of objects.';


--
-- Name: COLUMN old_objects.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN old_objects.id IS 'Database ID for the old object version.';


--
-- Name: COLUMN old_objects.current_object; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN old_objects.current_object IS 'Current version of the object.';


--
-- Name: COLUMN old_objects.log; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN old_objects.log IS 'Log entry for the old object information.';


--
-- Name: COLUMN old_objects.state; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN old_objects.state IS 'Sate of the object at the version.';


--
-- Name: COLUMN old_objects.owner; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN old_objects.owner IS 'Owner of the object at the version.';


--
-- Name: COLUMN old_objects.label; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN old_objects.label IS 'Label of the object at the version.';


--
-- Name: COLUMN old_objects.committed; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN old_objects.committed IS 'The point in time that this object version became the current object.';


--
-- Name: old_objects_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE old_objects_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: old_objects_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE old_objects_id_seq OWNED BY old_objects.id;


--
-- Name: old_objects_object_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE old_objects_object_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: old_objects_object_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE old_objects_object_seq OWNED BY old_objects.current_object;


--
-- Name: predicates; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE predicates (
    id bigint NOT NULL,
    rdf_namespace_id bigint NOT NULL,
    predicate character varying(1024) NOT NULL
);


--
-- Name: TABLE predicates; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE predicates IS 'RDF predicates used by the repository.';


--
-- Name: COLUMN predicates.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN predicates.id IS 'Database ID of the predicate.';


--
-- Name: COLUMN predicates.rdf_namespace_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN predicates.rdf_namespace_id IS 'Namespace the predicate belongs to.';


--
-- Name: COLUMN predicates.predicate; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN predicates.predicate IS 'RDF predicate.';


--
-- Name: predicates_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE predicates_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: predicates_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE predicates_id_seq OWNED BY predicates.id;


--
-- Name: rdf_namespaces; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE rdf_namespaces (
    id bigint NOT NULL,
    rdf_namespace character varying(1024) NOT NULL
);


--
-- Name: TABLE rdf_namespaces; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE rdf_namespaces IS 'RDF namespaces used in the repository.';


--
-- Name: COLUMN rdf_namespaces.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN rdf_namespaces.id IS 'Database ID of the RDF namespace.';


--
-- Name: COLUMN rdf_namespaces.rdf_namespace; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN rdf_namespaces.rdf_namespace IS 'The RDF namespace.';


--
-- Name: rdf_namespace_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE rdf_namespace_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: rdf_namespace_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE rdf_namespace_id_seq OWNED BY rdf_namespaces.id;


--
-- Name: resources; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE resources (
    id bigint NOT NULL,
    uri text NOT NULL,
    mime bigint
);


--
-- Name: TABLE resources; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE resources IS 'A list of all resources (URIs to file like things) managed by the repository.';


--
-- Name: COLUMN resources.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN resources.id IS 'ID of the URI';


--
-- Name: COLUMN resources.uri; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN resources.uri IS 'URI to the resource.';


--
-- Name: COLUMN resources.mime; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN resources.mime IS 'Mime of the URI.';


--
-- Name: sources; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE sources (
    id bigint NOT NULL,
    source text NOT NULL
);


--
-- Name: TABLE sources; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE sources IS 'Sources of data, such as a Drupal site.';


--
-- Name: COLUMN sources.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN sources.id IS 'Database ID of the data source.';


--
-- Name: COLUMN sources.source; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN sources.source IS 'The identifier of the source.';


--
-- Name: sources_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE sources_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: sources_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE sources_id_seq OWNED BY sources.id;


--
-- Name: uris_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE uris_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: uris_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE uris_id_seq OWNED BY resources.id;


--
-- Name: user_roles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE user_roles (
    id bigint NOT NULL,
    role character varying(1024),
    source_id bigint NOT NULL
);


--
-- Name: COLUMN user_roles.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN user_roles.id IS 'The database ID of the user role.';


--
-- Name: COLUMN user_roles.role; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN user_roles.role IS 'The role string.';


--
-- Name: COLUMN user_roles.source_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN user_roles.source_id IS 'The database ID of the source of the role.';


--
-- Name: user_roles_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE user_roles_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: user_roles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE user_roles_id_seq OWNED BY user_roles.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE users (
    id bigint NOT NULL,
    username text NOT NULL,
    source_id bigint NOT NULL
);


--
-- Name: TABLE users; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE users IS 'Users of the repository.';


--
-- Name: COLUMN users.id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN users.id IS 'Database ID of the user.';


--
-- Name: COLUMN users.username; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN users.username IS 'Identifier of the user.';


--
-- Name: COLUMN users.source_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN users.source_id IS 'Source of the user.';


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE users_id_seq OWNED BY users.id;


--
-- Name: users_source_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE users_source_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: users_source_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE users_source_seq OWNED BY users.source_id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY checksums ALTER COLUMN id SET DEFAULT nextval('checksums_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY datastream_relationships ALTER COLUMN id SET DEFAULT nextval('datastream_relationships_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY datastreams ALTER COLUMN id SET DEFAULT nextval('datastreams_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY date_issued ALTER COLUMN id SET DEFAULT nextval('date_issued_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY generate_ocr ALTER COLUMN id SET DEFAULT nextval('generate_ocr_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY has_language ALTER COLUMN id SET DEFAULT nextval('has_language_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY has_model ALTER COLUMN id SET DEFAULT nextval('has_model_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY image_height ALTER COLUMN id SET DEFAULT nextval('image_height_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY image_width ALTER COLUMN id SET DEFAULT nextval('image_width_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY is_constituent_of ALTER COLUMN id SET DEFAULT nextval('is_constituent_of_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY is_member_of ALTER COLUMN id SET DEFAULT nextval('is_member_of_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY is_member_of_collection ALTER COLUMN id SET DEFAULT nextval('is_member_of_collection_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY is_page_number ALTER COLUMN id SET DEFAULT nextval('is_page_number_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY is_page_of ALTER COLUMN id SET DEFAULT nextval('is_page_of_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY is_section ALTER COLUMN id SET DEFAULT nextval('is_section_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY is_sequence_number ALTER COLUMN id SET DEFAULT nextval('is_sequence_number_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY is_sequence_number_of ALTER COLUMN id SET DEFAULT nextval('is_sequence_number_of_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY log ALTER COLUMN id SET DEFAULT nextval('log_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY mimes ALTER COLUMN id SET DEFAULT nextval('mimes_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY object_relationships ALTER COLUMN id SET DEFAULT nextval('object_relationships_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY objects ALTER COLUMN id SET DEFAULT nextval('objects_id_seq'::regclass);


--
-- Name: owner; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY objects ALTER COLUMN owner SET DEFAULT nextval('objects_owner_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY old_datastreams ALTER COLUMN id SET DEFAULT nextval('old_datastreams_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY old_objects ALTER COLUMN id SET DEFAULT nextval('old_objects_id_seq'::regclass);


--
-- Name: current_object; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY old_objects ALTER COLUMN current_object SET DEFAULT nextval('old_objects_object_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY pid_namespaces ALTER COLUMN id SET DEFAULT nextval('namespaces_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY predicates ALTER COLUMN id SET DEFAULT nextval('predicates_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY rdf_namespaces ALTER COLUMN id SET DEFAULT nextval('rdf_namespace_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY resources ALTER COLUMN id SET DEFAULT nextval('uris_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY sources ALTER COLUMN id SET DEFAULT nextval('sources_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY user_roles ALTER COLUMN id SET DEFAULT nextval('user_roles_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY users ALTER COLUMN id SET DEFAULT nextval('users_id_seq'::regclass);


--
-- Name: source_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY users ALTER COLUMN source_id SET DEFAULT nextval('users_source_seq'::regclass);


--
-- Name: checksums_primary_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY checksums
    ADD CONSTRAINT checksums_primary_key PRIMARY KEY (id);


--
-- Name: datastream_is_manageable_by_role_primary_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY datastream_is_manageable_by_role
    ADD CONSTRAINT datastream_is_manageable_by_role_primary_key PRIMARY KEY (id);


--
-- Name: datastream_is_manageable_by_user_primary_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY datastream_is_manageable_by_user
    ADD CONSTRAINT datastream_is_manageable_by_user_primary_key PRIMARY KEY (id);


--
-- Name: datastream_is_viewable_by_role_primary_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY datastream_is_viewable_by_role
    ADD CONSTRAINT datastream_is_viewable_by_role_primary_key PRIMARY KEY (id);


--
-- Name: datastream_is_viewable_by_user_primary_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY datastream_is_viewable_by_user
    ADD CONSTRAINT datastream_is_viewable_by_user_primary_key PRIMARY KEY (id);


--
-- Name: datastream_relationships_primary_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY datastream_relationships
    ADD CONSTRAINT datastream_relationships_primary_key PRIMARY KEY (id);


--
-- Name: datastreams_primary_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY datastreams
    ADD CONSTRAINT datastreams_primary_key PRIMARY KEY (id);


--
-- Name: date_issued_primary_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY date_issued
    ADD CONSTRAINT date_issued_primary_key PRIMARY KEY (id);


--
-- Name: dc_contributor_primary_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY dc_contributor
    ADD CONSTRAINT dc_contributor_primary_key PRIMARY KEY (id);


--
-- Name: dc_coverage_primary_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY dc_coverage
    ADD CONSTRAINT dc_coverage_primary_key PRIMARY KEY (id);


--
-- Name: dc_creator_primary_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY dc_creator
    ADD CONSTRAINT dc_creator_primary_key PRIMARY KEY (id);


--
-- Name: dc_date_primary_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY dc_date
    ADD CONSTRAINT dc_date_primary_key PRIMARY KEY (id);


--
-- Name: dc_description_primary_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY dc_description
    ADD CONSTRAINT dc_description_primary_key PRIMARY KEY (id);


--
-- Name: dc_format_primary_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY dc_format
    ADD CONSTRAINT dc_format_primary_key PRIMARY KEY (id);


--
-- Name: dc_identifier_primary_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY dc_identifier
    ADD CONSTRAINT dc_identifier_primary_key PRIMARY KEY (id);


--
-- Name: dc_language_primary_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY dc_language
    ADD CONSTRAINT dc_language_primary_key PRIMARY KEY (id);


--
-- Name: dc_publisher_primary_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY dc_publisher
    ADD CONSTRAINT dc_publisher_primary_key PRIMARY KEY (id);


--
-- Name: dc_relation_primary_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY dc_relation
    ADD CONSTRAINT dc_relation_primary_key PRIMARY KEY (id);


--
-- Name: dc_rights_primary_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY dc_rights
    ADD CONSTRAINT dc_rights_primary_key PRIMARY KEY (id);


--
-- Name: dc_source_primary_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY dc_source
    ADD CONSTRAINT dc_source_primary_key PRIMARY KEY (id);


--
-- Name: dc_subject_primary_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY dc_subject
    ADD CONSTRAINT dc_subject_primary_key PRIMARY KEY (id);


--
-- Name: dc_title_primary_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY dc_title
    ADD CONSTRAINT dc_title_primary_key PRIMARY KEY (id);


--
-- Name: dc_type_primary_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY dc_type
    ADD CONSTRAINT dc_type_primary_key PRIMARY KEY (id);


--
-- Name: generate_ocr_primary_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY generate_ocr
    ADD CONSTRAINT generate_ocr_primary_key PRIMARY KEY (id);


--
-- Name: has_language_primary_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY has_language
    ADD CONSTRAINT has_language_primary_key PRIMARY KEY (id);


--
-- Name: has_model_primary_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY has_model
    ADD CONSTRAINT has_model_primary_key PRIMARY KEY (id);


--
-- Name: identifier; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY sources
    ADD CONSTRAINT identifier UNIQUE (source);


--
-- Name: CONSTRAINT identifier ON sources; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT identifier ON sources IS 'Only one entry per source.';


--
-- Name: image_height_primary_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY image_height
    ADD CONSTRAINT image_height_primary_key PRIMARY KEY (id);


--
-- Name: image_width_primary_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY image_width
    ADD CONSTRAINT image_width_primary_key PRIMARY KEY (id);


--
-- Name: is_constituent_of_primary_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY is_constituent_of
    ADD CONSTRAINT is_constituent_of_primary_key PRIMARY KEY (id);


--
-- Name: is_member_of_collection_primary_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY is_member_of_collection
    ADD CONSTRAINT is_member_of_collection_primary_key PRIMARY KEY (id);


--
-- Name: is_member_of_primary_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY is_member_of
    ADD CONSTRAINT is_member_of_primary_key PRIMARY KEY (id);


--
-- Name: is_page_number_primary_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY is_page_number
    ADD CONSTRAINT is_page_number_primary_key PRIMARY KEY (id);


--
-- Name: is_page_of_primary_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY is_page_of
    ADD CONSTRAINT is_page_of_primary_key PRIMARY KEY (id);


--
-- Name: is_section_primary_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY is_section
    ADD CONSTRAINT is_section_primary_key PRIMARY KEY (id);


--
-- Name: is_sequence_number_of_primary_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY is_sequence_number_of
    ADD CONSTRAINT is_sequence_number_of_primary_key PRIMARY KEY (id);


--
-- Name: is_sequence_number_primary_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY is_sequence_number
    ADD CONSTRAINT is_sequence_number_primary_key PRIMARY KEY (id);


--
-- Name: log_primary_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY log
    ADD CONSTRAINT log_primary_key PRIMARY KEY (id);


--
-- Name: mime_primary_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY mimes
    ADD CONSTRAINT mime_primary_key PRIMARY KEY (id);


--
-- Name: namespaces_primary_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY pid_namespaces
    ADD CONSTRAINT namespaces_primary_key PRIMARY KEY (id);


--
-- Name: object_dsid; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY datastreams
    ADD CONSTRAINT object_dsid UNIQUE (object_id, dsid);


--
-- Name: object_is_manageable_by_role_primary_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY object_is_manageable_by_role
    ADD CONSTRAINT object_is_manageable_by_role_primary_key PRIMARY KEY (id);


--
-- Name: object_is_manageable_by_user_primary_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY object_is_manageable_by_user
    ADD CONSTRAINT object_is_manageable_by_user_primary_key PRIMARY KEY (id);


--
-- Name: object_is_viewable_by_role_primary_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY object_is_viewable_by_role
    ADD CONSTRAINT object_is_viewable_by_role_primary_key PRIMARY KEY (id);


--
-- Name: object_is_viewable_by_user_primary_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY object_is_viewable_by_user
    ADD CONSTRAINT object_is_viewable_by_user_primary_key PRIMARY KEY (id);


--
-- Name: object_relationships_primary_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY object_relationships
    ADD CONSTRAINT object_relationships_primary_key PRIMARY KEY (id);


--
-- Name: objects_primary_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY objects
    ADD CONSTRAINT objects_primary_key PRIMARY KEY (id);


--
-- Name: old_datastreams_primary_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY old_datastreams
    ADD CONSTRAINT old_datastreams_primary_key PRIMARY KEY (id);


--
-- Name: old_objects_primary_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY old_objects
    ADD CONSTRAINT old_objects_primary_key PRIMARY KEY (id);


--
-- Name: one_datastream_version_at_a_time; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY old_datastreams
    ADD CONSTRAINT one_datastream_version_at_a_time UNIQUE (current_datastream, committed);


--
-- Name: CONSTRAINT one_datastream_version_at_a_time ON old_datastreams; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT one_datastream_version_at_a_time ON old_datastreams IS 'Only one datastream version can be committed at any time.';


--
-- Name: one_object_version_at_a_time; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY old_objects
    ADD CONSTRAINT one_object_version_at_a_time UNIQUE (current_object, committed);


--
-- Name: CONSTRAINT one_object_version_at_a_time ON old_objects; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT one_object_version_at_a_time ON old_objects IS 'Only one object version can be committed at any time.';


--
-- Name: predicates_primary_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY predicates
    ADD CONSTRAINT predicates_primary_key PRIMARY KEY (id);


--
-- Name: rdf_namespace_primary_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY rdf_namespaces
    ADD CONSTRAINT rdf_namespace_primary_key PRIMARY KEY (id);


--
-- Name: sources_primary_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY sources
    ADD CONSTRAINT sources_primary_key PRIMARY KEY (id);


--
-- Name: unique_checksums; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY checksums
    ADD CONSTRAINT unique_checksums UNIQUE (checksum);


--
-- Name: unique_checksums_per_uri; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY checksums
    ADD CONSTRAINT unique_checksums_per_uri UNIQUE (uri, type);


--
-- Name: CONSTRAINT unique_checksums_per_uri ON checksums; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT unique_checksums_per_uri ON checksums IS 'Each URI should only have one checksum of a given type.';


--
-- Name: unique_heights; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY image_height
    ADD CONSTRAINT unique_heights UNIQUE (rdf_subject);


--
-- Name: CONSTRAINT unique_heights ON image_height; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT unique_heights ON image_height IS 'Images only have one height.';


--
-- Name: unique_ids_in_namespaces; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY objects
    ADD CONSTRAINT unique_ids_in_namespaces UNIQUE (pid_id, namespace);


--
-- Name: CONSTRAINT unique_ids_in_namespaces ON objects; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT unique_ids_in_namespaces ON objects IS 'Namespaces only have on instance of a given id.';


--
-- Name: unique_log_entries; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY log
    ADD CONSTRAINT unique_log_entries UNIQUE (log_entry);


--
-- Name: CONSTRAINT unique_log_entries ON log; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT unique_log_entries ON log IS 'Log entries should be unique.';


--
-- Name: unique_mimes; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY mimes
    ADD CONSTRAINT unique_mimes UNIQUE (mime);


--
-- Name: unique_namespaces; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY pid_namespaces
    ADD CONSTRAINT unique_namespaces UNIQUE (namespace);


--
-- Name: CONSTRAINT unique_namespaces ON pid_namespaces; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT unique_namespaces ON pid_namespaces IS 'Only one entry per namespace.';


--
-- Name: unique_predicates_in_namespaces; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY predicates
    ADD CONSTRAINT unique_predicates_in_namespaces UNIQUE (rdf_namespace_id, predicate);


--
-- Name: CONSTRAINT unique_predicates_in_namespaces ON predicates; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT unique_predicates_in_namespaces ON predicates IS 'Namespaces should only declare predicates once.';


--
-- Name: unique_rdf_namespaces; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY rdf_namespaces
    ADD CONSTRAINT unique_rdf_namespaces UNIQUE (rdf_namespace);


--
-- Name: CONSTRAINT unique_rdf_namespaces ON rdf_namespaces; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT unique_rdf_namespaces ON rdf_namespaces IS 'Namespaces should only be in the database once.';


--
-- Name: unique_roles_in_sources; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY user_roles
    ADD CONSTRAINT unique_roles_in_sources UNIQUE (role, source_id);


--
-- Name: CONSTRAINT unique_roles_in_sources ON user_roles; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT unique_roles_in_sources ON user_roles IS 'Sources should only defined roles once.';


--
-- Name: unique_sequence_numbers; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY is_sequence_number_of
    ADD CONSTRAINT unique_sequence_numbers UNIQUE (rdf_subject, rdf_object, sequence_number);


--
-- Name: CONSTRAINT unique_sequence_numbers ON is_sequence_number_of; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT unique_sequence_numbers ON is_sequence_number_of IS 'Each subject has a unique sequece number for each object.';


--
-- Name: unique_source_user; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY users
    ADD CONSTRAINT unique_source_user UNIQUE (username, source_id);


--
-- Name: CONSTRAINT unique_source_user ON users; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT unique_source_user ON users IS 'Each source shold only identify a user once.';


--
-- Name: unique_uris; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY resources
    ADD CONSTRAINT unique_uris UNIQUE (uri);


--
-- Name: unique_widths; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY image_width
    ADD CONSTRAINT unique_widths UNIQUE (rdf_subject);


--
-- Name: CONSTRAINT unique_widths ON image_width; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT unique_widths ON image_width IS 'Images only have one width.';


--
-- Name: uri_primary_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY resources
    ADD CONSTRAINT uri_primary_key PRIMARY KEY (id);


--
-- Name: user_role_primary_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY user_roles
    ADD CONSTRAINT user_role_primary_key PRIMARY KEY (id);


--
-- Name: users_primary_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_primary_key PRIMARY KEY (id);


--
-- Name: datastream_is_manageable_by_role_datastream_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX datastream_is_manageable_by_role_datastream_index ON datastream_is_manageable_by_role USING btree (rdf_subject);


--
-- Name: INDEX datastream_is_manageable_by_role_datastream_index; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON INDEX datastream_is_manageable_by_role_datastream_index IS 'There will be many lookups by datastream.';


--
-- Name: datastream_is_manageable_by_role_role_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX datastream_is_manageable_by_role_role_index ON datastream_is_manageable_by_role USING btree (rdf_object);


--
-- Name: INDEX datastream_is_manageable_by_role_role_index; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON INDEX datastream_is_manageable_by_role_role_index IS 'Random lookups by role will be common.';


--
-- Name: datastream_is_manageable_by_user_datastream_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX datastream_is_manageable_by_user_datastream_index ON datastream_is_manageable_by_user USING btree (rdf_subject);


--
-- Name: INDEX datastream_is_manageable_by_user_datastream_index; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON INDEX datastream_is_manageable_by_user_datastream_index IS 'There will be many lookups by datastream.';


--
-- Name: datastream_is_manageable_by_user_user_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX datastream_is_manageable_by_user_user_index ON datastream_is_manageable_by_user USING btree (rdf_object);


--
-- Name: INDEX datastream_is_manageable_by_user_user_index; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON INDEX datastream_is_manageable_by_user_user_index IS 'Random lookups by user will be common.';


--
-- Name: datastream_is_viewable_by_role_datastream_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX datastream_is_viewable_by_role_datastream_index ON datastream_is_viewable_by_role USING btree (rdf_subject);


--
-- Name: INDEX datastream_is_viewable_by_role_datastream_index; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON INDEX datastream_is_viewable_by_role_datastream_index IS 'There will be many lookups by datastream.';


--
-- Name: datastream_is_viewable_by_role_role_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX datastream_is_viewable_by_role_role_index ON datastream_is_viewable_by_role USING btree (rdf_object);


--
-- Name: INDEX datastream_is_viewable_by_role_role_index; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON INDEX datastream_is_viewable_by_role_role_index IS 'Random lookups by role will be common.';


--
-- Name: datastream_is_viewable_by_user_datastream_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX datastream_is_viewable_by_user_datastream_index ON datastream_is_viewable_by_user USING btree (rdf_subject);


--
-- Name: INDEX datastream_is_viewable_by_user_datastream_index; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON INDEX datastream_is_viewable_by_user_datastream_index IS 'There will be many lookups by datastream.';


--
-- Name: datastream_is_viewable_by_user_user_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX datastream_is_viewable_by_user_user_index ON datastream_is_viewable_by_user USING btree (rdf_object);


--
-- Name: INDEX datastream_is_viewable_by_user_user_index; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON INDEX datastream_is_viewable_by_user_user_index IS 'Random lookups by user will be common.';


--
-- Name: date_issued_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX date_issued_index ON date_issued USING btree (rdf_object);


--
-- Name: INDEX date_issued_index; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON INDEX date_issued_index IS 'Ordering by date issued should be common.';


--
-- Name: fki_datastream_log_link; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_datastream_log_link ON datastreams USING btree (log);


--
-- Name: fki_datastream_relationships_datastream_link; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_datastream_relationships_datastream_link ON datastream_relationships USING btree (subject);


--
-- Name: fki_datastream_relationships_predicate_link; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_datastream_relationships_predicate_link ON datastream_relationships USING btree (predicate_id);


--
-- Name: fki_date_issued_subject_link; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_date_issued_subject_link ON date_issued USING btree (rdf_subject);


--
-- Name: fki_dc_contributor_subject_link; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_dc_contributor_subject_link ON dc_contributor USING btree (rdf_subject);


--
-- Name: fki_dc_coverage_subject_link; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_dc_coverage_subject_link ON dc_coverage USING btree (rdf_subject);


--
-- Name: fki_dc_creator_subject_link; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_dc_creator_subject_link ON dc_creator USING btree (rdf_subject);


--
-- Name: fki_dc_date_subject_link; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_dc_date_subject_link ON dc_date USING btree (rdf_subject);


--
-- Name: fki_dc_description_subject_link; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_dc_description_subject_link ON dc_description USING btree (rdf_subject);


--
-- Name: fki_dc_format_subject_link; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_dc_format_subject_link ON dc_format USING btree (rdf_subject);


--
-- Name: fki_dc_identifier_subject_link; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_dc_identifier_subject_link ON dc_identifier USING btree (rdf_subject);


--
-- Name: fki_dc_language_subject_link; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_dc_language_subject_link ON dc_language USING btree (rdf_subject);


--
-- Name: fki_dc_publisher_subject_link; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_dc_publisher_subject_link ON dc_publisher USING btree (rdf_subject);


--
-- Name: fki_dc_relation_subject_link; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_dc_relation_subject_link ON dc_relation USING btree (rdf_subject);


--
-- Name: fki_dc_rights_subject_link; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_dc_rights_subject_link ON dc_rights USING btree (rdf_subject);


--
-- Name: fki_dc_source_subject_link; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_dc_source_subject_link ON dc_source USING btree (rdf_subject);


--
-- Name: fki_dc_subject_subject_link; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_dc_subject_subject_link ON dc_subject USING btree (rdf_subject);


--
-- Name: fki_dc_title_subject_link; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_dc_title_subject_link ON dc_title USING btree (rdf_subject);


--
-- Name: fki_dc_type_subject_link; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_dc_type_subject_link ON dc_type USING btree (rdf_subject);


--
-- Name: fki_generate_ocr_subject_link; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_generate_ocr_subject_link ON generate_ocr USING btree (rdf_subject);


--
-- Name: fki_has_language_subject_link; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_has_language_subject_link ON has_language USING btree (rdf_subject);


--
-- Name: fki_has_model_object_key; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_has_model_object_key ON has_model USING btree (rdf_object);


--
-- Name: fki_has_model_subject_link; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_has_model_subject_link ON has_model USING btree (rdf_subject);


--
-- Name: fki_image_height_datastream_link; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_image_height_datastream_link ON image_height USING btree (rdf_subject);


--
-- Name: fki_image_width_datastream_link; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_image_width_datastream_link ON image_width USING btree (rdf_subject);


--
-- Name: fki_is_constituent_of_object_key; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_is_constituent_of_object_key ON is_constituent_of USING btree (rdf_object);


--
-- Name: fki_is_constituent_of_subject_link; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_is_constituent_of_subject_link ON is_constituent_of USING btree (rdf_subject);


--
-- Name: fki_is_member_of_collection_object_key; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_is_member_of_collection_object_key ON is_member_of_collection USING btree (rdf_object);


--
-- Name: fki_is_member_of_collection_subject_link; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_is_member_of_collection_subject_link ON is_member_of_collection USING btree (rdf_subject);


--
-- Name: fki_is_member_of_object_key; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_is_member_of_object_key ON is_member_of USING btree (rdf_object);


--
-- Name: fki_is_member_of_subject_link; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_is_member_of_subject_link ON is_member_of USING btree (rdf_subject);


--
-- Name: fki_is_page_number_subject_link; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_is_page_number_subject_link ON is_page_number USING btree (rdf_subject);


--
-- Name: fki_is_page_of_object_key; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_is_page_of_object_key ON is_page_of USING btree (rdf_object);


--
-- Name: fki_is_page_of_subject_link; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_is_page_of_subject_link ON is_page_of USING btree (rdf_subject);


--
-- Name: fki_is_section_subject_link; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_is_section_subject_link ON is_section USING btree (rdf_subject);


--
-- Name: fki_is_sequence_number_of_object_link; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_is_sequence_number_of_object_link ON is_sequence_number_of USING btree (rdf_object);


--
-- Name: fki_is_sequence_number_of_subject_link; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_is_sequence_number_of_subject_link ON is_sequence_number_of USING btree (rdf_subject);


--
-- Name: fki_is_sequence_number_subject_link; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_is_sequence_number_subject_link ON is_sequence_number USING btree (rdf_subject);


--
-- Name: fki_object_log_link; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_object_log_link ON objects USING btree (log);


--
-- Name: fki_object_namespace_link; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_object_namespace_link ON objects USING btree (namespace);


--
-- Name: fki_object_relationships_predicate_link; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_object_relationships_predicate_link ON object_relationships USING btree (predicate_id);


--
-- Name: fki_object_relationships_subject_link; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_object_relationships_subject_link ON object_relationships USING btree (subject);


--
-- Name: fki_object_user_link; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_object_user_link ON objects USING btree (owner);


--
-- Name: fki_old_datastream_datastream_link; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_old_datastream_datastream_link ON old_datastreams USING btree (current_datastream);


--
-- Name: fki_old_datastream_log_link; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_old_datastream_log_link ON old_datastreams USING btree (log);


--
-- Name: fki_old_datastreams_uri_link; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_old_datastreams_uri_link ON old_datastreams USING btree (uri_id);


--
-- Name: fki_old_object_object_link; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_old_object_object_link ON old_objects USING btree (current_object);


--
-- Name: fki_old_objects_log_link; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_old_objects_log_link ON old_objects USING btree (log);


--
-- Name: fki_old_objects_owner_link; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_old_objects_owner_link ON old_objects USING btree (owner);


--
-- Name: fki_predicate_rdf_namespace_link; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_predicate_rdf_namespace_link ON predicates USING btree (rdf_namespace_id);


--
-- Name: fki_uri_checksum_link; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_uri_checksum_link ON checksums USING btree (uri);


--
-- Name: fki_uri_link; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_uri_link ON datastreams USING btree (resource_id);


--
-- Name: fki_uri_mime_link; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_uri_mime_link ON resources USING btree (mime);


--
-- Name: fki_user_source_link; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_user_source_link ON users USING btree (source_id);


--
-- Name: is_sequence_number_of_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX is_sequence_number_of_index ON is_sequence_number_of USING btree (rdf_subject, rdf_object, sequence_number);


--
-- Name: INDEX is_sequence_number_of_index; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON INDEX is_sequence_number_of_index IS 'Everything in an index.';


--
-- Name: object_dsid_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX object_dsid_index ON datastreams USING btree (object_id, dsid);


--
-- Name: INDEX object_dsid_index; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON INDEX object_dsid_index IS 'Object & DSID is a common query.';


--
-- Name: object_is_manageable_by_role_object_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX object_is_manageable_by_role_object_index ON object_is_manageable_by_role USING btree (rdf_subject);


--
-- Name: INDEX object_is_manageable_by_role_object_index; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON INDEX object_is_manageable_by_role_object_index IS 'There will be many lookups by object.';


--
-- Name: object_is_manageable_by_role_role_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX object_is_manageable_by_role_role_index ON object_is_manageable_by_role USING btree (rdf_object);


--
-- Name: INDEX object_is_manageable_by_role_role_index; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON INDEX object_is_manageable_by_role_role_index IS 'Random lookups by role will be common.';


--
-- Name: object_is_manageable_by_user_object_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX object_is_manageable_by_user_object_index ON object_is_manageable_by_user USING btree (rdf_subject);


--
-- Name: INDEX object_is_manageable_by_user_object_index; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON INDEX object_is_manageable_by_user_object_index IS 'There will be many lookups by object.';


--
-- Name: object_is_manageable_by_user_user_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX object_is_manageable_by_user_user_index ON object_is_manageable_by_user USING btree (rdf_object);


--
-- Name: INDEX object_is_manageable_by_user_user_index; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON INDEX object_is_manageable_by_user_user_index IS 'Random lookups by user will be common.';


--
-- Name: object_is_viewable_by_role_object_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX object_is_viewable_by_role_object_index ON object_is_viewable_by_role USING btree (rdf_subject);


--
-- Name: INDEX object_is_viewable_by_role_object_index; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON INDEX object_is_viewable_by_role_object_index IS 'There will be many lookups by object.';


--
-- Name: object_is_viewable_by_role_role_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX object_is_viewable_by_role_role_index ON object_is_viewable_by_role USING btree (rdf_object);


--
-- Name: INDEX object_is_viewable_by_role_role_index; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON INDEX object_is_viewable_by_role_role_index IS 'Random lookups by role will be common.';


--
-- Name: object_is_viewable_by_user_object_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX object_is_viewable_by_user_object_index ON object_is_viewable_by_user USING btree (rdf_subject);


--
-- Name: INDEX object_is_viewable_by_user_object_index; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON INDEX object_is_viewable_by_user_object_index IS 'There will be many lookups by object.';


--
-- Name: object_is_viewable_by_user_user_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX object_is_viewable_by_user_user_index ON object_is_viewable_by_user USING btree (rdf_object);


--
-- Name: INDEX object_is_viewable_by_user_user_index; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON INDEX object_is_viewable_by_user_user_index IS 'Random lookups by user will be common.';


--
-- Name: object_label_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX object_label_index ON objects USING btree (label);


--
-- Name: INDEX object_label_index; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON INDEX object_label_index IS 'Objects are often queried/ordered by label.';


--
-- Name: pid_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX pid_index ON objects USING btree (pid_id);


--
-- Name: INDEX pid_index; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON INDEX pid_index IS 'There will be much random access on PIDs.';


--
-- Name: datastream_is_manageable_role_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY datastream_is_manageable_by_role
    ADD CONSTRAINT datastream_is_manageable_role_link FOREIGN KEY (rdf_object) REFERENCES user_roles(id);


--
-- Name: datastream_is_manageable_user_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY datastream_is_manageable_by_user
    ADD CONSTRAINT datastream_is_manageable_user_link FOREIGN KEY (rdf_object) REFERENCES users(id);


--
-- Name: datastream_is_viewable_role_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY datastream_is_viewable_by_role
    ADD CONSTRAINT datastream_is_viewable_role_link FOREIGN KEY (rdf_object) REFERENCES user_roles(id);


--
-- Name: datastream_is_viewable_user_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY datastream_is_viewable_by_user
    ADD CONSTRAINT datastream_is_viewable_user_link FOREIGN KEY (rdf_object) REFERENCES users(id);


--
-- Name: datastream_log_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY datastreams
    ADD CONSTRAINT datastream_log_link FOREIGN KEY (log) REFERENCES log(id);


--
-- Name: CONSTRAINT datastream_log_link ON datastreams; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT datastream_log_link ON datastreams IS 'Datastream versions can have log entries.';


--
-- Name: datastream_relationships_datastream_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY datastream_relationships
    ADD CONSTRAINT datastream_relationships_datastream_link FOREIGN KEY (subject) REFERENCES datastreams(id) ON DELETE CASCADE;


--
-- Name: CONSTRAINT datastream_relationships_datastream_link ON datastream_relationships; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT datastream_relationships_datastream_link ON datastream_relationships IS 'Datastream relationship subjects are datastreams.';


--
-- Name: datastream_relationships_predicate_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY datastream_relationships
    ADD CONSTRAINT datastream_relationships_predicate_link FOREIGN KEY (predicate_id) REFERENCES predicates(id);


--
-- Name: CONSTRAINT datastream_relationships_predicate_link ON datastream_relationships; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT datastream_relationships_predicate_link ON datastream_relationships IS 'Each predicate should be well formed.';


--
-- Name: date_issued_subject_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY date_issued
    ADD CONSTRAINT date_issued_subject_link FOREIGN KEY (rdf_subject) REFERENCES objects(id) ON DELETE CASCADE;


--
-- Name: CONSTRAINT date_issued_subject_link ON date_issued; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT date_issued_subject_link ON date_issued IS 'Each relation subject is an object.';


--
-- Name: dc_contributor_subject_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY dc_contributor
    ADD CONSTRAINT dc_contributor_subject_link FOREIGN KEY (rdf_subject) REFERENCES objects(id) ON DELETE CASCADE;


--
-- Name: CONSTRAINT dc_contributor_subject_link ON dc_contributor; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT dc_contributor_subject_link ON dc_contributor IS 'Each relation subject is an object.';


--
-- Name: dc_coverage_subject_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY dc_coverage
    ADD CONSTRAINT dc_coverage_subject_link FOREIGN KEY (rdf_subject) REFERENCES objects(id) ON DELETE CASCADE;


--
-- Name: CONSTRAINT dc_coverage_subject_link ON dc_coverage; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT dc_coverage_subject_link ON dc_coverage IS 'Each relation subject is an object.';


--
-- Name: dc_creator_subject_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY dc_creator
    ADD CONSTRAINT dc_creator_subject_link FOREIGN KEY (rdf_subject) REFERENCES objects(id) ON DELETE CASCADE;


--
-- Name: CONSTRAINT dc_creator_subject_link ON dc_creator; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT dc_creator_subject_link ON dc_creator IS 'Each relation subject is an object.';


--
-- Name: dc_date_subject_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY dc_date
    ADD CONSTRAINT dc_date_subject_link FOREIGN KEY (rdf_subject) REFERENCES objects(id) ON DELETE CASCADE;


--
-- Name: CONSTRAINT dc_date_subject_link ON dc_date; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT dc_date_subject_link ON dc_date IS 'Each relation subject is an object.';


--
-- Name: dc_description_subject_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY dc_description
    ADD CONSTRAINT dc_description_subject_link FOREIGN KEY (rdf_subject) REFERENCES objects(id) ON DELETE CASCADE;


--
-- Name: CONSTRAINT dc_description_subject_link ON dc_description; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT dc_description_subject_link ON dc_description IS 'Each relation subject is an object.';


--
-- Name: dc_format_subject_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY dc_format
    ADD CONSTRAINT dc_format_subject_link FOREIGN KEY (rdf_subject) REFERENCES objects(id) ON DELETE CASCADE;


--
-- Name: CONSTRAINT dc_format_subject_link ON dc_format; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT dc_format_subject_link ON dc_format IS 'Each relation subject is an object.';


--
-- Name: dc_identifier_subject_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY dc_identifier
    ADD CONSTRAINT dc_identifier_subject_link FOREIGN KEY (rdf_subject) REFERENCES objects(id) ON DELETE CASCADE;


--
-- Name: CONSTRAINT dc_identifier_subject_link ON dc_identifier; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT dc_identifier_subject_link ON dc_identifier IS 'Each relation subject is an object.';


--
-- Name: dc_language_subject_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY dc_language
    ADD CONSTRAINT dc_language_subject_link FOREIGN KEY (rdf_subject) REFERENCES objects(id) ON DELETE CASCADE;


--
-- Name: CONSTRAINT dc_language_subject_link ON dc_language; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT dc_language_subject_link ON dc_language IS 'Each relation subject is an object.';


--
-- Name: dc_publisher_subject_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY dc_publisher
    ADD CONSTRAINT dc_publisher_subject_link FOREIGN KEY (rdf_subject) REFERENCES objects(id) ON DELETE CASCADE;


--
-- Name: CONSTRAINT dc_publisher_subject_link ON dc_publisher; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT dc_publisher_subject_link ON dc_publisher IS 'Each relation subject is an object.';


--
-- Name: dc_relation_subject_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY dc_relation
    ADD CONSTRAINT dc_relation_subject_link FOREIGN KEY (rdf_subject) REFERENCES objects(id) ON DELETE CASCADE;


--
-- Name: CONSTRAINT dc_relation_subject_link ON dc_relation; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT dc_relation_subject_link ON dc_relation IS 'Each relation subject is an object.';


--
-- Name: dc_rights_subject_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY dc_rights
    ADD CONSTRAINT dc_rights_subject_link FOREIGN KEY (rdf_subject) REFERENCES objects(id) ON DELETE CASCADE;


--
-- Name: CONSTRAINT dc_rights_subject_link ON dc_rights; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT dc_rights_subject_link ON dc_rights IS 'Each relation subject is an object.';


--
-- Name: dc_source_subject_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY dc_source
    ADD CONSTRAINT dc_source_subject_link FOREIGN KEY (rdf_subject) REFERENCES objects(id) ON DELETE CASCADE;


--
-- Name: CONSTRAINT dc_source_subject_link ON dc_source; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT dc_source_subject_link ON dc_source IS 'Each relation subject is an object.';


--
-- Name: dc_subject_subject_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY dc_subject
    ADD CONSTRAINT dc_subject_subject_link FOREIGN KEY (rdf_subject) REFERENCES objects(id) ON DELETE CASCADE;


--
-- Name: CONSTRAINT dc_subject_subject_link ON dc_subject; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT dc_subject_subject_link ON dc_subject IS 'Each relation subject is an object.';


--
-- Name: dc_title_subject_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY dc_title
    ADD CONSTRAINT dc_title_subject_link FOREIGN KEY (rdf_subject) REFERENCES objects(id) ON DELETE CASCADE;


--
-- Name: CONSTRAINT dc_title_subject_link ON dc_title; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT dc_title_subject_link ON dc_title IS 'Each relation subject is an object.';


--
-- Name: dc_type_subject_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY dc_type
    ADD CONSTRAINT dc_type_subject_link FOREIGN KEY (rdf_subject) REFERENCES objects(id) ON DELETE CASCADE;


--
-- Name: CONSTRAINT dc_type_subject_link ON dc_type; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT dc_type_subject_link ON dc_type IS 'Each relation subject is an object.';


--
-- Name: generate_ocr_subject_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY generate_ocr
    ADD CONSTRAINT generate_ocr_subject_link FOREIGN KEY (rdf_subject) REFERENCES objects(id) ON DELETE CASCADE;


--
-- Name: CONSTRAINT generate_ocr_subject_link ON generate_ocr; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT generate_ocr_subject_link ON generate_ocr IS 'Each relation subject is an object.';


--
-- Name: has_language_subject_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY has_language
    ADD CONSTRAINT has_language_subject_link FOREIGN KEY (rdf_subject) REFERENCES objects(id) ON DELETE CASCADE;


--
-- Name: CONSTRAINT has_language_subject_link ON has_language; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT has_language_subject_link ON has_language IS 'Each relation subject is an object.';


--
-- Name: has_model_object_key; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY has_model
    ADD CONSTRAINT has_model_object_key FOREIGN KEY (rdf_object) REFERENCES objects(id) ON DELETE CASCADE;


--
-- Name: CONSTRAINT has_model_object_key ON has_model; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT has_model_object_key ON has_model IS 'Each relation object is a repository object.';


--
-- Name: has_model_subject_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY has_model
    ADD CONSTRAINT has_model_subject_link FOREIGN KEY (rdf_subject) REFERENCES objects(id) ON DELETE CASCADE;


--
-- Name: CONSTRAINT has_model_subject_link ON has_model; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT has_model_subject_link ON has_model IS 'Each relation subject is an object.';


--
-- Name: image_height_datastream_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY image_height
    ADD CONSTRAINT image_height_datastream_link FOREIGN KEY (rdf_subject) REFERENCES datastreams(id) ON DELETE CASCADE;


--
-- Name: CONSTRAINT image_height_datastream_link ON image_height; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT image_height_datastream_link ON image_height IS 'Images have heights.';


--
-- Name: image_width_datastream_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY image_width
    ADD CONSTRAINT image_width_datastream_link FOREIGN KEY (rdf_subject) REFERENCES datastreams(id) ON DELETE CASCADE;


--
-- Name: CONSTRAINT image_width_datastream_link ON image_width; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT image_width_datastream_link ON image_width IS 'Images have widths.';


--
-- Name: is_constituent_of_object_key; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY is_constituent_of
    ADD CONSTRAINT is_constituent_of_object_key FOREIGN KEY (rdf_object) REFERENCES objects(id) ON DELETE CASCADE;


--
-- Name: CONSTRAINT is_constituent_of_object_key ON is_constituent_of; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT is_constituent_of_object_key ON is_constituent_of IS 'Each relation object is a repository object.';


--
-- Name: is_constituent_of_subject_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY is_constituent_of
    ADD CONSTRAINT is_constituent_of_subject_link FOREIGN KEY (rdf_subject) REFERENCES objects(id) ON DELETE CASCADE;


--
-- Name: CONSTRAINT is_constituent_of_subject_link ON is_constituent_of; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT is_constituent_of_subject_link ON is_constituent_of IS 'Each relation subject is an object.';


--
-- Name: is_member_of_collection_object_key; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY is_member_of_collection
    ADD CONSTRAINT is_member_of_collection_object_key FOREIGN KEY (rdf_object) REFERENCES objects(id) ON DELETE CASCADE;


--
-- Name: CONSTRAINT is_member_of_collection_object_key ON is_member_of_collection; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT is_member_of_collection_object_key ON is_member_of_collection IS 'Each relation object is a repository object.';


--
-- Name: is_member_of_collection_subject_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY is_member_of_collection
    ADD CONSTRAINT is_member_of_collection_subject_link FOREIGN KEY (rdf_subject) REFERENCES objects(id) ON DELETE CASCADE;


--
-- Name: CONSTRAINT is_member_of_collection_subject_link ON is_member_of_collection; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT is_member_of_collection_subject_link ON is_member_of_collection IS 'Each relation subject is an object.';


--
-- Name: is_member_of_object_key; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY is_member_of
    ADD CONSTRAINT is_member_of_object_key FOREIGN KEY (rdf_object) REFERENCES objects(id) ON DELETE CASCADE;


--
-- Name: CONSTRAINT is_member_of_object_key ON is_member_of; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT is_member_of_object_key ON is_member_of IS 'Each relationship object is a repository object.';


--
-- Name: is_member_of_subject_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY is_member_of
    ADD CONSTRAINT is_member_of_subject_link FOREIGN KEY (rdf_subject) REFERENCES objects(id) ON DELETE CASCADE;


--
-- Name: CONSTRAINT is_member_of_subject_link ON is_member_of; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT is_member_of_subject_link ON is_member_of IS 'Each subject is an object.';


--
-- Name: is_page_number_subject_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY is_page_number
    ADD CONSTRAINT is_page_number_subject_link FOREIGN KEY (rdf_subject) REFERENCES objects(id) ON DELETE CASCADE;


--
-- Name: CONSTRAINT is_page_number_subject_link ON is_page_number; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT is_page_number_subject_link ON is_page_number IS 'Each relation subject is an object.';


--
-- Name: is_page_of_object_key; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY is_page_of
    ADD CONSTRAINT is_page_of_object_key FOREIGN KEY (rdf_object) REFERENCES objects(id) ON DELETE CASCADE;


--
-- Name: CONSTRAINT is_page_of_object_key ON is_page_of; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT is_page_of_object_key ON is_page_of IS 'Each relation object is a repository object.';


--
-- Name: is_page_of_subject_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY is_page_of
    ADD CONSTRAINT is_page_of_subject_link FOREIGN KEY (rdf_subject) REFERENCES objects(id) ON DELETE CASCADE;


--
-- Name: CONSTRAINT is_page_of_subject_link ON is_page_of; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT is_page_of_subject_link ON is_page_of IS 'Each relation subject is an object.';


--
-- Name: is_section_subject_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY is_section
    ADD CONSTRAINT is_section_subject_link FOREIGN KEY (rdf_subject) REFERENCES objects(id) ON DELETE CASCADE;


--
-- Name: CONSTRAINT is_section_subject_link ON is_section; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT is_section_subject_link ON is_section IS 'Each relation subject is an object.';


--
-- Name: is_sequence_number_of_object_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY is_sequence_number_of
    ADD CONSTRAINT is_sequence_number_of_object_link FOREIGN KEY (rdf_object) REFERENCES objects(id) ON DELETE CASCADE;


--
-- Name: CONSTRAINT is_sequence_number_of_object_link ON is_sequence_number_of; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT is_sequence_number_of_object_link ON is_sequence_number_of IS 'Each realtion object is a repository object.';


--
-- Name: is_sequence_number_of_subject_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY is_sequence_number_of
    ADD CONSTRAINT is_sequence_number_of_subject_link FOREIGN KEY (rdf_subject) REFERENCES objects(id) ON DELETE CASCADE;


--
-- Name: CONSTRAINT is_sequence_number_of_subject_link ON is_sequence_number_of; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT is_sequence_number_of_subject_link ON is_sequence_number_of IS 'Each subject is an object.';


--
-- Name: is_sequence_number_subject_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY is_sequence_number
    ADD CONSTRAINT is_sequence_number_subject_link FOREIGN KEY (rdf_subject) REFERENCES objects(id) ON DELETE CASCADE;


--
-- Name: CONSTRAINT is_sequence_number_subject_link ON is_sequence_number; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT is_sequence_number_subject_link ON is_sequence_number IS 'Each relation subject is an object.';


--
-- Name: manageable_by_role_datastream_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY datastream_is_manageable_by_role
    ADD CONSTRAINT manageable_by_role_datastream_link FOREIGN KEY (rdf_subject) REFERENCES datastreams(id) ON DELETE CASCADE;


--
-- Name: manageable_by_role_object_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY object_is_manageable_by_role
    ADD CONSTRAINT manageable_by_role_object_link FOREIGN KEY (rdf_subject) REFERENCES objects(id) ON DELETE CASCADE;


--
-- Name: manageable_by_user_datastream_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY datastream_is_manageable_by_user
    ADD CONSTRAINT manageable_by_user_datastream_link FOREIGN KEY (rdf_subject) REFERENCES datastreams(id) ON DELETE CASCADE;


--
-- Name: manageable_by_user_object_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY object_is_manageable_by_user
    ADD CONSTRAINT manageable_by_user_object_link FOREIGN KEY (rdf_subject) REFERENCES objects(id) ON DELETE CASCADE;


--
-- Name: mime_uri_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY resources
    ADD CONSTRAINT mime_uri_link FOREIGN KEY (mime) REFERENCES mimes(id);


--
-- Name: CONSTRAINT mime_uri_link ON resources; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT mime_uri_link ON resources IS 'URIs have mimes.';


--
-- Name: object_id_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY datastreams
    ADD CONSTRAINT object_id_link FOREIGN KEY (object_id) REFERENCES objects(id) ON DELETE CASCADE;


--
-- Name: CONSTRAINT object_id_link ON datastreams; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT object_id_link ON datastreams IS 'Datastreams belong to objects.';


--
-- Name: object_is_manageable_role_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY object_is_manageable_by_role
    ADD CONSTRAINT object_is_manageable_role_link FOREIGN KEY (rdf_object) REFERENCES user_roles(id);


--
-- Name: object_is_manageable_user_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY object_is_manageable_by_user
    ADD CONSTRAINT object_is_manageable_user_link FOREIGN KEY (rdf_object) REFERENCES users(id);


--
-- Name: object_is_viewable_role_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY object_is_viewable_by_role
    ADD CONSTRAINT object_is_viewable_role_link FOREIGN KEY (rdf_object) REFERENCES user_roles(id);


--
-- Name: object_is_viewable_user_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY object_is_viewable_by_user
    ADD CONSTRAINT object_is_viewable_user_link FOREIGN KEY (rdf_object) REFERENCES users(id);


--
-- Name: object_log_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY objects
    ADD CONSTRAINT object_log_link FOREIGN KEY (log) REFERENCES log(id);


--
-- Name: CONSTRAINT object_log_link ON objects; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT object_log_link ON objects IS 'Object versions have logs associated with them.';


--
-- Name: object_namespace_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY objects
    ADD CONSTRAINT object_namespace_link FOREIGN KEY (namespace) REFERENCES pid_namespaces(id);


--
-- Name: CONSTRAINT object_namespace_link ON objects; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT object_namespace_link ON objects IS 'Objects belong to namespaces.';


--
-- Name: object_relationships_predicate_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY object_relationships
    ADD CONSTRAINT object_relationships_predicate_link FOREIGN KEY (predicate_id) REFERENCES predicates(id);


--
-- Name: CONSTRAINT object_relationships_predicate_link ON object_relationships; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT object_relationships_predicate_link ON object_relationships IS 'The relationship has a well defined predicate.';


--
-- Name: object_relationships_subject_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY object_relationships
    ADD CONSTRAINT object_relationships_subject_link FOREIGN KEY (subject) REFERENCES objects(id) ON DELETE CASCADE;


--
-- Name: CONSTRAINT object_relationships_subject_link ON object_relationships; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT object_relationships_subject_link ON object_relationships IS 'Each object relationship subject is an object.';


--
-- Name: object_user_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY objects
    ADD CONSTRAINT object_user_link FOREIGN KEY (owner) REFERENCES users(id);


--
-- Name: CONSTRAINT object_user_link ON objects; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT object_user_link ON objects IS 'Objects can be owned by a user.';


--
-- Name: old_datastream_datastream_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY old_datastreams
    ADD CONSTRAINT old_datastream_datastream_link FOREIGN KEY (current_datastream) REFERENCES datastreams(id) ON DELETE CASCADE;


--
-- Name: CONSTRAINT old_datastream_datastream_link ON old_datastreams; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT old_datastream_datastream_link ON old_datastreams IS 'Old datastreams can be older versions of existing datastreams.';


--
-- Name: old_datastream_log_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY old_datastreams
    ADD CONSTRAINT old_datastream_log_link FOREIGN KEY (log) REFERENCES log(id);


--
-- Name: CONSTRAINT old_datastream_log_link ON old_datastreams; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT old_datastream_log_link ON old_datastreams IS 'Old datastream versions can have log entries.';


--
-- Name: old_datastreams_uri_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY old_datastreams
    ADD CONSTRAINT old_datastreams_uri_link FOREIGN KEY (uri_id) REFERENCES resources(id);


--
-- Name: CONSTRAINT old_datastreams_uri_link ON old_datastreams; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT old_datastreams_uri_link ON old_datastreams IS 'Old datastreams could have had resources.';


--
-- Name: old_objects_log_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY old_objects
    ADD CONSTRAINT old_objects_log_link FOREIGN KEY (log) REFERENCES log(id);


--
-- Name: CONSTRAINT old_objects_log_link ON old_objects; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT old_objects_log_link ON old_objects IS 'Old object info can have log entries.';


--
-- Name: old_objects_object_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY old_objects
    ADD CONSTRAINT old_objects_object_link FOREIGN KEY (current_object) REFERENCES objects(id) ON DELETE CASCADE;


--
-- Name: CONSTRAINT old_objects_object_link ON old_objects; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT old_objects_object_link ON old_objects IS 'Old objects are older versions of existing objects.';


--
-- Name: old_objects_owner_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY old_objects
    ADD CONSTRAINT old_objects_owner_link FOREIGN KEY (owner) REFERENCES users(id);


--
-- Name: CONSTRAINT old_objects_owner_link ON old_objects; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT old_objects_owner_link ON old_objects IS 'Old versions of objects could have belonged to users.';


--
-- Name: predicate_rdf_namespace_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY predicates
    ADD CONSTRAINT predicate_rdf_namespace_link FOREIGN KEY (rdf_namespace_id) REFERENCES rdf_namespaces(id);


--
-- Name: CONSTRAINT predicate_rdf_namespace_link ON predicates; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT predicate_rdf_namespace_link ON predicates IS 'Predicates belong to RDF namespaces.';


--
-- Name: role_source_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY user_roles
    ADD CONSTRAINT role_source_link FOREIGN KEY (source_id) REFERENCES sources(id);


--
-- Name: uri_checksum_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY checksums
    ADD CONSTRAINT uri_checksum_link FOREIGN KEY (uri) REFERENCES resources(id);


--
-- Name: CONSTRAINT uri_checksum_link ON checksums; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT uri_checksum_link ON checksums IS 'Checksums belong to URIs.';


--
-- Name: uri_datastream_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY datastreams
    ADD CONSTRAINT uri_datastream_link FOREIGN KEY (resource_id) REFERENCES resources(id);


--
-- Name: CONSTRAINT uri_datastream_link ON datastreams; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT uri_datastream_link ON datastreams IS 'Many datastreams or versions may point to the same URI.';


--
-- Name: user_source_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY users
    ADD CONSTRAINT user_source_link FOREIGN KEY (source_id) REFERENCES sources(id);


--
-- Name: CONSTRAINT user_source_link ON users; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT user_source_link ON users IS 'Users can belong to sources.';


--
-- Name: viewable_by_role_datastream_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY datastream_is_viewable_by_role
    ADD CONSTRAINT viewable_by_role_datastream_link FOREIGN KEY (rdf_subject) REFERENCES datastreams(id) ON DELETE CASCADE;


--
-- Name: viewable_by_role_object_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY object_is_viewable_by_role
    ADD CONSTRAINT viewable_by_role_object_link FOREIGN KEY (rdf_subject) REFERENCES objects(id) ON DELETE CASCADE;


--
-- Name: viewable_by_user_datastream_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY datastream_is_viewable_by_user
    ADD CONSTRAINT viewable_by_user_datastream_link FOREIGN KEY (rdf_subject) REFERENCES datastreams(id) ON DELETE CASCADE;


--
-- Name: viewable_by_user_object_link; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY object_is_viewable_by_user
    ADD CONSTRAINT viewable_by_user_object_link FOREIGN KEY (rdf_subject) REFERENCES objects(id) ON DELETE CASCADE;


--
-- Name: public; Type: ACL; Schema: -; Owner: -
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;


--
-- PostgreSQL database dump complete
--

