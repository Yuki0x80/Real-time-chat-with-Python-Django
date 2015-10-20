from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import auth
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
import json
from djangoChat.models import Message, ChatUser
from django.contrib.auth.models import User
import datetime
from django.utils.timezone import now as utcnow
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext,loader
from django.core.urlresolvers import reverse
import tweepy
import sys, re
import time
from django.shortcuts import render, redirect
from django.http import HttpRequest
import importlib
from django.conf import settings

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
CALLBACK_URL = 'http://127.0.0.1:8000/chat/get_callback/'

# if login index.html=chat screen else login screen
def index(request):
	if request.method == 'POST':
		print request.POST
	logged_users = []
	if request.user.username and request.user.profile.is_chat_user:
		print "come here"
		auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
		auth.set_access_token(request.session.get('key'), request.session.get('secret'))
		api = tweepy.API(auth_handler=auth)
		print request.user.username
		u = api.get_user(request.user.username)
		logged_users=u.screen_name
		context = {'logged_users':logged_users}
		return render(request, 'djangoChat/index.html', context)
	else:
		'''
		Twitter OAuth Authenticate
		'''
		auth_tw = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET, CALLBACK_URL)
		try:
			auth_url = auth_tw.get_authorization_url()
		except tweepy.TweepError:
			print 'Error! Failed to get request token. You have to access network'
			return HttpResponseRedirect(reverse('index'))
		request.session['request_token'] = auth_tw.request_token
		request.session.save()
		return HttpResponseRedirect(auth_url)

def get_callback(request):
    '''
    Callback
    '''
    # Example using callback (web app)
    verifier = request.GET.get('oauth_verifier')
    oauth_token = request.GET.get('oauth_token') 
    # Let's say this is a web app, so we need to re-build the auth handler first...
    auth_get = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth_get.set_access_token(oauth_token, verifier) 
    auth_get.request_token = request.session.get('request_token') 
    try:
        auth_get.get_access_token(verifier)
    except tweepy.TweepError:
        print 'Error! Failed to get access token.'
        return HttpResponseRedirect(reverse('index'))
    #get access token
    request.session['key'] = auth_get.access_token 
    request.session['secret'] = auth_get.access_token_secret 
    #get user_id
    user_id = int(tweepy.API(auth_get).me().id_str)
    print "auth_username"+auth_get.get_username()

    #authentication  DataBase!!:
    user=auth.authenticate(username=user_id, password=auth_get.access_token)

    if user is None:
		print "go to index"
		user = User.objects.create_user(username=user_id, password=auth_get.access_token)
		#user.userID=user_id
		user.username=user_id#auth_get.get_username()
		user.access_token = auth_get.access_token 
		user.access_token_secret = auth_get.access_token_secret
		user.save()
		#user = User.objects.get(username=user_id)
		user.backend = 'django.contrib.auth.backends.ModelBackend'
		engine = importlib.import_module(settings.SESSION_ENGINE)
		request.session = engine.SessionStore()

		user=auth.authenticate(username=user_id, password=auth_get.access_token)

    auth.login(request,user)
    cu = request.user.profile
    cu.is_chat_user = True
	#time
    cu.last_accessed = utcnow()
    cu.save()
    request.session['key'] = auth_get.access_token 
    request.session['secret'] = auth_get.access_token_secret 
    return HttpResponseRedirect(reverse('index'))


def logout(request):
	cu = request.user.profile
	cu.is_chat_user = False
	cu.save()
	return HttpResponse('succesfully logged out of chat')


@csrf_exempt
def chat_api(request):
	if request.method == 'POST':
		###Oauth system:userid for username
		auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
		auth.set_access_token(request.session.get('key'), request.session.get('secret'))
		api = tweepy.API(auth_handler=auth)
		##makes json
		d = json.loads(request.body)
		msg =  d.get('msg')
		if len(msg) > 120:
			print "error to much word"
			return 0
		u = api.get_user(request.user.username)
		user= u.screen_name
		gravatar = request.user.profile.gravatar_url
		m = Message(user=user,message=msg,gravatar=gravatar)
		m.save()
		res = {'id':m.id,'msg':m.message,'user':m.user,'time':m.time.strftime('%I:%M:%S %p').lstrip('0'),'gravatar':m.gravatar}
		data = json.dumps(res)
		try:
			auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
			auth.set_access_token(request.session.get('key'), request.session.get('secret'))
			api = tweepy.API(auth_handler=auth)
			""" test get tweet"""
			api.update_status(status=m.message+" "+"#test")
			#count=count+1
		except tweepy.TweepError,e:
			p = re.compile('^\[{u\'message\': u\'(.+)\', u\'code\': (\d+)}\]$')
			m = p.match(e.reason)
			if m:
				message =  m.group(1)
				code = m.group(2)
		return HttpResponse(data,content_type="application/json")
	# get request
	r = Message.objects.order_by('-time')[:10]
	res = []
	for msgs in reversed(r) :
		res.append({'id':msgs.id,'user':msgs.user,'msg':msgs.message,'time':msgs.time.strftime('%I:%M:%S %p').lstrip('0'),'gravatar':msgs.gravatar})
	data = json.dumps(res)
	print "response"
	return HttpResponse(data,content_type="application/json")


def logged_chat_users(request):
	u = ChatUser.objects.filter(is_chat_user=True)
	print "next sity"
	for j in u:
		elapsed = utcnow() - j.last_accessed
		if elapsed > datetime.timedelta(seconds=35):

			j.is_chat_user = False
			j.save()

	uu = ChatUser.objects.filter(is_chat_user=True)
	d = []
	for i in uu:
		print "i.username"+i.username
		d.append({'username': i.username,'gravatar':i.gravatar_url,'id':i.userID})
	data = json.dumps(d)
	return HttpResponse(data,content_type="application/json")


def update_time(request):
	if request.user.username:
		u = request.user.profile
		u.last_accessed = utcnow()
		u.is_chat_user = True
		u.save()
		return HttpResponse('updated')
	return HttpResponse('who are you?')