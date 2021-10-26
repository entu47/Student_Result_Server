from flask import render_template, url_for, flash, redirect, request, Blueprint
from result.models import Mark, Student, Module
from result import db, mail,session
from flask_mail import Message
import random
from result.students.utils import html_to_pdf,remove_resource
student = Blueprint('student', __name__,template_folder="templates")


def generate_otp():
	otp = random.randint(111111,999999)
	return otp

@student.route('/student')
def get_student():
	return render_template('students/home.html')


@student.route('/get_result', methods=['GET', 'POST'])
def get_result():
	if request.method == 'POST':
		roll_no = request.form.get('roll_no')
		var1 = Student.query.filter_by(roll_no=roll_no).first()
		if var1 is None:
			flash('Please Enter Valid Roll No','danger')
			return redirect('/get_result')
		email = var1.email
		msg = Message('OTP', sender='ak475885@gmail.com', recipients=[email])
		session['otp'] = str(generate_otp())
		msg.body = session['otp']
		mail.send(msg)
		flash('A six digit OTP has been sent to your registered email','info')
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
			    var1 = Mark.query.filter_by(stu_id=roll_no)
			    var2 = Student.query.filter_by(roll_no=roll_no).first()
			    email = var2.email
			    html = render_template('students/get_result.html', results=var1)
			    msg = Message('marks info', sender='ak475885@gmail.com', recipients=[email])
			    html_to_pdf(html,email,roll_no)
			    msg.body = '''Your Password is your Roll_No followed by characters of your email before '@' 
			    Lets Say Your Roll_No is 45 
			    And Your Email is abc34@example.com
			    Your Password is 45abc34 '''
			    with student.open_resource("../../out.pdf") as fp:
			    	msg.attach("out.pdf","application/pdf",fp.read())  
			    # msg.attach("mark_report", "application/pdf", pdf)
			    mail.send(msg)
			    remove_resource()
			    flash("Result has been sent to your Registered Email Id !", "success")
			else:
				flash("Oops you entered wrong OTP! Try Once Again", "danger")
			
		else:
			flash("Enter Your Roll No", "info")
		return redirect(url_for('student.get_student'))
			


@student.route('/add_sub', methods=['GET', 'POST'])
def add_sub():
	if request.method == 'POST':
		roll_no = request.form.get("roll_no")
		sub_lis = request.form.getlist("sub")
		var1 = Student.query.get(roll_no)
		if var1 is None:
			flash('Please Enter Valid Roll No','danger')
			return redirect('/add_sub')
		for i in sub_lis:
			var3 = Mark.query.filter_by(stu_id=roll_no,sub_id=i).first()
			if var3:
				continue
			mark1 = Mark(stu_id=roll_no, sub_id=i, marks=0)
			db.session.add(mark1)
		db.session.commit()
		flash('Subject Added Successfully','success')
		return redirect('/student')
	modules = Module.query.all()
	return render_template('students/subject.html', modules=modules)

	# var = Module.query.all()
	# l = []
	# for i in var:
	# 	l.append(i.module_id, i.module_name)
	# return jsonify(l)


