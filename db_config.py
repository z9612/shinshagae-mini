import pymysql
from datetime import timedelta, datetime

class db_connection : 
    def get_db() :
        project_db = pymysql.connect(
            user='giun',
            passwd='12345',
            host='database-1.cyrzsv0jbwjm.ap-northeast-2.rds.amazonaws.com',
            db='project',
            charset='utf8',
            autocommit=True
        )
            
        return project_db
    
class EventDao:
    def __init__(self):
            pass
    def select_all(self):
        cursor = db_connection.get_db().cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM event;"
        cursor.execute(sql)
        result = cursor.fetchall()

        db_connection.get_db().close()
        return result
    
    def select_one(self,event_id):
        cursor = db_connection.get_db().cursor(pymysql.cursors.DictCursor)
        print("받은 event_id ::: ", event_id)
        sql = "SELECT * FROM event where id=%s;"
        cursor.execute(sql,(event_id))
        result = cursor.fetchone()
        
        db_connection.get_db().close()
        return result
        
    def insert_event(self, title, memo, start_date, end_date, url, priority):

        start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M")
        end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M")

        #시간 차이가 30분 이내면 30분 추가
        if (end_date - start_date).total_seconds() < 30 * 60:
            end_date += timedelta(minutes=30)
            print("시간 적용완료 ::: " , end_date)

        cursor = db_connection.get_db().cursor(pymysql.cursors.DictCursor)

        print("priority ::: " , priority)
        match priority :
            case '높음' :
                priority = 'event-important'
            case '중간' :
                priority = 'event-info'
            case '낮음' :
                priority = ''

        sql = "insert into event(title, memo, start_date, end_date, url, class) values(%s, %s, %s, %s, %s, %s)"

        result = cursor.execute(sql,(title, memo, start_date,end_date,url, priority))

        print(f"insert_num :: {result}")

        db_connection.get_db().close()
        return result
    
    def update_event(self, event_id, title, memo, start_date, end_date, url, priority):
        cursor = db_connection.get_db().cursor(pymysql.cursors.DictCursor)
        
        print("priority ::: " , priority)
        match priority :
            case '높음' :
                priority = 'event-important'
            case '중간' :
                priority = 'event-info'
            case '낮음' :
                priority = ''
        
        sql = "UPDATE event SET title=%s, memo=%s, start_date=%s, end_date=%s, url=%s, class=%s WHERE id=%s"
        result = cursor.execute(sql,(title, memo, start_date, end_date, url, priority,event_id))

        print(f"update_num :: {result}")

        db_connection.get_db().close()
        return result
        
    def delete_event(self, eventid):
        cursor = db_connection.get_db().cursor(pymysql.cursors.DictCursor)
        sql = "delete from event where id=%s"

        result = cursor.execute(sql,(eventid))

        print(f"delete_num :: {result}")

        db_connection.get_db().close()
        return result