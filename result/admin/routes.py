from flask import render_template, flash, redirect, request, Blueprint
from result import db
from result.models import Student, Module, Mark
admin = Blueprint('admin', __name__, template_folder="templates")


@admin.route('/admin', methods=['GET'])
def get_admin():
    return render_template('admin/home.html')


@admin.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        roll_no = request.form.get('roll_no')
        name = request.form.get('name')
        email = request.form.get('email')
        student1 = Student.query.filter_by(roll_no=roll_no).first()
        student2 = Student.query.filter_by(email=email).first()
        if student1 or student2:
            flash('Email or Roll_No Already Taken', 'danger')
            return redirect('/add_student')
        student = Student(roll_no=roll_no, name=name, email=email)
        db.session.add(student)
        db.session.commit()
        flash('Student Added Successfully', 'success')
        return redirect('/admin')
    return render_template('admin/student_register.html')


@admin.route('/add_module', methods=['GET', 'POST'])
def add_module():
    if request.method == 'POST':
        module_id = request.form.get('module_id')
        module_name = request.form.get('module_name')
        module1 = Module.query.filter_by(module_id=module_id).first()
        if module1:
            flash('Module_Id Already Taken ', 'danger')
            return redirect('/add_module')
        module = Module(module_id=module_id, module_name=module_name)
        db.session.add(module)
        db.session.commit()
        flash('Module Added Successfully', 'success')
        return redirect('/admin')
    return render_template('admin/module_register.html')


@admin.route('/update_marks', methods=['GET', 'POST'])
def update_marks():
    if request.method == 'POST':
        roll_no = request.form.get('roll_no')
        mark1 = Mark.query.filter_by(stu_id=roll_no)
        mark2 = Mark.query.filter_by(stu_id=roll_no).first()
        if mark2 is None:
            flash('please enter valid roll_no', 'danger')
            return redirect('/update_marks')
        else:
            return render_template('admin/marks.html', marks=mark1,
                                   roll_no=roll_no)
    return render_template('admin/enter_detail.html')


@admin.route('/save_marks/<int:roll_no>', methods=['POST'])
def save_marks(roll_no):
    if request.method == 'POST':
        marks = Mark.query.filter_by(stu_id=roll_no)
        for mark in marks:
            mark.marks = request.form.get(str(mark.mark_id))
        db.session.commit()
    flash('Marks Updated Successfully', 'success')
    return redirect('/admin')
