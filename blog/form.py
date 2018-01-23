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

	#saving decrypted content to database
	def decrypt_content(self):
		data = self.cleaned_data['content']+'\n'
		lines = data.split('\n')
		newLines = []
		tags = {r'\[kbd\]': '<code>', r'\[/kbd\]': '</code>',
				r'\[b\]': '<b>', r'\[/b\]': '</b>', 
				r'\[line\]': '<hr>', 
				r'\[img\]': '<img src="', r'\[/img\]': '" class="img-thumbnail">', 
				r'\[snippet\]': '<pre class="prettyprint">', r'\[/snippet\]': '</pre>'}
		for l in lines:
			for t in tags:
				l = re.sub(t, tags[t], l)

			parts = l.split('[/url]')
			if '' in parts:
				parts.remove('')
			for i in range(len(parts)):
				if '[url]' in parts[i]:
					part = parts[i].split('[url]')
					if len(part) > 1:
						address = part[1]
						parts[i] = part[0] + '<a href="' + address + '" target="_blank">' + address + '</a>'
					else:
						parts[i] = '<a href="' + part[0] + '" target="_blank">' + part[0] + '</a>'
			l = ''.join(parts)
			newLines.append(l)
		newData = '\n'.join(newLines)
		return newData


"""
CommentForm
"""
class CommentForm(forms.ModelForm):
	content = forms.CharField(required=True, widget=forms.Textarea(attrs={'cols':'50', 'placeholder':'Comment here...'}))

	class Meta:
		model = Comment
		fields = ('content',)

	def decrypt_content(self):
		data = self.cleaned_data['content']+'\n'
		lines = data.split('\n')
		newLines = []
		brackets = {'<': '&lt;', '>': '&gt;', r'(?i)javascript':'J-A-V-A-S-C-R-I-P-T'}
		tags = {r'\[kbd\]': '<code>', r'\[/kbd\]': '</code>',
				r'\[b\]': '<b>', r'\[/b\]': '</b>', 
				r'\[line\]': '<hr>', 
				r'\[img\]': '<img src="', r'\[/img\]': '" class="img-thumbnail">', 
				r'\[snippet\]': '<pre class="prettyprint">', r'\[/snippet\]': '</pre>'}
		for l in lines:
			for b in brackets:
				l = re.sub(b, brackets[b], l)
			for t in tags:
				l = re.sub(t, tags[t], l)

			parts = l.split('[/url]')
			if '' in parts:
				parts.remove('')
			print(parts)
			for i in range(len(parts)):
				if '[url]' in parts[i]:
					part = parts[i].split('[url]')
					if len(part) > 1:
						address = part[1]
						parts[i] = part[0] + '<a href="' + address + '" target="_blank">' + address + '</a>'
					else:
						parts[i] = '<a href="' + part[0] + '" target="_blank">' + part[0] + '</a>'
			
			l = ''.join(parts)
			newLines.append(l)
		newData = '\n'.join(newLines)
		return newData


"""
Registration
"""
class Registration(UserCreationForm):					#create a subclass 'UserCreateForm' under superclass 'UserCreationFrom'
	username = forms.CharField(required=True, max_length=20, widget=forms.TextInput(attrs={'autofocus':'autofocus'}))
	email = forms.EmailField(required=True, help_text='Valid email required')
	password1 = forms.CharField(
		required=True, 
		min_length=8 ,
		help_text='<ul><li>At least 8 chars with numbers + characters</li><li>Should Not be common password</li><li>Should not be similiar to your profile information</li></ul>', 
		widget=forms.PasswordInput)

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