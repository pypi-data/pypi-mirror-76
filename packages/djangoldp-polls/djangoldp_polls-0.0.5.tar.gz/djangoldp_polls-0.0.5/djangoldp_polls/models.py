from django.conf import settings
from django.db import models
from djangoldp.models import Model
from django.db.models import Sum

from djangoldp_conversation.models import Conversation
from djangoldp_circle.models import Circle

User = settings.AUTH_USER_MODEL
User.name=User.get_full_name



#========================

#========================

class Tag (Model):
	name = models.CharField(max_length=250,verbose_name="Name")

	class Meta :
		serializer_fields = ['@id','name']
		anonymous_perms = ['view']
		authenticated_perms = ['inherit','add']

	def __str__(self):
		return self.name


class PollOption (Model):
	name = models.CharField(max_length=250,verbose_name="Options available for a vote")

	class Meta :
		serializer_fields = ['@id','name']
		nested_fields = ['userVote','relatedPollOptions']
		anonymous_perms = ['view','add']
		authenticated_perms =  ['inherit','add']


	def __str__(self):
		return self.name

class Poll (Model):
	created_at = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='createdVotes', null=True,blank=True)
	title = models.CharField(max_length=250,verbose_name="Title")
	image = models.URLField(blank=True, null=True, verbose_name="Illustration de l'évènement")
	hostingOrganisation = models.CharField(max_length=250,verbose_name="Name of the hosting organisation")
	startDate = models.DateField(verbose_name="Date de début", blank=True, null=True ) 
	endDate =  models.DateField(verbose_name="Date de fin" )
	shortDescription = models.CharField(max_length=250,verbose_name="Short description")
	longDescription = models.TextField(verbose_name="Long description")
	tags = models.ManyToManyField(Tag, related_name='tags', blank=True)
	pollOptions = models.ManyToManyField(PollOption, related_name='relatedPollOptions', blank=True)
	debate = models.ManyToManyField(Conversation, related_name='debates', blank=True)
	circle = models.ForeignKey(Circle, null=True, related_name="polls")

	class Meta : 
		serializer_fields = ['@id','created_at','debate','pollOptions','votes','author','title','image','hostingOrganisation','startDate','endDate','shortDescription','longDescription','tags']
		nested_fields = ['tags','votes','pollOptions','debate']
		anonymous_perms = ['view','add','change']
		authenticated_perms = ['inherit','add']

	def __str__(self):
		return self.title



class Vote (Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user',null=True,blank=True)
	chosenOption =  models.ForeignKey(PollOption, related_name='userVote')
	relatedPoll = models.ForeignKey(Poll, related_name='votes')

	class Meta :
		auto_author = "user"
		serializer_fields = ['@id','chosenOption','relatedPoll']
		nested_fields = []
		anonymous_perms = ['view','add','change']
		authenticated_perms =  ['inherit','add']
	