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
	country = forms.ChoiceField(required=False, choices=(
		('',''),
		('AF', 'Afghanistan'),
		('AL', 'Albania'),
		('DZ', 'Algeria'),
		('AS', 'American Samoa'),
		('AD', 'Andorra'),
		('AO', 'Angola'),
		('AI', 'Anguilla'),
		('AQ', 'Antarctica'),
		('AG', 'Antigua and Barbuda'),
		('AR', 'Argentina'),
		('AM', 'Armenia'),
		('AW', 'Aruba'),
		('AU', 'Australia'),
		('AT', 'Austria'),
		('AZ', 'Azerbaijan'),
		('BS', 'Bahamas, The'),
		('BH', 'Bahrain'),
		('BD', 'Bangladesh'),
		('BB', 'Barbados'),
		('BY', 'Belarus'),
		('BE', 'Belgium'),
		('BZ', 'Belize'),
		('BJ', 'Benin'),
		('BM', 'Bermuda'),
		('BT', 'Bhutan'),
		('BO', 'Bolivia'),
		('BA', 'Bosnia and Herzegovina'),
		('BW', 'Botswana'),
		('BV', 'Bouvet Island'),
		('BR', 'Brazil'),
		('IO', 'British Indian Ocean Territory'),
		('BN', 'Brunei'),
		('BG', 'Bulgaria'),
		('BF', 'Burkina Faso'),
		('BI', 'Burundi'),
		('CI', "Côte d'Ivoire"),
		('KH', 'Cambodia'),
		('CM', 'Cameroon'),
		('CA', 'Canada'),
		('CV', 'Cape Verde'),
		('KY', 'Cayman Islands'),
		('CF', 'Central African Republic'),
		('TD', 'Chad'),
		('GB-CHA', 'Channel Islands'),
		('CL', 'Chile'),
		('CN', 'China'),
		('CX', 'Christmas Island'),
		('CC', 'Cocos (Keeling) Islands'),
		('CO', 'Colombia'),
		('KM', 'Comoros'),
		('CG', 'Congo'),
		('CD', 'Congo (DRC)'),
		('CK', 'Cook Islands'),
		('AU', 'Coral Sea Islands'),
		('CR', 'Costa Rica'),
		('HR', 'Croatia'),
		('CU', 'Cuba'),
		('CY', 'Cyprus'),
		('CZ', 'Czech Republic'),
		('DK', 'Denmark'),
		('DJ', 'Djibouti'),
		('DM', 'Dominica'),
		('DO', 'Dominican Republic'),
		('EC', 'Ecuador'),
		('EG', 'Egypt'),
		('SV', 'El Salvador'),
		('GQ', 'Equatorial Guinea'),
		('ER', 'Eritrea'),
		('EE', 'Estonia'),
		('ET', 'Ethiopia'),
		('FK', 'Falkland Islands (Islas Malvinas)'),
		('FO', 'Faroe Islands'),
		('FJ', 'Fiji Islands'),
		('FI', 'Finland'),
		('FR', 'France'),
		('FX', 'France, Metropolitan'),
		('GF', 'French Guiana'),
		('PF', 'French Polynesia'),
		('TF', 'French Southern and Antarctic Lands'),
		('GA', 'Gabon'),
		('GM', 'Gambia, The'),
		('GE', 'Georgia'),
		('DE', 'Germany'),
		('GH', 'Ghana'),
		('GI', 'Gibraltar'),
		('GR', 'Greece'),
		('GL', 'Greenland'),
		('GD', 'Grenada'),
		('GP', 'Guadeloupe'),
		('GU', 'Guam'),
		('GT', 'Guatemala'),
		('GB-GSY', 'Guernsey'),
		('GN', 'Guinea'),
		('GW', 'Guinea-Bissau'),
		('GY', 'Guyana'),
		('HT', 'Haiti'),
		('HM', 'Heard Island and McDonald Islands'),
		('HN', 'Honduras'),
		('HK', 'Hong Kong SAR'),
		('HU', 'Hungary'),
		('IS', 'Iceland'),
		('IN', 'India'),
		('ID', 'Indonesia'),
		('IR', 'Iran'),
		('IQ', 'Iraq'),
		('IE', 'Ireland'),
		('IL', 'Israel'),
		('IT', 'Italy'),
		('JM', 'Jamaica'),
		('JP', 'Japan'),
		('GB-JSY', 'Jersey'),
		('JO', 'Jordan'),
		('KZ', 'Kazakhstan'),
		('KE', 'Kenya'),
		('KI', 'Kiribati'),
		('KR', 'Korea'),
		('KW', 'Kuwait'),
		('KG', 'Kyrgyzstan'),
		('LA', 'Laos'),
		('LV', 'Latvia'),
		('LB', 'Lebanon'),
		('LS', 'Lesotho'),
		('LR', 'Liberia'),
		('LY', 'Libya'),
		('LI', 'Liechtenstein'),
		('LT', 'Lithuania'),
		('LU', 'Luxembourg'),
		('MO', 'Macau SAR'),
		('MK', 'Macedonia, Former Yugoslav Republic of'),
		('MG', 'Madagascar'),
		('MW', 'Malawi'),
		('MY', 'Malaysia'),
		('MV', 'Maldives'),
		('ML', 'Mali'),
		('MT', 'Malta'),
		('GB-IOM', 'Man, Isle of'),
		('MH', 'Marshall Islands'),
		('MQ', 'Martinique'),
		('MR', 'Mauritania'),
		('MU', 'Mauritius'),
		('YT', 'Mayotte'),
		('MX', 'Mexico'),
		('FM', 'Micronesia'),
		('MD', 'Moldova'),
		('MC', 'Monaco'),
		('MN', 'Mongolia'),
		('MS', 'Montserrat'),
		('MA', 'Morocco'),
		('MZ', 'Mozambique'),
		('MM', 'Myanmar'),
		('NA', 'Namibia'),
		('NR', 'Nauru'),
		('NP', 'Nepal'),
		('AN', 'Netherlands Antilles'),
		('NL', 'Netherlands, The'),
		('NC', 'New Caledonia'),
		('NZ', 'New Zealand'),
		('NI', 'Nicaragua'),
		('NE', 'Niger'),
		('NG', 'Nigeria'),
		('NU', 'Niue'),
		('NF', 'Norfolk Island'),
		('KP', 'North Korea'),
		('MP', 'Northern Mariana Islands'),
		('NO', 'Norway'),
		('OM', 'Oman'),
		('PK', 'Pakistan'),
		('PW', 'Palau'),
		('PA', 'Panama'),
		('PG', 'Papua New Guinea'),
		('PY', 'Paraguay'),
		('PE', 'Peru'),
		('PH', 'Philippines'),
		('PN', 'Pitcairn Islands'),
		('PL', 'Poland'),
		('PT', 'Portugal'),
		('PR', 'Puerto Rico'),
		('QA', 'Qatar'),
		('RE', 'Reunion'),
		('RO', 'Romania'),
		('RU', 'Russia'),
		('RW', 'Rwanda'),
		('ST', 'São Tomé and Príncipe'),
		('WS', 'Samoa'),
		('SM', 'San Marino'),
		('SA', 'Saudi Arabia'),
		('SN', 'Senegal'),
		('YU', 'Serbia and Montenegro'),
		('SC', 'Seychelles'),
		('SL', 'Sierra Leone'),
		('SG', 'Singapore'),
		('SK', 'Slovakia'),
		('SI', 'Slovenia'),
		('SB', 'Solomon Islands'),
		('SO', 'Somalia'),
		('ZA', 'South Africa'),
		('GS', 'South Georgia and the South Sandwich Islands'),
		('ES', 'Spain'),
		('LK', 'Sri Lanka'),
		('SH', 'St. Helena'),
		('KN', 'St. Kitts and Nevis'),
		('LC', 'St. Lucia'),
		('PM', 'St. Pierre and Miquelon'),
		('VC', 'St. Vincent and the Grenadines'),
		('SD', 'Sudan'),
		('SR', 'Suriname'),
		('SJ', 'Svalbard and Jan Mayen'),
		('SZ', 'Swaziland'),
		('SE', 'Sweden'),
		('CH', 'Switzerland'),
		('SY', 'Syria'),
		('TJ', 'Tajikistan'),
		('TZ', 'Tanzania'),
		('TH', 'Thailand'),
		('TP', 'Timor-Leste'),
		('TG', 'Togo'),
		('TK', 'Tokelau'),
		('TO', 'Tonga'),
		('TT', 'Trinidad and Tobago'),
		('TN', 'Tunisia'),
		('TR', 'Turkey'),
		('TM', 'Turkmenistan'),
		('TC', 'Turks and Caicos Islands'),
		('TV', 'Tuvalu'),
		('UM', 'U.S. Minor Outlying Islands'),
		('UG', 'Uganda'),
		('UA', 'Ukraine'),
		('AE', 'United Arab Emirates'),
		('GB', 'United Kingdom'),
		('US', 'United States'),
		('UY', 'Uruguay'),
		('UZ', 'Uzbekistan'),
		('VU', 'Vanuatu'),
		('VA', 'Vatican City'),
		('VE', 'Venezuela'),
		('VN', 'Viet Nam'),
		('VI', 'Virgin Islands'),
		('VG', 'Virgin Islands, British'),
		('WF', 'Wallis and Futuna'),
		('YE', 'Yemen'),
		('ZM', 'Zambia'),
		('ZW', 'Zimbabwe'),
		)
	)
	postcode = forms.CharField(required=False, max_length=6)
	state = forms.ChoiceField(required=False, choices=(('',''),))
	city = forms.CharField(required=False)

	class Meta:
		model = Profile
		fields = ('gender','day_of_birth', 'country', 'state', 'city', 'address', 'postcode')