__author__ = 'mullapudi'

from flask import Flask,request,redirect,Blueprint,render_template,flash,session,Blueprint,url_for,make_response
from flask.ext.login import LoginManager,UserMixin,confirm_login, fresh_login_required,current_user,login_required,login_user,logout_user

from admin_authentication import *
from updating_order_status_in_database import *
from tracking_status_from_database import *
from admin_secret_question_answer_authentication import *
from adding_new_order_to_database import *
from mail_the_details import *

blueprint = Blueprint('app', __name__, url_prefix='/title')

@blueprint.route('/', methods=['GET', 'POST'])
def title():
    # Located at https://yourdomain.com/login
    return render_template('title.html')

@blueprint.route('/home/', methods=['GET', 'POST'])
def home():
    return redirect('/title/')

@blueprint.route('/mainpage/', methods=['GET', 'POST'])
def mainpage():
    return render_template('adminPage1.html')




@blueprint.route('/admin/', methods=['GET', 'POST'])
def admin():
    return render_template('admin_login.html')

@blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    # Located at https://yourdomain.com/login/login
    un = request.form['un']
    pwd = request.form['pwd']
    error_message1="Sorry,Incorrect Username or Password,Try Again"
    error_message2="Please enter the required credintials for login"
    if un == '' or pwd == '':
        return render_template('admin_login.html',error_message2=error_message2)
    print un,pwd
    if verify_from_database_admin(un,pwd):
        session['username']=un
        if session['username']:
            print "session recorded"
            response=make_response()
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate" # HTTP 1.1.
            response.headers["Pragma"] = "no-cache" # HTTP 1.0.
            response.headers["Expires"] = "0" # Proxies.
        print "admin authentication successful"
        return render_template('adminPage1.html')
    else:
        return render_template('admin_login.html',error_message1=error_message1)

@blueprint.route('/addnew/', methods=['GET', 'POST'])
def addnew():
    # Located at https://yourdomain.com/login/addnew
    return render_template('adminPage2.html')

@blueprint.route('/adding/', methods=['GET', 'POST'])
def adding():
    pid = request.form['pid']
    usid = request.form['usid']
    address = request.form['address']
    status = request.form['status']
    phno = request.form['phno']
    email = request.form['email']
    ord_date = request.form['ord_date']
    del_date = request.form['del_date']
    error_message='Please enter all the required details to add'
    if pid == '' or usid == '' or address == '' or status == '' or phno == '' or email == '' or ord_date == '' or del_date == '':
        return render_template('adminPage2.html',error_message=error_message)

    tid=addnew_to_database(pid,usid,address,status,phno,email,ord_date,del_date)
    text ='Your order tracking id is '+ tid +' and it is in shipment '
    subject='Order Status Notification'
    send_Email(email,text,subject)
    return render_template('adminPage4.html')

@blueprint.route('/updatestatus/', methods=['GET', 'POST'])
def updatestatus():
    # Located at https://yourdomain.com/login/addnew
    return render_template('adminPage3.html')

@blueprint.route('/updating/', methods=['GET', 'POST'])
def updating():
    tid=request.form['tid']
    status=request.form['status']
    error_message1='Please enter all the required details to update'
    error_message2="Sorry,No Records were found with the provided Tracking ID"
    if tid == '' or status == '':
        return render_template('adminPage3.html',error_message1=error_message1)
    result=updating_status_in_database(tid,status)
    if result:
        text ='Your order with tracking ID '+ tid +' is '+ result[1]
        subject='Order Status Notification'
        send_Email(result[0],text,subject)
        return render_template('adminPage5.html')
    else:
        return render_template('adminPage3.html',error_message2=error_message2)

@blueprint.route('/forgotpassword/', methods=['GET', 'POST'])
def forgotpassword():
    return render_template('forgotpassword.html')

secret_question_dictionary={'mothers_maidenname':'what is your mothers maiden name','firstschool':'what is the name of your first school'}

@blueprint.route('/forgotpassword1/', methods=['GET', 'POST'])
def forgotpassword1():
    un=request.form['un']
    error_message1="Sorry,No Records were found with the provided Username"
    error_message2="please enter the Username"
    if un == '':
        return render_template('forgotpassword.html',error_message2=error_message2)
    else:
        secret_question_small=admin_secret_question(un)

        if secret_question_small:
            secret_question=secret_question_dictionary[secret_question_small]
            return render_template('forgotpassword1.html',secret_question=secret_question,un=un)
        else:
            return render_template('forgotpassword.html',error_message1=error_message1)


@blueprint.route('/verify_secret_answer/', methods=['GET', 'POST'])
def verify_secret_answer():
    ans=request.form['ans']
    un=request.form['un']
    secret_question=request.form['secret_question']
    error_message1='please enter the Answer to the secret question'
    error_message2='Sorry,answer was incorrect'
    password_mailed_confirmation="Your password had mailed to your Email,Kindly check your Email"

    if ans == '':
        return render_template('forgotpassword1.html',error_message1=error_message1,un=un,secret_question=secret_question)
    else:
        result=admin_secret_answer(un)

        if result[2] == ans:
            text ='Your password is '+ result[0]
            subject='Password'
            send_Email(result[1],text,subject)
            return render_template('admin_login.html',password_mailed_confirmation=password_mailed_confirmation)
        else:
            return render_template('forgotpassword1.html',error_message2=error_message2,un=un,secret_question=secret_question)


@blueprint.route('/logout/', methods=['GET', 'POST'])
def logout():
    print session
    session.pop('username',None)
    print session
    if not session.get('username'):
        print "session deleted"
    return redirect('/title/admin/')

@blueprint.route('/user/', methods=['GET', 'POST'])
def user():
    return render_template('user_login.html')

@blueprint.route('/user_track/', methods=['GET', 'POST'])
def user_track():
    tid=request.form['tid']
    error_message1="Sorry,No Records were found with the provided Tracking ID"
    error_message2="Please enter the Tracking ID"
    if tid == '':
        return render_template('user_login.html',error_message2=error_message2)
    status=track_status_from_database(tid)
    print status
    if status:
        return render_template('Track_Result.html',status=status)
    else:
        return render_template('user_login.html',error_message1=error_message1)

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

app.register_blueprint(blueprint)

if __name__ == "__main__":
    app.run(debug=True)