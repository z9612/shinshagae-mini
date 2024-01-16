from flask import *
import mylogging2 as mylog
# pip install flask-cors
from flask_cors import CORS
import deptDAO as dao


app = Flask(__name__)
#CORS(app)
# Origin(출처)는 URL의 구성요소 중에서도 스킴(프로토콜), 호스트(도메인), 포트로 정의
CORS(app, resource={r'*':{'origins':'*'}}) # 모든 요청에 대한 CORS
# CORS(app,resource={r'*':{'origins':'localhost:5000/'}}) # localhost:5000/ 에서만 허용
# CORS(app,resource={r'/api/*':{'origins':'*'}}) # /api/로 시작되는 end_point만 허용


@app.route('/')
def hello() :
    return 'index'

@app.route('/dept')
def dept_manager():
    return render_template('dept.html')

@app.route('/api/depts')
def get_depts():
    mylog.logger.info('부서 리스트 출력')
    return jsonify(dao.selectDept())

@app.route('/api/depts/<int:deptno>')
def get_dept(deptno) :
    return jsonify(dao.selectDeptbyDeptno(deptno))  # args => json 형식으로 변경

@app.route('/api/depts', methods=['POST'])
def post_dept() :
    try :
        dept_json = request.get_json()
        print('>>>>>>', type(dept_json))
        print('>>>>>>', dept_json)
        result = dao.insertDept(dept_json['dname'], dept_json['loc'])

        mylog.logger.info('부서 정보 입력...')

        if result :
            return jsonify({'code' : 200, 'msg' : 'insert ok!'})
        else :
            return jsonify({'code' : 200, 'msg' : 'insert notthing!'})    

    except Exception as e :
        mylog.logger.error('입력 오류 Exception 발생 !')
        print(e)
        return jsonify({'code' : 500, 'msg' : 'server Error!!!!'})
    
@app.route('/api/depts/<int:deptno>', methods=['PUT'])
def put_dept(deptno) :

    try:
        req_data = request.get_json()
        print(type(req_data))
        print(req_data)        
        result = dao.updateDept(deptno, req_data['dname'], req_data['loc'])

        mylog.logger.info('부서 정보 수정...')

        if result :
            return jsonify({'code' : 200, 'msg' : 'edit ok!'})
        else :
            return jsonify({'code' : 200, 'msg' : 'edit notthing!'})
  
    except Exception as e :
        mylog.logger.error('수정 오류 Exception 발생 !')
        return jsonify({'code' : 500, 'msg' : 'server Error!!!!'})


@app.route('/api/depts/<int:deptno>', methods=['DELETE'])
def delete_dept(deptno) :

    try:
        result = dao.deleteDeptbydeptno(deptno)
        if result :
            return jsonify({'code' : 200, 'msg' : 'delete ok!'})
        else :
            return jsonify({'code' : 200, 'msg' : 'delete notthing!'})
    except Exception as e :
        mylog.logger.error('삭제 오류 Exception 발생 !')
        return jsonify({'code' : 500, 'msg' : 'server Error!!!!'})


if __name__ == '__main__' :
    app.run(debug=True)