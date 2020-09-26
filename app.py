from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from datetime import datetime
from sqlalchemy import desc
from flask import render_template
import numpy as np
import sys
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties
import base64
from io import BytesIO

app=Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] ='postgres://brjgqjmnamwnxc:2038ec5ace178f7e6f34d1015384a39e7274126f60488b14a5403582ae5a8966@ec2-3-95-87-221.compute-1.amazonaws.com:5432/d3s7d1dsfli0sd'

app.config[
    'SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
groupId=0
class usermessage(db.Model):
    __tablename__ ='usermessage'
    id = db.Column(db.String(50), primary_key=True)
    group_num = db.Column(db.Text)
    nickname = db.Column(db.Text)
    group_id = db.Column(db.String(50))
    type = db.Column(db.Text)
    status = db.Column(db.Text)
    account = db.Column(db.Text)
    user_id = db.Column(db.String(50))
    message = db.Column(db.Text)
    birth_date = db.Column(db.TIMESTAMP)

def get_debtPeople(mode):
    userId = request.values['userId']
    data_UserData = usermessage.query.filter(usermessage.user_id==userId).filter(usermessage.status=='debt_set')
    DebtPeopleString=''
    for _data in data_UserData:
        DebtPeopleString += _data.nickname.strip(' ') +' '
    new_list = DebtPeopleString.strip(' ').replace('  ',' ').split(' ')
    new_list=list(set(new_list)) #刪除重複

    if mode ==1:
        return len(new_list)
    elif mode ==2:
        return new_list
    else:
        return 0

@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'POST':
        userId = request.values['userId']
        data_OweData = usermessage.query.order_by(usermessage.birth_date).filter(usermessage.user_id==userId).filter(usermessage.status=='owe').filter(usermessage.type=='user')
        data_BorrowData = usermessage.query.order_by(usermessage.birth_date).filter(usermessage.user_id==userId).filter(usermessage.status=='borrow').filter(usermessage.type=='user')
        save_dic = {}
        save_list = []
        count=0
        for _Data in data_OweData:
            count+=1
            save_dic['number'] = count
            save_dic['account'] = _Data.account
            save_dic['message'] = _Data.message
            save_dic['debtPerson'] ="欠/"+str(_Data.group_num)
            save_dic['debtStatus'] = _data.status
            save_list.append(save_dic)
            save_dic = {}
        for _Data in data_BorrowData:
            count+=1
            save_dic['number'] = count
            save_dic['account'] = _Data.account
            save_dic['message'] = _Data.message
            save_dic['debtPerson'] ="借/"+str(_Data.group_num)
            save_dic['debtStatus'] = _data.status
            save_list.append(save_dic)
            save_dic = {}

        debtPerson_list=get_debtPeople(2)
        person_total=''
        total = 0
        for i in range(get_debtPeople(1)):
            debtPerson = str(debtPerson_list[i])        
            for j in range(len(save_list)):
                historyPerson = str(save_list[j]['debtPerson'])
                msgStatus = str(save_list[j]['debtStatus'])
                if debtPerson == historyPerson:
                    if msgStatus == "owe":
                        total -= int(history_list[j]['Account'])
                    if msgStatus == "borrow":
                        total += int(history_list[j]['Account'])
            if total > 0:
                person_total += '我共借'+str(debtPerson)+str(total)+'元'+'\n'
            if total < 0:
                total=abs(total)
                person_total += '我共欠'+str(debtPerson)+str(total)+'元'+'\n'
            total = 0
      
        
        return render_template('index_form.html',**locals())

    return render_template('home.html',**locals())

@app.route('/submit',methods=['POST','GET'])
def submit():
    groupId = 0

    return groupId

if __name__ =="__main__":
    app.run()
