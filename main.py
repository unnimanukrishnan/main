from flask import Flask,render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('login.html')
@app.route('/view_complaints')
def view_complaints():
    return render_template('complaints.html')
@app.route('/view_feedback')
def view_feedback():
    return render_template('feedback.html')
@app.route('/view_registeredusers')
def view_registeredusers():
    return render_template('registeredusers.html')
@app.route('/view_reply')
def view_reply():
    return render_template('reply.html')
@app.route('/view_adminhome')
def view_adminhome():
    return render_template('adminhome.html')


@app.route('/logout')
def logout():
    return render_template('login.html')






if __name__ == '__main__':
    app.run()
