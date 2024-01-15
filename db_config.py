import pymysql

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
        
    def insert_event(self, title, memo, start_date, end_date, url, priority):
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
    
    # def update_book(self, bookid, bookname, publisher, price):
    #     cursor = db_connection.get_db().cursor(pymysql.cursors.DictCursor)
    #     sql = "update book set bookname=%s, publisher=%s, price=%s where bookid=%s"
    #     result = cursor.execute(sql,(bookname, publisher, price, bookid))

    #     print(f"update_num :: {result}")

    #     db_connection.get_db().close()
    #     return result
        
    # def delete_book(self, bookid):
    #     cursor = db_connection.get_db().cursor(pymysql.cursors.DictCursor)
    #     sql = "delete from book where bookid=%s"

    #     result = cursor.execute(sql,(bookid))

    #     print(f"delete_num :: {result}")

    #     db_connection.get_db().close()
    #     return result