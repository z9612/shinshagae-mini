from flask import *
# from flask_sqlalchemy import pagination

import math
import pymysql

db = pymysql.connect(
    host="database-1.cyrzsv0jbwjm.ap-northeast-2.rds.amazonaws.com",
    user="jjh",
    passwd="12345",
    db="project",
    charset="utf8",
)

cur = db.cursor()

board_bp = Blueprint("board", __name__)


@board_bp.route("/board")
def board():  # 게시판 목록
    # page = request.args.get("page", 1, type=int)
    # per_page = 10
    sql = "select b.postno,u.userid,b.title,b.content,b.view_count,b.comment_count,b.create_date,b.modify_date from board b,user u where b.userno=u.userno"

    cur.execute(sql)
    data_list = cur.fetchall()
    # pagination_instance = get_pagination(data_list, page, per_page)
    return render_template(
        "board.html", data_list=data_list)

# return render_template(
#     "board.html", data_list=pagination_instance.items, pagination=pagination_instance
# )


# def get_pagination(data_list, page, per_page):
#     start = (page - 1) * per_page
#     end = start + per_page
#     paginated_data = data_list[start:end]

#     # 페이징 객체 생성
#     pagination_instance = pagination(page, per_page)

#     # 페이징된 데이터를 설정
#     pagination_instance.items = paginated_data

#     return pagination_instance


@board_bp.route("/makepost")
def makepost():  # 게시물 작성 페이지 이동
     return render_template("makepost.html")


@board_bp.route("/write_post_action", methods=["GET", "POST"])
def write_post_action():  # 게시물 작성 버튼 -> sql에 작성 내용 입력
    if request.method == "GET":
        # title = request.form.get("title")
        # writer = request.form.get("writer")
        # content = request.form.get("content")

        # sql = "INSERT INTO board (title, content, userno) VALUES(%s, %s, %s)"
        # values = (title, content, writer)
        # cur.execute(sql, values)
        # db.commit()
        # return redirect(url_for("board.board"))
        return 'GET방식입니다.'
    elif request.method =="POST":
        title = request.form.get("title")
        writer = request.form.get("writer")
        content = request.form.get("content")
        sql = "INSERT INTO board (title, content, userno) VALUES(%s, %s, %s)"
        values = (title, content, writer)
        cur.execute(sql, values)
        db.commit()
        return redirect(url_for("board.board"))

# @board_bp.route("/update_list/<int:postno>",methods=['POST'])
# def update_list(postno):#게시물 수정 버튼을 통해 게시물 수정창으로 이동
#    return redirect(url_for('updatepost',postno=postno))


@board_bp.route("/updatepost/<int:postno>", methods=["GET", "POST"])
def updatepost(postno):  # 게시물 수정 작업
    if request.method == "POST":  # 게시물 수정 post방식
        title = request.form.get("title")
        content = request.form.get("content")
        sql = f"update board set title='{title}',content='{content}' where postno={postno}"
        cur.execute(sql)
        db.commit()
        return redirect(url_for("board.board"))
    elif request.method == "GET":  # 게시물 수정 get방식
        sql = f"select * from board where postno={postno}"
        cur.execute(sql)
        post_data = cur.fetchone()
        return render_template("updatepost.html", postno=postno, post_data=post_data)
    else:
        abort(405)


@board_bp.route("/delete_list/<int:postno>", methods=["POST"])
def delete_list(postno):  # 게시물 삭제 버튼
    sql = f"delete from board where postno='{postno}' "
    cur.execute(sql)
    cur.connection.commit()
    return redirect(url_for("board.board"))


@board_bp.route("/post/<int:postno>", methods=["GET"])
def post(postno):  # 게시물 클릭시 내용 확인
    plus_count_view(postno)  # 조회수 증가 함수
    sql_comment = f"select * from comment where postno={postno}"  # 댓들 발췌 쿼리
    cur.execute(sql_comment)
    a = cur.fetchall()
    print("a: ", a)
    sql_post = f"select * from board where postno={postno}"
    cur.execute(sql_post)
    b = cur.fetchall()
    print("b: ", b)
    return render_template("post.html", postno=postno, post_list=b, comment_list=a)


def plus_count_view(postno):  # 조회수 증가 함수
    if postno is not None:
        sql = f"update board set view_count=view_count+1 where postno={postno}"  # 조회수 증가 쿼리
        cur.execute(sql)
        db.commit()


@board_bp.route("/write_comment_action", methods=["POST"])
def write_comment_action():  # 댓글 작성 버튼
    writer_comment = request.form.get("writer")
    content_comment = request.form.get("content")
    postno_comment = request.form.get("postno")
    sql = "INSERT INTO comment (userno,content,postno) VALUES(%s,%s,%s)"
    values = (writer_comment, content_comment, postno_comment)
    cur.execute(sql, values)
    db.commit()
    return redirect(request.referrer)
    # return redirect(url_for('post',postno=postno_comment))


@board_bp.route("/delete_comment_list<int:commentno>", methods=["POST"])  # 댓글 삭제 함수
def delete_comment_list(commentno):
    sql = f"delete from comment where commentno={commentno}"
    cur.execute(sql)
    cur.connection.commit()
    return redirect(request.referrer)


# if __name__ == "__main__":
#    board_bp.run(debug=True)
