import pymysql
import UserController

def db_conn():
    db = pymysql.connect(
    user = 'jh',
    passwd = '12345',
    host = 'database-1.cyrzsv0jbwjm.ap-northeast-2.rds.amazonaws.com',
    db = 'project',
    charset = 'utf8',
    autocommit = True
    )
    #객체 만들어서 반환해주기
    return db

#유저등록
def insertUser(userid, email, userpasswd, username, iddate):
    con = db_conn()
    cursor = con.cursor()

    sql_insert = 'insert into user (userid, email, userpasswd, username, iddate) values (%s,%s,%s,%s,%s)'
    result_num = cursor.execute(sql_insert,(userid, email, userpasswd, username, iddate))
    #결과 반환하지않고 걍 cursor.execute(sql_insert,(dname,loc)) 이렇게 할 수도 있음.
    
    cursor.close()
    con.close()
    
    return result_num

#유저삭제
def deleteUser(userid):
    con = db_conn()
    cursor = con.cursor()

    sql_delete = 'delete from user where userid = %s'
    result_num = cursor.execute(sql_delete,(userid))

    cursor.close()
    con.close()
    
    return result_num


#유저정보찾기
def search_user(userid,userpasswd):

    con = db_conn()
    cursor = con.cursor(cursor=pymysql.cursors.DictCursor)

    #입력받은 userid, userpasswd에 대하여 sql테이블user에서 있으면
    sql_search = 'select * from user where userid = %s and userpasswd = %s'
    cursor.execute(sql_search,(userid,userpasswd))

    #질문 >> 값이 없을때 result값이 무엇인지############-> None임 
    result = cursor.fetchone()
    
    cursor.close()
    con.close()

    return result



#유저 정보 출력
def print_user(userid,userpasswd):

    con = db_conn()
    cursor = con.cursor(cursor=pymysql.cursors.DictCursor)

    #입력받은 userid, userpasswd에 대하여 sql테이블user에서 있으면
    sql_search = 'select * from user where userid = %s and userpasswd = %s'
    cursor.execute(sql_search,(userid,userpasswd))

    #질문 >> 값이 없을때 result값이 무엇인지############-> None임 
    result = cursor.fetchone()

    cursor.close()
    con.close()

    return result


#유저 업데이트
def updateUser(userid, email, userpasswd, username):

    con = db_conn()
    cursor = con.cursor()

    #입력받은 userid, userpasswd에 대하여 sql테이블user에서 있으면
    sql_update = 'update user set userid=%s, email=%s, userpasswd=%s where username=%s'
    result_num = cursor.execute(sql_update,(userid, email, userpasswd, username))

    # sql_insert = 'insert into user (userid, email, userpasswd, username, iddate) values (%s,%s,%s,%s,%s)'
    # result_num = cursor.execute(sql_insert,(userid, email, userpasswd, username, iddate))


    cursor.close()
    con.close()

    return result_num