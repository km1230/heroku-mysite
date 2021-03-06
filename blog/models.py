from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.template.defaultfilters import truncatewords
from multiselectfield import MultiSelectField
from mysite.storage_backends import MediaStorage

"""
Post Model
"""
class Post(models.Model):
	title = models.CharField(max_length=100)					#CharField need to define max_length
	content = models.TextField()
	author = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
	photo = models.URLField(null=True, blank=True)
	photo_upload = models.ImageField(null=True, blank=True, storage=MediaStorage())
	create_time = models.DateTimeField(auto_now_add=True)
	edit_time = models.DateTimeField(null=True, blank=True, auto_now=True)
	tag = MultiSelectField(null=True, blank=True, choices=(
		('Python3.6','Python3.6'),		
		('Django2.0', 'Django2.0'),
		('PHP', 'PHP'),
		('Nodejs','Nodejs'),
		('Javascript','Javascript'),
		('CSS','CSS'),
		('Font-end','Font-end'),
		('Back-end','Back-end'),
		('Bootstrap','Bootstrap'),
		))

	def __str__(self):
		return self.title


"""
Comment
"""
class Comment(models.Model):
	parent_post = models.ForeignKey(Post, on_delete=models.CASCADE)
	author = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
	content = models.TextField()
	create_time = models.DateTimeField(auto_now_add=True)
	edit_time = models.DateTimeField(null=True, blank=True, auto_now=True)

	def __str__(self):
		return '%s %s %s' % (self.parent_post, self.author, self.edit_time)

	@property
	def short_content(self):
		return truncatewords(self.content, 10)



"""
Additional Profile Model
"""
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	gender = models.CharField(blank=True, max_length=1)
	day_of_birth = models.DateField(null=True, blank=True)
	address = models.TextField(blank=True)
	country = models.CharField(blank=True, max_length=100)
	postcode = models.CharField(blank=True, max_length=6)
	state = models.CharField(blank=True, max_length=100)
	city = models.CharField(blank=True, max_length=100)

	def __str__(self):
		return self.user.username

@receiver(post_save, sender=User)
def createuser(sender, instance, created, **kwargs):
    if created:
      	Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def updateuser(sender, instance, **kwargs):
    instance.profile.save()
