from flask import Flask, render_template, url_for, redirect,request,flash
from flask_mysqldb import MySQL

app = Flask(__name__)#to get current file and consider this file as main file
#MySQL Connection
app.config["MYSQL_HOST"] ="localhost"
app.config["MYSQL_USER"] ="root"
app.config["MYSQL_PASSWORD"] ="1430"
app.config["MYSQL_DB"] ="crud"
app.config["MYSQL_CURSORCLASS"] ="DictCursor" #To retrive the data in Dictionary format
mysql=MySQL(app) #connection string

#Loading Home Page
@app.route('/')
def home():
    con=mysql.connection.cursor()
    sql = "SELECT * FROM users"
    con.execute(sql)
    res=con.fetchall()
    return render_template("home.html",datas = res)

#Adding New User
@app.route("/addusers", methods=['POST', 'GET'])
def add_users():
    if request.method == "POST":
        name = request.form['name']
        age = request.form['age']
        city = request.form['city']
        con = mysql.connection.cursor()
        sql = "Insert into users(Name,city,age) values(%s,%s,%s)"
        con.execute(sql, [name, city, age])
        mysql.connection.commit()
        con.close()
        flash("User Details Added")
        return redirect(url_for("home"))
    return render_template("add_users.html")

#Edit Existing Users
@app.route("/editusers/<string:id>", methods=['POST', 'GET'])


def edit_users(id):
    con = mysql.connection.cursor()
    if request.method == "POST":
        name = request.form['name']
        age = request.form['age']
        city = request.form['city']
        con = mysql.connection.cursor()
        sql = "update  users set Name=%s,city=%s,age=%s where ID=%s"
        con.execute(sql, [name, city, age,id])
        mysql.connection.commit()
        con.close()
        flash("User Details Updated")
        return redirect(url_for("home"))
    sql = "select * from users where ID=%s"
    con.execute(sql,[id])
    res=con.fetchone() #bcoz fetching single value

    return render_template("edit_users.html",datas=res)


#Delete Existing Users
@app.route("/deleteusers/<string:id>", methods=['POST', 'GET'])
def delete_users(id):
    con = mysql.connection.cursor()
    sql = "delete from users where ID=%s"
    con.execute(sql, [id])
    mysql.connection.commit()
    con.close()
    flash("User Details Deleted")
    return redirect(url_for("home"))



if(__name__=='__main__'):
    app.secret_key="1430"
    app.run(debug=True)
