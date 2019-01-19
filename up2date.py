from flask import Flask,render_template
from flask import request,session,redirect,json,flash
import MySQLdb,string,smtplib

app = Flask(__name__)
mysql = MySQLdb.connect(host='localhost',user="root",password="24184075",db="project")
cursor = mysql.cursor()

@app.route('/')
def rest():
 return render_template('rest.html')

@app.route('/home')
def hello_world():
    author = "Shetty"
    name = "You"
    return render_template('index.html', author=author, name=name)

@app.route('/signup', methods = ['POST'])
def signup():
    _name = request.form['name']
    _email = request.form['email']
    _password = request.form['psw']
    cursor.callproc('sp_createUser',(_name,_email,_password))
    data=cursor.fetchall() 
    if len(data) is 0 :
        mysql.commit()
        sql = "CREATE TABLE "+_name+" (`id` INT NOT NULL AUTO_INCREMENT,`type` VARCHAR(45) NULL,`topic` VARCHAR(45) NOT NULL,`description` VARCHAR(100) NULL,`date_time` DATETIME NOT NULL,PRIMARY KEY (`id`))"
        cursor.execute(sql)
        mysql.commit()
        return render_template('rest.html')
    else:
        return json.dumps({'html':'Username Exists Try Again'})
   
@app.route('/login', methods = ['POST'])
def login():
    _email = request.form['_email_']
    _password = request.form['_psw_']
    cursor.execute("Select user_name from users where user_email=%s and user_password=%s",(_email,_password))
    result=cursor.fetchone()
    print(result)
    session['result']=result
    if result == None :
         flash('There was some error')
    else:
        return render_template("emails.html",result=result)

@app.route('/home1')    
def login_1():
    return render_template('login.html')

if __name__ == '__main__':
    app.secret_key = 'some secret key'
    app.run(debug=True)