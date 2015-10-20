from django.db import models
from datetime import datetime
from django.contrib.auth.signals import user_logged_in, user_logged_out  
from django.contrib.auth.models import User
import urllib, hashlib, binascii

class Message(models.Model):
	user = models.CharField(max_length=20)
	message = models.TextField(max_length=120)
	time = models.DateTimeField(auto_now_add=True)
	gravatar = models.CharField(max_length=300)

	def __unicode__(self):
		return self.user

def generate_avatar(email):
	a = "http://www.gravatar.com/avatar/"
	a+=hashlib.md5(email.lower()).hexdigest()
	a+='?d=identicon'
	return a
	
#Make hash by username
def hash_username(username):
	a = binascii.crc32(username)
	return a

class ChatUser(models.Model):
	user = models.OneToOneField(User)
	userID =  models.IntegerField()
	username = models.BigIntegerField(primary_key=True)
	access_token = models.CharField(max_length=255)
	access_token_secret = models.CharField(max_length=255)
	is_chat_user = models.BooleanField(default=False)
	gravatar_url = models.CharField(max_length=300)
	last_accessed = models.DateTimeField(auto_now_add=True)

#lambda = make Value property=it mean getter
User.profile = property(lambda u: ChatUser.objects.get_or_create(user=u,defaults={'username':u.username,'userID':hash_username(u.username)})[0])
#User.profile = property(lambda u: ChatUser.objects.get_or_create(user=u,defaults={'username':u.username,'userID':id})[0])
