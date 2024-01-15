import pymysql
import db_config 
from flask import *
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

db_config.db_connection.get_db()
event_dao = db_config.EventDao()

@app.route('/')
def home():
    return render_template('calendar_events.html')


@app.route('/insert_event', methods=['POST'])
def insert_event():
    #시작 날짜/종료 일자 검증 로직 필요

    #실제 db에 insert 하기
    event_name = request.form['event_name']
    memo = request.form['memo']
    from_date = request.form['from_date']
    end_date = request.form['end_date']
    url = request.form['url']
    priority = request.form['priority']

    print(f"------------결과값 {event_name}, {memo}, {from_date} {end_date} {url} {priority} ------------")
    event_dao.insert_event(event_name, memo, from_date,end_date, url, priority)

    return redirect(url_for("home"))


@app.route('/calendar-events')
def calendar_events():
    conn = None
    cursor = None
    try:
        conn = db_config.db_connection.get_db()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        ## 자기자신의 일정만 보이게하기 where문에 추가 필요
        cursor.execute("SELECT id, title, url, class, UNIX_TIMESTAMP(start_date)*1000 as start, UNIX_TIMESTAMP(end_date)*1000 as end FROM event") 
        rows = cursor.fetchall()
        resp = jsonify({'success' : 1, 'result' : rows})
        resp.status_code = 200
        print(resp)
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

if __name__ == "__main__":
    app.run(debug=True)
