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
def board():
    sql = "select * from board"
    cur.execute(sql)
    a = cur.fetchall()
    return render_template("board.html", data_list=a)


@app.route("/makepost")
def makepost():
    return render_template("makepost.html")

@app.route('/write_action',methods=['GET','POST'])
def write_action():
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


@app.route("/post")
def post():
    writer = request.args.get('writer')
    other_value = request.args.get('other_value')
    return render_template("post.html",content=other_value,title=writer)


if __name__ == "__main__":
    app.run(debug=True)
    
