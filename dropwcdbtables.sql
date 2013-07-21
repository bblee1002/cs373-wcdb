-- dropwcdbtables.sql
DROP TABLE IF EXISTS auth_group;
DROP TABLE IF EXISTS auth_group_permissions;
DROP TABLE IF EXISTS auth_message;
DROP TABLE IF EXISTS auth_permission;
DROP TABLE IF EXISTS auth_user;
DROP TABLE IF EXISTS auth_user_groups;
DROP TABLE IF EXISTS auth_user_user_permissions;
DROP TABLE IF EXISTS django_content_type;
DROP TABLE IF EXISTS django_session;
DROP TABLE IF EXISTS django_site;
DROP TABLE IF EXISTS wcdb_crisis;
DROP TABLE IF EXISTS wcdb_li;
DROP TABLE IF EXISTS wcdb_org;
DROP TABLE IF EXISTS wcdb_person;
DROP TABLE IF EXISTS wcdb_relations;
COMMIT;
