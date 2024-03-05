from flask import *
import chatdb 
import msgdb
import logging
from logging.config import fileConfig

app =Flask(__name__)

chat_bp = Blueprint("chat", __name__)

# 로깅 설정
#fileConfig('logging.conf', encoding='utf-8')
logger = logging.getLogger(__name__)
bp_logger = logging.getLogger(__name__ + '.chat_bp')

logger.debug("This is a debug message from chat_main.py")

@chat_bp.route("/chatroom")
def index():
    print(__name__) 
    print("로그 시작")
    bp_logger.debug("로그 테스트!!!!!!!!!!!!!")
    print("로그 끝")
    return render_template('chatroom.html')

@chat_bp.route("/chatroom2",methods=['POST','GET'])
def chatroom2():
    id=request.form["id"]
    title=request.form["title"]
    print(title)
    result=[]
    result.append(title)
    return render_template('chatroom2.html',result=result)

@chat_bp.route('/chatroom/share',methods=['POST','GET'])
def share():
    chatid=request.form["chatid"]
    userno=request.form["userno"]
    shr_event=chatdb.ShowShareDate(chatid)
    print(shr_event)
    result1=shr_event
    result2=[]
    list_len=len(shr_event)
    result2.append(list_len)
    result2.append(chatid)
    result2.append(userno)
    for i in range(len(result1)):
        
        result2.append(result1[i]['userno'])
        result2.append(result1[i]['event'])
    
    return render_template('showshare.html',result1=result2)
@chat_bp.route('/chatroom/sharing', methods=['POST','GET'])
def sharing():
    print('here')
    if request.method=='POST':
            title=request.form["title"]        
            userno=request.form["userno"]
            chatid=request.form["chatid"]
            #userid=request.form["userid"]
           # print(userid) 
            if chatid:
                is_chat=chatdb.SearchChatRoom(chatid)

                is_date=chatdb.ShowDate(userno)


                for i in range(len(is_date)):
                    if(title==is_date[i]['title']):
                       result1=[]
                       result1.append(chatid)
                       result1.append(userno)
                       result1.append(title)
                 #      result1.append(userid)
                 #     print(result1[0])
                 #     print(result1[1])
                 #     print(result1[2])
                       return render_template("chat2.html",result1=result1)

@chat_bp.route('/chatroom/dateroom',methods=['POST','GET'])
def dateroom():
    userno=request.form["userno"]
    chatid=request.form["chatid"]
    print('here')
    #userid=request.form["userid"]
   
   #print('dateroom = ' ,userid)
    event=request.form["event"]
    shr_event=chatdb.ShareDate(userno,chatid,event)
    return render_template('dateroom.html')

@chat_bp.route('/chatroom/date',methods=['POST','GET'])
def date():
    userno=request.form["userno"]
    chatid=request.form["chatid"]
    event=request.form["event"]
    shr_event2=chatdb.SShareDate(userno,event)
    return render_template('date.html')

@chat_bp.route('/chatroom/chat',methods=['POST','GET'])
def chat():
    if request.method=='POST':
            
            userno=request.form["userno"]
            chatid=request.form["chatid"]
        
            if chatid:
                is_chat=chatdb.SearchChatRoom(chatid)
                
                is_date=chatdb.ShowDate(userno)
                
                
                #  for i in range(len(is_date)):
                  #  print(is_date[i]['title'])
                
                if is_chat:     
                    result1=[]
                    list_len=len(is_date)
                  #  print('약속 수 = list_len')
                    result1.append(chatid) #
                    result1.append(userno) #
                    result1.append(list_len)
                    for i in range(len(is_date)):
                        result1.append(is_date[i]['title'])
                 #   print(result1)                             
                    return render_template("chat.html",result1=result1) 
                
                else:    
                    mk_chat=chatdb.MakeChatRoom(chatid)
                    result1=list(chatid)
                    result1=[]
                    result1.append(chatid) 
                    result1.append(userno) 
                    
                    return render_template("newchat.html",result1=result1) 
            else:
                print('null')
                return render_template("nochatid.html")
        

    else:
          return render_template('chatroom.html')
@chat_bp.route('/chatroom/chatting',methods=['POST'])
def chatting():
    text=request.form['text']
    chatid=request.form['chatid']
    userno=request.form['userno']
    send_msg=msgdb.sendmessage(chatid,userno,text)
    show_msg=msgdb.showmessage(chatid)
    result1=show_msg
    result2=[] # chatid ,userno 먼저 저장하고 채팅 로그 저장하는 리스트 
    for i in range(len(result1)):
         if i== 0 : 
             result2.append(result1[i]['chatid']) 
    
         else :break
    result2.append(userno)       


    for i in range(len(result1)):
            result2.append(result1[i]['userno'])
            result2.append(result1[i]['text'])
    list_len=len(result2)-2
    result2.insert(0,list_len)  


       
    return render_template("chatting.html",result1=result2) 


if(__name__=='__main__'):
   app.run(debug=True)
