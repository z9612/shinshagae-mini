import secrets
import db_config 
from flask import *
from flask_cors import CORS
from board import board_bp
from userlogin import user_bp
from chat_main import chat_bp
import logging
from logging.config import fileConfig

app = Flask(__name__)
app.config['SECRET_KEY'] = app.config['SECRET_KEY'] = secrets.token_hex(24)

# 로깅 설정
fileConfig('logging.conf', encoding='utf-8')
logger = logging.getLogger(__name__)

CORS(app)

db_config.db_connection.get_db()
event_dao = db_config.EventDao()

app.register_blueprint(board_bp)
app.register_blueprint(user_bp)
app.register_blueprint(chat_bp)

@app.route('/')
def home():
    logger.info("Home route accessed")
    logger.info(f"userno :::{session['login-info'].get('userno', None)} ")
    return render_template('calendar_events.html', userno=session['login-info'].get('userno', None))

# 자신의 이벤트 전체 보기
@app.route('/calendar-events')
def calendar_events():
    logger.info("Calendar events route accessed")
    resp = event_dao.select_all(session['login-info'].get('userno', None))
    return resp

# 한 이벤트 상세보기
@app.route('/calendar_events.html/<event_id>')
def select_one(event_id):
    logger.info(f"Select one route accessed - event_id: {event_id}")
    result = event_dao.select_one(event_id)
    logger.info("Result :: " , result)
    return render_template('result_data.html', result=result, userno=session['login-info'].get('userno', None))

@app.route('/insert_event', methods=['POST'])
def insert_event():
    userno = session['login-info'].get('userno', None)
    event_name = request.form['event_name']
    memo = request.form['memo']
    from_date = request.form['from_date']
    end_date = request.form['end_date']
    priority = request.form['priority']

    # 시작 일자와 끝 일자 비교
    if from_date > end_date:
        logger.warning("Insert event - Invalid date range")
        return render_template('alert.html')
    elif end_date < from_date:
        logger.warning("Insert event - Invalid date range")
        return render_template('alert.html')
    else:
        logger.info(f"Insert event - user: {userno}, event_name: {event_name}, memo: {memo}, from_date: {from_date}, end_date: {end_date}, priority: {priority}")
        event_dao.insert_event(event_name, memo, from_date, end_date, priority, userno)
        return redirect(url_for("home"))

# 수정 겸 삭제
@app.route('/update_event', methods=['POST'])
def update_event():
    action_type = request.form['submitType']

    # update
    if action_type == '수정':
        logger.info("Update event route accessed - 수정")
        id = request.form['id']
        event_name = request.form['event_name']
        memo = request.form['memo']
        from_date = request.form['from_date']
        end_date = request.form['end_date']
        priority = request.form['priority']
        userno = session['login-info'].get('userno', None)

        # 시작 일자와 끝 일자 비교
        if from_date > end_date:
            logger.warning("Update event - Invalid date range")
            return render_template('alert.html')
        elif end_date < from_date:
            logger.warning("Update event - Invalid date range")
            return render_template('alert.html')
        else:
            logger.info(f"Update event - id: {id}, event_name: {event_name}, memo: {memo}, from_date: {from_date}, end_date: {end_date}, priority: {priority}, userno: {userno}")
            event_dao.update_event(id, event_name, memo, from_date, end_date, priority, userno)
            return redirect(url_for("home"))
    # delete
    elif action_type == '삭제':
        id = request.form['id']
        logger.info(f"Delete event - id: {id}, userno: {session['login-info'].get('userno', None)}")
        event_dao.delete_event(id, session['login-info'].get('userno', None))
        return redirect(url_for("home"))
    else:
        logger.warning("Invalid action type")
        return 'Invalid action type'

if __name__ == "__main__":
    app.run(debug=True)
