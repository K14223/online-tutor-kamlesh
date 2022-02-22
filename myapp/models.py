from django.db import models

# Create your models here.
class Tutor(models.Model):
	fname=models.CharField(max_length=100)
	lname=models.CharField(max_length=100)
	email=models.CharField(max_length=100)
	mobile=models.CharField(max_length=100)
	password=models.CharField(max_length=100)
	cpassword=models.CharField(max_length=100)
	usertype=models.CharField(max_length=100)
	user_image=models.ImageField(upload_to='images/')
	status=models.CharField(max_length=100,default="inactive")
	def __str__(self):
		return self.fname

class Student(models.Model):
	tutor=models.ForeignKey(Tutor,on_delete=models.CASCADE,blank=True,null=True)
	fname=models.CharField(max_length=100)
	lname=models.CharField(max_length=100)
	email=models.CharField(max_length=100)
	mobile=models.CharField(max_length=100)
	password=models.CharField(max_length=100)
	cpassword=models.CharField(max_length=100)
	usertype=models.CharField(max_length=100)
	user_image=models.ImageField(upload_to='images/')
	status=models.CharField(max_length=100,default="inactive")
	def __str__(self):
		return self.fname

class Parent(models.Model):
	
	student=models.ForeignKey(Student,on_delete=models.CASCADE,blank=True,null=True,default="")
	tutor=models.ForeignKey(Tutor,on_delete=models.CASCADE,blank=True,null=True,default="")
	fname=models.CharField(max_length=100)
	lname=models.CharField(max_length=100)
	email=models.CharField(max_length=100)
	mobile=models.CharField(max_length=100)
	password=models.CharField(max_length=100)
	cpassword=models.CharField(max_length=100)
	usertype=models.CharField(max_length=100)
	user_image=models.ImageField(upload_to='images/')
	status=models.CharField(max_length=100,default="inactive")
	semail=models.CharField(max_length=100,default="",blank=True,null=True)
	def __str__(self):
		return self.fname

class Tutor_details(models.Model):
	tutor=models.ForeignKey(Tutor,on_delete=models.CASCADE)
	tname=models.CharField(max_length=100)
	cname=models.CharField(max_length=100)
	subject_details=models.TextField()
	address=models.TextField()
	identity_proof=models.FileField(upload_to='id_proof/')
	qualification_details=models.TextField()
	extra_details=models.TextField()
	def _str_(self):
		return self.tname

class Contact(models.Model):
	name=models.CharField(max_length=100)
	email=models.CharField(max_length=100)
	mobile=models.CharField(max_length=100)
	feedback=models.TextField()
	def __str__(self):
		return self.name


class Student_Contact(models.Model):
	name=models.CharField(max_length=100)
	email=models.CharField(max_length=100)
	mobile=models.CharField(max_length=100)
	feedback=models.TextField()
	def __str__(self):
		return self.name

class Parent_Contact(models.Model):
	name=models.CharField(max_length=100)
	email=models.CharField(max_length=100)
	mobile=models.CharField(max_length=100)
	feedback=models.TextField()
	def __str__(self):
		return self.name


class Add_batch(models.Model):
	tutor=models.ForeignKey(Tutor,on_delete=models.CASCADE)
	bnum=models.CharField(max_length=100)
	bname=models.CharField(max_length=100)
	bsubject=models.CharField(max_length=100)
	bdate=models.CharField(max_length=100)
	btime=models.CharField(max_length=100)
	bday=models.CharField(max_length=100)
	bdetail=models.CharField(max_length=100)
	def __str__(self):
		return self.bname


class Fees_master(models.Model):
	tutor_detail=models.ForeignKey(Tutor_details,on_delete=models.CASCADE,blank=True,null=True,default="")
	fees_value=models.CharField(max_length=100,blank=True,null=True,default="")
	tutor_name=models.CharField(max_length=100,default="",blank=True,null=True)
	subject_details=models.CharField(max_length=100,default="",blank=True,null=True)
	def __str__(self):
		return self.tutor_detail.tname+" "+self.tutor_detail.tutor.lname


class Student_request(models.Model):
	fees_master=models.ForeignKey(Fees_master,on_delete=models.CASCADE, blank=True,null=True)
	tutor=models.ForeignKey(Tutor,on_delete=models.CASCADE, blank=True,null=True)
	student=models.ForeignKey(Student,on_delete=models.CASCADE, blank=True,null=True)
	rstatus=models.CharField(max_length=100,default="pending")
	pstatus=models.CharField(max_length=100,default="Pending")
	subject_name=models.CharField(max_length=100)
	def __str__(self):
		return self.student.fname



class Add_student_batch(models.Model):
	
	tutor=models.ForeignKey(Tutor,on_delete=models.CASCADE)
	student=models.ForeignKey(Student,on_delete=models.CASCADE)
	# add_batch=models.ForeignKey(Add_batch,on_delete=models.CASCADE)
	bnum=models.CharField(max_length=100,default="")
	bdate=models.CharField(max_length=100)
	btime=models.CharField(max_length=100)
	fname=models.CharField(max_length=100)
	lname=models.CharField(max_length=100)
	email=models.CharField(max_length=100)
	mobile=models.CharField(max_length=100)

class Attendance(models.Model):
	tutor=models.ForeignKey(Tutor,on_delete=models.CASCADE)
	student=models.ForeignKey(Student,on_delete=models.CASCADE)
	add_batch=models.ForeignKey(Add_batch,on_delete=models.CASCADE)
	astatus=models.CharField(max_length=100,default="Absent")
	datetime=models.CharField(max_length=100)


class Upload_by_tutor(models.Model):
	tutor=models.ForeignKey(Tutor,on_delete=models.CASCADE)
	bnum=models.CharField(max_length=100)
	filename=models.FileField(upload_to='tutor_doc/')

class Content_by_student(models.Model):
	student=models.ForeignKey(Student,on_delete=models.CASCADE)
	tutor=models.ForeignKey(Tutor,on_delete=models.CASCADE,null=True,blank=True)
	date=models.CharField(max_length=100,null=True,blank=True,default="")
	fname=models.FileField(upload_to='student_doc/')


class Admin(models.Model):
	fname=models.CharField(max_length=100)
	lname=models.CharField(max_length=100)
	email=models.CharField(max_length=100)
	mobile=models.CharField(max_length=100)
	password=models.CharField(max_length=100)
	cpassword=models.CharField(max_length=100)
	user_image=models.ImageField(upload_to='images/')
	def __str__(self):
		return self.fname