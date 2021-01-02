create table message
(
    id      int auto_increment
        primary key,
    source  int            null,
    target  int            null,
    time    datetime       null,
    message varchar(20000) null,
    status  int            null
);

INSERT INTO chat_py.message (id, source, target, time, message, status) VALUES (12, 1, 2, '2021-01-01 18:50:54', '123', 1);
INSERT INTO chat_py.message (id, source, target, time, message, status) VALUES (13, 2, 1, '2021-01-01 18:53:30', '12', 1);
INSERT INTO chat_py.message (id, source, target, time, message, status) VALUES (14, 2, 1, '2021-01-01 19:31:20', 'ok', 1);
INSERT INTO chat_py.message (id, source, target, time, message, status) VALUES (15, 1, 2, '2021-01-01 19:31:38', 'hhh', 1);
INSERT INTO chat_py.message (id, source, target, time, message, status) VALUES (16, 2, 1, '2021-01-01 19:31:48', 'pu', 1);
INSERT INTO chat_py.message (id, source, target, time, message, status) VALUES (17, 2, 3, '2021-01-01 19:32:21', '123', 1);
INSERT INTO chat_py.message (id, source, target, time, message, status) VALUES (18, 1, 2, '2021-01-01 19:36:42', '1', 1);
INSERT INTO chat_py.message (id, source, target, time, message, status) VALUES (19, 1, 2, '2021-01-01 21:54:19', '22', 1);
INSERT INTO chat_py.message (id, source, target, time, message, status) VALUES (20, 2, 1, '2021-01-01 21:54:22', '11', 1);
INSERT INTO chat_py.message (id, source, target, time, message, status) VALUES (21, 2, 1, '2021-01-01 21:54:26', '22', 1);
INSERT INTO chat_py.message (id, source, target, time, message, status) VALUES (22, 2, 1, '2021-01-01 22:01:49', '2', 1);
INSERT INTO chat_py.message (id, source, target, time, message, status) VALUES (23, 2, 1, '2021-01-01 22:03:15', '2', 1);
INSERT INTO chat_py.message (id, source, target, time, message, status) VALUES (24, 1, 55, '2021-01-01 22:48:56', '12', 1);
INSERT INTO chat_py.message (id, source, target, time, message, status) VALUES (25, 55, 1, '2021-01-01 22:49:00', 'over', 1);
INSERT INTO chat_py.message (id, source, target, time, message, status) VALUES (26, 1, 55, '2021-01-01 22:49:04', 'nice', 1);
INSERT INTO chat_py.message (id, source, target, time, message, status) VALUES (27, 65, 1, '2021-01-02 18:14:33', 'hello', 1);
INSERT INTO chat_py.message (id, source, target, time, message, status) VALUES (28, 1, 65, '2021-01-02 18:15:49', '你好你好', 1);
INSERT INTO chat_py.message (id, source, target, time, message, status) VALUES (29, 65, 1, '2021-01-02 18:15:56', '在干嘛呢', 1);
INSERT INTO chat_py.message (id, source, target, time, message, status) VALUES (30, 1, 65, '2021-01-02 18:16:05', '写python文档呀', 1);
INSERT INTO chat_py.message (id, source, target, time, message, status) VALUES (31, 1, 3, '2021-01-02 18:34:03', '给离线的好友发送消息', 1);
INSERT INTO chat_py.message (id, source, target, time, message, status) VALUES (32, 1, 3, '2021-01-02 18:34:07', '1111', 1);
INSERT INTO chat_py.message (id, source, target, time, message, status) VALUES (33, 3, 1, '2021-01-02 18:35:57', '我看到了', 1);