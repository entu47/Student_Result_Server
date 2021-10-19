from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify
from result.models import Mark, Student, Module
from result import db
student = Blueprint('student', __name__)

@student.route('/get_result', methods = ['GET', 'POST'])
def get_result():
	if request.method == 'POST':
		roll_no = request.form.get('roll_no')
		var1 = Mark.query.filter_by(stu_id=roll_no)
		d = {}

		for i in var1:
			d[str(i.module.module_name)] = i.marks
		return d
	return render_template('result_ac.html')
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


