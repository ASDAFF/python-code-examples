from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django import forms
import django_countries
import datetime
import tagging
from tagging.models import Tag
from django.db.models import Q
from thumbs import ImageWithThumbsField
# language constants
from language_constants import LANGUAGE
from django.utils.translation import ugettext as _

PUSHTYPES = enumerate(("yesno", "versus","multi","comment"))

class pushitem(models.Model):
    title = models.CharField(max_length = 150,help_text=LANGUAGE['Nameofthepush'])
    background = models.CharField(max_length = 500, help_text=LANGUAGE['Backgroundinfo'],blank=True)
    url = models.URLField(blank=True,help_text=LANGUAGE['URLformoreinformation'])
    type = models.IntegerField(choices = PUSHTYPES)
    votes_total = models.IntegerField(default = 0)
    owner = models.ForeignKey(User ,related_name = 'owner')
    publicPush = models.BooleanField(default = True)    
    timestamp = models.DateTimeField(default=datetime.datetime.now)
    voter = models.ManyToManyField(User, through = "pushitem_voter")
    follow = models.ManyToManyField(User , related_name = 'follow')
    report = models.ManyToManyField(User , related_name = 'report')
    searchfield = models.TextField()
    editorpick = models.BooleanField(default = False)
    pushimage = models.ForeignKey("image")
    comment = models.ManyToManyField("self",related_name = 'comments', blank=True)
    #comments are just related pushes.
    #tags = TagField()
    language = models.CharField(max_length=2)

    def __str__(self):
        return "%s"%self.title
    def __unicode__(self):
        return self.title
    def related(self):       
        foundlist = pushitem.objects.filter(Q(searchfield__contains= self.title.lower()), type__in=[0, 1, 2]).exclude(id=self.id)
        searchwordlist = self.title.split(' ')
        for thisword in searchwordlist:
            if len(thisword)>4:
                foundlist =foundlist | pushitem.objects.filter(Q(searchfield__contains= thisword.lower()), type__in=[0, 1, 2]).exclude(id = self.id)
        return foundlist

    def opposingcomments(self,thisuser = None):
        try:
            if thisuser:
                myvote = pushitem_voter.objects.filter(pushitem = self,user = thisuser)[0].voted_for
                #othervotelist = pushitem_voter.objects.filter(pushitem = self).exclude(user = thisuser,voted_for=myvote).distinct()
                othervotelist = pushitem_voter.objects.filter(pushitem = self).exclude(voted_for=myvote).distinct()
                commentuserlist = []
                for thisvote in othervotelist:
                    commentuserlist.append(thisvote.user.id)
                # get all comments in self that belong to othervotelist users
                #othervotelist = pushitem.objects.filter(type = 3,owner__in = [50,] )
                commentuserlist = list(set(commentuserlist)) # makes list unique users only
                comments = self.comment.all()
                alternativecomments =[]
                for thiscomment in comments:
                    if thiscomment.owner.id in commentuserlist:
                        alternativecomments.append(thiscomment)
                return alternativecomments
            else:
                return['not logged in']
        except:
            return []


    def save(self,*args, **kwargs):
        self.searchfield = ' '.join([self.title.lower(), self.background.lower()])
            #self.searchfield += '|'.join(self.ballotnames).lower()
        thisisnew = not self.id
        r = super(pushitem, self).save(*args, **kwargs)
        if thisisnew:
            for thisballot in self.ballotdata:
                ballot = ballotitem(pushitem=self,name = thisballot["name"], pushimage=thisballot["image"])
                ballot.save()
        return r

# supress AlreadyRegistered exception so we can import
# models for unit testing
try:
    tagging.register(pushitem)
except tagging.AlreadyRegistered:
    pass


TYPE_CHOICES = (
    (0, 'Yes / No'),
    (1, 'versus'),
    (2, 'multi-flip'),
)

class ballotitem(models.Model):    
    name=  models.CharField(max_length = 150)
    votes = models.IntegerField(blank=True, null=True, default=0)
    pushitem = models.ForeignKey("pushitem")
    pushimage = models.ForeignKey("image")
    def __unicode__(self):
        return self.name
    def __str__(self):
        return "%s"%self.name
    class Meta:
        ordering = ['name']
    
    def save(self, force_insert=False, force_update=False):
        """
        Make sure votes never go below zero
        """
        if self.votes < 0:
            self.votes = 0
        return super(ballotitem, self).save()   
        

class pushitem_voter(models.Model):
    pushitem = models.ForeignKey(pushitem)
    user = models.ForeignKey(User)
    voted_for= models.ForeignKey(ballotitem)
    def __str__(self):
        return "%s"%self.voted_for.id


class image(models.Model):
    title = models.CharField(max_length = 100)
    image = ImageWithThumbsField(upload_to ="photos", sizes=((120,125),(200,250)))
    caption = models.CharField(max_length = 250, blank =True)
    def __str__(self):
        return "%s"%self.title
    def __unicode__(self):
        return self.title

class pushimage(image):
    pushitem = models.ForeignKey("pushitem",related_name = 'pushitem')

class ballotimage(image):
    ballotitem = models.ForeignKey("ballotitem")

class avatarimage(image):
    avatar_user = models.ForeignKey(User,related_name = 'avatar_user')

    class Meta:
        ordering = ['title',]
    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return('photo_detail',None,{'object_id':self.id})
        
    
class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)    
    country = django_countries.CountryField(null=True, blank=True)
    profile = models.TextField(blank=True)
    dob = models.DateField(blank=True)
    
    # add by me ticket 7
    url_site = models.URLField(default='', blank=True, null=True)
    bio = models.TextField(default='', blank=True, null=True)
    gender = models.CharField(max_length=1, choices=[('m', _('Male')), ('f', _('Female'))], default='m')
        
    def __str__(self):
        return "%s"%self.user
    
    def __unicode__(self):
        return "%s"%self.user
    
    def age(self):
        today = datetime.date.today()
        try: # raised when birth date is February 29 and the current year is not a leap year
            birthday = self.dob.replace(year=today.year)
        except:
            birthday = self.dob.replace(year=today.year, day=born.day-1)
        if birthday > today:
            return today.year - self.dob.year - 1
        else:
            return today.year - self.dob.year
