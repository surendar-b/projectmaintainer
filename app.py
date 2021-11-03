from flask import Flask,render_template,request,redirect,url_for,session
from flask_mysqldb import MySQL
from MySQLdb.cursors import re
from MySQLdb import _mysql


db=_mysql.connect('localhost','root','surendar','project')

app=Flask(__name__)



#app.config['MYSQL_HOST']='localhost'
#app.config['MYSQL_USER']='root'
#app.config['MYSQL_PASSWORD']=''
#app.config['MYSQL_DB']='project'

app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql=MySQL(app)


@app.route("/")
@app.route('/login', methods=['GET','POST'])
def login():
     msg=''
     typeo='admin'
     if request.method == 'POST' and 'uname' in request.form and 'pwd' in request.form:
          username=request.form['uname']
          password=request.form['pwd']
          #cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
          #cursor.excute('SELECT * FROM users WHERE uname = % s AND password = % s AND type= % s',(username, password, typeo, ))
          db.query('SELECT * FROM users WHERE uname = % s AND password = % s AND type= % s',(username, password, typeo, )')
          account=cursor.fetchone()
          print(account)
          if account:
               session['loggedin'] = True
               session['id'] = account['id']
               session['username']=account['username']
               msg1 = 'login Successfully....!!!!!'
               return render_template('user_dashboard.html', msg1 = msg)
          else:
               msg2='username password are incorrect pls try again'
     return render_template('login.html')
