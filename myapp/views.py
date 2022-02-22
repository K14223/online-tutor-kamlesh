from django.shortcuts import render,redirect
from .models import Tutor,Student,Parent,Tutor_details,Contact,Add_batch,Fees_master,Student_request,Add_student_batch,Attendance,Upload_by_tutor,Content_by_student,Admin
import random
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse

import random
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse,HttpResponseRedirect 	
from django.core.files.storage import FileSystemStorage
from .utils import render_to_pdf
import os
from django.contrib.staticfiles import finders
from django.template.loader import render_to_string,get_template

import tempfile
from reportlab.pdfgen import canvas
from django.template import Context
from xhtml2pdf import pisa
from io import StringIO
import datetime 
# Create your views here.
def link_callback(uri, rel):
            """
            Convert HTML URIs to absolute system paths so xhtml2pdf can access those
            resources
            """
            result = finders.find(uri)
            if result:
                    if not isinstance(result, (list, tuple)):
                            result = [result]
                    result = list(os.path.realpath(path) for path in result)
                    path=result[0]
            else:
                    sUrl = settings.STATIC_URL        # Typically /static/
                    sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
                    mUrl = settings.MEDIA_URL         # Typically /media/
                    mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

                    if uri.startswith(mUrl):
                            path = os.path.join(mRoot, uri.replace(mUrl, ""))
                    elif uri.startswith(sUrl):
                            path = os.path.join(sRoot, uri.replace(sUrl, ""))
                    else:
                            return uri

            # make sure that file exists
            if not os.path.isfile(path):
                    raise Exception(
                            'media URI must start with %s or %s' % (sUrl, mUrl)
                    )
            return path
# def all_tutor_pdf(request):
	# if 'email' in request.session:
	# 	tutors=Tutor_details.objects.all()
	# 	return render(request,"all_tutor_pdf.html",{'tutors':tutors})
	# else:
	# 	return HttpResponseRedirect(reverse('login'))
	# =============================


	# tutors=Tutor_details.objects.all()
	# template=get_template("all_tutor_pdf.html")
	# context={'tutors':tutors}
	# html=template.render(context)
	# result=StringIO()
	#pdf=pisa.pisaDocument(StringIO(html),dest=result)
	
	


	# template_path = 'all_tutor_pdf.html'
	# context = {'tutors':tutors}
    # # Create a Django response object, and specify content_type as pdf
	# response = HttpResponse(content_type='application/pdf')
	# response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # # find the template and render it.
	# template = get_template(template_path)
	# html = template.render(context)
	# # if not pdf.err:
	# # 	return HttpResponse(result.getvalue(),content_type='application/pdf')
	# # else:
	# # 	return HttpResponse('Errors')
	# pisa_status = pisa.CreatePDF(
    #    html, dest=response, link_callback=link_callback)
    # # if error then show some funy view
	# if pisa_status.err:
	# 	return HttpResponse('We had some errors <pre>' + html + '</pre>')
	# return response
def index(request):
    return render(request,'index.html')

# def login(request):
#     return render(request,'login.html')
    

# def signup(request):
#     return render(request,'signup.html')
def about(request):
	return render(request,'about.html')

def contact(request):
		try:
			tutor=Tutor.objects.get(email=request.session['email'])
			if request.method=="POST":
				Contact.objects.create(
					name=request.POST['name'],
					email=request.POST['email'],
					mobile=request.POST['mobile'],
					feedback=request.POST['feedback']
					)
				msg="Contact Saved Successfully"
				return render(request,'tutor_contact.html',{'msg':msg})
			else:
				return render(request,'tutor_contact.html',{'tutor':tutor})
		except:
			try:
				student=Student.objects.get(email=request.session['email'])
				if request.method=="POST":
					Contact.objects.create(
						name=request.POST['name'],
						email=request.POST['email'],
						mobile=request.POST['mobile'],
						feedback=request.POST['feedback']
						)
					msg="Contact Saved Successfully"
					return render(request,'student_contact.html',{'msg':msg})
				else:
					return render(request,'student_contact.html',{'student':student})
			except:
				try:
					parent=Parent.objects.get(email=request.session['email'])
					if request.method=="POST":
						Contact.objects.create(
							name=request.POST['name'],
							email=request.POST['email'],
							mobile=request.POST['mobile'],
							feedback=request.POST['feedback']
							)
						msg="Contact Saved Successfully"
						return render(request,'parent_contact.html',{'msg':msg})
					else:
						return render(request,'parent_contact.html',{'parent':parent})
				except:
					if request.method=="POST":
						Contact.objects.create(
							name=request.POST['name'],
							email=request.POST['email'],
							mobile=request.POST['mobile'],
							feedback=request.POST['feedback']
						)
						msg="Contact Saved Successfully"
						return render(request,'contact.html',{'msg':msg})
					else:
						return render(request,'contact.html')

def signup(request):
	if request.method=="POST":
		f=request.POST['fname']
		l=request.POST['lname']
		e=request.POST['email']
		m=request.POST['mobile']
		p=request.POST['password']
		cp=request.POST['cpassword']
		ut=request.POST['usertype']
		ui=request.FILES['user_image']
		semail=request.POST['studentemail']
		if ut=="tutor":
			try:
				tutor=Tutor.objects.get(email=e)
				msg="Email Already Registered"
				return render(request,'signup.html',{'msg':msg})
			except:
				if p==cp:
					tid=Tutor.objects.create(fname=f,lname=l,email=e,mobile=m,password=p,cpassword=cp,usertype=ut,user_image=ui)
					rec=[e,]	
					subject="OTP For Successfully Registrations"
					otp=random.randint(1000,9999)
					message="Your OTP for Registration Is"+str(otp)
					email_from=settings.EMAIL_HOST_USER
					send_mail(subject,message,email_from,rec)
					msg="User Signup Successfully"
					print("-------------------> OTP",otp)
					return render(request, 'otp.html',{'otp':otp,'email':e,'ut':ut})
				else:
					msg="Password & Confirm Password Does Not Matched"
					return render(request,'signup.html',{'msg':msg})
		elif ut=="student":
			try:
				student=Student.objects.get(email=e)
				msg="Email Already Registered"
				return render(request,'signup.html',{'msg':msg})
			except:
				if p==cp:
					# tutor=Tutor.objects.get(pk=request.POST['tname'])tutor=tutor,
					Student.objects.create(fname=f,lname=l,email=e,mobile=m,password=p,cpassword=cp,usertype=ut,user_image=ui)
					rec=[e,]	
					subject="OTP For Successfully Registrations"
					otp=random.randint(1000,9999)
					message="Your OTP for Registration Is"+str(otp)
					email_from=settings.EMAIL_HOST_USER
					send_mail(subject,message,email_from,rec)
					msg="User Signup Successfully"
					
					return render(request, 'otp.html',{'otp':otp,'email':e,'ut':ut})


				else:
					msg="Password & Confirm Password Does Not Matched"
					return render(request,'signup.html',{'msg':msg})
		elif ut=="parent":
			try:
				parent=Parent.objects.get(email=e)
				msg="Email Already Registered"
				return render(request,'signup.html',{'msg':msg})
			except:
				if p==cp:
					Parent.objects.create(fname=f,lname=l,email=e,mobile=m,password=p,cpassword=cp,usertype=ut,user_image=ui,semail=semail)
					rec=[e,]	
					subject="OTP For Successfully Registrations"
					otp=random.randint(1000,9999)
					message="Your OTP for Registration Is"+str(otp)
					email_from=settings.EMAIL_HOST_USER
					send_mail(subject,message,email_from,rec)
					msg="User Signup Successfully"
					return render(request, 'otp.html',{'otp':otp,'email':e,'ut':ut})


				else:
					msg="Password & Confirm Password Does Not Matched"
					return render(request,'signup.html',{'msg':msg})
	else:
		tutors=Tutor.objects.all()
		return render(request,"signup.html",{'tutors':tutors})
def parent_index(request):
	parent=Parent.objects.filter(email=request.session['email'])
	print(parent)
	# student=Student.objects.filter(parent=parent)
	# print(student)
	# parent=Parent.object.filter(parent=parent)
	add_batch=Add_student_batch.objects.get(tutor=parent[0].tutor,student=parent[0].student)
	fees_master=Fees_master.objects.all()
	print(fees_master)
	print(add_batch.bnum)
	student_request=Student_request.objects.filter(student=parent[0].student)
	return render(request,'parent_index.html',{'parent':parent,'add_batch':add_batch,'student_request':student_request})
	
def login(request):
	if request.method=="POST":
		print("Login POST Method")
		ut=""
		e=request.POST['email']
		p=request.POST['password']
		try:
			ut=request.POST['usertype']
		except:
			msg="Please Select User Type"
			return render(request,'login.html',{'msg':msg})
		if ut=="tutor":

			try:
				tutor=Tutor.objects.get(email=e,password=p)
				if tutor.status=="active" and tutor.usertype=="tutor":
					request.session['fname']=tutor.fname
					request.session['email']=tutor.email
					request.session['tid']=tutor.id
					request.session['usertype']=tutor.usertype
					#print("-------------------------------------->",request.session.email)
					request.session['user_image']=tutor.user_image.url
					student_requests=Student_request.objects.filter(tutor=tutor,rstatus="Pending",pstatus="Pending")
					return render(request,'tutor_index.html',{'ut':ut,'student_requests':student_requests})
				else:
					pass

			except Exception as e:
				print("-------------------->e",e)
				msg="User Name or Pasword is Incorrect"
				return render(request,'login.html',{'msg':msg})
		elif ut=="student":
			try:
				student=Student.objects.get(email=e,password=p)
				if student.status=="active" and student.usertype=="student":
					request.session['fname']=student.fname
					request.session['email']=student.email
					request.session['usertype']=student.usertype
					request.session['tid']=student.id
					
					request.session['user_image']=student.user_image.url
					return render(request,'student_index.html')
				else:
					pass
			except Exception as e:
				print("--------------",e)
				msg="User Name or Pasword is Incorrect 123"
				return render(request,'login.html',{'msg':msg})
		elif ut=="parent":
			try:
				parent=Parent.objects.get(email=e,password=p)
				if parent.status=="active" and parent.usertype=="parent":
					request.session['fname']=parent.fname
					request.session['email']=parent.email
					request.session['usertype']=parent.usertype
					request.session['tid']=parent.id
					request.session['user_image']=parent.user_image.url
					return render(request,'parent_index.html',{'ut':ut})
				else:
					pass
			except Exception as e:
				print(e)
				msg="User Name or Pasword is Incorrect"
				return render(request,'login.html',{'msg':msg})
		else:
			pass

	else:
		print("Else Called")
		try:
			print("Try Called")
			if request.session['usertype']=="tutor":
				print("Session Found")
				return redirect('tutor_index')
		except Exception as e:
			print("E Tutor: ",e)
			try:
				if request.session['usertype']=="student":
					return redirect('student_index')
			except Exception as e:
				print("E Student: ",e)
				
				try:
					if request.session['usertype']=="parent":
						return redirect('parent_index')
				except Exception as e:
					print("E Parent: ",e)
					return render(request,'login.html')

def logout(request):
	try:
		del request.session['email']
		del request.session['fname']
		del request.session['tid']
		del request.session['usertype']
		del request.session['user_image']
		return render(request,'login.html')
	except:
		return render(request,'login.html')

def student_index(request):
	student=Student.objects.get(email=request.session['email'])
	student_request=Student_request.objects.filter(student=student)
	add_student_batchs=Add_student_batch.objects.filter(student=student)
	print(add_student_batchs)


	###
	add_student_batch=Add_student_batch.objects.filter(student=student)
	print(add_student_batch[0].bnum)
	
	upload_by_tutor=Upload_by_tutor.objects.filter(bnum=add_student_batch[0].bnum)
	print(upload_by_tutor)
	###


	return render(request,'student_index.html',{'student_request':student_request,'add_student_batchs':add_student_batchs})

def verify_otp(request):
	myvar=""
	otp=request.POST['otp']
	gotp=request.POST['gotp']
	email=request.POST['email']
	ut=request.POST['usertype']
	print(otp)
	print(gotp)
	print(email)
	print(ut)
	#if ut=="tutor":
	try:
		myvar=request.POST['myvar']
	except:
		pass
	if otp==gotp and myvar=="forgot_password" and ut=="tutor":
		return render(request,'enter_new_password.html',{'email':email,'ut':ut})
	elif otp==gotp and ut=="tutor":

		
		tutor=Tutor.objects.get(email=email)
		tutor.status="active"
		tutor.save()
		return render(request,'login.html')
	
	#elif ut=="student":
	try:
		myvar=request.POST['myvar']
	except:
		pass
	if otp==gotp and myvar=="forgot_password" and ut=="student":
		return render(request,'enter_new_password.html',{'email':email,'ut':ut})
	elif otp==gotp and ut=="student":
		student=Student.objects.get(email=email)
		student.status="active"
		student.save()
		return render(request,'login.html')
	
	try:
		myvar=request.POST['myvar']
	except:
		pass
	if otp==gotp and myvar=="forgot_password" and ut=="parent":
		return render(request,'enter_new_password.html',{'email':email,'ut':ut})
	elif otp==gotp  and ut=="parent":
		parent=Parent.objects.get(email=email)
		parent.status="active"
		parent.save()
		return render(request,'login.html')
	else:
		msg="Incorrect OTP..Try Again!!"
		return render(request,'otp.html',{'otp':gotp,'email':email,'msg':msg})


def otp(request):
    return render(request,'otp.html')



def forgot_password(request):
    if request.method=="POST":

        email=request.POST['email']
        npassword=request.POST['npassword']
        cnpassword=request.POST['cnpassword']
        ut=request.POST['usertype']
        if ut=="tutor":
	        tutor=Tutor.objects.get(email=email)
	        if npassword==cnpassword:
	           tutor.password=npassword 
	           tutor.cpassword=npassword
	           tutor.save()
	           return render(request,'login.html',{'ut':ut})
	        else:
	        	msg="New Password & Confirm New Password Does Not Match"
	        	return render(request,'enter_new_password.html',{'msg':msg,'email':email,'ut':ut})
        elif ut=="student":
	        student=Student.objects.get(email=email)
	        if npassword==cnpassword:
	           student.password=npassword 
	           student.cpassword=npassword
	           student.save()
	           return render(request,'login.html',{'ut':ut})
	        else:
	            msg="New Password & Confirm New Password Does Not Match"
	            return render(request,'enter_new_password.html',{'msg':msg,'email':email,'ut':ut})
        elif ut=="parent":
	        parent=Parent.objects.get(email=email)
	        if npassword==cnpassword:
	           parent.password=npassword 
	           parent.cpassword=npassword
	           parent.save()
	           return render(request,'login.html',{'ut':ut})
	        else:
	            msg="New Password & Confirm New Password Does Not Match"
	            return render(request,'enter_new_password.html',{'msg':msg,'email':email,'ut':ut})
    else:
        return render(request,'enter_email.html')


def enter_email(request):
	print("Enter_Email Called")
	if request.method=="POST":
		email=request.POST['email']
		ut=request.POST['usertype']
		print(email)
		print(ut)
		if ut=="tutor":
			try:
				print("try called")
				tutor=Tutor.objects.get(email=email)
				if tutor.status=="inactive":
					rec=[email,]	
					subject="OTP For Activate your Account."
					otp=random.randint(1000,9999)
					message="Your OTP for Activations Is"+str(otp)
					email_from=settings.EMAIL_HOST_USER
					send_mail(subject, message, email_from, rec)				
					msg="User Signup Successfully"
					
					return render(request, 'otp.html',{'email':email,'ut':ut,'otp':otp})
				elif tutor.status=="active":
					print("active")
					rec=[email,]	
					subject="OTP For Forgot Password."
					otp=random.randint(1000,9999)
					message="Your OTP for Forgot Password Is"+str(otp)
					email_from=settings.EMAIL_HOST_USER
					send_mail(subject, message, email_from, rec)				
					myvar="forgot_password"
					
					return render(request, 'otp.html',{'email':email,'ut':ut,'otp':otp,'myvar':myvar})
			except Exception as e:
				
				msg="Email is not registered with us."
				return render(request,'enter_email.html',{'msg':msg})
		elif ut=="student":
			try:
				student=Student.objects.get(email=email)
				if student.status=="inactive" :
					rec=[email,]	
					subject="OTP For Activate your Account."
					otp=random.randint(1000,9999)
					message="Your OTP for Activations Is"+str(otp)
					email_from=settings.EMAIL_HOST_USER
					send_mail(subject, message, email_from, rec)				
					msg="User Signup Successfully"
					
					return render(request, 'otp.html',{'email':email,'ut':ut,'otp':otp})
				elif student.status=="active" :
					rec=[email,]	
					subject="OTP For Forgot Password."
					otp=random.randint(1000,9999)
					message="Your OTP for Forgot Password Is"+str(otp)
					email_from=settings.EMAIL_HOST_USER
					send_mail(subject, message, email_from, rec)				
					myvar="forgot_password"
					
					return render(request, 'otp.html',{'email':email,'ut':ut,'otp':otp,'myvar':myvar})
			except:
				msg="Email is not registered with us."
				return render(request,'enter_email.html',{'msg':msg})
		elif ut=="parent":
			try:
				parent=Parent.objects.get(email=email)
				if parent.status=="inactive" :
					rec=[email,]	
					subject="OTP For Activate your Account."
					otp=random.randint(1000,9999)
					message="Your OTP for Activations Is"+str(otp)
					email_from=settings.EMAIL_HOST_USER
					send_mail(subject, message, email_from, rec)				
					msg="User Signup Successfully"
					
					return render(request, 'otp.html',{'email':email,'ut':ut,'otp':otp,'myvar':myvar})
				elif parent.status=="active" :
					rec=[email,]	
					subject="OTP For Forgot Password."
					otp=random.randint(1000,9999)
					message="Your OTP for Forgot Password Is"+str(otp)
					email_from=settings.EMAIL_HOST_USER
					send_mail(subject, message, email_from, rec)				
					myvar="forgot_password"
					return render(request, 'otp.html',{'email':email,'ut':ut,'otp':otp,'myvar':myvar})
			except:
				msg="Email is not registered with us."
				return render(request,'enter_email.html',{'msg':msg})

def enter_email_page(request):
	return render(request,'enter_email.html')

def tutor_change_password(request):
    if request.method=="POST":
        opassword=request.POST['opassword']
        npassword=request.POST['npassword']
        cnpassword=request.POST['cnpassword']

        tutor=Tutor.objects.get(email=request.session['email'])

        if tutor.password==opassword:
            if npassword==cnpassword:
                tutor.password=npassword
                tutor.cpassword=npassword
                tutor.save()
                return redirect('logout')
            else:
                msg="New password and confirm New password does not Matched"
                return render(request,'tutor_change_password.html',{'msg':msg})
        else:
            msg="Old Password Does not Matched"
            return render(request,'tutor_change_password.html',{'msg':msg})
    else:
        return render(request,'tutor_change_password.html')

def student_change_password(request):
	print("----------------------")
	if request.method=="POST":
		opassword=request.POST['opassword']
		npassword=request.POST['npassword']
		cnpassword=request.POST['cnpassword']
		student=Student.objects.get(email=request.session['email'])

		if student.password==opassword:
			if npassword==cnpassword:
				student.password=npassword
				student.cpassword=npassword
				student.save()
				return redirect('logout')
			else:
				msg="New password and confirm New password does not Matched"
				return render(request,'student_change_password.html',{'msg':msg})
		else:
			msg="Old Password Does not Matched"
			return render(request,'student_change_password.html',{'msg':msg})
	else:
		return render(request,'student_change_password.html')

def parent_change_password(request):
	if request.method=="POST":
		opassword=request.POST['opassword']
		npassword=request.POST['npassword']
		cnpassword=request.POST['cnpassword']

		tutor=Tutor.objects.get(email=request.session['email'])

		if tutor.password==opassword:
			if npassword==cnpassword:
				parent.password=npassword
				parent.cpassword=npassword
				parent.save()
				return redirect('logout')
			else:
				msg="New password and confirm New password does not Matched"
				return render(request,'parent_change_password.html',{'msg':msg})
		else:
			msg="Old Password Does not Matched"
			return render(request,'parent_change_password.html',{'msg':msg})
	else:
		return render(request,'parent_change_password.html')


def tutor_details(request):
	tutor=Tutor.objects.get(email=request.session['email'])
	if request.method=="POST":
		# print(pk)
		if request.POST['submit']=="edit":
			print("Edit Called")
			# print(pk)
			tutor_detail=Tutor_details.objects.get(tutor=tutor)
			tutor_detail.tname=request.POST['tname']
			tutor_detail.cname=request.POST['cname']
			tutor_detail.address=request.POST['address']
			tutor_detail.subject_details=request.POST['subject_details']
			tutor_detail.qualification_details=request.POST['qualification_details']
			tutor_detail.extra_details=request.POST['extra_details']
			try:
				tutor_detail.identity_proof=request.FILES['identity_proof']
				tutor_detail.save()
				return render(request,'tutor_details.html',{'msg':msg,'tutor_detail':tutor_detail})
			except:
				tutor_detail.save()
				msg="Details Updated Successfully!!"
				return render(request,'tutor_details.html',{'msg':msg,'tutor_detail':tutor_detail})
		elif request.POST['submit']=="submit":
			print("Hello")
			tutor_detail=Tutor_details.objects.create(tutor=tutor,tname=request.POST['tname'],cname=request.POST['cname'],address=request.POST['address'],subject_details=request.POST['subject_details'],qualification_details=request.POST['qualification_details'],extra_details=request.POST['extra_details'],identity_proof=request.FILES['identity_proof'])
		
			msg="Details Uploaded Successfully!!"
			return render(request,'tutor_details.html',{'msg':msg,'tutor_detail':tutor_detail})
		else:
			pass
	else:
		tutor_detail=Tutor_details()
		msg=""
		tutor=Tutor.objects.get(email=request.session['email'])
		print(tutor.fname)
		try:
			tutor_detail=Tutor_details.objects.get(tutor=tutor)
			print("TNAME : ",tutor_detail.tname)
		except Exception as e:
			print("Except : ",e)
		if not tutor_detail:
			msg="Details in Pending...Please check!!"
		else:
			pass
		print("Done")
		return render(request,'tutor_details.html',{'msg':msg,'tutor_detail':tutor_detail})

def student_details(request):
	if request.method=="POST":
		sn=request.POST['sname']
		fn=request.POST['fname']
		mn=request.POST['mname']
		scn=request.POST['scname']
		address=request.POST['address']
		idp=request.FILES['identity_proof']
		Student_details.objects.create(sname=sn,fname=fn,mname=mn,scname=scn,address=address,identity_proof=idp)
		msg="Details Uploaded Successfully!!"
		return render(request,'student_details.html',{'msg':msg})
	else:
		msg="Details in Pending...Please check!!"
		return render(request,'student_details.html',{'msg':msg})



def header(request):
    return render(request,'header.html')

def tutor_index(request):
	tutor=Tutor.objects.get(email=request.session['email'])
	print(tutor)
	student_request=Student_request.objects.filter(tutor=tutor)
	print(student_request)
	return render(request,'tutor_index.html',{'student_request':student_request})

def index_3(request):
    return render(request,'index-3.html')

# def change_password(request):
# 	return render(request,'change_password.html')

# def all_tutor(request):
# 	all_tutor=Tutor.objects.all()
# 	return render(request,'all_tutor.html',{'all_tutor':all_tutor})

def all_tutor(request):
	tutor_list=[]
	tutors=Tutor.objects.all()
	for i in tutors:
		tutor_detail=Tutor_details.objects.get(tutor=i)
		tutor_list.append(tutor_detail)
	print(tutor_list)
	return render(request,'all_tutor.html',{'tutors':tutors,'tutor_list':tutor_list})

def parent_all_tutor(request):
	tutor_list=[]
	tutors=Tutor.objects.all()
	for i in tutors:
		tutor_detail=Tutor_details.objects.get(tutor=i)
		tutor_list.append(tutor_detail)
	print(tutor_list)
	return render(request,'parent_all_tutor.html',{'tutors':tutors,'tutor_list':tutor_list})

def view_tutor_details(request,pk):
	print("pk--------:",pk)
	# tutor=Tutor.objects.get(pk=pk)
	tutor_detail=Tutor_details.objects.get(pk=pk)
	return render(request,'view_tutor_details.html',{'tutor_detail':tutor_detail})

def parent_view_tutor_details(request,pk):
	tutor=Tutor.objects.get(pk=pk)
	tutor_detail=Tutor_details.objects.get(tutor=tutor)
	return render(request,'parent_view_tutor_details.html',{'tutor_detail':tutor_detail})


def visitor_all_tutor(request):
	tutor_list=[]
	tutors=Tutor.objects.all()
	for i in tutors:
		tutor_detail=Tutor_details.objects.get(tutor=i)
		tutor_list.append(tutor_detail)
	print(tutor_list)
	return render(request,'visitor_all_tutor.html',{'tutors':tutors,'tutor_list':tutor_list})


def feesdetails(request):
	return render(request,'feesdetails.html')

def payfees(request):
	return render(request,'payfees.html')

# def attendance(request):
# 	return render(request,'attendance.html')

def student_attendance(request):

	return render(request,'student_attendance.html')

def parent_attendance_show(request):
	return render(request,'parent_attendance_show.html')


def add_batch(request):
	return render(request,'add_batch.html')

def tutor_profile(request):
	tutor=Tutor.objects.get(email=request.session['email'])
	if request.method=="POST":
		tutor.fname=request.POST['fname']
		tutor.lname=request.POST['lname']
		tutor.email=request.POST['email']
		tutor.mobile=request.POST['mobile']
		tutor.save()
		msg="Profile Updated successfully"
		return render(request,"tutor_profile.html",{'msg':msg})
	else:
		return render(request,"tutor_profile.html",{'tutor':tutor})

def student_profile(request):
	student=Student.objects.get(email=request.session['email'])
	if request.method=="POST":
		student.fname=request.POST['fname']
		student.lname=request.POST['lname']
		student.email=request.POST['email']
		student.mobile=request.POST['mobile']
		student.save()
		msg="Profile Updated successfully"
		return render(request,"student_profile.html",{'msg':msg})
	else:
		return render(request,"student_profile.html",{'student':student})
# def view_tutor_details(request):
# 	return render(request,'view_tutor_details.html')

# def add_batch(request):
	# tutor=Tutor.objects.get(email=request.session['email'])
	# if request.method=="POST":
	# 	add_batch=Add_batch.objects.get(tutor=tutor)
	# 	add_batch.bnum=request.POST['bnum']
	# 	add_batch.bname=request.POST['bname']
	# 	add_batch.bsubject=request.POST['bsuject']
	# 	add_batch.bday=request.POST['bday']
	# 	add_batch.btime=request.POST['btime']
	# 	add_batch.bdetail=request.POST['bdetail']
	# 	add_batch.save()
	# 	msg="Batch Created successfully"
	# 	return render(request,"add_batch.html",{'msg':msg})
	# else:


def edit_batch(request):
	# tutor=Tutor.objects.get(email=request.session['email'])
	
	# if request.method=="POST":
	# 	add_batch=Add_batch.objects.get(tutor=tutor)
	# 	add_batch.bnum=request.POST['bnum']
	# 	add_batch.bname=request.POST['bname']
	# 	add_batch.bsubject=request.POST['bsuject']
	# 	add_batch.bday=request.POST['bday']
	# 	add_batch.btime=request.POST['btime']
	# 	add_batch.bdetail=request.POST['bdetail']
	# 	add_batch.save()
	# 	msg="Batch Details Updated successfully"
		return render(request,"edit_batch.html")

def attendance(request):
	# students=Student.objects.all()
	tutor=Tutor.objects.get(email=request.session['email'])
	
	add_student_batch=Add_batch.objects.filter(tutor=tutor)
	
	add_student_in_batch=Add_student_batch.objects.filter(tutor=tutor,bnum=request.POST['bnum'])
	time=add_student_in_batch[0].btime
	print(add_student_in_batch)
	return render(request,"attendance.html",{'add_batchs':add_student_batch,'add_student_in_batch':add_student_in_batch,'time':time})

def add_batch(request):
	
	tutor=Tutor.objects.get(email=request.session['email'])
	tutor_details=Tutor_details.objects.get(tutor=tutor)
	subjects=tutor_details.subject_details.split(",")
	print(subjects)
	if request.method=="POST":
		#add_batch=Add_batch.objects.get(tutor=tutor)
		bnum=request.POST['bnum']
		bname=request.POST['bname']
		bsubject=request.POST['bsubject']
		bdate=request.POST['bdate']
		btime=request.POST['btime']
		bday=request.POST['bday']
		bdetail=request.POST['bdetail']
		Add_batch.objects.create(bnum=bnum,bname=bname,bsubject=bsubject,bdate=bdate,btime=btime,bday=bday,bdetail=bdetail,tutor=tutor)
		msg="Batch Added Successfully!!"
		return render(request,'add_batch.html',{'msg':msg})
	else:
		msg="Details in Pending...Please check!!"
		return render(request,'add_batch.html',{'msg':msg,'tutor_details':tutor_details,'subjects':subjects})


def view_batch_by_tutor(request):
	tutor=Tutor.objects.get(email=request.session['email'])
	add_batchs=Add_batch.objects.filter(tutor=tutor)
	print("--------My Batch------")
	msg="Batch Deleted Successfully"
	return render(request,"view_batch_by_tutor.html",{'add_batchs':add_batchs,'msg':msg})

def batch_display(request):
	tutor=Tutor.objects.get(email=request.session['email'])
	add_batchs=Add_batch.objects.filter(tutor=tutor)
	return render(request,"batch_display.html",{'add_batchs':add_batchs})

def my_students_tutor(request):
	tutor=Tutor.objects.get(email=request.session['email'])
	# students=Student.objects.filter(tutor=tutor)
	student_request=Student_request.objects.filter(tutor=tutor,rstatus="Complete")
	return render(request,'my_students_tutor.html',{'student_request':student_request})


def all_student_fees(request):
	tutor=Tutor.objects.get(email=request.session['email'])
	students=Student.objects.filter(tutor=tutor)
	return render(request,'all_student_fees.html',{'students':students})

def all_student_in_my_batch(request,pk):
	print("Pk ::::::::: ",pk)
	tutor=Tutor.objects.get(email=request.session['email'])
	all_student_in_batch=Add_student_batch.objects.filter(tutor=tutor,bnum=pk)
	print(all_student_in_batch)
	students=Student.objects.filter(tutor=tutor)
	return render(request,'all_student_in_my_batch.html',{'students':students,'all_student_in_batch':all_student_in_batch})


def all_student_by_tutor(request):
	students=Student.objects.all()
	return render(request,'all_student_by_tutor.html',{'students':students})


def apply_for_new_course(request):
		return render(request,'apply_for_new_course.html')

def enroll(request,pk):
	# student=Student.objects.get(pk=pk)
	tutor_detail=Tutor_details.objects.get(pk=pk)
	print(type(tutor_detail.subject_details))
	sd=tutor_detail.subject_details.split(",")
	total=len(sd)
	msg="Your Request haave been sent to the selected tutor. wait for the Response! "
	return render(request,'enroll.html',{'tutor_detail':tutor_detail,'sd':sd,'total':total+3})

def enroll_student(request):
	print("Enroll Student Called")
	if request.method=="POST":
		subject_name=request.POST['subject']
		print(subject_name)
		print(type(subject_name))
		tutor_id=request.POST['tutor_id']
		tutor=Tutor.objects.get(pk=tutor_id)
		student_id=request.POST['student_id']
		student=Student.objects.get(pk=student_id)
		Student_request.objects.create(subject_name=subject_name,tutor=tutor,student=student)
		msg="Your Request has been send successfully"
		return render(request,'enroll_student.html',{'msg':msg})
	else:
		msg="Please Select Subject"
		return render(request,'enroll_student.html',{'msg':msg})
	
def selected_student_batch(request,pk):
	add_batch=Add_batch.objects.all()
	student_request=Student_request.objects.get(pk=pk)
	return render(request,'selected_student_batch.html',{'add_batch':add_batch,'student_request':student_request})

def complete_add(request):
	# Student_request=Student_request.objects.all()
	if request.method=="POST":
		bnum=request.POST['bnum']
		bdate=request.POST['bdate']
		btime=request.POST['btime']
		fname=request.POST['fname']
		lname=request.POST['lname']
		mobile=request.POST['mobile']
		email=request.POST['email']
		tutor_id=request.POST['tutor_id']
		
		student_id=request.POST['student_id']
		tutor=Tutor.objects.get(pk=tutor_id)
		student=Student.objects.get(pk=student_id)
		all_batch=Add_student_batch.objects.all()
		flag=True
		for i in all_batch:
			if i.student==student:
				msg="Student Already In Batch"
				return render(request,'complete_add.html',{'msg':msg})
		else:
			Add_student_batch.objects.create(bnum=bnum,bdate=bdate,btime=btime,fname=fname,lname=lname,mobile=mobile,email=email,tutor=tutor,student=student)
			return render(request,'complete_add.html')
		
			

	
	else:
		return render(request,'complete_add.html')

def delete_batch(request,pk):
	add_batch=Add_batch.objects.get(pk=pk)
	add_batch.delete()
	return render(request,'view_batch_by_tutor.html',{'msg':msg})




def complete_attendance(request):

	if request.method=="POST":
		tutor=Tutor.objects.get(email=request.session['email'])
		bnum=request.POST['bnum']
		add_batch=Add_batch.objects.get(bnum=bnum)
		date=request.POST['adate']
		present=request.POST.getlist('Present')
		absent=request.POST.getlist('Absent')
		for i in present:
			sid=int(i)
			student=Student.objects.get(id=sid)
			Attendance.objects.create(tutor=tutor,student=student,add_batch=add_batch,astatus="Present",datetime=date)
		for i in absent:
			sid=int(i)
			student=Student.objects.get(id=sid)
			Attendance.objects.create(tutor=tutor,student=student,add_batch=add_batch,astatus="Absent",datetime=date)
		return render(request,'complete_attendance.html')
	else:
		return render(request,'attendance.html')


def view_attendnce_tutor(request):
	attendance=Attendance.objects.all()
	return render(request,'view_attendnce_tutor.html',{'attendance':attendance})

def view_attendance_by_tutor(request):
	add_batch=Add_batch.objects.all()
	return render(request,'view_attendance_by_tutor.html',{'add_batch':add_batch})


def view_attendance_student(request):
	student=Student.objects.get(email=request.session['email'])
	attendance=Attendance.objects.filter(student=student)
	return render(request,'view_attendance_student.html',{'attendance':attendance})



def upload_content_tutor(request):
	add_batch=Add_batch.objects.all()
	tutor=Tutor.objects.get(email=request.session['email'])
	upload_content_tutor=Upload_by_tutor.objects.filter(tutor=tutor)
	if request.method=="POST":
		
		filename=request.FILES['filename']
		bnum=request.POST['bnum']
		# add_batch=Add_batch.objects.get(bnum=bnum)
		# tuto=Tutor.objects.get(id)
		Upload_by_tutor.objects.create(tutor=tutor,filename=filename,bnum=bnum)
		return render(request,'upload_content_tutor.html')
	else:
		return render(request,'upload_content_tutor.html',{'add_batch':add_batch,'upload_content_tutor':upload_content_tutor})

	return render(request,'upload_content_tutor.html',{'add_batch':add_batch,'upload_content_tutor':upload_content_tutor})

def upload_content_student(request):
	student=Student.objects.get(email=request.session['email'])
	attendance=Attendance.objects.filter(student=student)
	upload_content_student=Content_by_student.objects.filter(student=student)
	print("-----------------------------------",upload_content_student)
	if request.method=="POST":
		print("TID : ",request.POST['tid'])
		
		tutor=Tutor.objects.get(id=request.POST['tid'])
		attendance=Attendance.objects.get(student=student,tutor=tutor)
		# add_batch=Add_batch.objects.get(tutor=tutor,student=student)
		# print(attendance)
		fname=request.FILES['fname']
		date=request.POST['date']
		print("------------------------",tutor)
		Content_by_student.objects.create(tutor=tutor,student=student,fname=fname,date=date)
		
		return render(request,'upload_content_student.html',{'upload_content_student':upload_content_student})
	else:
		return render(request,'upload_content_student.html',{'attendance':attendance,'upload_content_student':upload_content_student})
	return render(request,'upload_content_student.html',{'attendance':attendance,'upload_content_student':upload_content_student})


def view_content_student(request):
	student=Student.objects.get(email=request.session['email'])
	add_student_batch=Add_student_batch.objects.get(student=student)
	# print(add_student_batch[0].bnum)
	upload_by_tutor=Upload_by_tutor.objects.filter(bnum=add_student_batch.bnum)
	bnum=upload_by_tutor[0].bnum
	add_batch=Add_batch.objects.get(bnum=bnum)
	subject=add_batch.bsubject
	# print(upload_by_tutor)
	return render(request,'view_content_student.html',{'add_student_batch':add_student_batch,'upload_by_tutor':upload_by_tutor,'subject':subject})

def batch_report(request):
	tutor=Tutor.objects.get(email=request.session['email'])
	if request.method=="POST":
		filter_name=request.POST['filter_name']
		search=request.POST['search']
		if filter_name=="bname":
			all_batch=Add_batch.objects.filter(tutor=tutor,bname=search)
			return render(request,'batch_report.html',{'all_batch':all_batch})
		elif filter_name=="bnum":
			all_batch=Add_batch.objects.filter(tutor=tutor,bnum=search)
			return render(request,'batch_report.html',{'all_batch':all_batch})
		elif filter_name=="bsubject":
			all_batch=Add_batch.objects.filter(tutor=tutor,bsubject=search)
			return render(request,'batch_report.html',{'all_batch':all_batch})
	else:

		
		all_batch=Add_batch.objects.filter(tutor=tutor)
		return render(request,'batch_report.html',{'all_batch':all_batch})

def batch_report_pdf(request):
	
	tutor=Tutor.objects.get(email=request.session['email'])
	if request.POST['action'] == "search":
	
		tutor=Tutor.objects.get(email=request.session['email'])
		if request.method=="POST":
			filter_name=request.POST['filter_name']
			search=request.POST['search']
			request.session['searchname']=search
			request.session['filtername']=filter_name

			print("=================> search value store ",search)
			if filter_name=="bname":
				all_batch=Add_batch.objects.filter(tutor=tutor,bname=search)
				return render(request,'batch_report.html',{'all_batch':all_batch})
			elif filter_name=="bnum":
				all_batch=Add_batch.objects.filter(tutor=tutor,bnum=search)
				return render(request,'batch_report.html',{'all_batch':all_batch})
			elif filter_name=="bsubject":
				all_batch=Add_batch.objects.filter(tutor=tutor,bsubject=search)
				return render(request,'batch_report.html',{'all_batch':all_batch})
		else:

			all_batch=Add_batch.objects.filter(tutor=tutor)
			return render(request,'batch_report.html',{'all_batch':all_batch})

	
	elif request.POST['action'] == 'export':
		print("--------------->export button click")
		tutor=Tutor.objects.get(email=request.session['email'])
		if request.method=="POST":
			
			
			if "searchname" in request.session:
				search=request.session['searchname']
				filter_name=request.session['filtername']
				print("=================> search value store ",search)

				if filter_name=="bname":
					all_batch=Add_batch.objects.filter(tutor=tutor,bname=search)
					context = {'all_batch':all_batch}
					print("------------>> value pdf ")
					
					template_path = 'batch_report_pdf.html'
					all_batch=Add_batch.objects.filter(tutor=tutor,bnum=search)
					context = {'all_batch':all_batch}
					# Create a Django response object, and specify content_type as pdf
					response = HttpResponse(content_type='application/pdf')
					response['Content-Disposition'] = 'attachment; filename="report.pdf"'
					# find the template and render it.
					template = get_template(template_path)
					html = template.render(context)
					print("-----?> creating report ")
					
					del request.session['searchname']
					del request.session['filtername']
					# if not pdf.err:
					# 	return HttpResponse(result.getvalue(),content_type='application/pdf')
					# else:
					# 	return HttpResponse('Errors')
					pisa_status = pisa.CreatePDF(
					html, dest=response, link_callback=link_callback)
					# if error then show some funy view
					if pisa_status.err:
						return HttpResponse('We had some errors <pre>' + html + '</pre>')
					return response


				elif filter_name=="bnum":
					all_batch=Add_batch.objects.filter(tutor=tutor,bnum=search)
					context = {'all_batch':all_batch}
					print("------------->>>> export pdf number wise ")
					# return render(request,'batch_report.html',{'all_batch':all_batch})
					
					template_path = 'batch_report_pdf.html'
					all_batch=Add_batch.objects.filter(tutor=tutor,bnum=search)
					context = {'all_batch':all_batch}
					# Create a Django response object, and specify content_type as pdf
					response = HttpResponse(content_type='application/pdf')
					response['Content-Disposition'] = 'attachment; filename="report.pdf"'
					# find the template and render it.
					template = get_template(template_path)
					html = template.render(context)
					print("-----?> creating report ")
					
					del request.session['searchname']
					del request.session['filtername']
					# if not pdf.err:
					# 	return HttpResponse(result.getvalue(),content_type='application/pdf')
					# else:
					# 	return HttpResponse('Errors')
					pisa_status = pisa.CreatePDF(
					html, dest=response, link_callback=link_callback)
					# if error then show some funy view
					if pisa_status.err:
						return HttpResponse('We had some errors <pre>' + html + '</pre>')
					return response
			else:
				all_batch=Add_batch.objects.all()	
				template_path = 'batch_report_pdf.html'
				context = {'all_batch':all_batch}
				# Create a Django response object, and specify content_type as pdf
				response = HttpResponse(content_type='application/pdf')
				response['Content-Disposition'] = 'attachment; filename="report.pdf"'
				# find the template and render it.
				template = get_template(template_path)
				html = template.render(context)
				# if not pdf.err:
				# 	return HttpResponse(result.getvalue(),content_type='application/pdf')
				# else:
				# 	return HttpResponse('Errors')
				pisa_status = pisa.CreatePDF(
				html, dest=response, link_callback=link_callback)
				# if error then show some funy view
				if pisa_status.err:
					return HttpResponse('We had some errors <pre>' + html + '</pre>')
				return response		
		else:
			all_batch=Add_batch.objects.filter(tutor=tutor)
			context = {'all_batch':all_batch}
			print("---->>> else part of export ")
			return render(request,'batch_report.html',{'all_batch':all_batch})

		print("------------>> outside the if .. else")
		all_batch=Add_batch.objects.all()	
		template_path = 'batch_report_pdf.html'
		context = {'all_batch':all_batch}
		# Create a Django response object, and specify content_type as pdf
		response = HttpResponse(content_type='application/pdf')
		response['Content-Disposition'] = 'attachment; filename="report.pdf"'
		# find the template and render it.
		template = get_template(template_path)
		html = template.render(context)
		# if not pdf.err:
		# 	return HttpResponse(result.getvalue(),content_type='application/pdf')
		# else:
		# 	return HttpResponse('Errors')
		pisa_status = pisa.CreatePDF(
		html, dest=response, link_callback=link_callback)
		# if error then show some funy view
		if pisa_status.err:
			return HttpResponse('We had some errors <pre>' + html + '</pre>')
		return response
	else:
		all_batch=Add_batch.objects.filter(tutor=tutor)
		context = {'all_batch':all_batch}
		
		del request.session['searchname']
		del request.session['filtername']
		return render(request,'batch_report.html',{'all_batch':all_batch})


def tutor_attendance_report(request):
	tutor=Tutor.objects.get(email=request.session['email'])
	attendance=Attendance.objects.filter(tutor=tutor)
	if request.method=="POST":
		if request.POST['action']=="search":
			filter_name=request.POST['filter_name']
			search=request.POST['search']
			attendance=[]
			if filter_name=="date":
				t1=Attendance.objects.filter(date=search,tutor=tutor)
				return render(request,'tutor_attendance_report.html',{'attendance':t1})
			elif filter_name=="present":
				tutor=Tutor.objects.get(email=request.session['email'])
				t1=Attendance.objects.filter(present=search,tutor=tutor)
				return render(request,'tutor_attendance_report.html',{'attendance':t1})
			elif filter_name=="absent":
				# tutors=Tutor.objects.get(fname=search)
				t1=Attendance.objects.filter(absent=search)
				return render(request,'tutor_attendance_report.html',{'attendance':t1})
	else:
		return render(request,'tutor_attendance_report.html',{'attendance':attendance})
	return render(request,'tutor_attendance_report.html',{'attendance':attendance})


def student_view_my_tutor(request):
	student=Student.objects.get(email=request.session['email'])
	add_student_batch=Add_student_batch.objects.filter(student=student)
	return render(request,'student_view_my_tutor.html',{'add_student_batch':add_student_batch})


def student_batch_report(request):
	student=Student.objects.get(email=request.session['email'])
	add_student_batch=Add_student_batch.objects.filter(student=student)
	# print("------------------",add_student_batch[0].bnum)
	# upload_by_tutor=Upload_by_tutor.objects.filter(bnum=add_student_batch.bnum)
	# bnum=upload_by_tutor[0].bnum
	# add_batch=Add_batch.objects.get(bnum=bnum)
	# subject=add_batch.bsubject
	# print(upload_by_tutor)
	if request.method=="POST":
		if request.POST['action']=="search":
			filter_name=request.POST['filter_name']
			search=request.POST['search']
			attendance=[]
			if filter_name=="bnum":
				t1=Add_student_batch.objects.filter(bnum=search,student=student)
				return render(request,'student_batch_report.html',{'add_student_batch':t1})
			elif filter_name=="btime":
				t1=Add_student_batch.objects.filter(btime=search,student=student)
				return render(request,'student_batch_report.html',{'add_student_batch':t1})
			elif filter_name=="fname":
				tutor=Tutor.objects.get(fname=search)
				print("--================================>",tutor)
				t1=Add_student_batch.objects.filter(tutor=tutor,student=student)
				return render(request,'student_batch_report.html',{'add_student_batch':t1})
	else:
		return render(request,'student_batch_report.html',{'add_student_batch':add_student_batch})
	

	# return render(request,'student_batch_report.html',{'add_student_batch':add_student_batch,'upload_by_tutor':upload_by_tutor,'subject':subject})
	
def student_attendance_report(request):
	student=Student.objects.get(email=request.session['email'])
	attendance=Attendance.objects.filter(student=student)
	print("------------------------>",attendance)
	if request.method=="POST":
		if request.POST['action']=="search":
			filter_name=request.POST['filter_name']
			search=request.POST['search']
			student_attendance_report=[]
			if filter_name=="bnum":
				add_batch=Add_batch.objects.get(bnum=search)
				print("------------------------------Add Batch",add_batch)
				t1=Attendance.objects.filter(add_batch=add_batch,student=student)
				print("t1-------------------------------------->",t1)
				return render(request,'student_attendance_report.html',{'attendance':t1})
			elif filter_name=="datetime":
				# student=Student.objects.get(fname=search)
				t1=Attendance.objects.filter(datetime=search,student=student)
				return render(request,'student_attendance_report.html',{'attendance':t1})
			elif filter_name=="astatus":
				# student=Student.objects.get(lname=search)
				t1=Attendance.objects.filter(astatus=search,student=student)
				return render(request,'student_attendance_report.html',{'attendance':t1})
			elif filter_name=="astatus":
				# student=Student.objects.get(lname=search)
				t1=Attendance.objects.filter(astatus=search,student=student)
				return render(request,'student_attendance_report.html',{'attendance':t1})
	else:
		return render(request,'student_attendance_report.html',{'attendance':attendance})
	

def student_view_content_report(request):
	student=Student.objects.get(email=request.session['email'])
	add_student_batch=Add_student_batch.objects.get(student=student)
	# print(add_student_batch[0].bnum)
	upload_by_tutor=Upload_by_tutor.objects.filter(bnum=add_student_batch.bnum)
	bnum=upload_by_tutor[0].bnum
	add_batch=Add_batch.objects.get(bnum=bnum)
	subject=add_batch.bsubject
	# print(upload_by_tutor)
	return render(request,'student_view_content_report.html',{'add_student_batch':add_student_batch,'upload_by_tutor':upload_by_tutor,'subject':subject})
	

def parent_fees_recipt(request):
	return render(request,'parent_fees_recipt.html')

def parent_pay_fees(request):
	return render(request,'parent_pay_fees.html')

def parent_batch_report(request):
	parent=Parent.objects.get(email=request.session['email'])
	student=Student.objects.filter(parent=parent)
	print("------------------------------------>",student)
	add_student_batch=Add_student_batch.objects.filter(student=parent.student)
	print("------------------------------------>",add_student_batch)
	if request.method=="POST":
		if request.POST['action']=="search":
			filter_name=request.POST['filter_name']
			search=request.POST['search']
			student=[]
			if filter_name=="bnum":
				# add_batch=Add_batch.objects.get(bnum=search)
				t1=Add_student_batch.objects.filter(bnum=search,student=parent.student)
				return render(request,'parent_batch_report.html',{'add_student_batch':t1})
			elif filter_name=="btime":
				t1=Add_student_batch.objects.filter(btime=search,student=parent.student)
				return render(request,'parent_batch_report.html',{'add_student_batch':t1})
			elif filter_name=="fname":
				tutor=Tutor.objects.get(fname=search)
				print("------------------------------>")
				t1=Add_student_batch.objects.filter(tutor=tutor,student=parent.student)
				return render(request,'parent_batch_report.html',{'add_student_batch':t1})
	else:
		return render(request,'parent_batch_report.html',{'add_student_batch':add_student_batch})
	

def parent_attendance_report(request):
	parent=Parent.objects.get(email=request.session['email'])
	print("-------------------------------------->",parent)
	student=Student.objects.filter(parent=parent)
	print("------------------------------------>",student)
	attendance=Attendance.objects.filter(student=parent.student)
	if request.method=="POST":
		if request.POST['action']=="search":
			filter_name=request.POST['filter_name']
			search=request.POST['search']
			student=[]
			if filter_name=="bnum":
				add_batch=Add_batch.objects.get(bnum=search)
				t1=Attendance.objects.filter(add_batch=add_batch,student=parent.student)
				return render(request,'parent_attendance_report.html',{'attendance':t1})
			elif filter_name=="datetime":
				t1=Attendance.objects.filter(datetime=search)
				return render(request,'parent_attendance_report.html',{'attendance':t1})
			elif filter_name=="astatus":
				t1=Attendance.objects.filter(astatus=search,student=parent.student)
				return render(request,'parent_attendance_report.html',{'attendance':t1})
			elif filter_name=="astatus":
				t1=Attendance.objects.filter(astatus=search,student=parent.student)
				return render(request,'parent_attendance_report.html',{'attendance':t1})
			elif filter_name=="fname":
				tutor=Tutor.objects.get(fname=search)
				print("---------------------------------------------",tutor)
				t1=Attendance.objects.filter(tutor=tutor,student=parent.student)
				return render(request,'parent_attendance_report.html',{'attendance':t1})
	else:
		return render(request,'parent_attendance_report.html',{'attendance':attendance})

def parent_all_tutor_report(request):
	tutors=Tutor_details.objects.all()
	if request.method=="POST":
		if request.POST['action']=="search":
			filter_name=request.POST['filter_name']
			search=request.POST['search']
			student=[]
			if filter_name=="fname":
				tutor=Tutor.objects.get(fname=search)
				print("---------------------------------------------",tutor)
				t1=Tutor_details.objects.filter(tutor=tutor)
				print("---------------------------------------------",t1)
				return render(request,'parent_all_tutor_report.html',{'tutors':t1})
			elif filter_name=="lname":
				tutor=Tutor.objects.get(lname=search)
				t1=Tutor_details.objects.filter(tutor=tutor)
				return render(request,'parent_all_tutor_report.html',{'tutors':t1})
			elif filter_name=="address":
				t1=Tutor_details.objects.filter(address=search)
				return render(request,'parent_all_tutor_report.html',{'tutors':t1})
			elif filter_name=="subject_details":
				t1=Tutor_details.objects.filter(subject_details=search)
				return render(request,'parent_all_tutor_report.html',{'tutors':t1})
	else:
		return render(request,'parent_all_tutor_report.html',{'tutors':tutors})
	

def view_content_by_tutor(request):
	tutor=Tutor.objects.get(email=request.session['email'])
	add_batch=Add_batch.objects.filter(tutor=tutor)
	bnum=add_batch[0].bnum
	bsubject=add_batch[0].bsubject
	bname=add_batch[0].bname
	content_by_student=Content_by_student.objects.filter(tutor=tutor)
	return render(request,'view_content_by_tutor.html',{'content_by_student':content_by_student,'bnum':bnum,'bsubject':bsubject,'bname':bname})

def manage_fees_tutor(request):
	tutor=Tutor.objects.get(email=request.session['email'])
	tutor_detail=Tutor_details.objects.get(tutor=tutor)
	sd=tutor_detail.subject_details.split(",")
	print(sd)
	if request.method=="POST":
		print("POST CALLED")
		fees_value=request.POST.getlist('fees_value')
		tutor_name=request.POST['tname']
		subject_details=request.POST['subject']
		print("tutor Name-----------------",tutor_name)
		print("Fees : ----------------------------------",fees_value)
		tutor_id=request.POST['tutor_id']

		print("Tutor_ID : ---------",tutor_id)
		tutor=Tutor_details.objects.get(pk=tutor_id)
		Fees_master.objects.create(fees_value=fees_value,tutor_detail=tutor,tutor_name=tutor_name,subject_details=subject_details)
		msg="Fees Updated SuccessFully"
		return render(request,'manage_fees_tutor.html',{'tutor_detail':tutor_detail,'sd':sd,'msg':msg})
	else:
		
		return render(request,'manage_fees_tutor.html',{'tutor_detail':tutor_detail,'sd':sd})
	
def admin_login(request):
	if request.method=="POST":
		e=request.POST['email']
		p=request.POST['password']
		print("Admin Email----------",e)
		print("Admin Email----------",p)
		try:
			admin=Admin.objects.get(email=e,password=p)
			print("Admin---------------------->",admin)
			request.session['fname']=admin.fname
			request.session['email']=admin.email
			request.session['user_image']=admin.user_image.url
			return render(request,'admin_index.html')
		except Exception as e:
			print("-------------------->e",e)
			msg="User Name or Pasword is Incorrect"
			return render(request,'admin_login.html',{'msg':msg})
	else:
		return render(request,'admin_login.html')

def admin_logout(request):
	try:
		del request.session['email']
		del request.session['fname']
		del request.session['user_image']
		return render(request,'admin_login.html')
	except:
		return render(request,'admin_login.html')

def admin_header(request):
	return render(request,'admin_header.html')

def admin_index(request):
	return render(request,'admin_index.html')


def admin_tutor(request):
	tutor_detail=Tutor_details.objects.all()
	return render(request,'admin_tutor.html',{'tutor_detail':tutor_detail})

def admin_student(request):
	student=Student.objects.all()
	return render(request,'admin_student.html',{'student':student})

def admin_parent(request):
	parent=Parent.objects.all()
	return render(request,'admin_parent.html',{'parent':parent})

def admin_tutor_detail(request,pk):
	tutor_detail=Tutor_details.objects.get(pk=pk)
	print(tutor_detail)
	return render(request,'admin_tutor_detail.html',{'admin_tutor_detail':admin_tutor_detail,'tutor_detail':tutor_detail})

def admin_tutor_info(request,pk):
	tutor_detail=Tutor_details.objects.get(pk=pk)
	add_batch=Add_batch.objects.filter(tutor=tutor_detail.tutor)
	print(add_batch)
	return render(request,'admin_tutor_info.html',{'tutor_detail':tutor_detail,'add_batch':add_batch})

def admin_batch_info(request,bnum):
	print("batch Number-----------------------------",bnum)
	add_batch=Add_batch.objects.get(bnum=bnum)
	print("Add Batch Object:",add_batch)
	add_student_batch=Add_student_batch.objects.filter(bnum=bnum)
	print("All Student Batch-------------------",add_batch)
	return render(request,'admin_batch_info.html',{'add_batch':add_batch,'add_student_batch':add_student_batch})

def admin_student_detail(request,pk):
	print(pk)
	student=Student.objects.get(pk=pk)
	parent=Parent.objects.get(student=student)
	return render(request,'admin_student_detail.html',{'parent':parent,'student':student})


def admin_student_info(request,pk):
	print(pk)
	student=Student.objects.get(pk=pk)
	parent=Parent.objects.get(student=student)
	tutor=Tutor.objects.get(pk=parent.tutor.pk)
	ab=Add_batch.objects.filter(tutor=tutor)
	add_batch=ab[0]
	return render(request,'admin_student_info.html',{'student':student,'parent':parent,'tutor':tutor,'add_batch':add_batch})

def admin_parent_detail(request,pk):
	print(pk)
	parent=Parent.objects.get(pk=pk)
	# student=Student.objects.get(pk=pk)
	print("Student Objects:--------------------->",pk)
	# parent=Parent.objects.get(student=student),{'parent':parent,'student':student}
	return render(request,'admin_parent_detail.html',{'parent':parent})

def admin_parent_info(request,pk):
	print(pk)
	parent=Parent.objects.get(pk=pk)
	student=Student.objects.get(parent=parent)
	return render(request,'admin_parent_info.html',{'parent':parent,'student':student})

def admin_tutor_report(request):
	tutors=Tutor_details.objects.all()
	if request.method=="POST":
		if request.POST['action']=="search":
			filter_name=request.POST['filter_name']
			search=request.POST['search']
			tutors=[]
			if filter_name=="fname":
				t1=Tutor.objects.filter(fname=search)
				for i in t1:
					t=Tutor_details.objects.get(tutor=i)
					tutors.append(t)
				return render(request,'admin_tutor_report.html',{'tutors':tutors})
			elif filter_name=="lname":
				t1=Tutor.objects.filter(lname=search)
				for i in t1:
					t=Tutor_details.objects.get(tutor=i)
					tutors.append(t)
				return render(request,'admin_tutor_report.html',{'tutors':tutors})
		elif request.POST['action']=="export":
			filter_name=request.POST['filter_name']
			search=request.POST['search']
			tutors=[]
			if filter_name=="fname":
				t1=Tutor.objects.filter(fname=search)
				for i in t1:
					t=Tutor_details.objects.get(tutor=i)
					tutors.append(t)
				return render(request,'admin_tutor_report.html',{'tutors':tutors})
			template_path = 'admin_tutor_report_pdf.html'
			context = {'tutors': 'tutors'}
			response = HttpResponse(content_type='application/pdf')
			response['Content-Disposition'] = 'attachment; filename="Tutor.pdf"'
			template = get_template(template_path)
			html = template.render(context)
			pisa_status = pisa.CreatePDF(
			html, dest=response, link_callback=link_callback)
			if pisa_status.err:
				return HttpResponse('We had some errors <pre>' + html + '</pre>')
			return response
	else:
		return render(request,'admin_tutor_report.html',{'tutors':tutors})

def admin_student_report(request):
	students=Student.objects.all()
	if request.method=="POST":
		if request.POST['action']=="search":
			filter_name=request.POST['filter_name']
			search=request.POST['search']
			student=[]
			if filter_name=="fname":
				t1=Student.objects.filter(fname=search)
				return render(request,'admin_student_report.html',{'students':t1})
			elif filter_name=="lname":
				t1=Student.objects.filter(lname=search)
				return render(request,'admin_student_report.html',{'students':t1})
			elif filter_name=="tname":
				tutors=Tutor.objects.get(fname=search)
				t1=Student.objects.filter(tutor=tutors)
				return render(request,'admin_student_report.html',{'students':t1})
	else:
		return render(request,'admin_student_report.html',{'students':students})


def admin_parent_report(request):
	parent=Parent.objects.all()
	if request.method=="POST":
		if request.POST['action']=="search":
			filter_name=request.POST['filter_name']
			search=request.POST['search']
			parent=[]
			if filter_name=="fname":
				t1=Parent.objects.filter(fname=search)
				return render(request,'admin_parent_report.html',{'parent':t1})
			elif filter_name=="lname":
				t1=Parent.objects.filter(lname=search)
				return render(request,'admin_parent_report.html',{'parent':t1})
			elif filter_name=="tname":
				tutors=Tutor.objects.get(fname=search)
				t1=Parent.objects.filter(tutor=tutors)
				return render(request,'admin_parent_report.html',{'parent':t1})
	else:
		return render(request,'admin_parent_report.html',{'parent':parent})

def admin_batch_report(request):
	all_batch=Add_batch.objects.all()
	#return render(request,'admin_batch_report.html',{'batch':batch})
	if request.method=="POST":
		filter_name=request.POST['filter_name']
		search=request.POST['search']

		if filter_name=="bname":
			all_batch=Add_batch.objects.filter(bname=search)
			return render(request,'admin_batch_report.html',{'all_batch':all_batch})
		elif filter_name=="bnum":
			all_batch=Add_batch.objects.filter(bnum=search)
			return render(request,'admin_batch_report.html',{'all_batch':all_batch})
		elif filter_name=="bsubject":
			all_batch=Add_batch.objects.filter(bsubject=search)
			return render(request,'admin_batch_report.html',{'all_batch':all_batch})
		elif filter_name=="btime":
			all_batch=Add_batch.objects.filter(btime=search)
			return render(request,'admin_batch_report.html',{'all_batch':all_batch})
		elif filter_name=="fname":
			tutor=Tutor.objects.get(fname=search)
			all_batch=Add_batch.objects.filter(tutor=tutor)
			return render(request,'admin_batch_report.html',{'all_batch':all_batch})

	else:	
		# all_batch=Add_batch.objects.filter(tutor=tutor)
		return render(request,'admin_batch_report.html',{'all_batch':all_batch})

def admin_attendance_report(request):
	all_batch=Add_batch.objects.all()
	#return render(request,'admin_batch_report.html',{'batch':batch})
	if request.method=="POST":
		filter_name=request.POST['filter_name']
		search=request.POST['search']

		if filter_name=="bname":
			all_batch=Add_batch.objects.filter(bname=search)
			return render(request,'admin_attendance_report.html',{'all_batch':all_batch})
		elif filter_name=="bnum":
			all_batch=Add_batch.objects.filter(bnum=search)
			return render(request,'admin_attendance_report.html',{'all_batch':all_batch})
		elif filter_name=="bsubject":
			all_batch=Add_batch.objects.filter(bsubject=search)
			return render(request,'admin_attendance_report.html',{'all_batch':all_batch})
		elif filter_name=="btime":
			all_batch=Add_batch.objects.filter(btime=search)
			return render(request,'admin_attendance_report.html',{'all_batch':all_batch})
		elif filter_name=="fname":
			tutor=Tutor.objects.get(fname=search)
			all_batch=Add_batch.objects.filter(tutor=tutor)
			return render(request,'admin_attendance_report.html',{'all_batch':all_batch})

	else:	
		# all_batch=Add_batch.objects.filter(tutor=tutor)
		return render(request,'admin_attendance_report.html',{'all_batch':all_batch})


def admin_attendance_click(request,pk):
	add_batch=Add_batch.objects.get(pk=pk)
	attendance=Attendance.objects.filter(add_batch=add_batch)
	if request.method=="POST":
		filter_name=request.POST['filter_name']
		search=request.POST['search']

		if filter_name=="all":
			attendance=Attendance.objects.filter(add_batch=add_batch)
			return render(request,'admin_attendance_click.html',{'attendance':attendance})
		elif filter_name=="present":
			attendance=Attendance.objects.filter(present=search)
			return render(request,'admin_attendance_click.html',{'attendance':attendance})
		elif filter_name=="absent":
			attendance=Attendance.objects.filter(absent=search)
			return render(request,'admin_attendance_click.html',{'attendance':attendance})
		elif filter_name=="datetime":
			attendance=Attendance.objects.filter(datetime=search)
			return render(request,'admin_attendance_click.html',{'attendance':attendance})
		elif filter_name=="month":
			all_batch=Add_batch.objects.filter(month=month)
			return render(request,'admin_attendance_click.html',{'attendance':attendance})

	else:	
		# all_batch=Add_batch.objects.filter(tutor=tutor)
		return render(request,'admin_attendance_click.html',{'attendance':attendance})
	
def admin_attendance_click_pdf(request):
	# add_batch=Add_batch.objects.all()
	attendance=Attendance.objects.all()
	if request.method=="POST":
		filter_name=request.POST['filter_name']
		search=request.POST['search']
		print("search : ",search)
		if filter_name=="all":
			attendance=Attendance.objects.all()
			return render(request,'admin_attendance_click.html',{'attendance':attendance})
		elif filter_name=="astatus":
			attendance=Attendance.objects.filter(astatus=search)
			return render(request,'admin_attendance_click.html',{'attendance':attendance})
		
		elif filter_name=="datetime":
			attendance=Attendance.objects.filter(datetime=search)
			datee=datetime.datetime.strptime(attendance[0].datetime,"%Y-%m-%d")
			print(datee.month)
			return render(request,'admin_attendance_click.html',{'attendance':attendance})
		elif filter_name=="month":
			attendance_list=[]
			#all_batch=Add_batch.objects.filter(month=month)
			attendance1=Attendance.objects.all()
			j=0
			for i in attendance1:
				datee=datetime.datetime.strptime(attendance1[j].datetime,"%Y-%m-%d")
				print("--------------------->",datee.month)
				if str(datee.month)==search:
					print("match found")
					attendance_list.append(i)
				j=j+1
			
			print(attendance_list)
			return render(request,'admin_attendance_click.html',{'attendance':attendance_list})
	else:	
		return render(request,'admin_attendance_click.html',{'attendance':attendance})

def tutor_student_report(request):
	tutor=Tutor.objects.get(email=request.session['email'])
	add_student_batch=Add_student_batch.objects.filter(tutor=tutor)
	if request.method=="POST":
		if request.POST['action']=="search":
			filter_name=request.POST['filter_name']
			search=request.POST['search']
			add_student_batch=[]
			if filter_name=="bnum":
				t1=Add_student_batch.objects.filter(bnum=search)
				return render(request,'tutor_student_report.html',{'add_student_batch':t1})
			elif filter_name=="fname":
				student=Student.objects.get(fname=search)
				t1=Add_student_batch.objects.filter(student=student)
				return render(request,'tutor_student_report.html',{'add_student_batch':t1})
			elif filter_name=="lname":
				student=Student.objects.get(lname=search)
				t1=Add_student_batch.objects.filter(student=student)
				return render(request,'tutor_student_report.html',{'add_student_batch':t1})
	else:
		return render(request,'tutor_student_report.html',{'add_student_batch':add_student_batch})
	

def tutor_student_report_click(request):
	tutor=Tutor.objects.get(email=request.session['email'])
	
	attendance=Attendance.objects.filter(tutor=tutor)
	print("---------------------->",attendance)
	return render(request,'tutor_student_report_click.html',{'attendance':attendance})