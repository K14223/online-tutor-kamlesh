from django.contrib import admin
from .models import Tutor,Student,Parent,Tutor_details,Contact,Add_batch,Fees_master,Student_request,Add_student_batch,Attendance,Upload_by_tutor,Content_by_student,Admin
# Register your models here.

class Customizations(admin.ModelAdmin):
	list_display=('fname','lname','mobile','email','usertype','user_image')
	list_editable=('mobile','user_image')
	list_per_page=5
	search_fields=('fname',)
	list_filter=('lname','email')
	list_per_page=5


class CustomizationsDetails(admin.ModelAdmin):
	list_display=('tname','cname','subject_details','identity_proof')
	list_editable=('identity_proof','cname')
	search_fields=('subject_details',)
	list_filter=('subject_details',)
	list_per_page=5

class AttendanceDetail(admin.ModelAdmin):
	list_display=('student','astatus','datetime')
	search_fields=('fname',)
	list_filter=('astatus',)
	list_per_page=5
class Add_student_batch_cstm(admin.ModelAdmin):
	list_display=('fname','lname','tutor','bnum','bdate','btime')
	list_filter=('btime','bdate')
	search_fields=('bnum','btime')
	list_per_page=5

class Add_batch_cstm(admin.ModelAdmin):
	list_display=('bname','tutor','bnum','bsubject','bdate','bday','btime')
	list_filter=('tutor','bdate',)
	search_fields=('tutor','bsubject',)
	list_per_page=5

class Contact_cstm(admin.ModelAdmin):
	list_display=('name','email','mobile')
	list_filter=('name',)
	search_fields=('name','email',)
	list_per_page=5

class Student_request_cstm(admin.ModelAdmin):
	list_display=('student','tutor','rstatus','pstatus','subject_name')
	list_filter=('pstatus','rstatus','subject_name',)
	search_fields=('student','tutor','subject_name',)
	list_per_page=5


class FeesMastert_cstm(admin.ModelAdmin):
	list_display=('tutor_name','subject_details','fees_value',)
	search_fields=('tutor_detail',)
	list_per_page=5


admin.site.register(Tutor,Customizations)
admin.site.register(Student,Customizations)
admin.site.register(Parent,Customizations)
admin.site.register(Tutor_details,CustomizationsDetails)
admin.site.register(Contact,Contact_cstm)
admin.site.register(Add_batch,Add_batch_cstm)
admin.site.register(Fees_master,FeesMastert_cstm)
admin.site.register(Student_request,Student_request_cstm)
admin.site.register(Add_student_batch,Add_student_batch_cstm)
admin.site.register(Attendance,AttendanceDetail)
admin.site.register(Upload_by_tutor)
admin.site.register(Content_by_student)
admin.site.register(Admin)