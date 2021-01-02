create table user
(
    id     int            not null
        primary key,
    name   varchar(50)    null,
    status int default -1 null,
    ip     int default 0  null,
    port   int default 0  null
);

INSERT INTO chat_py.user (id, name, status, ip, port) VALUES (1, 'lankerens', -1, 0, 0);
INSERT INTO chat_py.user (id, name, status, ip, port) VALUES (2, 'ryder', -1, 0, 0);
INSERT INTO chat_py.user (id, name, status, ip, port) VALUES (3, 'orzz', -1, 0, 0);
INSERT INTO chat_py.user (id, name, status, ip, port) VALUES (55, 'tdm', -1, 0, 0);
INSERT INTO chat_py.user (id, name, status, ip, port) VALUES (65, 'gjx', -1, 0, 0);