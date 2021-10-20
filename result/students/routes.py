from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify
from result.models import Mark, Student, Module
from result import db, mail
from flask_mail import Message
import random
import pdfkit
import os
student = Blueprint('student', __name__)

otp = 0

def generate_otp():
	global otp
	otp = random.randint(000000,999999)
	return otp

@student.route('/get_result', methods = ['GET', 'POST'])
def get_result():
	if request.method == 'POST':
		roll_no = request.form.get('roll_no')
		var1 = Student.query.filter_by(roll_no=roll_no).first()
		email = var1.email
		msg = Message('OTP', sender='ak475885@gmail.com', recipients=[email])
		msg.body = str(generate_otp())
		# mail.login(os.environ.get('EMAIL_USER'),os.environ.get('EMAIL_PASS'))
		mail.send(msg)
		return render_template('validate.html', roll_no=roll_no)
		# d = {}

		# for i in var1:
		# 	d[str(i.module.module_name)] = i.marks
		# return d
	return render_template('result_ac.html')


@student.route('/validate/<int:roll_no>', methods=['GET','POST'])
def validate(roll_no):
	if request.method == 'POST':
		user_otp = request.form.get('user_otp')
		if str(user_otp) == str(otp):
			var1 = Mark.query.filter_by(stu_id=roll_no)
			var2 = Student.query.filter_by(roll_no=roll_no).first()
			email = var2.email
			html = render_template('get_result.html', results=var1)
			msg = Message('marks info', sender='ak475885@gmail.com', recipients=[email])
			pdf = pdfkit.from_string(html, False)
			msg.html=html
			msg.attach("mark_report", "application/pdf", pdf)
			mail.send(msg)
			return "result sent to registered email"
		else:
			return "Agli Baar"


@student.route('/add_sub', methods=['GET', 'POST'])
def add_sub():
	if request.method == 'POST':
		roll_no = request.form.get("roll_no")
		sub_lis = request.form.getlist("sub")
		for i in sub_lis:
			mark1 = Mark(stu_id=roll_no, sub_id=i, marks=56)
			db.session.add(mark1)
		db.session.commit()
		return "sub and marks added"
	modules = Module.query.all()
	return render_template('result.html', modules=modules)

	# var = Module.query.all()
	# l = []
	# for i in var:
	# 	l.append(i.module_id, i.module_name)
	# return jsonify(l)


