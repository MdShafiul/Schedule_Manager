from flask import Flask , render_template , request , redirect , session
from flask_mysqldb import MySQL
import yaml
import matplotlib.pyplot as plt
import smtplib
from flask_mail import Mail , Message
import random
import string

app = Flask(__name__)
#mail_config
app.config['DEBUG']=True
app.config['TESTING'] = False
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USE_SSL']=True
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USERNAME'] = '*********@gmail.com'
app.config['MAIL_PASSWORD']= '****************'                         #app password for gmail
app.config['MAIL_DEFAULT_SENDER'] = '**********@gmail.com'
app.config['MAIL_ASCII_ATTACHMENTS'] = False
#mail_config
mail = Mail(app)

app.secret_key = b'\xc6\xfd\xfb\x7f\xb6tb\xc26"\x19Z\\\\A\xf3\xb1\xa4-\xf9\xf5\x03)U'

db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']


mysql = MySQL(app)


@app.route('/forget_pass' , methods=['GET','POST'])
def robot():
    if request.method == 'POST':
        userInput = request.form
        session["code"] = randomString(10)
        msg = Message("Change Password", recipients=[userInput['Email']])
        msg.body = "Click here to change password\n "+"http://127.0.0.1:5000/forget_pass"+"/"+userInput['Email']+"/"+session.get('code', None)+"\nIf you don't want to change then leave it."
        mail.send(msg)
        return redirect('/')
    return render_template("forget_password.html")


@app.route('/forget_pass/<email>/<code>' , methods=['GET','POST'])
def change_password( email , code ):
    code_var = session.get('code', None)
    if code_var == code :
        if request.method == 'POST' :
            userInput = request.form
            cur = mysql.connection.cursor()
            cur.execute("update account set password = %s where email = %s;", (userInput['Pass'], email))
            mysql.connection.commit()
            return redirect('/')

    else:
        return "invalid url"

    return render_template("Set_Password.html")


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def init_gantt1(table):
    cur = mysql.connection.cursor()
    cur.execute("WITH RECURSIVE Cpaths (id , path , length , eft) AS(  SELECT Aactivity , CAST(Aactivity AS CHAR(200)) , 1 ,  Duration    FROM ( select * from users where Name = %s ) as users    WHERE Predecessor = 'none'  UNION ALL  SELECT u.Aactivity , CONCAT(cp.path, ' -> ', u.Aactivity) , cp.length + 1 ,  cp.eft + u.Duration    FROM Cpaths AS cp JOIN ( select * from users where Name = %s ) as u      ON cp.id = u.Predecessor) , Cpaths1 (id , path , lft) AS(  SELECT Aactivity , CAST(Aactivity AS CHAR(200)) ,  (select max(eft) from Cpaths)    FROM ( select * from users where Name = %s ) as users    WHERE Aactivity not in ( select Predecessor from ( select * from users where Name = %s ) as users )  UNION ALL  SELECT u.Predecessor , CONCAT(cp.path, ' <- ', u.predecessor) ,  cp.lft - u.Duration    FROM Cpaths1 AS cp JOIN ( select * from users where Name = %s ) as u      ON cp.id = u.Aactivity),main ( id , path , length , est , eft , lst , lft , tf , Duration ) as(	SELECT Cpaths.id , Cpaths.path , Cpaths.length , max(Cpaths.eft) - duration as est , max(Cpaths.eft) as eft , min(Cpaths1.lft) - Duration as lst ,  min(Cpaths1.lft) as lft , - max(Cpaths.eft) + min(Cpaths1.lft) as tf , Duration FROM Cpaths , Cpaths1 , ( select * from users where Name = %s ) as users		where Aactivity = Cpaths.id and			  Aactivity = Cpaths1.id 		group by Cpaths.id ORDER BY Cpaths.id) ,for_ff( id , ff ) as(	select m1.id , min(m2.est) - m1.eft as ff from main as m1 , main as m2 , ( select * from users where Name = %s ) as u		where		m1.id = u.Predecessor and 		m2.id = u.Aactivity		group by m1.id)select count(*) , max(lft) from(select main.id , path , length , est , eft , lst , lft , tf , ifnull(ff,0) as ff , Duration	from main left join for_ff    on 		main.id = for_ff.id ) as ow;" , ( table , table , table , table , table , table , table ))

    record = cur.fetchall()

    xtlim = record[0][1]
    num = record[0][0]
    num1 = num
    x3 = 70/num

    fig, gnt = plt.subplots()
    gnt.set_ylim(0, 80)

    gnt.set_xlim(0, xtlim)
    gnt.set_xlabel('time')
    gnt.set_ylabel('Activity')

    cur.execute( "WITH RECURSIVE Cpaths (id , path , length , eft) AS(  SELECT Aactivity , CAST(Aactivity AS CHAR(200)) , 1 ,  Duration    FROM ( select * from users where Name = %s ) as users    WHERE Predecessor = 'none'  UNION ALL  SELECT u.Aactivity , CONCAT(cp.path, ' -> ', u.Aactivity) , cp.length + 1 ,  cp.eft + u.Duration    FROM Cpaths AS cp JOIN ( select * from users where Name = %s ) as u      ON cp.id = u.Predecessor) , Cpaths1 (id , path , lft) AS(  SELECT Aactivity , CAST(Aactivity AS CHAR(200)) ,  (select max(eft) from Cpaths)    FROM ( select * from users where Name = %s ) as users    WHERE Aactivity not in ( select Predecessor from ( select * from users where Name = %s ) as users )  UNION ALL  SELECT u.Predecessor , CONCAT(cp.path, ' <- ', u.predecessor) ,  cp.lft - u.Duration    FROM Cpaths1 AS cp JOIN ( select * from users where Name = %s ) as u      ON cp.id = u.Aactivity),main ( id , path , length , est , eft , lst , lft , tf , Duration ) as(	SELECT Cpaths.id , Cpaths.path , Cpaths.length , max(Cpaths.eft) - duration as est , max(Cpaths.eft) as eft , min(Cpaths1.lft) - Duration as lst ,  min(Cpaths1.lft) as lft , - max(Cpaths.eft) + min(Cpaths1.lft) as tf , Duration FROM Cpaths , Cpaths1 , ( select * from users where Name = %s ) as users		where Aactivity = Cpaths.id and			  Aactivity = Cpaths1.id 		group by Cpaths.id ORDER BY Cpaths.id) ,for_ff( id , ff ) as(	select m1.id , min(m2.est) - m1.eft as ff from main as m1 , main as m2 , ( select * from users where Name = %s ) as u		where		m1.id = u.Predecessor and 		m2.id = u.Aactivity		group by m1.id)select main.id , path , length , est , eft , lst , lft , tf , ifnull(ff,0) as ff , Duration	from main left join for_ff    on 		main.id = for_ff.id;", (table, table, table, table, table, table, table))
    userDetails = cur.fetchall()


    tick = []
    tlabel = []

    for data in userDetails :
        tick.append(x3 * num)
        tlabel.append(data[0])
        num -= 1

    tick.reverse()
    tlabel.reverse()

    gnt.set_yticks(tick)
    gnt.set_yticklabels(tlabel)

    gnt.grid(True)

    tot = 1

    for data in userDetails :
       # num += 1
        tot += 1
        if tot % 2 == 1:
            gnt.broken_barh( [( data[3] , data[9] )] , ( num1 * x3 , x3 ) , facecolors=('tab:green') )
            gnt.broken_barh( [( max( data[4] , data[5]) , data[6] - max( data[4] , data[5]) )] , ( num1 * x3 , x3 ) , facecolors=('tab:red') )
            gnt.broken_barh( [( data[5] , max( data[4] - data[5] , 0 ) )] , ( num1 * x3 , x3 ) , facecolors=('tab:grey') )
        elif tot % 2 == 0:
            gnt.broken_barh([(data[3], data[9])], (num1 * x3 , x3), facecolors=('tab:orange'))
            gnt.broken_barh( [( max( data[4] , data[5]), data[6] - max( data[4] , data[5]) )], (num1 * x3 , x3), facecolors=('tab:red'))
            gnt.broken_barh([(data[5], max(data[4] - data[5], 0))], (num1 * x3, x3), facecolors=('tab:grey'))
        num1 -= 1

    plt.savefig("static/gantt1.png")


def init_gantt():

    fig, gnt = plt.subplots()
    gnt.set_ylim(0, 50)

    gnt.set_xlim(0, 160)
    gnt.set_xlabel('seconds since start')
    gnt.set_ylabel('Processor')

    gnt.set_yticks([15, 25, 35])
    gnt.set_yticklabels(['1', '2', '3'])

    gnt.grid(True)

    gnt.broken_barh([(40, 50)], (35, 10), facecolors=('tab:orange'))
    gnt.broken_barh([(110, 10), (150, 10)], (15, 10),
                    facecolors='tab:blue')

    gnt.broken_barh([(10, 50), (100, 20), (130, 10)], (25, 10),
                    facecolors=('tab:red'))

    plt.savefig("static/gantt1.png")


@app.route('/' , methods=['GET','POST'])
def start():
    cur = mysql.connection.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users( Aactivity varchar(20) , Predecessor	varchar(20) , Duration int , Name varchar(20) );")
    mysql.connection.commit()
    cur.execute("create table if not exists account( person varchar(30) , email varchar(100) , password varchar(30) );")
    mysql.connection.commit()
    cur.execute("create table if not exists dataTable( person varchar(30) , tableName varchar(30) );")
    mysql.connection.commit()

    if request.method == 'POST' and "person" in request.form:
        dbUp = request.form
        person = dbUp['person']
        email = dbUp['email']
        password = dbUp['password']
        cur.execute("insert into account( person , email , password ) values(%s, %s, %s)" , ( person , email , password ) )
        mysql.connection.commit()
        cur.close()
        session["name"] = person
        return redirect('/%s' % person)

    elif request.method == 'POST' and request.form['email']:
        dbIn = request.form
        email = dbIn['email']
        password = dbIn['password']
        check = cur.execute("select * from account where email = %s and password = %s;" , ( email , password ))

        if check > 0:
            records = cur.fetchall()

            session["name"] = records[0][0]

            cur.close()
            return redirect('/%s' % records[0][0])

        else:
            cur.close()
            return redirect('/')

    return render_template("start.html")


@app.route('/<name>')
def profile(name):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM datatable where person = (%s)" , (name,) )
    records = cur.fetchall()
    return render_template("profile.html" , name=name , records = records )


@app.route('/<name>/addTable' , methods=['GET','POST'])
def addTable(name):
    if request.method == 'POST':
        userInput = request.form
        TableName = userInput['Table']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO dataTable(Person, tableName) VALUES(%s, %s)", (name, TableName))
        mysql.connection.commit()
        cur.close()
        return redirect('/%s' % name )
    return render_template("addTable.html")


@app.route('/<name>/deleteTable' , methods=['GET','POST'])
def deleteTable(name):
    if request.method == 'POST':
        userInput = request.form
        TableName = userInput['Table']
        cur = mysql.connection.cursor()
        cur.execute("delete from users where Name = (%s)", (TableName,))
        mysql.connection.commit()
        cur.execute("delete from dataTable where tableName = (%s)", (TableName,))
        mysql.connection.commit()
        return redirect('/%s' % name)
    return render_template("deleteTable.html")


@app.route('/<username>/<table>/add' , methods=['GET','POST'])
def add(username, table ):
    if request.method == 'POST':
        userDetails = request.form
        activity = userDetails['Activity']
        predecessor = userDetails['Predecessor']
        duration = userDetails['Duration']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(Aactivity, Predecessor, Duration, Name) VALUES(%s, %s, %s, %s)" , ( activity , predecessor , int(duration) , table ))
        mysql.connection.commit()
        cur.close()
        return redirect('/%s/%s' % (username , table))
    return render_template("add.html")


@app.route('/<username>/<table>/delete' , methods=['GET','POST'])
def delete(username, table ):
    if request.method == 'POST':
        userDetails = request.form
        activity = userDetails['Activity']
        cur = mysql.connection.cursor()
        cur.execute("with recursive cte( activity ) as (	SELECT Aactivity     FROM ( select * from users where Name = %s ) as users    WHERE Aactivity = %s  UNION ALL  SELECT u.Aactivity     FROM cte JOIN ( select * from users where Name = %s ) as u      ON cte.activity = u.Predecessor) delete from users 	where Name = %s and Aactivity in    ( select * from cte );" , (table,activity,table,table))
        mysql.connection.commit()
        cur.close()
        return redirect('/%s/%s' % (username, table))
    return render_template("delete.html")


@app.route('/<username>/<table>')
def home(username, table ):
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM users where Name = (%s) order by Aactivity asc", (table,) )

    userDetails = cur.fetchall()
    return render_template('show_home.html' , userDetails=userDetails , table = table , username=username)


@app.route('/<username>/<table>/result')
def result( username , table):
    cur = mysql.connection.cursor()
    resultValue = cur.execute("WITH RECURSIVE Cpaths (id , path , length , eft) AS(  SELECT Aactivity , CAST(Aactivity AS CHAR(200)) , 1 ,  Duration    FROM ( select * from users where Name = %s ) as users    WHERE Predecessor = 'none'  UNION ALL  SELECT u.Aactivity , CONCAT(cp.path, ' -> ', u.Aactivity) , cp.length + 1 ,  cp.eft + u.Duration    FROM Cpaths AS cp JOIN ( select * from users where Name = %s ) as u      ON cp.id = u.Predecessor) , Cpaths1 (id , path , lft) AS(  SELECT Aactivity , CAST(Aactivity AS CHAR(200)) ,  (select max(eft) from Cpaths)    FROM ( select * from users where Name = %s ) as users    WHERE Aactivity not in ( select Predecessor from ( select * from users where Name = %s ) as users )  UNION ALL  SELECT u.Predecessor , CONCAT(cp.path, ' <- ', u.predecessor) ,  cp.lft - u.Duration    FROM Cpaths1 AS cp JOIN ( select * from users where Name = %s ) as u      ON cp.id = u.Aactivity),main ( id , path , length , est , eft , lst , lft , tf , Duration ) as(	SELECT Cpaths.id , Cpaths.path , Cpaths.length , max(Cpaths.eft) - duration as est , max(Cpaths.eft) as eft , min(Cpaths1.lft) - Duration as lst ,  min(Cpaths1.lft) as lft , - max(Cpaths.eft) + min(Cpaths1.lft) as tf , Duration FROM Cpaths , Cpaths1 , ( select * from users where Name = %s ) as users		where Aactivity = Cpaths.id and			  Aactivity = Cpaths1.id 		group by Cpaths.id ORDER BY Cpaths.id) ,for_ff( id , ff ) as(	select m1.id , min(m2.est) - m1.eft as ff from main as m1 , main as m2 , ( select * from users where Name = %s ) as u		where		m1.id = u.Predecessor and 		m2.id = u.Aactivity		group by m1.id)select main.id , path , length , est , eft , lst , lft , tf , ifnull(ff,0) as ff , Duration	from main left join for_ff    on 		main.id = for_ff.id order by main.id asc;" , ( table , table , table , table , table , table , table ))
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('show_result.html' , userDetails=userDetails , table = table , username=username)


@app.route('/<username>/<table>/gantt')
def gantt( username , table ):
    init_gantt1(table)
    return render_template('Gantt.html' , table = table , username = username);


if __name__ == "__main__":
    app.run(debug=True)