import pymysql

# 用户注册
def register(id, name):
    # 连接database
    conn = pymysql.connect(host="127.0.0.1", user="root", password="0212", database="chat_py", charset="utf8")
    cursor = conn.cursor()
    id = int(id)
    sql0 = "select * from user where id = '%d' or name = '%s'" % (id, name)
    rows = cursor.execute(sql0)
    if rows > 0 :
        return False

    sql = "INSERT into user(id, name) values('%d','%s')" % (id, name)
    # print(sql)
    rows = cursor.execute(sql)
    conn.commit()
    if rows == 0:
        return False
    return True



