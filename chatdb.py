import pymysql
# DB 연결 : connect()

# DB 연결한 Connection 객체를 반환하는 함수
def db_conn():
    db=pymysql.connect(

    host='database-1.cyrzsv0jbwjm.ap-northeast-2.rds.amazonaws.com',
    user='dh',
    password='12345',
    db='project', 
    charset='utf8',
    autocommit=True
    )
    return db

def ShowShareDate(chatid):
    result=[]
    con=db_conn()
    cursor=con.cursor(pymysql.cursors.DictCursor)
    sql_select='select userno,chatid,event from project.shareevent where chatid=%s'
    cursor.execute(sql_select,chatid)
    result=cursor.fetchall()
    cursor.close()
    con.close()
    return result

def ShareDate(userno,chatid,event):
    con =db_conn()
    cursor=con.cursor()
    sql_insert='insert into project.shareevent (userno,chatid,event)  values(%s,%s,%s);'
    result_num=cursor.execute(sql_insert,(userno,chatid,event))
    cursor.close()
    con.close()
    return result_num

def SShareDate(userno,event):
    con =db_conn()
    cursor=con.cursor()
    sql_insert='insert into project.event (userno,title)  values(%s,%s);'
    result_num=cursor.execute(sql_insert,(userno,event))
    cursor.close()
    con.close()
    return result_num

def ShowDate(userno):
    result=[]
    con=db_conn()
    cursor=con.cursor(pymysql.cursors.DictCursor)
    sql_select='select * from project.event where userno=%s'
    cursor.execute(sql_select,userno)
    result=cursor.fetchall()
    cursor.close()
    con.close()
    return result

def SearchChatRoom(chatid):
    result=[]
    con=db_conn()
    cursor=con.cursor(pymysql.cursors.DictCursor)
    sql_select='select * from project.chatroom where chatid=%s'
    cursor.execute(sql_select,chatid)
    result=cursor.fetchone()
    cursor.close()
    con.close()
    return result

def MakeChatRoom(chatid):
    con =db_conn()
    cursor=con.cursor()
    sql_insert='insert into project.chatroom (chatid)  values(%s);'
    result_num=cursor.execute(sql_insert,chatid)
    cursor.close()
    con.close()
    return result_num