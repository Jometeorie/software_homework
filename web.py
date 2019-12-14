import pymysql
def connect_database():
    db = pymysql.connect("localhost", "root", "zych@0715", "TWS")
    return db

from flask import Flask
from flask import request, render_template, redirect, url_for
from flask import session
app = Flask(__name__)
app.secret_key = "DragonFire"

import datetime
import time
import random

import main
from main import init
from person import User
from product import Product
#  import TWS
MY_TWS = init()


@app.route("/", methods = ['GET'])
def login():
    return render_template('login.html')

def get_user_info(EID):
    sql = '''SELECT  * FROM EMPLOYEE WHERE EID = ('%s')'''
    try:
        conn = connect_database()
        cursor = conn.cursor()
        cursor.execute(sql % (EID))
        answers = cursor.fetchall()
        conn.close()
        return answers
    except:
        print('获取用户信息失败！')
        conn.close()

@app.route("/", methods = ['POST'])
def loginin():
    username = request.form['username']
    password = request.form['password']

    sql = '''SELECT * FROM LOGIN WHERE EID = ('%s') AND Password = ('%s')'''
    try:
        conn = connect_database()
        cursor = conn.cursor()
        cursor.execute(sql % (username, password))
        answers = cursor.fetchall()
        
        if answers:
            session['username'] = username
            session['password'] = password
            session['user_info'] = get_user_info(username)
            return redirect(url_for('select'))
        else:
            return render_template('login.html', answer = 0)
        
        conn.close()
    except:
        print('登陆失败！')
        conn.close()

    return redirect(url_for('select'))

@app.route("/select", methods = ['GET'])
def select():
    # 权限，专家或者员工，员工将被限制部分权限
    Etype = session['user_info'][0][4]
    return render_template('func_select.html', com_name = session['user_info'][0][3], work_type = session['user_info'][0][4], employee = session['user_info'][0][1])

@app.route("/select", methods = ['POST'])
def select_choice():
    # 跳转界面的类别
    jump_type = request.form['jump']
    if jump_type == '查看租借信息':
        return redirect(url_for('lend_info'))
    elif jump_type == '查看工具信息':
        return redirect(url_for('tool_info'))
    elif jump_type == '请求工具':
        return redirect(url_for('choose_company'))
    elif jump_type == '维护员工信息(管理员)':
        Etype = session['user_info'][0][4]
        if Etype == '员工':
            return render_template('func_select.html', Etype = Etype)
        return redirect(url_for('employee_info'))
    elif jump_type == '处理工具请求(管理员)':
        return redirect(url_for('process_request'))

def get_employee_info():
    sql = '''SELECT * FROM EMPLOYEE WHERE Soncmp = ('%s')'''
    try:
        conn = connect_database()
        cursor = conn.cursor()
        cursor.execute(sql % (session['user_info'][0][3]))
        answers = cursor.fetchall()
    except:
        print('查询用户信息失败2！')
        conn.close()
    ID = list()
    name = list()
    rank = list()
    for answer in answers:
        ID.append(answer[0])
        name.append(answer[1])
        rank.append(answer[4])
    length = len(ID)
    return ID, name, rank, length

@app.route('/employee_info', methods = ['GET'])
def employee_info():
    try:
        user_info = session['user_info']
    except:
        return '请先登陆！'
    ID, name, rank, length = get_employee_info()

    return render_template('employ_info.html', ID = ID, name = name, rank = rank, length = length)

@app.route('/employee_info', methods = ['POST'])
def employee_update():
    ID = request.form['ID']
    name = request.form['name']
    rank = request.form['rank']
    state = request.form['state']

    if state == '提交':
        sql = '''UPDATE EMPLOYEE SET Name = ('%s'), Worktype = ('%s') WHERE EID = ('%s')'''
        try:
            conn = connect_database()
            cursor = conn.cursor()
            cursor.execute(sql % (name, rank, ID))
            conn.commit()
        except:
            print('更新员工失败！')
            conn.close()
    elif state == '清除':
        sql = '''DELETE FROM EMPLOYEE WHERE EID = ('%s')'''
        try:
            conn = connect_database()
            cursor = conn.cursor()
            cursor.execute(sql % (ID))
            conn.commit()
        except:
            print('删除员工失败！')
            conn.close()

    ID, name, rank, length = get_employee_info()

    return render_template('employ_info.html', ID = ID, name = name, rank = rank, length = length)

def get_tool_info(Soncmp):
    sql = '''SELECT * FROM TOOL WHERE Soncmp = ('%s') AND Borrow = 0'''
    try:
        conn = connect_database()
        cursor = conn.cursor()
        cursor.execute(sql % (Soncmp))
        answers = cursor.fetchall()
    except:
        print('查询工具信息失败！')
        conn.close()
    TID = list()
    Tname = list()
    Ttype = list()
    Tstate = list()
    for answer in answers:
        TID.append(answer[0])
        Tname.append(answer[1])
        Ttype.append(answer[2])
        if answer[4] == 1:
            Tstate.append('正常')
        else:
            Tstate.append('损坏')
    length = len(TID)

    return TID, Tname, Ttype, Tstate, length

@app.route('/tool_info', methods = ['GET'])
def tool_info():
    TID, Tname, Ttype, Tstate, length = get_tool_info(session['user_info'][0][3])

    return render_template('tool_info.html', TID = TID, Tname = Tname, Ttype = Ttype, Tstate = Tstate, length = length)

@app.route('/tool_info', methods = ['POST'])
def tool_back():
    return redirect(url_for('select'))

def get_lend_info():
    sql = '''SELECT * FROM LEND WHERE EID = ('%s')'''
    try:
        conn = connect_database()
        cursor = conn.cursor()
        cursor.execute(sql % (session['username']))
        answers = cursor.fetchall()
    except:
        print('查询租借信息失败！')
        conn.close()
    LID = list()
    Ltime = list()
    EID = list()
    TID = list()
    for answer in answers:
        LID.append(answer[0])
        Ltime.append(answer[1])
        EID.append(answer[2])
        TID.append(answer[3])
    length = len(LID)

    return LID, Ltime, EID, TID, length

@app.route('/lend_info', methods = ['GET'])
def lend_info():
    LID, Ltime, EID, TID, length = get_lend_info()

    return render_template('lend_info.html', LID = LID, Ltime = Ltime, EID = EID, TID = TID, length = length)

@app.route('/lend_info', methods = ['POST'])
def lend_back():
    return redirect(url_for('select'))

@app.route('/tool_request', methods = ['GET'])
def get_tool_request():
    TID, Tname, Ttype, Tstate, length = get_tool_info(session['jump'])

    return render_template('tool_request.html', TID = TID, Tname = Tname, Ttype = Ttype, Tstate = Tstate, length = length, accuracy = 1)

@app.route('/tool_request', methods = ['POST'])
def post_tool_requset():
    TID = request.form['TID']
    sql = '''SELECT * FROM TOOL WHERE Soncmp = ('%s') AND TID = ('%s') AND Good = 1 AND Borrow = 0'''
    try:
        conn = connect_database()
        cursor = conn.cursor()
        cursor.execute(sql % (session['jump'], TID))
        answers = cursor.fetchall()
    except:
        print('获取工具信息失败2！')
        conn.close()
    # 成功获取到工具请求
    if answers:
        sql = '''UPDATE TOOL SET Borrow = -1 WHERE TID = ('%s')'''
        try:
            conn = connect_database()
            cursor = conn.cursor()
            cursor.execute(sql % (answers[0][0]))
            conn.commit()
        except:
            print('更新工具状态失败！')
            conn.close()
        sql = '''INSERT INTO LENDTMP VALUE ('%s', '%s', '%s')'''
        try:
            ltime = time.localtime()
            timeStr=time.strftime("%Y-%m-%d %H:%M:%S", ltime)
            conn = connect_database()
            cursor = conn.cursor()
            cursor.execute(sql % (session['username'], timeStr, TID))
            conn.commit()
        except:
            print('插入LENDTMP失败！')
            conn.close()
        TID, Tname, Ttype, Tstate, length = get_tool_info(session['jump'])
        return render_template('tool_request.html', TID = TID, Tname = Tname, Ttype = Ttype, Tstate = Tstate, length = length, accuracy = 1)
    else:
        TID, Tname, Ttype, Tstate, length = get_tool_info(session['jump'])
        return render_template('tool_request.html', TID = TID, Tname = Tname, Ttype = Ttype, Tstate = Tstate, length = length, accuracy = 0)

@app.route('/choose_company', methods = ['GET'])
def choose_company():
    return render_template('choose_company.html')

@app.route('/choose_company', methods = ['POST'])
def post_choose_company():
    session['jump'] = request.form['jump']
    return redirect(url_for('get_tool_request'))

def get_lend_info2(Soncmp):
    sql = '''SELECT Lendtime, EMPLOYEE.EID, EMPLOYEE.Name, TOOL.TID, TOOL.Name FROM LENDTMP NATURAL JOIN EMPLOYEE JOIN TOOL ON  TOOL.TID=LENDTMP.TID WHERE EMPLOYEE.Soncmp = ('%s')'''
    try:
        conn = connect_database()
        cursor = conn.cursor()
        cursor.execute(sql % (Soncmp))
        answers = cursor.fetchall()
        print(Soncmp)
        print(answers)
    except:
        print('获取指定公司的租借信息失败！')
        conn.close()
    Lendtime = list()
    EID = list()
    employee_name = list()
    TID = list()
    tool_name = list()
    for answer in answers:
        Lendtime.append(answer[0])
        EID.append(answer[1])
        employee_name.append(answer[2])
        TID.append(answer[3])
        tool_name.append(answer[4])
    length = len(Lendtime)

    return Lendtime, EID, employee_name, TID, tool_name, length

@app.route('/process_request', methods = ['GET'])
def process_request():
    a = get_lend_info2(session['user_info'][0][3])

    return render_template('process_request.html', Ename = a[2], TID = a[3], Tname = a[4], Rtime = a[0], length = a[5], EID = a[1])

@app.route('/process_request', methods = ['POST'])
def post_process_request():
    response = request.form['state']
    TID = request.form['TID']
    EID = request.form['EID']
    EName = request.form['Ename']
    TName = request.form['Tname']
    if response == '许可':
        ltime=time.localtime()
        timeStr=time.strftime("%Y-%m-%d %H:%M:%S", ltime)
        # 调用宗佬的模拟
        MY_TWS.run(User(EName), Product(TName))


        sql = '''INSERT INTO LEND VALUE ('%s', '%s', '%s', '%s')'''
        try:
            conn = connect_database()
            cursor = conn.cursor()
            cursor.execute(sql % (str(int(random.random()*999999999)), timeStr, EID, TID))
            conn.commit()
        except:
            print('插入LEND失败！')
            conn.close()
    elif response == '拒绝':
        sql = '''UPDATE TOOL SET Borrow = 0 WHERE TID = ('%s')'''
        try:
            conn = connect_database()
            cursor = conn.cursor()
            cursor.execute(sql % (TID))
            conn.commit()
        except:
            print('更新TOOL的Borrow状态失败！')
            conn.close()
    sql = '''DELETE FROM LENDTMP WHERE TID = ('%s')'''
    try:
        conn = connect_database()
        cursor = conn.cursor()
        cursor.execute(sql % (TID))
        conn.commit()
    except:
        print('删除LENDTMP失败！')
        conn.close()
    return redirect(url_for('process_request'))

if __name__ == '__main__':
    app.run(debug = True, port = 8900, host = '0.0.0.0')

