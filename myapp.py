from flask import Flask,render_template, request,redirect,url_for
import pymysql

con = None
cur = None

app = Flask(__name__)

def connectToDb():
    global con, cur
    con = pymysql.connect(host="localhost",user="root",database="tejas",password="")
    cur = con.cursor()

def disconnecttoDB():
    cur.close()
    con.close()

def getAllpersonData():
    connectToDb()   
    selectquery= "SELECT * from success;"
    cur.execute(selectquery)
    data = cur.fetchall()
    disconnecttoDB()
    return data

def insertToStudentTable(Name,Age,City,Roll_No):
    try:
        connectToDb() 
        insertQuery = "insert INTO success(Name,Age,City,Roll_No) values(%s,%s,%s,%s);"
        cur.execute(insertQuery,(Name,Age,City,Roll_No))
        con.commit()
        disconnecttoDB()
        return True
    except:
        disconnecttoDB()
        return False 

def getOnepersonData(a):
    connectToDb()   
    selectquery= "SELECT * from success WHERE Roll_No=%s;"
    cur.execute(selectquery,(a,))
    data = cur.fetchone()
    disconnecttoDB()
    return data        

def updatestudentToTable(Name,Age,City,Roll_No):
    try:
        connectToDb()
        updateQuery="UPDATE success SET Name=%s,Age=%s,City=%s WHERE Roll_No=%s ;"
        cur.execute(updateQuery,(Name,Age,City,Roll_No))
        con.commit()
        disconnecttoDB()
        return True
    except Exception as e:
        print(e)
        disconnecttoDB()
        return False

def deletestudent(a):
    try:
        connectToDb()
        deleteQuery="DELETE FROM success WHERE Roll_No=%s;"
        cur.execute(deleteQuery,(a,))
        con.commit()
        disconnecttoDB()
        return True
    except:
        disconnecttoDB()
        return False




    
@app.route("/") 
@app.route('/index/')
def Index():
    data = getAllpersonData()
    return render_template('Index.html', data=data)

@app.route("/add/",methods=['GET','POST'])    
def addstudent():
    if request.method =='POST':
        data =request.form
        if  insertToStudentTable(data['txtName'],data['txtAge'],data['txtCity'],data['txtRoll_No']):
            message ="Record inserted successfully."
        else:
               message= "Due to some issue couldn't insert record." 
        return render_template("insert.html",message=message)
    return render_template("insert.html")

@app.route("/edit/", methods=['GET','POST'])
def updateStudent():
    Roll_No=request.args.get('Roll_No',type=int,default=1)
    data=getOnepersonData(Roll_No)
    if request.method =="POST":
        fdata = request.form
        print(fdata)
        if updatestudentToTable(fdata['txtName'], fdata['txtAge'], fdata['txtCity'],Roll_No):
         
         message="Record updated successfully"
        else:
         message="Due to some issue could't update record"
        return render_template('update.html', message=message)
    return render_template("update.html",data=data)

@app.route("/delete/", methods=['GET','POST'])
def deletestudentToTable():   
    Roll_No=request.args.get('Roll_No',type=int,default=1)
    deletestudent(Roll_No)
    return redirect(url_for("Index"))




if __name__ =='__main__':
    app.run(debug=True)
