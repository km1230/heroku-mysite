from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db.models import Q
from .models import Post, Comment
from .form import PostForm, CommentForm, Registration, UserAccount, UserProfile
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.template.defaultfilters import truncatewords
from django.http import JsonResponse
import re


"""
Font page of blog
"""
def blogindex(request):
	post_list = Post.objects.all().order_by('-create_time')
	for post in post_list:
		post.title = '🔖 ' + post.title
	p = Paginator(post_list, 5)
	page = request.GET.get('page')
	posts = p.get_page(page)
	return render(request, 'blog.html', {'posts': posts})

def post_tag(request, key):
	post_list = [p for p in Post.objects.all().order_by('-create_time') if key in p.tag]
	for post in post_list:
		post.title = '🔖 ' + post.title
	p = Paginator(post_list, 5)
	page = request.GET.get('page')
	posts = p.get_page(page)
	return render(request, 'blog.html', {'posts': posts})

def search(request):
	query = request.GET['q']
	error = ''
	if query:
		posts = Post.objects.filter(
					        Q(title__icontains=query) |
					        Q(content__icontains=query)
				        ).order_by('-create_time')
	if len(posts) < 1:
		error = 'Sorry No result :('
	return render(request, 'archives.html', {'posts':posts, 'error':error})

"""
Register
"""
def register(request):
	if request.user.is_authenticated:
		return blogindex(request)

	if request.method == "POST":
		form = Registration(request.POST)
		if form.is_valid():
			checkfault, error = form.check_email()
			
			if checkfault == False:
				user = form.save()
				username = request.POST.get('username')			#to collect 'username' & 'password' from form method=POST
				password = request.POST.get('password1')
				user = auth.authenticate(username=username, password=password)		#auth.authenicate() hv 2 attrib, username & password
				auth.login(request, user)
				title = "registration"						#auth.login()
				return sendmail(request, title=title)
			else:
				return render(request, 'registration/registration.html', {'form':form, 'error':error})

		else:
			form = Registration()
			error = 'There is something wrong about your information!'
			return render(request, 'registration/registration.html', {'form': form, 'error': error})
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
	
	#find sections and insert id to section headers
	line = post.content.split('\n')
	pattern = r'\d+?\.\s\<b\>\[(.*)\]\<\/b\>'		#to find ---> 5. <b> [escaping the angle brackets]</b>
	sections = []
	newLine = []
	for l in line:
		searchObj = re.search(pattern, l)
		if searchObj:
			section = searchObj.group(1)
			sections.append(section)
			l = '<div id="' + section + '"></div>' + '\n' + l
		newLine.append(l)
	post.content = '\n'.join(newLine)

	error = ''
	if request.user.is_authenticated:
		if request.method == "POST":
			temp = CommentForm(request.POST)
			if temp.is_valid():
				content = temp.decrypt_content()
				form = temp.save(commit=False)
				form.content = content
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
	comment = Comment.objects.filter(parent_post=post).order_by('create_time')
	return render(request, 'post.html', {'post': post, 'comment': comment, 'form':form, 'error':error, 'sections':sections})


"""
Archives
"""
def archives(request):
	post_list = Post.objects.order_by('-create_time')
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
			content = temp.decrypt_content()
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
List all Post by author
"""
def edit_list(request):
	if request.user.is_authenticated:
		post_list = Post.objects.filter(author=request.user).order_by('-create_time')
		error = ''
		if post_list:
			p = Paginator(post_list, 20)
			page = request.GET.get('page')
			posts = p.get_page(page)
		else: 
			error = 'You have no threads.'
	else:
		return blogindex(request)
	return render (request, 'list.html', {'posts':posts, 'error':error})

"""
Encrypt Content
"""
def encrypt_content(target):
	content = target.content
	newLines=[]
	brackets = {'&lt;': '<', '&gt;': '>', 'J-A-V-A-S-C-R-I-P-T':'javascript'}
	tags = {'<code>':'[kbd]', '</code>':'[/kbd]',
			'<b>':'[b]', '</b>':'[/b]', 
			'<hr>':'[line]', 
			r'<a href=".*?blank">': '[url]', '</a>':'[/url]',
			'<img src="':'[img', '" class="img-thumbnail">':'[/img]', 
			'<pre class="prettyprint">':'[snippet]', '</pre>':'[/snippet]'}
	lines = content.split('\n')
	for l in lines:
		for b in brackets:
			l = re.sub(b, brackets[b], l)
		for t in tags:
			l = re.sub(t, tags[t], l)
		newLines.append(l)
	newData = '\n'.join(newLines)
	return newData


"""
Edit Post
"""
def post_edit(request, key):
	post = Post.objects.get(pk=key)
	if request.user != User.objects.get(username='admin'):
		return blogindex(request)

	if request.method == "POST":
		temp = PostForm(request.POST, instance=post)
		if temp.is_valid():
			content = temp.decrypt_content()
			form = temp.save(commit=False)
			form.content = content
			form.save()
			url = reverse('page', kwargs={'key':key})
			return render(request, 'edit_done.html', {'url': url})
		else:
			content = encrypt_content(post);
			form = PostForm(initial={'content':content}, instance=post)

	else:
		content = encrypt_content(post);
		form = PostForm(initial={'content':content}, instance=post)
	return render(request, 'post_edit.html', {'form':form, 'post':post})


"""
Delete Post
"""
def post_delete(request, key):
	post = Post.objects.get(pk=key)
	post.delete()
	return render(request, 'delete_done.html')


"""
List all Comments by author
"""
def comment_list(request):
	if request.user.is_authenticated:
		comment_list = Comment.objects.filter(author=request.user).order_by('-edit_time')
		error = ''
		if comment_list:
			p = Paginator(comment_list, 20)
			page = request.GET.get('page')
			comments = p.get_page(page)
		else: 
			error = 'You have no threads.'
	else:
		return blogindex(request)
	return render (request, 'comment_list.html', {'comments':comments, 'error':error})

"""
Edit Comment
"""
def comment_edit(request, key):
	comment = Comment.objects.get(pk=key)
	parent = comment.parent_post
	if comment.author != request.user :
		return comment_list(request)

	if request.method == "POST":
		temp = CommentForm(request.POST, instance=comment)
		if temp.is_valid():
			content = temp.decrypt_content()
			form = temp.save(commit=False)
			form.content = content
			form.save()
			url = reverse('page', kwargs={'key':parent.pk})
			return render(request, 'edit_done.html', {'url': url})
		else:
			content = encrypt_content(comment)
			form = CommentForm(initial={'content':content}, instance=comment)

	else:
		content = encrypt_content(comment)
		form = CommentForm(initial={'content':content}, instance=comment)
	return render(request, 'comment_edit.html', {'form':form, 'comment':comment})


"""
Delete Post
"""
def comment_delete(request, key):
	comment = Comment.objects.get(pk=key)
	comment.delete()
	return render(request, 'delete_done.html')



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


"""
JSON Feed
"""
def json_feed(request):
	data = {
	    "version": "https://jsonfeed.org/version/1",
	    "title": "Dev Junior",
	    "home_page_url": "http://devjunior.com",
	    "feed_url": "http://www.devjunior.com/feed.json",
	    "icon": "http://www.devjunior.com/static/img/favicon_200.png",
	    "favicon": "http://www.devjunior.com/static/img/favicon.ef83680e7b40.png",
	    "items": []
	}
	posts = Post.objects.order_by('-create_time')
	for post in posts:
		post_dict = {}
		post_dict['id'] = str(post.pk)
		post_dict['title'] = post.title
		post_dict['author'] = {'name':'Kavie'}
		post_dict['content_html'] = post.content
		post_dict['summary'] = truncatewords(post.content, 20)
		post_dict['url'] = reverse('page', kwargs={'key':post.pk})
		data['items'].append(post_dict)

	return JsonResponse(data)


