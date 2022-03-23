from flask import Flask, render_template, request, session, jsonify

from DBConnection import Db

app = Flask(__name__)
app.secret_key="hiii"

@app.route('/login')
def login():
    return render_template('admin_index.html')
@app.route('/')
def log():
    return render_template('index.html')

@app.route('/login_post',methods=['post'])
def login_post():
    username=request.form['textfield']
    password=request.form['textfield2']

    db=Db()
    qry="select * from login where username='"+username+"' and password='"+password+"'"
    res=db.selectOne(qry)

    if res is not None:
        session['l_id']=res['lid']
        type=res['type']

        if type=='admin':
            return '''<script>alert('login successfully');window.location='/login'</script>'''
        else:
            return '''<script>alert('invalid user');window.location='/'</script>'''
    else:
        return '''<script>alert('invalid user');window.location='/'</script>'''


    return 'ok'
@app.route('/view_complaints')
def view_complaints():
    db = Db()
    q = " SELECT `complaint`.*,`users`.`name`,`users`.`phone` FROM `complaint` INNER JOIN `users` ON `complaint`.`ulid`=`users`.`ulid`"
    res =db.select(q)
    return render_template('complaints.html',data=res)

@app.route('/view_complaints_post',methods=['post'])
def view_complaints_post():
    frm=request.form['textfield']
    to=request.form['textfield2']
    db=Db()
    q= "SELECT `complaint`.*,`users`.`name`,`users`.`phone` FROM `complaint` INNER JOIN `users` ON `complaint`.`ulid`=`users`.`ulid` where complaint.date BETWEEN '"+frm+"' and '"+to+"'"
    res=db.select(q)
    return render_template('complaints.html',data=res)



@app.route('/view_feedback')
def view_feedback():
    db=Db()
    q="SELECT  `feedback`.*,`users`.`name`,`users`.`phone` FROM `feedback` INNER JOIN `users` ON `feedback`.`ulid`=`users`.`ulid`"
    res=db.select(q)
    return render_template('feedback.html',data=res)
@app.route('/view_feedback_post',methods=['post'])
def view_feedback_post():
    frm=request.form['textfield']
    to=request.form['textfield2']
    db=Db()
    q="SELECT  `feedback`.*,`users`.`name`,`users`.`phone` FROM `feedback` INNER JOIN `users` ON `feedback`.`ulid`=`users`.`ulid`where feedback.date BETWEEN '"+frm+"' and '"+to+"'"
    res=db.select(q)
    return render_template('feedback.html', data=res)

@app.route('/view_registeredusers')
def view_registeredusers():
    db=Db()
    q="SELECT * FROM `users`"
    res=db.select(q)
    return render_template('registeredusers.html',data=res)

@app.route('/view_registeredusers_post',methods=['post'])
def view_registeredusers_post():
    registeredusers=request.form['textfield']
    db=Db()
    q="SELECT * FROM users where name LIKE '%"+registeredusers+"%'"
    res=db.select(q)
    return render_template('registeredusers.html', data=res)
@app.route('/send_reply/<id>')
def send_reply(id):
    db=Db()
    qry="select * from complaint where cid='"+id+"'"
    res=db.selectOne(qry)
    return render_template('reply.html',data=res)

@app.route('/send_reply_post',methods=['post'])
def send_reply_post():
    r_id=request.form['textfield']
    reply=request.form['textarea']
    db=Db()
    q="update complaint set reply='"+reply+"',status='ok' where cid='"+str(r_id)+"'"
    res=db.update(q)
    return '''<script>alert('replied');window.location='/view_complaints'</script>'''


@app.route('/view_adminhome')
def view_adminhome():
    return render_template('adminhome.html')


@app.route('/change_password')
def change_password():
    return render_template('change password.html')
@app.route('/change_password_post',methods=['post'])
def change_password_post():
    current=request.form['textfield']
    newp=request.form['textfield2']
    confirmp=request.form['textfield2']
    db=Db()
    q="select * from login where password='"+current+"'"
    res=db.selectOne(q)
    if res!=None:
        if newp==confirmp:
            qry="update login set password='"+newp+"' where lid='"+str(session['l_id'])+"'"
            res1=db.update(qry)
            return '''<script>alert('password changed');window.location='/'</script>'''
        else:
            return '''<script>alert('password not changed');window.location='/change_password'</script>'''
    else:
        return '''<script>alert('Current Password must be valid');window.location='/change_password'</script>'''




@app.route('/logout')
def logout():
    return render_template('login.html')

#----------------------------------android


@app.route('/and_login_post',methods=['post'])
def and_login_post():
    username=request.form['uname']
    password=request.form['passw']

    db=Db()
    qry="select * from login where username='"+username+"' and password='"+password+"'"
    res=db.selectOne(qry)

    if res is not None:
        session['l_id']=res['lid']
        type=res['type']

        return jsonify(status="ok",lid=res['lid'])
    else:
        return jsonify(status="no")

    

@app.route('/and_post',methods=['post'])
def and_post_post():
    db=Db()
    qry="SELECT * FROM `post`"
    res=db.select(qry)
    return jsonify(status="ok")


    pass





if __name__ == '__main__':
    app.run()
