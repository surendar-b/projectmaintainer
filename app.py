from flask import Flask,render_template,request,redirect,url_for,session,jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors 
import re
from MySQLdb import _mysql


app=Flask(__name__)

  
app.secret_key = 'app secret'

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='project'
#app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql=MySQL(app)

#load login html and validate login info and redirect to dashboard.
@app.route("/")
@app.route('/login', methods=['GET','POST'])
def login():
     msg=''
     print("****************",request.method)
     if request.method == 'POST':
          #username=request.form['uname']
          #password=request.form['pwd']
        try:
          data = request.get_json()
          username=data['uname']
          print("*****************",data['uname'])
          password=data['pwd']     
          cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
          cursor.execute('SELECT * FROM users WHERE user_id = % s AND password = % s',(username, password,))
          #db.query('SELECT * FROM users WHERE uname = % s AND password = % s AND type= % s',(username, password, typeo, )')
          account=cursor.fetchone()
          print("************************",account)
          if account:
               session['loggedin'] = True
               #session['id'] = account['id']
               session['uname']=account['uname']
               session['uid']=account['user_id']
               session['type']=account['type']
               msg = 'login Successfully....!!!!!'
               data={"message":msg,"type":account['type']}
               return jsonify({"status":200,"data":data})
          else:
            msg2='username password are incorrect pls try again'
            return jsonify({"status":500,"data":msg2})
        except Exception as e:
          print(e)
          return jsonify({"status":500,"data":e})
     return render_template('login.html')

#redirecting to status page
@app.route('/status',methods=['GET'])
def status():
     print("@@#!#!#@#@#@#@")
     return render_template('status.html')


#redirect to home
@app.route('/home',methods=['GET','POST'])
def home():
     print("************",session['type'])
     if session['type']=='student':
        return render_template('user_dashboard.html')
     elif session['type']=='admin':
          return render_template('student.html')
     elif session['type']=="staff":
          return render_template('staff_dashboard.html')  

#redirect to alter title page
@app.route('/altpage',methods=['GET','POST'])
def altpage():
     return render_template('alt_title.html')

#choose guide insert project detail
@app.route('/project',methods=['POST'])
def project():
     print("********************")
     try:
       data = request.get_json()
       staff_id=data['staffid']
       print("******************")
       batch=data['batch']
       pname=data['pname']
       cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
       cursor.execute("insert into project (stud_id,staff_id,batch,projectName) values (%s,%s,%s,%s)",(session['uid'],staff_id,batch,pname))
       mysql.connection.commit()
       print("added ************")
       data={"status":200,"data":"project added successfully"}
       return jsonify(data)
     except Exception as e:
        print(e)
        return jsonify({"status":500,"data":e})

#alter title insertion
@app.route('/alter',methods=['PUT'])
def alter():
     #alter_title=request.form['a_title']
     try:
       alter_title=request.get_json()
       pname=alter_title['pname']
       status=""
       cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
       cursor.execute('update project set projectName= %s, status= %s  where stud_id=%s', (pname, status, session["uid"]))
       mysql.connection.commit()
       data={"status":200,"data":"sucessfull update"}
       return jsonify(data)
     except Exception as e:
       print(e)
       return jsonify({"status":500,"data":e})


#admin insert student
@app.route('/add',methods=['POST'])
def add():
     try:    
       data = request.get_json()
       user_id=data['uid']
       uname=data['uname']
       utype=data['type']
       password=data['password']
       empty=""
       if user_id == empty :
          return jsonify({"status":500,"data":"missing feild"})
       if utype=='student':
          #insert into users table
          cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
          cursor.execute("insert into users (uname,user_id,type,password) values (%s,%s,%s,%s)",(uname,user_id,utype,password))
          mysql.connection.commit()
          #for student table
          department=data['department']
          batch=data['batch']
          cursor.execute("insert into student (std_id,department,batch) values (%s,%s,%s)",(user_id,department,batch))
          mysql.connection.commit()
          return jsonify({"status":200,"data":"student added"})
       else:
          print("add staff ********************")
          #insert users for staff
          cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
          cursor.execute("insert into users (uname,user_id,type,password) values (%s,%s,%s,%s)",(uname,user_id,utype,password))
          mysql.connection.commit()
          #for staff table
          department=data['department']
          status=data['status']
          cursor.execute("insert into staff (user_id,department,status) values (%s,%s,%s)",(user_id,department,status))
          mysql.connection.commit()
          return jsonify({"status":200,"data":"staff added"})
     except Exception as e:
       print(e)
       return jsonify({"status":500,"data":e})


#admin staff view
@app.route('/staffview',methods=['GET'])
def staffview():
     try:
       print("******************************,**********")
       cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
       cursor.execute("SELECT users.uname,users.user_id,staff.department,staff.status FROM staff inner join users on staff.user_id =users.user_id where users.type='staff'")
       staffInfo=cursor.fetchall()
       data={"status":200,"data":staffInfo}
       return jsonify(data)
     except Exception as e:
       print(e)
       return jsonify({"status":500,"data":e})


#students information to staff
@app.route('/studentview',methods=['GET'])
def studentview():
     try:
       cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
       cursor.execute("SELECT users.uname,users.user_id,student.department,student.batch FROM student inner join users on student.std_id =users.user_id where users.type='student'")
       studInfo=cursor.fetchall()
       data={"status":200,"data":studInfo}
       return jsonify(data)
     except Exception as e:
       print(e)
       return jsonify({"status":500,"data":e})


#add staff page
@app.route('/addstaff',methods=['GET'])
def addstaff():
     return render_template('add_staff.html')


#add student page
@app.route('/addstudent',methods=['GET'])
def addstudent():
     return render_template('add_student.html')


#list all project based on staffID
@app.route('/staff/studentlist',methods=['GET'])
def staffproject():
     try:
       cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
       cursor.execute("select users.uname,project.batch,project.stud_id,project.projectName,project.status,project.r1,project.r2,project.r3 from project inner join users on project.stud_id=users.user_id where project.staff_id = %s",(session['uid'],))
       staffInfo=cursor.fetchall()
       data={"status":200,"data":staffInfo}
       return jsonify(data)
     except Exception as e:
       print(e)
       return jsonify({"status":500,"data":e})

#list student project based on studentID
@app.route('/student/project',methods=['GET'])
def studentProject():
     try:
       print("----------->",session['uid'])
       cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
       cursor.execute("select users.uname,project.batch,project.staff_id,project.projectName,project.status,project.r1,project.r2,project.r3 from project inner join users on project.staff_id=users.user_id where project.stud_id = %s ",(session["uid"],))
       staffInfo=cursor.fetchall()
       data={"status":200,"data":staffInfo}
       return jsonify(data)
     except Exception as e:
       print(e)
       return jsonify({"status":500,"data":e})



#change status to the proect title
@app.route('/student/status',methods=['PUT'])
def stdstatus():
     try:
          data = request.get_json()
          print("###############################")
          status=data['status']
          stud_id=data['stud_id']
          cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
          cursor.execute('update project set status= %s  where stud_id=%s', (status, stud_id))
          mysql.connection.commit()
          return jsonify({"status":200,"data":"successfully added"})
     except Exception as e:
          print(e)
          return jsonify({"status":500,"data":"failed on updating"})


#update review to the proect title
@app.route('/student/review',methods=['PUT'])
def review():
     try:
          data = request.get_json()
          print("###############################",data)
          r1=data['r1']
          r2=data['r2']
          r3=data['r3']
          stud_id=data['stud_id']
          print("################",r1,r2,r3)
          cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
          cursor.execute('update project set r1= %s,r2=%s,r3=%s  where stud_id=%s', (r1,r2,r3,stud_id))
          mysql.connection.commit()
     except Exception as e:
          print(e)
     return jsonify({"status":200,"data":"successfully added"})


#change status of a staff
@app.route('/staff/status',methods=['PUT'])
def staffstatus():
     try:
          data = request.get_json()
          print("###############################",data)
          status=data['status']
          user_id=data['user_id']
          cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
          cursor.execute('update staff set status= %s where user_id=%s', (status,user_id))
          mysql.connection.commit()
     except Exception as e:
          print(e)
     return jsonify({"status":200,"data":"successfully added"})

#add the student
@app.route('/addstudent',methods=['GET'])
def admin():
     return render_template('admin.html')



@app.route('/student',methods=['GET'])
def student():
     return render_template('student.html')

@app.route('/staff',methods=['GET'])
def staff():
     return render_template('staff.html')

@app.route('/staffhome',methods=['GET'])
def staffhome():
     return render_template('staff_dashboard.html')

@app.route('/staffupdate/<stud_id>',methods=['GET'])
def staffupdatestatus(stud_id):
     print(stud_id)
     return render_template('staff_update_status.html',stud_id=stud_id)

@app.route('/staffstatus/<staff_id>',methods=['GET'])
def staffstatusupdate(staff_id):
     print(staff_id)
     return render_template('update_staff_status.html',staff_id=staff_id)

@app.route('/staffupdate/review/<stud_id>',methods=['GET'])
def staffupdatereview(stud_id):
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute('SELECT * FROM project WHERE stud_id = % s',(stud_id,))
     account=cursor.fetchone()
     return render_template('staff_review_update.html',stud_id=stud_id,r1=account['r1'],r2=account['r2'],r3=account['r3'])


#guide ids
@app.route('/stafflist',methods=['GET'])
def stafflist():
      print("********* stafflist call *************")
      cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
      cursor.execute('SELECT user_id FROM staff')
      account=cursor.fetchall()
      return jsonify({"status":200,"data":account})


#redirect to update tile
@app.route('/updatetitle',methods=['GET'])
def updatetitle():
     return render_template('update_title.html')



#students information to staff
@app.route('/studentsearch/<batch>/<dep>',methods=['GET'])
def studentsearch(batch,dep):
     try:
       cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
       cursor.execute("SELECT users.uname,users.user_id,student.department,student.batch FROM student inner join users on student.std_id =users.user_id where users.type='student' and student.department= %s and student.batch=%s",(dep,batch))
       studInfo=cursor.fetchall()
       data={"status":200,"data":studInfo}
       return jsonify(data)
     except Exception as e:
       print(e)
       return jsonify({"status":500,"data":e})



#admin staff view
@app.route('/staffsearch/<dep>',methods=['GET'])
def staffsearch(dep):
     try:
       print("******************************,**********")
       cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
       cursor.execute("SELECT users.uname,users.user_id,staff.department,staff.status FROM staff inner join users on staff.user_id =users.user_id where users.type='staff' and staff.department='"+dep+"'")
       staffInfo=cursor.fetchall()
       data={"status":200,"data":staffInfo}
       return jsonify(data)
     except Exception as e:
       print(e)
       return jsonify({"status":500,"data":e})


@app.route('/staff/search/<batch>',methods=['GET'])
def staffsearching(batch):
     try:
       cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
       cursor.execute("select users.uname,project.batch,project.stud_id,project.projectName,project.status,project.r1,project.r2,project.r3 from project inner join users on project.stud_id=users.user_id where project.staff_id = %s and project.batch= '"+batch+"'",(session['uid'],))
       staffInfo=cursor.fetchall()
       data={"status":200,"data":staffInfo}
       return jsonify(data)
     except Exception as e:
       print(e)
       return jsonify({"status":500,"data":e})


@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('uid', None)
   session.pop('uname', None)
   session.pop('type', None)
   return redirect(url_for('login'))