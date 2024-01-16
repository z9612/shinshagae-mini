from flask import *
import chatdb 
import msgdb

app =Flask(__name__)

@app.route("/chatroom")
def index():
   return render_template('chatroom.html')





@app.route('/chatroom/chat',methods=['POST','GET'])
def chat():
    if request.method=='POST':
            chatid=request.form["chatid"]
            userid=request.form["userid"]
            print('###userid###')
            print(userid)
            if chatid:
                is_chat=chatdb.SearchChatRoom(chatid)
                if is_chat:     
                    result1=[]
                    result1.append(chatid) #
                    result1.append(userid) #
                    print(result1)                             
                    return render_template("chat.html",result1=result1) 
                
                else:    
                    mk_chat=chatdb.MakeChatRoom(chatid)
                    result1=list(chatid)
                    result1=[]
                    result1.append(chatid) 
                    result1.append(userid) 
                    
                    return render_template("newchat.html",result1=result1) 
            else:
                print('null')
                return render_template("nochatid.html")
        

    else:
          return 'no data'
@app.route('/chatroom/chatting',methods=['POST'])
def chatting():
    text=request.form['text']
    chatid=request.form['chatid']
    userid=request.form['userid']
    send_msg=msgdb.sendmessage(chatid,userid,text)
    show_msg=msgdb.showmessage(chatid)
    result1=show_msg
    result2=[] # chatid ,userid 먼저 저장하고 채팅 로그 저장하는 리스트 
    for i in range(len(result1)):
         if i== 0 : 
             result2.append(result1[i]['chatid']) 
    
         else :break
    result2.append(userid)       


    for i in range(len(result1)):
            result2.append(result1[i]['userid'])
            result2.append(result1[i]['text'])
    list_len=len(result2)-2
    result2.insert(0,list_len)  


       
    return render_template("chatting.html",result1=result2) 
        


   


if(__name__=='__main__'):
   app.run(debug=True)