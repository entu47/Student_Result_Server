from flask import render_template, url_for, flash, redirect, request, Blueprint
from result import db
from result.models import Student, Module, Mark
admin = Blueprint('admin', __name__)

@admin.route('/add_student', methods=['GET', 'POST'])
def add_result():
	if request.method == 'POST':
		roll_no = request.form.get('roll_no')
		name = request.form.get('name')
		email = request.form.get('email')
		student = Student(roll_no=roll_no, name=name, email=email)
		db.session.add(student)
		db.session.commit()
	return render_template('student_register.html')

@admin.route('/add_module', methods=['GET', 'POST'])
def add_module():
	if request.method == 'POST':
		module_id = request.form.get('module_id')
		module_name = request.form.get('module_name')
		module = Module(module_id=module_id, module_name=module_name)
		db.session.add(module)
		db.session.commit()
	return render_template('module_register.html')
