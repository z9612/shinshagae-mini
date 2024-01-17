from flask import *
from flask_cors import CORS
import dbconnect as d


user_bp = Blueprint('user',__name__)

@user_bp.before_request
def before_request():
    g.userno = session.get('userno', None)
# @user_bp.route("/")
# def index():
#     return "Hello, World!"

@user_bp.route("/signup" ,methods=['POST','GET'])
def signup():
    if request.method=='GET':
        return render_template('sign_up.html')
    else:
        userid=request.form['userid']
        email = request.form['email']
        userpasswd = request.form['userpasswd']
        username = request.form['username']
        iddate=request.form['iddate']
        #db에 유저정보 저장 (회원가입완료)#######db에 저장되면서, 문구도뜨면서, 다시로그인하는화면으로 가게해야함
        return str(d.insertUser(userid,email,userpasswd,username,iddate))
    
@user_bp.route('/login', methods=['POST','GET'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    else:
        action_type = request.form['submitType']
        userid=request.form['userid']
        userpasswd = request.form['userpasswd']

        user = d.search_user(userid, userpasswd)

        #LOGIN 눌렀을때(로그인진행)
        if action_type == 'LOGIN':
            if d.search_user(userid,userpasswd)==None: # 유저아닐때
                return f'<script>alert("아이디와 비번 확인해주세요!!. {userid}님")</script>'
          
            else: #유저일때
                session['login-info'] = user
                # userno = session['login-info'].get('userno', None)
                print("!!!!! >> " , session['login-info'].get('userno', None))
                return redirect(url_for('home'))
                # return f'<script>alert("반갑습니다.{userid}님")</script>'
                ##### 위의 문구 뜬 다음, 캘린더페이지로 이동해야함
            
        #SIGNUP 눌렀을때(회원가입페이지로이동)
        elif action_type == 'SIGNUP':
            return redirect(url_for('signup'))
        
# --------------------------------------------

@user_bp.route('/mypage', methods=['POST','GET'])
def mypage():
    if request.method == 'GET': #걍 들어왔을때
        return render_template('mypage.html',userno=g.userno) # mypage에서 한번 더 아이디와 로그인확인!!
    
    else: #회원정보수정, 탈퇴하기 누를때 여기임 
        action_type = request.form['submitType']
        userid=request.form['userid']
        userpasswd = request.form['userpasswd']

        #회원정보수정 눌렀을때(#######)
        if action_type == '회원정보수정':
            if d.search_user(userid,userpasswd)==None: # 유저아닐때
                return '<script>alert("아이디와 비번 확인해주세요!!")</script>'
          
            else: #유저일때
                return redirect(url_for('update'))
            
            
        #탈퇴하기 눌렀을때(#####)
        elif action_type == '탈퇴하기':
            if d.search_user(userid,userpasswd)==None: # 유저아닐때
                return '<script>alert("아이디와 비번 확인해주세요!!")</script>'
          
            else: #유저일때
                return redirect(url_for('delete'))


@user_bp.route('/update', methods=['POST','GET'])
def update():
    if request.method=='GET': #걍 들어왔을때
        return render_template('update.html') # 수정필요 ===============================
          # update.html에 일단 보여지는거니까 유저정보나타내는거 일단 쭉쓰기
    else: # post로들어왔을때 (뭔가 입력받았을 때)

        userid=request.form['userid']
        email = request.form['email']
        userpasswd = request.form['userpasswd']
        username = request.form['username']

        # return '<script>alert("저장되었습니다")</script>' # 여기에 db에 수정된 내용 들어가야함.
        return str(d.updateUser(userid,email,userpasswd,username))


@user_bp.route('/delete', methods=['POST','GET'])
def delete():
    if request.method == 'GET': #걍 들어왔을때
        return render_template('delete.html')
    else: # 네 아니오
        action_type = request.form['submitType']

        if action_type == '네':
            return '<script>alert("탈퇴되었습니다!")</script>'
        elif action_type =='아니오':
            return '<script>alert("탈퇴하지않으셨습니다!")</script>'


if __name__=='__main__':
    user_bp.run(debug=True)



#d.deleteUser(userid) 삭제하는거 했음.>> 회원가입페이지에서 이용됨