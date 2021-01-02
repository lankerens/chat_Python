import pymysql

# 用户注册
def register(id, name):
    # 连接database
    conn = pymysql.connect(host="127.0.0.1", user="root", password="0212", database="chat_py", charset="utf8")
    cursor = conn.cursor()
    id = int(id)
    sql0 = "select * from `user` where id = '%d' or name = '%s'" % (id, name)
    rows = cursor.execute(sql0)
    if rows > 0 :
        return False

    sql = "INSERT into `user`(id, name) values('%d','%s')" % (id, name)
    # print(sql)
    rows = cursor.execute(sql)
    conn.commit()
    if rows == 0:
        return False
    return True



#  创建群组
def createGroup(mid, name):
    # 连接database
    conn = pymysql.connect(host="127.0.0.1", user="root", password="0212", database="chat_py", charset="utf8")
    cursor = conn.cursor()

    mid = int(mid)

    sql = "insert into `group`(name) values('%s')" % (name)

    # print(sql)
    rows = cursor.execute(sql)
    last_id = cursor.lastrowid

    # 这里会有多线程写读问题吗， 一定是刚刚插入的 ？？  innodb 底层并没有对这种同步吧。。。
    sql0 = "insert into `group_member`(id, memberID) values('%d', '%d')" % (last_id, mid)
    rows2 = cursor.execute(sql0)
    conn.commit()
    if rows == 0 or rows2 == 0:
        conn.rollback()
        return False
    return True


#  加入群组
def joinGroup(id, mid):
    # 连接database
    conn = pymysql.connect(host="127.0.0.1", user="root", password="0212", database="chat_py", charset="utf8")
    cursor = conn.cursor()
    mid = int(mid)
    id = int(id)

    sql0 = "select * from `group_member`where id = '%d' and memberID = '%d'" % (id, mid)
    rows = cursor.execute(sql0)
    if rows > 0:
        return False

    sql = "insert into `group_member`(id, memberID) values('%d', '%d')" % (id, mid)
    # print(sql)
    rows = cursor.execute(sql)
    conn.commit()
    if rows == 0:
        conn.rollback()
        return False
    return True

#  退出群组
def exitGroup(id, mid):
    # 连接database
    conn = pymysql.connect(host="127.0.0.1", user="root", password="0212", database="chat_py", charset="utf8")
    cursor = conn.cursor()
    mid = int(mid)
    id = int(id)

    sql0 = "select * from group_member where id = '%d' and memberID = '%d'" % (id, mid)
    rows = cursor.execute(sql0)
    if rows == 0:
        return False

    sql = "delete from group_member where id = '%d' and memberID = '%d'" % (id, mid)
    # print(sql)
    rows = cursor.execute(sql)
    conn.commit()
    if rows == 0:
        conn.rollback()
        return False
    return True
