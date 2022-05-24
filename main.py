import demjson
from flask import Flask, render_template, request, session, jsonify, redirect

from DBConnection import Db
from EmotionChecking import emotions
app = Flask(__name__)
app.secret_key="hiii"
staticpath="C:\\ProjectFinal\\main\\main\\static\\"
@app.route('/login')
def login():
    if session["logout"] == "1":
        return render_template('admin_index.html')
    else:
        return redirect('/logout')
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
            session["logout"]="1"
            return '''<script>alert('login successfully');window.location='/login'</script>'''
        else:
            return '''<script>alert('invalid user');window.location='/'</script>'''
    else:
        return '''<script>alert('invalid user');window.location='/'</script>'''



@app.route('/view_complaints')
def view_complaints():
    if session["logout"]=="1":
        db = Db()
        q = " SELECT `complaint`.*,`users`.`name`,`users`.`phone` FROM `complaint` INNER JOIN `users` ON `complaint`.`ulid`=`users`.`ulid`"
        res =db.select(q)
        return render_template('complaints.html',data=res)
    else:
        return redirect('/logout')

@app.route('/view_complaints_post',methods=['post'])
def view_complaints_post():
    if session["logout"] == "1":
        frm=request.form['textfield']
        to=request.form['textfield2']
        db=Db()
        q= "SELECT `complaint`.*,`users`.`name`,`users`.`phone` FROM `complaint` INNER JOIN `users` ON `complaint`.`ulid`=`users`.`ulid` where complaint.date BETWEEN '"+frm+"' and '"+to+"'"
        res=db.select(q)
        return render_template('complaints.html',data=res)
    else:
        return redirect('/logout')



@app.route('/view_feedback')
def view_feedback():
    if session["logout"] == "1":
        db=Db()
        q="SELECT  `feedback`.*,`users`.`name`,`users`.`phone` FROM `feedback` INNER JOIN `users` ON `feedback`.`ulid`=`users`.`ulid`"
        res=db.select(q)
        return render_template('feedback.html',data=res)
    else:
        return redirect('/logout')
@app.route('/view_feedback_post',methods=['post'])
def view_feedback_post():
    if session["logout"] == "1":
        frm=request.form['textfield']
        to=request.form['textfield2']
        db=Db()
        q="SELECT  `feedback`.*,`users`.`name`,`users`.`phone` FROM `feedback` INNER JOIN `users` ON `feedback`.`ulid`=`users`.`ulid`where feedback.date BETWEEN '"+frm+"' and '"+to+"'"
        res=db.select(q)
        return render_template('feedback.html', data=res)
    else:
        return redirect('/logout')

@app.route('/view_registeredusers')
def view_registeredusers():
    if session["logout"] == "1":
        db=Db()
        q="SELECT * FROM `users`"
        res=db.select(q)
        return render_template('registeredusers.html',data=res)
    else:
        return redirect('/logout')

@app.route('/view_registeredusers_post',methods=['post'])
def view_registeredusers_post():
    if session["logout"] == "1":
        registeredusers=request.form['textfield']
        db=Db()
        q="SELECT * FROM users where name LIKE '%"+registeredusers+"%'"
        res=db.select(q)
        return render_template('registeredusers.html', data=res)
    else:
        return redirect('/logout')
@app.route('/send_reply/<id>')
def send_reply(id):
    if session["logout"] == "1":
        db=Db()
        qry="select * from complaint where cid='"+id+"'"
        res=db.selectOne(qry)
        return render_template('reply.html',data=res)
    else:
        return redirect('/logout')

@app.route('/send_reply_post',methods=['post'])
def send_reply_post():
    if session["logout"] == "1":
        r_id=request.form['textfield']
        reply=request.form['textarea']
        db=Db()
        q="update complaint set reply='"+reply+"',status='ok' where cid='"+str(r_id)+"'"
        res=db.update(q)
        return '''<script>alert('replied');window.location='/view_complaints'</script>'''
    else:
        return redirect('/logout')


@app.route('/view_adminhome')
def view_adminhome():
    if session["logout"] == "1":
        return render_template('adminhome.html')
    else:
        return redirect('/logout')


@app.route('/change_password')
def change_password():
    if session["logout"] == "1":
        return render_template('change password.html')
    else:
        return redirect('/logout')
@app.route('/change_password_post',methods=['post'])
def change_password_post():
    if session["logout"] == "1":
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
    else:
        return redirect('/logout')
@app.route('/web_and_analysis/<lid>')
def web_and_analysis(lid):
    db = Db()
    if session["logout"] == "1":
        res = db.select("SELECT * FROM `post` WHERE `uid`='"+lid+"'")
        emotion = []
        r = {}
        em = emotions()
        if len(res)>0:
            for i in res:
                # print(i["post"])
                emotion.append(em.pred(i["post"]))
                # print(emotion)

        re2="SELECT `comment` FROM `comment` WHERE `uid`='"+lid+"'"
        res2=db.select(re2)
        if len(res2)>0:
            for i in res2:
                print(i["comment"])
                emotion.append(em.pred(i["comment"]))
        print(emotion)
        count_neu = emotion.count("neutral")
        print("count neu=", count_neu)
        count_sad = emotion.count("sadness")
        print("count sad=", count_sad)
        count_fear = emotion.count("fear")
        print("count fear=", count_fear)
        count_joy = emotion.count("joy")
        print("count joy=", count_joy)
        count_anger = emotion.count("anger")
        print("count anger=", count_anger)
        total_count = len(emotion)

        print("total count=", total_count)
        if total_count>0:
            per_neu = (float(count_neu) / float(total_count)) * 100
            print("percentage neutral=", per_neu)
            per_sad = (float(count_sad) / float(total_count)) * 100
            print("percentage sad=", per_sad)
            per_fear = (float(count_fear) / float(total_count)) * 100
            print("percentage fear=", per_fear)
            per_joy = (float(count_joy) / float(total_count)) * 100
            print("percentage joy=", per_joy)
            per_anger = (float(count_anger) / float(total_count)) * 100
            print("percentage joy=", per_anger)

            # if len(res) > 0:
            #     r['status'] = "1"
            #     r['neutral'] = per_neu
            #     r['sad'] = per_sad
            #     r['fear'] = per_fear
            #     r['joy'] = per_joy
            #     r['anger'] = per_anger
            # else:
            #     r['status'] = "0"
            labels=["neutral","sad","fear","joy","anger"]
            values=[per_neu,per_sad,per_fear,per_joy,per_anger]


            print(labels)
            print(values)


            return render_template('chrt.html',labels=labels,values=values)
        else:
            return "No data"
    else:
        return redirect('/logout')

@app.route('/logout')
def logout():
    session["logout"] = "0"
    return render_template('index.html')


#----------------------------------android
@app.route('/and_user_reg',methods=["post"])
def and_user_reg():
    # `ulid`, `name`, `dob`, `gender`, `place`, `photo`, `phone`, `email`

    name=request.form["name"]
    dob=request.form["dob"]
    gender=request.form["gender"]
    place=request.form["place"]

    photo=request.form["photo"]
    import time
    import base64


    timestr = time.strftime("%Y%m%d-%H%M%S")
    print(timestr)
    a = base64.b64decode(photo)
    fh = open(staticpath+"user\\" + timestr + ".jpg", "wb")
    path = "/static/user/" + timestr + ".jpg"
    fh.write(a)
    fh.close()
    phone=request.form["phone"]
    email=request.form["email"]
    pasw=request.form["passw"]
    d=Db()
    lg="INSERT INTO `login`(`username`,`password`,`type`)VALUES('"+email+"','"+pasw+"','user')"
    lid=d.insert(lg)
    usr="INSERT INTO `users`(`ulid`,`name`,`dob`,`gender`,`place`,`photo`,`phone`,`email`)VALUE" \
        "('"+str(lid)+"','"+name+"','"+dob+"','"+gender+"','"+place+"','"+path+"','"+phone+"','"+email+"')"
    d.insert(usr)
    return jsonify(status="ok")

@app.route('/and_login_post',methods=['post'])
def and_login_post():
    username=request.form['usnm']
    password=request.form['pswd']

    db=Db()
    qry="select * from login where username='"+username+"' and password='"+password+"'"
    res=db.selectOne(qry)
    print(qry)
    if res is not None:
        session['l_id']=res['lid']
        type=res['type']

        return jsonify(status="ok",login_id=res['lid'],type="user")
    else:
        return jsonify(status="no")

    

@app.route('/and_view_profile',methods=['post'])
def and_view_profile():
    db=Db()
    lid=request.form["lid"]
    qry="SELECT * FROM `users` WHERE `ulid`='"+lid+"'"
    res=db.selectOne(qry)
    # `name`, `dob`, `gender`, `place`, `photo`, `phone`, `email`
    return jsonify(status="ok",name=res["name"],dob=res["dob"],gen=res["dob"],place=res['place'],photo=res["photo"],phone=res["phone"],email=res["email"])


@app.route('/and_view_users',methods=["post"])
def and_view_users():
    lid=request.form["lid"]
    d=Db()
    q="SELECT * FROM `users` where ulid!='"+lid+"'"
    res=d.select(q)
    if len(res)>0:
        ls=[]
        for i in res:
            q1="SELECT * FROM `friendrequest` WHERE (`frmid`='"+lid+"' AND toid='"+str(i["ulid"])+"')OR (`frmid`='"+str(i["ulid"])+"' AND toid='"+lid+"')"
            r=d.selectOne(q1)
            if r is not None:
                a={'name':i['name'],'email':i['email'],'photo':i['photo'],'status':'yes','ulid':i["ulid"]}
                ls.append(a)
            else:
                a = {'name': i['name'], 'email': i['email'], 'photo': i['photo'], 'status': 'not','ulid':i["ulid"]}
                ls.append(a)



        return jsonify(status="ok",users=ls)


    else:
        return jsonify(status="ok")

@app.route('/and_send_friend_request',methods=["post"])
def and_send_friend_request():
    lid=request.form["lid"]
    tolid=request.form["tolid"]
    q="INSERT INTO `friendrequest`(`frmid`,`toid`,`status`)VALUES('"+lid+"','"+tolid+"','pending')"
    d=Db()
    res=d.insert(q)
    return jsonify(status="ok")
@app.route('/and_cancel_friend_request',methods=["post"])
def and_cancel_friend_request():
    lid=request.form["lid"]
    tolid=request.form["tolid"]
    q="delete from `friendrequest` where (`frmid`='"+lid+"' and `toid`='"+tolid+"') or (`frmid`='"+tolid+"' and `toid`='"+lid+"')"
    d=Db()
    res=d.delete(q)
    return jsonify(status="ok")

@app.route('/and_view_friend_request',methods=["post"])
def and_view_friend_request():
    lid=request.form["lid"]
    q="SELECT `users`.*,`friendrequest`.* FROM `users` INNER JOIN `friendrequest` ON `users`.`ulid`=`friendrequest`.`frmid` WHERE `friendrequest`.`toid`='"+lid+"' and friendrequest.status='pending'"
    d=Db()
    res=d.select(q)
    print(res)
    return jsonify(status="ok",users=res)

@app.route('/and_accept_or_reject_request',methods=["post"])
def and_accept_or_reject_request():
    frid=request.form["frid"]
    status=request.form["status"]
    q="UPDATE `friendrequest` SET `status`='"+status+"' WHERE frid='"+frid+"'"
    d=Db()
    d.update(q)
    return jsonify(status="ok")

@app.route('/and_my_friend',methods=["post"])
def and_my_friend():
    lid=request.form["lid"]
    q="SELECT `users`.*,`friendrequest`.* FROM `users` INNER JOIN `friendrequest` ON `users`.`ulid`=`friendrequest`.`frmid` WHERE `friendrequest`.`toid`='"+lid+"' and friendrequest.status!='pending' union SELECT `users`.*,`friendrequest`.* FROM `users` INNER JOIN `friendrequest` ON `users`.`ulid`=`friendrequest`.`toid` WHERE `friendrequest`.`frmid`='"+lid+"' and friendrequest.status!='pending'"
    d=Db()
    res=d.select(q)
    print(res)
    return jsonify(status="ok",users=res)
@app.route('/and_delete_friend',methods=["post"])
def and_delete_friend():
    frid=request.form["frid"]
    q="DELETE FROM `friendrequest` WHERE `frid`='"+frid+"'"
    d=Db()
    res=d.delete(q)
    return jsonify(status="ok")

@app.route('/and_block_friend',methods=["post"])
def and_block_friend():
    frid=request.form["frid"]
    fromid=request.form["lid"]
    toid=request.form["tolid"]
    q="UPDATE `friendrequest` SET `status`='blocked' WHERE `frid`='"+frid+"'"
    d=Db()
    res=d.update(q)

    q="INSERT INTO `block`(`uid`,`blockeddate`,`fromid`) VALUES('"+toid+"',curdate(),'"+fromid+"') "
    d=Db()
    d.insert(q)
    return jsonify(status="ok")

@app.route('/and_unblock_friend',methods=["post"])
def and_unblock_friend():
    frid=request.form["frid"]
    fromid=request.form["lid"]
    toid=request.form["tolid"]
    q="UPDATE `friendrequest` SET `status`='accepted' WHERE `frid`='"+frid+"'"
    d=Db()
    res=d.update(q)

    q="delete from `block` where `uid`='"+toid+"'and `fromid`='"+fromid+"'"
    d=Db()
    d.delete(q)
    return jsonify(status="ok")
@app.route('/and_upload_post',methods=["post"])
def and_upload_post():
    lid=request.form["lid"]
    post=request.form["post"]
    q="INSERT INTO post(`uid`,`post`,`date`)VALUES('"+lid+"','"+post+"',curdate())"
    d=Db()
    d.insert(q)
    return jsonify(status="ok")
@app.route('/and_view_my_post',methods=["post"])
def and_view_my_post():
    lid=request.form["lid"]
    q="SELECT * FROM `post` WHERE `uid`='"+lid+"'"
    d=Db()
    res=d.select(q)
    return jsonify(status="ok",users=res)

@app.route('/and_send_post_like',methods=["post"])
def and_send_post_like():
    postid=request.form["postid"]
    lid=request.form["lid"]

    d=Db()
    q="SELECT * FROM `like` WHERE `uid`='"+lid+"' AND `pid`='"+postid+"'"
    res=d.selectOne(q)
    if res is not None:
        return jsonify(status="exist")
    else:
        q1="INSERT INTO `like`(`uid`,`like`,`pid`)VALUES('"+lid+"','1','"+postid+"')"
        d=Db()
        d.insert(q1)
        return jsonify(status="ok")
@app.route('/and_send_comments',methods=["post"])
def and_send_comments():
    postid=request.form["postid"]
    comments=request.form["comments"]
    lid=request.form["lid"]
    q="INSERT INTO `comment`(`pid`,`uid`,`comment`,date)VALUES('"+postid+"','"+lid+"','"+comments+"',curdate())"
    d=Db()
    d.insert(q)
    return jsonify(status="ok")
@app.route('/and_view_comment',methods=["post"])
def and_view_comment():
    postid=request.form["postid"]
    d=Db()
    q="SELECT `comment`.*,`users`.* FROM `comment` INNER JOIN users on `users`.`ulid`=`comment`.`uid` WHERE `comment`.`pid`='"+postid+"'"
    res=d.select(q)
    return jsonify(status="ok",users=res)

@app.route('/and_view_all_post',methods=["post"])
def and_view_all_post():
    lid=request.form["lid"]
    q = "SELECT `toid` as id FROM `friendrequest` WHERE `frmid`='" + lid + "' AND STATUS='accepted' UNION SELECT `frmid` as id FROM `friendrequest` WHERE `toid`='" + lid + "' AND STATUS='accepted'"
    d = Db()
    res = d.select(q)
    ls = []
    if len(res) > 0:
        for i2 in res:
            dd = Db()
            p = "SELECT `post`.*,`users`.* FROM `post` INNER JOIN `users` ON `post`.`uid`=`users`.`ulid` WHERE `post`.`uid`='"+str(i2["id"])+"'"
            re = dd.select(p)
            if len(re) > 0:
                for i in re:
                    a = {'pid': i["pid"], 'post': i["post"], 'date': i["date"], 'name': i["name"], 'photo': i["photo"]}
                    ls.append(a)
                return jsonify(status="ok", users=ls)
            else:
                return jsonify(status="no")
    else:
        return jsonify(status="no")



@app.route('/user_Shsre_post',methods=["post"])
def user_Shsre_post():
    postid=request.form["postid"]
    uid=request.form["lid"]
    q="INSERT INTO share(`toid`,`pid`,`date`)VALUES('"+uid+"','"+postid+"',curdate())"
    d=Db()
    d.insert(q)
    return jsonify(status="ok")
@app.route('/view_shared_post',methods=["post"])
def view_shared_post():
    lid=request.form["lid"]
    q="SELECT `toid` as id FROM `friendrequest` WHERE `frmid`='"+lid+"' AND STATUS='accepted' UNION SELECT `frmid` as id FROM `friendrequest` WHERE `toid`='"+lid+"' AND STATUS='accepted'"
    d=Db()
    res=d.select(q)
    ls=[]
    if len(res)>0:
        for i2 in res:
            dd=Db()
            p="SELECT `post`.*,`users`.* FROM `post` INNER JOIN `users` ON `post`.`uid`=`users`.`ulid` INNER JOIN `share` ON `share`.`pid` =`post`.`pid` WHERE `share`.`toid`='"+str(i2["id"])+"' union SELECT `post`.*,`users`.* FROM `post` INNER JOIN `users` ON `post`.`uid`=`users`.`ulid` INNER JOIN `share` ON `share`.`pid` =`post`.`pid` WHERE `share`.`toid`='"+str(lid)+"'"
            re=dd.select(p)
            if len(re)>0:
                for i in re:
                    a={'pid':i["pid"],'post':i["post"],'date':i["date"],'name':i["name"],'photo':i["photo"]}
                    ls.append(a)
                return jsonify(status="ok",users=ls)
            else:
                return jsonify(status="no")
    else:
        return jsonify(status="no")

@app.route('/andsentcomplaint',methods=["post"])
def andsentcomplaint():
    lid=request.form["lid"]
    com=request.form["complaint"]
    q="INSERT INTO `complaint`(`ulid`,`complaint`,`reply`,`status`,`date`)VALUES('"+lid+"','"+com+"','pending','pending',curdate())"
    d=Db()
    d.insert(q)
    return jsonify(status="ok")



@app.route('/send_feedback',methods=["post"])
def send_feedback():
    uid=request.form["uid"]
    feedback=request.form["feedback"]
    q="INSERT INTO `feedback` (`ulid`,`feedback`,`date`) VALUES ('"+uid+"','"+feedback+"',curdate())"
    d=Db()
    d.insert(q)
    return jsonify(status="ok")



@app.route('/and_viewreply',methods=["post"])
def and_viewreply():
    lid=request.form["lid"]
    q="SELECT * FROM `complaint` WHERE `ulid`='"+lid+"'"
    d=Db()
    res=d.select(q)
    return jsonify(status="ok",data=res)

@app.route('/and_rating_sadd',methods=["post"])
def and_rating_sadd():
    lid=request.form["lid"]
    rate=request.form["rating"]
    q="INSERT INTO `rating`(`uid`,`rating`) VALUES('"+lid+"','"+rate+"')"
    d=Db()
    d.insert(q)
    return jsonify(status="ok")
@app.route('/analysis',methods=["post"])
def and_analysis():

    lid = request.form['lid']
    db = Db()
    res = db.select("SELECT * FROM `post` WHERE `uid`='"+lid+"'")
    emotion = []
    r = {}

    from EmotionChecking import emotions
    em = emotions()
    if len(res)>0:
        for i in res:
            print(i["post"])
            emotion.append(em.pred(i["post"]))
            print(emotion)

    re2="SELECT `comment` FROM `comment` WHERE `uid`='"+lid+"'"
    res2=db.select(re2)
    if len(res2)>0:
        for i in res2:
            print(i["comment"])
            emotion.append(em.pred(i["comment"]))
            print(emotion)

    re3 = "SELECT `chat` FROM `chat` WHERE `frmid`='"+lid+"'"
    res3 = db.select(re3)
    if len(res3) > 0:
        for i in res3:
            print(i["chat"])
            emotion.append(em.pred(i["chat"]))
            print(emotion)
    count_neu = emotion.count("neutral")+emotion.count("empty")
    print("count neu=", count_neu)
    count_sad = emotion.count("sadness")
    print("count sad=", count_sad)
    count_fear = emotion.count("fear")+emotion.count("fun")
    print("count fear=", count_fear)
    count_joy = emotion.count("joy")+emotion.count("love")+emotion.count("surprise")+emotion.count("happiness")
    print("count joy=", count_joy)
    count_anger = emotion.count("anger")+emotion.count("hate")
    print("count anger=", count_anger)

    count_dist = emotion.count("worry")
    print("count dist=", count_dist)

    total_count = len(emotion)
    print("total count=", total_count)
    per_neu = (float(count_neu) / float(total_count)) * 100
    print("percentage neutral=", per_neu)
    per_sad = (float(count_sad) / float(total_count)) * 100
    print("percentage sad=", per_sad)
    per_fear = (float(count_fear) / float(total_count)) * 100
    print("percentage fear=", per_fear)
    per_joy = (float(count_joy) / float(total_count)) * 100
    print("percentage joy=", per_joy)
    per_anger = (float(count_anger) / float(total_count)) * 100

    per_dist = (float(count_dist) / float(total_count)) * 100
    print("percentage anger=", per_dist)

    if len(res) > 0:
        r['status'] = "1"
        r['neutral'] = per_neu
        r['sad'] = per_sad
        r['fear'] = per_fear
        r['joy'] = per_joy
        r['anger'] = per_anger
    else:
        r['status'] = "0"
    # return demjson.encode(r)
    return jsonify(status="ok",Neutral=per_neu,Sad=per_sad,Fearful=per_fear,Happy=per_joy,Angry=per_anger,Disgusted=per_dist)

@app.route('/in_message', methods=['POST'])
def message():
    fr_id = request.form["fid"]
    to_id = request.form["toid"]
    message = request.form["msg"]
    query7 = "INSERT INTO `chat`(`frmid`,`toid`,`chat`,DATE) VALUES ('" + fr_id + "' ,'" + to_id + "','" + message + "',CURDATE())"
    print(query7);
    d=Db()
    res=d.insert(query7)
    # from EmotionChecking import emotional
    # em=emotional()
    # resem=em.lik(message)
    #
    # q="INSERT INTO `chat_emo`(`ulid`,`emotions`)VALUE('"+fr_id+"','"+resem+"')"
    # d.insert(q)
    return jsonify(status="ok")

@app.route('/view_message', methods=['POST'])
def msg():
    fid = request.form["fid"]
    toid = request.form["toid"]
    # name = request.form["name"]
    lmid = request.form['lastmsgid'];

    #  query = "select *  from chat_coach_user where (sender_id='" + fr_id + "' and receiver_id='" + to_id + "') or (sender_id='" + to_id + "'  and receiver_id='" + fr_id + "')"
    query="SELECT `frmid`,`chat`,`date`,`chid` FROM `chat` WHERE `chid`>'"+lmid+"' AND ((`frmid`='"+toid+"' AND  `toid`='"+fid+"') OR (`toid`='"+toid+"' AND `frmid`='"+fid+"')  )  ORDER BY `chid` ASC"
    d=Db()
    res=d.select(query)

    print(query)
    print(res)
    return jsonify(status='ok', res1=res)


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
