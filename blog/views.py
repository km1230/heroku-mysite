from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Post, Comment
from .form import PostForm, CommentForm, Registration, UserAccount, UserProfile
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


"""
Font page of blog
"""
def blogindex(request):
	post_list = list(reversed(Post.objects.order_by('time')))
	for post in post_list:
		post.title = '🔖 ' + post.title
	p = Paginator(post_list, 5)
	page = request.GET.get('page')
	posts = p.get_page(page)
	return render(request, 'blog.html', {'posts': posts})

def post_tag(request, key):
	post_list = [p for p in Post.objects.all().order_by('time') if key in p.tag]
	post_list = list(reversed(post_list))
	for post in post_list:
		post.title = '🔖 ' + post.title
	p = Paginator(post_list, 5)
	page = request.GET.get('page')
	posts = p.get_page(page)
	return render(request, 'blog.html', {'posts': posts})

"""
Register
"""
def register(request):
	if request.user.is_authenticated:
		return blogindex(request)

	if request.method == "POST":
		form = Registration(request.POST)
		if form.is_valid():
			checkfault, errorcode = form.check_email()
			
			if checkfault == False:
				user = form.save()
				username = request.POST.get('username')			#to collect 'username' & 'password' from form method=POST
				password = request.POST.get('password1')
				user = auth.authenticate(username=username, password=password)		#auth.authenicate() hv 2 attrib, username & password
				auth.login(request, user)
				title = "registration"						#auth.login()
				return sendmail(request, title=title)
			else:
				return render(request, 'registration/registration.html', {'form':form, 'errorcode':errorcode})

		else:
			form = Registration()
			errorcode = 'There is something wrong about your information!'
			return render(request, 'registration/registration.html', {'form': form, 'errorcode': errorcode})
	else:
		form = Registration()
		return render(request, 'registration/registration.html', {'form': form})


"""
My Login page that redirecting to blogindex()

def loginpage(request):

	if request.user.is_authenticated:
		return blogindex(request)					#redirect() can be urls name

	if request.method == "POST":
		username = request.POST.get('username')			#to collect 'username' & 'password' from form method=POST
		password = request.POST.get('password')
		user = auth.authenticate(username=username, password=password)		#auth.authenicate() hv 2 attrib, username & password

		if user:

			if user.is_active:
				auth.login(request, user)
				loginstatus = True						#auth.login()
				return blogindex(request)
			else:
				loginstatus = False
				return render(request, 'registration/login.html', {'loginstatus': loginstatus})
		else:
			loginstatus = False
			return render(request, 'registration/login.html', {'loginstatus': loginstatus})
	else:
		loginstatus = None
		return render(request, 'registration/login.html', {'loginstatus': loginstatus})
"""


"""
Logout function
"""
@login_required
def logout(request):
	auth.logout(request)
	return blogindex(request)


"""
Change Password Done
"""
@login_required
def changepassworddone(request):
	status = request.user.is_authenticated
	title = 'changepassword'
	sendmail(request, title=title)
	return render(request, 'registration/password_change_done.html')


"""
MyAccount
"""
@login_required
def useraccount(request):
	status = request.user.is_authenticated
	if request.method == "POST":
		form = UserAccount(request.POST, instance=request.user)
		profile_form = UserProfile(request.POST, instance=request.user.profile)
		if form.is_valid() and profile_form.is_valid():
			form.save()
			profile_form.save()
			return blogindex(request)
		else:
			form = UserAccount(instance=request.user)
			profile_form = UserProfile(instance=request.user.profile)
			error = 'There is something wrong about your information!'
			return render(request, 'registration/myaccount.html', {'form':form, 'profile_form':profile_form, 'error':error})
	else:
		form = UserAccount(instance=request.user)
		profile_form = UserProfile(instance=request.user.profile)
		return render(request, 'registration/myaccount.html', {'form':form, 'profile_form':profile_form})
		

"""
Post details
"""
def post_page(request, key):
	post = Post.objects.get(pk=key)
	post.title = "🔖 " + post.title
	error = ''
	if request.user.is_authenticated:
		if request.method == "POST":
			temp = CommentForm(request.POST)
			if temp.is_valid():
				content = temp.change_content()
				form = temp.save(commit=False)
				form.content = content
				print('form.content: '+form.content)
				form.parent_post = post
				form.author = request.user
				form.save()
				form = CommentForm()
			else:
				form = CommentForm()
				error = 'There is something wrong of your comment content!'
		else:
			form = CommentForm()
	else:
		form = ''
	comment = list(reversed(Comment.objects.filter(parent_post=post).order_by('time')))
	return render(request, 'post.html', {'post': post, 'comment': comment, 'form':form, 'error':error})


"""
Archives
"""
def archives(request):
	post_list = list(reversed(Post.objects.order_by('time')))
	p = Paginator(post_list, 20)
	page = request.GET.get('page')
	posts = p.get_page(page)
	return render(request, 'archives.html', {'posts':posts})


"""
Add new post
"""
@login_required
def post_new(request):
	if request.user != User.objects.get(username='admin'):
		return blogindex(request)

	if request.method == "POST":
		temp = PostForm(request.POST)     #request.POST to collect data from forms
		if temp.is_valid():
			content = temp.change_content()
			postform = temp.save(commit=False)
			postform.content = content
			postform.author = User.objects.get(username='admin')
			postform.save()							#as long as the ModelForm is used to associate models to forms, save() can be used
			return blogindex(request)
		else: 
			postform = PostForm()
			
	else:
		postform = PostForm()
	return render(request, 'post_new.html', {'form':postform})

"""
Sending Email
"""
def sendmail(request, title):
	if title == "registration":
		email_title = 'Kavie Blog - Confirmation of Registration'
		email_content = render_to_string('registration/registration_email.html', {'username': request.user.username})

	elif title == "changepassword":
		email_title = 'Kavie Blog - Password Changed'
		email_content = render_to_string('registration/changepassword_email.html', {'username': request.user.username})

	recipient = request.user.email

	send_mail(
			email_title,
			'',										#to render plain text message
			'kavieblog@gmail.com',
			[recipient,],
			html_message=email_content,				#to render HTML message
	)
	return blogindex(request)