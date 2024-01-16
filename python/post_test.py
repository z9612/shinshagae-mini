from flask import *
import dbconnect as d

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello, World!"

# 5000번으로 들어왔을떄, 호스트 방식으로 요청이들어오고 url 들어온거 확인하ㅣㄱ. (라우팅설정!!)
@app.route('/login', methods=['POST'])
def login():

    uname=request.form['uname']
    pw = request.form['pass']

    if uname == 'nam' and pw=='12345' :
    #if uname == 'nam' and pw=='12345': # uname이 user테이블에 userid와 일치하는게 있는지.
        # uname이 user테이블에 userid와 일치하는게 있는지.
        return f'반갑습니다.{uname}님'
    else:
        return f'아이디/비밀번호를 다시 확인해주세요!!'

if __name__=='__main__':
    app.run()
