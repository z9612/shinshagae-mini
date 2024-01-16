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

def showmessage(chatid):
    result=[]
    con=db_conn()
    cursor=con.cursor(pymysql.cursors.DictCursor)
    sql_select='select chatid,userid,text from project.chatting where chatid=%s '
    cursor.execute(sql_select,chatid)
    result=cursor.fetchall()
    cursor.close()
    con.close()
    return result

def sendmessage(chatid,userid,text):
    con =db_conn()
    cursor=con.cursor()
    sql_insert='insert into project.chatting (text,chatid,userid)  values(%s,%s,%s);'
    result_num=cursor.execute(sql_insert,(text,chatid,userid))
    cursor.close()
    con.close()
    return result_num