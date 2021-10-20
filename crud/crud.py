# -*- coding: utf-8 -*-
from flask import Flask, render_template,request,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_

app = Flask(__name__)
app.secret_key = "Secret Key" #암호화시 필요한 키 값
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crud.db' #DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #이벤트 처리하는 옵션 추가적인 메모리를 필요로 하므로 꺼둠

db = SQLAlchemy(app)

class Employee(db.Model):
    idx = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FirstName = db.Column(db.String(10))
    LastName = db.Column(db.String(10))
    Email = db.Column(db.String(200))
    UserName = db.Column(db.String(10))
    Password = db.Column(db.String(10))
    Confirm = db.Column(db.String(200)) #추후 본인확인용


    def __init__(self, FirstName, LastName,Email,UserName,Password,Confirm):
        self.FirstName = FirstName
        self.LastName = LastName
        self.Email = Email
        self.UserName = UserName
        self.Password = Password
        self.Confirm = Confirm
    
@app.route('/crud')
def index():
    all_data = Employee.query.order_by(Employee.idx.desc()).all() # select * from Employee 내림차순 정렬 
    return render_template("user-form.html", all_data=all_data)
    
@app.route('/crud/insert', methods=['POST'])
def insert():
    FirstName = request.form['FirstName']
    LastName = request.form['LastName']
    Email = request.form['Email']
    UserName = request.form['UserName']
    Password = request.form['Password']
    Confirm = request.form['Confirm']

    insertUser = Employee(FirstName, LastName,Email,UserName,Password,Confirm)
    db.session.add(insertUser)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/crud/delete/<uid>')
def delete(uid):
    print(uid)
    delUser = Employee.query.filter(Employee.idx == uid).first()
    # delUser = Employee.query.get(uid) # select * from Employee where userid=3
    db.session.delete(delUser)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/crud/Edit', methods=['POST'])
def update():
    updateUser = Employee.query.get(request.form.get('idx'))
    updateUser.FirstName = request.form['FirstName']
    updateUser.LastName = request.form['LastName']
    updateUser.Email = request.form['Email']
    updateUser.UserName = request.form['UserName']
    db.session.commit()
    return redirect(url_for('index'))
    
# @app.route('/login',methods=['POST'])
# def Usrlogin():
#     username = request.form['username']
#     password = request.form['password']
#     log_data = Employee.query.filter(and_(Employee.UserName == username),(Employee.Password==password)).first()
#     if log_data is not None:
#         return redirect(url_for('index'))
#     else:
#         flash('아이디나 비밀번호가 일치하지 않습니다')
#         return redirect(url_for('index'))
        
if __name__=="__main__":
    app.run(host='0.0.0.0',port='5001')