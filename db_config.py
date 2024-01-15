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