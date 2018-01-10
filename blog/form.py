from django import forms
from .models import Post, Comment, Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
import re

"""
PostForm
"""
class PostForm(forms.ModelForm):
	title = forms.CharField(required=True, widget=forms.TextInput(attrs={'size':'30','placeholder':'Enter title here ...', 'autofocus':'autofocus'}))
	content = forms.CharField(required=True, widget=forms.Textarea(attrs={'cols':'30', 'placeholder':'Enter content here...'}))
	photo = forms.URLField(required=False, widget=forms.URLInput(attrs={'size':'30', 'placeholder':'Enter image url here if any ...'}))

	class Meta:			#define which model from models.py is going to use the form
		model = Post
		fields = ('title', 'content', 'photo', 'photo_upload','tag')  #which fields are being used in the form

	def change_content(self):
		data = self.cleaned_data['content']+'\n'
		lines = data.split('\n')
		newLines = []
		for l in lines:
			l = re.sub('`kbd`', '<code>', l)
			l = re.sub('`endkbd`', '</code>', l)
			l = re.sub('`bold`', '<b>', l)
			l = re.sub('`endbold`', '</b>', l)
			l = re.sub('`line`', '<hr>', l)
			l = re.sub('`url`', '<a href="', l)
			l = re.sub('`midurl`', '" target="_blank">', l)
			l = re.sub('`endurl`', '</a>', l)
			l = re.sub('`img`', '<img src="', l)
			l = re.sub('`endimg`', '" class="img-thumbnail">', l)
			l = re.sub('`snippet`', '<pre class="prettyprint">', l)
			l = re.sub('`endsnippet`', '</pre>', l)
			newLines.append(l)
		newData = '\n'.join(newLines)
		print('newData: '+newData)
		return newData

"""
CommentForm
"""
class CommentForm(forms.ModelForm):
	content = forms.CharField(required=True, widget=forms.Textarea(attrs={'cols':'50', 'placeholder':'Comment here...'}))

	class Meta:
		model = Comment
		fields = ('content',)

	def change_content(self):
		data = self.cleaned_data['content']+'\n'
		lines = data.split('\n')
		newLines = []
		for l in lines:
			l = re.sub('<', '&lt;', l)	
			l = re.sub('>', '&gt;', l)
			l = re.sub('`kbd`', '<code>', l)
			l = re.sub('`endkbd`', '</code>', l)
			l = re.sub('`bold`', '<b>', l)
			l = re.sub('`endbold`', '</b>', l)
			l = re.sub('`line`', '<hr>', l)
			l = re.sub('`url`', '<a href="', l)
			l = re.sub('`midurl`', '" target="_blank">', l)
			l = re.sub('`endurl`', '</a>', l)
			l = re.sub('`img`', '<img src="', l)
			l = re.sub('`endimg`', '" class="img-thumbnail">', l)
			l = re.sub('`snippet`', '<pre class="prettyprint">', l)
			l = re.sub('`endsnippet`', '</pre>', l)
			newLines.append(l)
		newData = '\n'.join(newLines)
		print('newData: '+newData)
		return newData


"""
Registration
"""
class Registration(UserCreationForm):					#create a subclass 'UserCreateForm' under superclass 'UserCreationFrom'
	username = forms.CharField(required=True, max_length=20, widget=forms.TextInput(attrs={'autofocus':'autofocus'}))
	email = forms.EmailField(required=True, help_text='Valid email required')
	password1 = forms.CharField(required=True, min_length=8 ,
		help_text='8-20 chars, with at least 1 alphabet + 1 number, may also add special characters', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('username', 'email', 'password1','password2')

	def check_email(self):
		form_data = self.cleaned_data
		fault = False
		errorcode = ''						#default setting as if there is any error
		if User.objects.filter(email=form_data['email']).count() > 0:
			errorcode = 'Email Already Exits!'
			fault = True
		return fault, errorcode


"""
UserAccount
"""
class UserAccount(UserChangeForm):
	username = forms.CharField(required=True, disabled=True)
	email = forms.EmailField(required=False, help_text='You may update your email address')
	first_name = forms.CharField(required=False, label='Nickname', help_text='You may update your nickname for display')
	password = forms.CharField(
		required=False, 
		help_text='You may change your password at <a href="../password_reset/">here</a>'
		)

	class Meta:
		model = User
		fields = ('username', 'first_name', 'email', 'password')

class UserProfile(forms.ModelForm):
	gender = forms.ChoiceField(required=False, choices=(('',''),('M','M'),('F','F')))
	day_of_birth = forms.DateField(required=False, widget=forms.widgets.SelectDateWidget(years=range(1917,2018)))
	address = forms.CharField(required=False)
	city = forms.CharField(required=False)
	postcode = forms.CharField(required=False, max_length=6)

	class Meta:
		model = Profile
		fields = ('gender','day_of_birth','address','city','postcode')