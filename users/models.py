from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from my_project import settings
from PIL import Image
# Create your models here.


class Activities(models.Model):
	activity = models.CharField(primary_key=True, max_length= 100)

	def __str__(self):
		return self.activity
	
	

class UserManager(BaseUserManager):
	def create_user(self, username, email, date_of_birth, password=None):
		if not email:
			return ValueError("Users must have an email address")
		
		if not username:
			return ValueError("Users must have an username")

		if not date_of_birth:
			return ValueError("Users must have a Date Of Birth")

		user = self.model(
			email= self.normalize_email(email),
			username = username,
			date_of_birth = date_of_birth,
			)
		user.set_password(password)
		user.save(using= self._db)
		return user


	def create_superuser(self, username, email, date_of_birth, password):
		user = self.create_user(
			email= self.normalize_email(email),
			username = username,
			date_of_birth = date_of_birth,
			password= password,
			)

		user.admin = True
		user.staff = True
		user.active = True

		user.save(using= self._db)
		return user



class User(AbstractBaseUser):
	email = models.EmailField(verbose_name="email", max_length=60)
	username = models.CharField(max_length=60, unique=True)
	date_of_birth = models.DateField(verbose_name= "Date Of Birth")
	medical_history = models.TextField(null=True)
	activities = models.ForeignKey(Activities, null=True, on_delete= models.SET_NULL)
	



	is_active = models.BooleanField(default=True)
	staff = models.BooleanField(default=False)
	admin = models.BooleanField(default=False)

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = [ 'email', 'date_of_birth']

	objects = UserManager()

	def __str__(self):
		return self.username + " " + self.email

	def has_perm(self, perm, obj=None):
		return self.admin

	def has_module_perms(self, perm, obj=None):
		return True
	

	@property
	def is_admin(self):
		return self.admin

	@property
	def is_staff(self):
		return self.staff

	@property
	def active(self):
		return self.active
	


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete= models.CASCADE)
	#add anyother fields you like here


	image = models.ImageField(default = 'default.jpg', upload_to = 'profile_dir')

	def __str__(self):
		return f'{ self.user.username } Profile'

	def save(self, *args, **kwargs):
		super(Profile, self).save(*args, **kwargs)
		img = Image.open(self.image.path)

		if img.height > 300 or img.width > 300:
			output_size = (300,300)
			img.thumbnail(output_size)
			img.save(self.image.path)
			

