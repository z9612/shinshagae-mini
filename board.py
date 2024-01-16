from flask import *
import pymysql

db = pymysql.connect(
    host="database-1.cyrzsv0jbwjm.ap-northeast-2.rds.amazonaws.com",
    user="jjh",
    passwd="12345",
    db="project",
    charset="utf8",
)

app = Flask(__name__)
cur = db.cursor()

@app.route("/board")
def board(): # 게시판 목록
    sql = "select b.postno,u.userid,b.title,b.content,b.view_count,b.comment_count,b.create_date,b.modify_date from board b,user u where b.userno=u.userno"
    cur.execute(sql)
    a = cur.fetchall()
    return render_template("board.html", data_list=a)

@app.route("/makepost")
def makepost(): #게시물 작성 페이지 이동
    return render_template("makepost.html")

@app.route('/write_post_action',methods=['GET','POST'])
def write_post_action(): #게시물 작성 버튼 -> sql에 작성 내용 입력
    if request.method =='POST':
        title = request.form.get("title")
        writer = request.form.get("writer")
        content = request.form.get("content")

        sql="INSERT INTO board (title, content, userno) VALUES(%s, %s, %s)"
        values=(title,content,writer)
        cur.execute(sql,values)
        db.commit()
        return redirect(url_for('board'))
    else:
        return "THis is a GET request"

@app.route("/update_list/<int:postno>",methods=['POST']) 
def update_list(postno):#게시물 수정 버튼을 통해 게시물 수정창으로 이동
    return redirect(url_for('updatepost',postno=postno))
        
@app.route("/updatepost/<int:postno>",methods=['GET','POST'])
def updatepost(postno): #게시물 수정 작업 
    if request.method=='POST': # 게시물 수정 post방식
        title=request.form.get("title")
        content=request.form.get("content")
        sql=f"update board set title='{title}',content='{content}' where postno={postno}"
        cur.execute(sql)
        db.commit()
        return  redirect(url_for('board'))
    elif request.method=='GET': #게시물 수정 get방식 
        sql = f"select * from board where postno={postno}"
        cur.execute(sql)
        post_data = cur.fetchone()
        return render_template("updatepost.html", postno=postno,post_data=post_data)
    else:
        abort(405)



@app.route("/delete_list/<int:postno>",methods=['POST'])
def delete_list(postno): #게시물 삭제 버튼 
    sql= f"delete from board where postno='{postno}' "
    cur.execute(sql)
    cur.connection.commit()
    return redirect(url_for('board'))


@app.route("/post",methods=["GET"])
def post():  # 게시물 클릭시 내용 확인
    writer = request.args.get('writer')
    other_value = request.args.get('other_value')
    postno_board = request.args.get('other_value2')
    plus_count_view(postno_board) # 조회수 증가 함수
    #sql=f"select * from comment where postno={postno_board}" #댓들 발췌 쿼리
    sql=f"select c.commentno,u.userid,c.content,c.postno from comment c, user u where c.userno=u.userno and c.postno={postno_board}"
    cur.execute(sql)
    a=cur.fetchall()
    return render_template("post.html",content=other_value,title=writer,
                          postno=postno_board,comment_list=a)

def plus_count_view(postno): #조회수 증가 함수
    if postno is not None:
        sql = f"update board set view_count=view_count+1 where postno={postno}" # 조회수 증가 쿼리
        cur.execute(sql)
        db.commit()

    
@app.route('/write_comment_action',methods=['GET','POST'])
def write_comment_action(): # 댓글 작성 버튼 
    if request.method =='POST':
        writer_comment=request.form.get("writer")
        content_comment =request.form.get('content')
        postno_comment=int(request.form.get('postno'))
        sql="INSERT INTO comment (userno,content,postno) VALUES(%s,%s,%s)"
        values=(writer_comment,content_comment,postno_comment)
        cur.execute(sql,values)
        db.commit()
        return redirect(request.referrer)
        #return redirect(url_for('post',postno=postno_comment))

@app.route('/delete_comment_list<int:commentno>',methods=['POST']) #댓글 삭제 함수
def delete_comment_list(commentno):
    sql=f"delete from comment where commentno={commentno}"
    cur.execute(sql)
    cur.connection.commit()
    return redirect(request.referrer)

if __name__ == "__main__":
    app.run(debug=True)
