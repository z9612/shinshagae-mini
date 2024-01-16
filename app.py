import pymysql
import db_config 
from flask import *
from flask_cors import CORS
from board import board_bp
from userlogin import user_bp
from chat_main import chat_bp

app = Flask(__name__)

CORS(app)

db_config.db_connection.get_db()
event_dao = db_config.EventDao()

# app.register_blueprint(board_bp)
app.register_blueprint(user_bp)
app.register_blueprint(chat_bp)

@app.route('/')
def home():
    return render_template('calendar_events.html')

#자신의 이벤트 전체 보기
@app.route('/calendar-events')
def calendar_events():
    resp = event_dao.select_all()
    return resp

#한 이벤트 상세보기
@app.route('/calendar_events.html/<event_id>')
def select_one(event_id):
    result = event_dao.select_one(event_id)
    print("result :: " , result)
    return render_template('result_data.html', result=result)

@app.route('/insert_event', methods=['POST'])
def insert_event():
    #실제 db에 insert 하기

    #userno = userno
    event_name = request.form['event_name']
    memo = request.form['memo']
    from_date = request.form['from_date']
    end_date = request.form['end_date']
    priority = request.form['priority']

    # 시작 일자와 끝 일자 비교
    if from_date > end_date:
        return render_template('alert.html')
    elif end_date < from_date :
        return render_template('alert.html')
    else:
        print(f"------------결과값 {event_name}, {memo}, {from_date}, {end_date} , {priority} ------------")
        event_dao.insert_event(event_name, memo, from_date, end_date, priority)

        return redirect(url_for("home"))
    
#수정 겸 삭제   
@app.route('/update_event' , methods=['POST'])
def update_event():
    action_type = request.form['submitType']

    #수정할 이벤트 번호, 내용 등 입력받기
    
    #update
    if action_type == '수정':
        print("수정 들어옴")

        id= request.form['id']
        event_name = request.form['event_name']
        memo = request.form['memo']
        from_date = request.form['from_date']
        end_date = request.form['end_date']
        priority = request.form['priority']

        # 시작 일자와 끝 일자 비교
        if from_date > end_date:
            return render_template('alert.html')
        elif end_date < from_date :
            return render_template('alert.html')
        else :
            print(f"------------결과값 {id}, {event_name}, {memo}, {from_date}, {end_date}, {priority} ------------")
            event_dao.update_event(id, event_name, memo, from_date, end_date, priority)
            return redirect(url_for("home"))
    #delete
    elif action_type == '삭제':
        id= request.form['id']
        event_dao.delete_event(id)

        return redirect(url_for("home"))
    else:
        return 'Invalid action type'


if __name__ == "__main__":
    app.run(debug=True)
