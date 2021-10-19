from result import db


class Student(db.Model):
    roll_no = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=True)
    mark = db.relationship('Mark', backref='student', lazy=True)


class Module(db.Model):
	module_id = db.Column(db.Integer, primary_key=True)
	module_name = db.Column(db.String(20), nullable=False)
	module = db.relationship('Mark', backref='module', lazy=True)


class Mark(db.Model):
	mark_id = db.Column(db.Integer, primary_key=True)
	stu_id = db.Column(db.Integer, db.ForeignKey('student.roll_no'), nullable=False)
	sub_id = db.Column(db.Integer, db.ForeignKey('module.module_id'), nullable=False)
	marks = db.Column(db.Integer, nullable=True, default=0)


