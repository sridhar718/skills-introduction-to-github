from flask import Flask, render_template, request, redirect, url_for
import sqlite3

con = sqlite3.connect('database.db')
cr = con.cursor()

cr.execute("create table if not exists data (member TEXT, project TEXT)")

cr.execute("create table if not exists accounts (username TEXT, password TEXT, admin TEXT)")
 
cr.execute("create table if not exists members (member TEXT, project TEXT, taskid TEXT, status TEXT, date TEXT, description TEXT, remarks TEXT)")
headings = ['member', 'project', 'taskid', 'status', 'date', 'description', 'remarks']

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/view')
def view():
    con = sqlite3.connect('database.db')
    cr = con.cursor()

    cr.execute("select * from members")
    result = cr.fetchall()

    return render_template('view.html',  headings=headings, result=result)
    
@app.route('/addpage')
def addpage():
    con = sqlite3.connect('database.db')
    cr = con.cursor()

    cr.execute("select * from data")
    result = cr.fetchall()
    
    return render_template('add.html', result=result)

@app.route('/edit/<name>')
def edit(name):
    con = sqlite3.connect('database.db')
    cr = con.cursor()

    cr.execute("select * from data")
    result = cr.fetchall()

    cr.execute("select * from members where member = '"+name+"'")
    data = cr.fetchone()

    return render_template('edit.html',  data=data, result=result)

@app.route('/edituser/<name>')
def edituser(name):
    con = sqlite3.connect('database.db')
    cr = con.cursor()

    cr.execute("select * from data")
    result = cr.fetchall()

    cr.execute("select * from members where member = '"+name+"'")
    data = cr.fetchone()

    return render_template('userlog.html', user=name, data=data, result=result)

@app.route('/remove/<name>')
def remove(name):
    con = sqlite3.connect('database.db')
    cr = con.cursor()

    cr.execute("delete from members where member ='"+name+"'")
    con.commit()

    return redirect(url_for('view'))

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(username, password)
        
        con = sqlite3.connect('database.db')
        cr = con.cursor()

        cr.execute("select * from accounts where username = '"+username+"' and password = '"+password+"'")
        result = cr.fetchone()

        if result:
            admin = result[2]
            user = result[0]

            if admin == 'yes':
                return redirect(url_for('view'))
            else:
                cr.execute("select * from data")
                result = cr.fetchall()

                cr.execute("select * from members where member = '"+user+"'")
                data = cr.fetchall()
                
                if data:
                    return render_template('userlog.html', msg="Login successfully", user=user, result=result)
                else:
                    return render_template('userlog.html', msg="Login successfully",user=user, result=result)
        else:
            return render_template('index.html', msg="Entered wrong username or password")  

    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        data = request.form
        row = []
        for key in data:
            row.append(data[key])

        con = sqlite3.connect('database.db')
        cr = con.cursor()

        cr.execute("insert into members values (?, ?, ?, ?, ?, ?, ?)",  row)
        con.commit()

        return redirect(url_for('view'))    
    return render_template('add.html')

@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        data = request.form
        row = []
        for key in data:
            row.append(data[key])

        con = sqlite3.connect('database.db')
        cr = con.cursor()

        cr.execute("update members set project=?, taskid=?, status=?, date=?, description=?, remarks=? where member='"+row[0]+"'", row[1:])
        con.commit()

        return redirect(url_for('view'))    
    return render_template('add.html')

@app.route('/userupdate', methods=['GET', 'POST'])
def userupdate():
    if request.method == 'POST':
        data = request.form
        row = []
        for key in data:
            row.append(data[key])

        con = sqlite3.connect('database.db')
        cr = con.cursor()

        user = row[0]

        cr.execute("update members set project=?, taskid=?, status=?, date=?, description=?, remarks=? where member='"+row[0]+"'", row[1:])
        con.commit()

        cr.execute("select * from data")
        result = cr.fetchall()

        return render_template('userlog.html', msg="data updated successfully", user=user, result=result)   
    return render_template('index.html')

@app.route('/userdata', methods=['GET', 'POST'])
def userdata():
    if request.method == 'POST':
        data = request.form
        row = []
        for key in data:
            row.append(data[key])

        con = sqlite3.connect('database.db')
        cr = con.cursor()

        cr.execute("insert into members values (?, ?, ?, ?, ?, ?, ?)",  row)
        con.commit()

        cr.execute("select * from data")
        result = cr.fetchall()
        
        return render_template('userlog.html', msg="data added successfully", user=row[0], result=result)   
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
