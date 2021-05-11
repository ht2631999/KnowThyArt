from django.db import models
from django.utils import timezone
from users.models import User, Activities
from django.urls import reverse

# Create your models here.
class Post(models.Model):
	title = models.CharField(max_length=100)
	
	content = models.TextField()
	
	author = models.ForeignKey(User, on_delete= models.CASCADE ) 	#ForeignKey function is to have a foreignkey from other tables

	date_posted = models.DateTimeField(default=timezone.now) 	
	
	activity = models.ForeignKey(Activities, null=True, on_delete= models.SET_NULL)
	
	register_url = models.URLField(max_length = 300, null=True)
	def __str__(self):
		return self.title


	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk': self.pk})
	#auto_now=True (in the DateTimeField) sets the time and date whenever the object is modified

	# last_modified = models.DateTimeField(auto_now=True) 
	# Use this last_modified later if required