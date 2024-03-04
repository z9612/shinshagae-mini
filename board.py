from flask import *
from flask_paginate import Pagination, get_page_args
import logging
from logging.config import fileConfig
import math
import pymysql

db = pymysql.connect( # DB mysql 연결
    user='nana',
    passwd='nana1234',
    host='database-1.cvgatyvcfvop.ap-northeast-2.rds.amazonaws.com',
    db="project",
    charset="utf8",
)

cur = db.cursor() 
#fileConfig('logging.conf', encoding='utf-8')
logger = logging.getLogger(__name__)
board_bp = Blueprint("board", __name__)


@board_bp.route("/board")
def board():  # 게시판 목록
    logger.info("open board - event_id: 게시판열람")
    page, per_page, offset = get_page_args(
        page_parameter="page", per_page_parameter="per_page"
    )
    sql = """select b.postno,u.userid,b.title,b.content,b.view_count,b.comment_count,b.create_date,b.modify_date 
            from board b,user u 
            where b.userno=u.userno 
            order by b.postno desc"""  # 게시판 목록 불러오는 sql
    cur.execute(sql)
    data_list = cur.fetchall()
    total = len(data_list)
    pagination_instance = get_pagination(  # 페이징 함수 불러옴
        page=page,
        per_page=per_page,
        total=total,
        record_name="data_list",
        format_total=True,
        format_number=True,
    )
    paginated_data = data_list[offset : offset + per_page]
    return render_template(
        "board.html", data_list=paginated_data, pagination=pagination_instance
    )


def get_pagination(
    page, per_page, total, record_name, format_total=False, format_number=False
):  # 페이징 함수
    return Pagination(
        page=page,
        per_page=per_page,
        total=total,
        record_name=record_name,
        format_total=format_total,
        format_number=format_number,
    )


@board_bp.route("/makepost")
def makepost():  # 게시물 작성 페이지 이동
    return render_template("dnf주소/makepost.html")


@board_bp.route("/write_post_action", methods=["GET", "POST"])
def write_post_action():  # 게시물 작성 버튼 -> sql에 작성 내용 입력
    if request.method == "GET":
        return "잘못된 정보입니다."
    elif request.method == "POST":
        title = request.form.get("title")
        writer = session["login_info"].get("userno", None)
        content = request.form.get("content")
        sql = "INSERT INTO board (title, content, userno) VALUES(%s, %s, %s)"
        values = (title, content, writer)
        cur.execute(sql, values)
        db.commit()
        return redirect(url_for("board.board"))


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

    sql_post = f"""select b.*,u.userid 
            from board b, user u 
            where postno={postno} and b.userno=u.userno"""
    cur.execute(sql_post)
    b = cur.fetchall()
    return render_template("post.html", postno=postno, post_list=b, comment_list=get_comments(postno))

def get_comments(postno):
    sql_comment = f"""SELECT c.*, u.userid
        FROM comment c, user u
        WHERE postno = {postno} AND c.userno = u.userno """  # 댓들 발췌 쿼리
    cur.execute(sql_comment)
    return cur.fetchall()



def plus_count_view(postno):  # 조회수 증가 함수
    if postno is not None:
        sql = f"""update board # 조회수 증가 쿼리
                set view_count=view_count+1 
                where postno={postno}"""  
        cur.execute(sql)
        db.commit()


def count_comment(): # 댓글 수 카운팅하는 쿼리 사용하는 함수  
    sql = "update board set comment_count=(select count(*) from comment where board.postno=comment.postno)"
    cur.execute(sql)
    db.commit()


@board_bp.route("/write_comment_action", methods=["POST"])
def write_comment_action():  # 댓글 작성 버튼
    writer_comment = session["login_info"].get("userno", None)
    content_comment = request.form.get("content")
    postno_comment = request.form.get("postno")
    sql = "INSERT INTO comment (userno,content,postno) VALUES(%s,%s,%s)"
    values = (writer_comment, content_comment, postno_comment)
    cur.execute(sql, values)
    db.commit()
    count_comment()
    return redirect(request.referrer)


@board_bp.route("/delete_comment_list<int:commentno>", methods=["POST"])  # 댓글 삭제 함수
def delete_comment_list(commentno):
    sql = f"delete from comment where commentno={commentno}"
    cur.execute(sql)
    cur.connection.commit()
    return redirect(request.referrer)
