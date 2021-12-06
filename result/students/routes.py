from flask import render_template, url_for, flash, redirect, request, Blueprint
from result.models import Mark, Student, Module
from result import db, mail, session
from flask_mail import Message
import random
from result.students.utils import html_to_pdf, remove_resource
student = Blueprint('student', __name__, template_folder="templates")


def generate_otp():
    otp = random.randint(111111, 999999)
    return otp


class Email:
    def __init__(self, receiver, sender, title, body, html=None, attach=None):
        self.receiver = receiver
        self.sender = sender
        self.title = title
        self.body = body
        self.attach = attach
        self.html = html

    def send_email(self):
        msg = Message(self.title, sender=self.sender,
                      recipients=[self.receiver])
        msg.body = self.body
        msg.html = self.html
        # msg.attach() ---- Feature is about to come
        mail.send(msg)


@student.route('/student')
def get_student():
    return render_template('students/home.html')


@student.route('/get_result', methods=['GET', 'POST'])
def get_result():
    if request.method == 'POST':
        roll_no = request.form.get('roll_no')
        student = Student.query.filter_by(roll_no=roll_no).first()
        if student is None:
            flash('Please Enter Valid Roll No', 'danger')
            return redirect('/get_result')
        email = student.email
        message = Email(email, 'ak475885@gmail.com', 'OTP', session['otp'])
        message.send_email()
        flash('A six digit OTP has been sent to your registered email', 'info')
        return render_template('students/validate.html', roll_no=roll_no)

    return render_template('students/enter_detail.html')


@student.route('/validate/<int:roll_no>', methods=['POST'])
def validate(roll_no):
    if request.method == 'POST':
        user_otp = request.form.get('user_otp')
        if 'otp' in session:
            num = session['otp']
            session.pop('otp', None)
            if num == user_otp:
                mark = Mark.query.filter_by(stu_id=roll_no)
                student = Student.query.filter_by(roll_no=roll_no).first()
                email = student.email
                html = render_template(
                    'students/get_result.html', results=mark)

                html_to_pdf(html, email, roll_no)
                body = '''Your Password is your Roll_No followed
                           by characters of your email before '@'
                           Lets Say Your Roll_No is 45
                           And Your Email is abc34@example.com
                            Your Password is 45abc34 '''
                # with student.open_resource("../../out.pdf") as fp:
                #     msg.attach("out.pdf", "application/pdf", fp.read())
                # msg.attach("mark_report", "application/pdf", pdf)

                message = Email(email, 'ak475885@gmail.com', 'Marks_Info',
                                body, html)
                message.send_email()
                remove_resource()
                flash("Result has been sent to your Registered Email Id !",
                      "success")
            else:
                flash("Oops you entered wrong OTP! Try Once Again", "danger")

        else:
            flash("Enter Your Roll No", "info")
        return redirect(url_for('student.get_student'))


@student.route('/add_module', methods=['GET', 'POST'])
def add_module():
    if request.method == 'POST':
        roll_no = request.form.get("roll_no")
        subjects = request.form.getlist("sub")
        student = Student.query.get(roll_no)
        if student is None:
            flash('Please Enter Valid Roll No', 'danger')
            return redirect('/add_module')
        for subject in subjects:
            mark = Mark.query.filter_by(stu_id=roll_no, sub_id=subject).first()
            if mark:
                continue
            mark_new = Mark(stu_id=roll_no, sub_id=subject, marks=0)
            db.session.add(mark_new)
        db.session.commit()
        flash('Subject Added Successfully', 'success')
        return redirect('/student')
    modules = Module.query.all()
    return render_template('students/subject.html', modules=modules)

    # var = Module.query.all()
    # l = []
    # for subject in var:
    # 	l.append(subject.module_id, subject.module_name)
    # return jsonify(l)
