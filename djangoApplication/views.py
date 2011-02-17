from django.template import loader,Context
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core import serializers
from django.shortcuts import *
from models import *
from forms import commentForm, pushitemForm, UserForm, UserProfileForm
from django import forms
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from tagging.models import Tag
from tagging.models import TaggedItem
from django.conf import settings
from math import log
from django.contrib.auth import logout
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
# language constants
from language_constants import *
# is user logged in
from decorators import ajax_required
import copy
import logging

from django.utils.translation import ugettext as _

try:
    import json
except ImportError:
    import simplejson as json
    
# configure logger
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')
    
ITEMS_PER_PAGE = 10
@login_required
def comment(request):        
    if request.POST :
        commentform = commentForm(request.POST) # A form bound to the POST data
        if 'comment_parent' in request.POST :
            if commentform.is_valid :
                try:
                    commentpush = commentform.save(commit = False)
                    commentpush.type = 3
                    commentpush.owner = request.user
                    commentpush.pushimage = image.objects.get(title="_noimage")
                    r= []
                    agree = image.objects.filter(title= '_agree')[0]
                    disagree = image.objects.filter(title= '_disagree')[0]
                    r.append({'name':LANGUAGE['agree'] , 'image':agree})
                    r.append({'name':LANGUAGE['disagree'] , 'image':disagree})
                    commentpush.ballotdata = r
                    commentpush.save()
                    commentpush.ballotdata = []
                    commentpush.comment.add(pushitem.objects.get(id=request.POST['comment_parent']))
                    comment.title = "Comment" # not using comment titles in UI, but can't be blank or null
                    commentpush.save()
                    return commentpush
                except Exception, ex:
                    logging.debug('salcat.views.comment: Exception: %s' % ex)
            else:
                logging.debug("Invalid Comment: %s" % commentform)


def makepage(request,pagequerydict ,contextoverridedict= {}, template = "yesnocatalogue.html"):
    c = comment(request) #process comment POSTing
    #return HttpResponseRedirect('/commented/') # Redirect after POST        
    pagequerydict = pagequerydict.exclude(Q(type=3)) # ignore comment type
    paginator = Paginator(pagequerydict, ITEMS_PER_PAGE)
    if request.user.is_authenticated:
        logged_in = True
    else:
        logged_in = False
    if pagequerydict.count()> 6:
        mostrecent = pagequerydict[:5]
    else:
        mostrecent = pagequerydict    
    editorpick = pushitem.objects.filter(editorpick = True).order_by('-timestamp')[:5]
    
    if 'page' in request.GET:
        page = int(request.GET['page'])
    else:
        page = 1
    try:
        pagedlistings = paginator.page(page)
    except:
        raise Http404    
    t = loader.get_template(template)
    defaultcontext = { 'SITE_URL':settings.SITE_URL,
                    'MEDIA_URL':settings.MEDIA_URL,
                    'alllistings': pagedlistings.object_list,
                    'mostrecent': mostrecent ,
                    'title': 'all sites',
                    'editorpick': editorpick,
                    'message': None,
                    'logged_in': logged_in,
                    'show_paginator': paginator.num_pages > 1,
                    'has_prev': pagedlistings.has_previous(),
                    'has_next': pagedlistings.has_next(),
                    'page': page,
                    'pages': paginator.num_pages,
                    'next_page': page + 1,
                    'prev_page': page - 1,
                    'showall': False,
                    'user': request.user,
                    'homepageTitle': LANGUAGE['homepageTitle'],
                    }
    
    defaultcontext.update(contextoverridedict)    
    contextdict =  RequestContext(request,defaultcontext)    
    #c = Context(contextdict)
    return HttpResponse(t.render(contextdict))

def catalogue(request, message = None):
    pagequerydict = pushitem.objects.all().filter(language=request.LANGUAGE_CODE).order_by('?').exclude(Q(type = 3))
    r = makepage(request,pagequerydict,{'title':LANGUAGE['homepageTitle'],'message':message})
    return r

def menu(request):
    try:
        thismenu = request.GET.get('menu')
    except:
        thismenu = 'random'
    finally:
        thistemplate = 'yesnocatalogue.html'
        try:
            if thismenu == 'random' or thismenu == '':
                pagequerydict = pushitem.objects.all().filter(language=request.LANGUAGE_CODE).order_by('?')
                r = makepage(request,pagequerydict,{'menu':'random'},thistemplate)
                return r
            elif thismenu == 'my':
                pagequerydict = pushitem.objects.filter(owner=request.user.pk).order_by('-timestamp')
                r = makepage(request,pagequerydict,{'menu':'my','title':_('My pushes') },thistemplate)
                return r
            elif thismenu == 'pop':
                pagequerydict  = pushitem.objects.all().filter(language=request.LANGUAGE_CODE).order_by('-votes_total')
                r = makepage(request,pagequerydict,{'menu':'pop','title':_('Popular')},thistemplate)
                return r
            elif thismenu == 'editors':
                pagequerydict = pushitem.objects.filter(editorpick= True, language=request.LANGUAGE_CODE).order_by('-timestamp')
                r = makepage(request,pagequerydict,{'menu':'eds','title':_('Editors Picks')},thistemplate)
                return r
            elif thismenu == 'cloud':
                #return HttpResponseRedirect('/cloud/') # Redirect after POST
                pagequerydict = pushitem.objects.all().filter(language=request.LANGUAGE_CODE).order_by('-timestamp')

                r = makepage(request,pagequerydict,{'menu':'new','tagcloud':tagcloud(),'title':_('cloud')},'cloud.html')
                return r
            #thismenu == 'new':
        except:
            pass
        pagequerydict = pushitem.objects.all().filter(language=request.LANGUAGE_CODE).order_by('-timestamp')
        r = makepage(request,pagequerydict,{'menu':'new','title':_('menu except')},thistemplate)
        return r


def item(request,template = "yesnocatalogue.html"):
    try:
        template = 'item.html'
        thisid = request.GET['id']
        pagequerydict = pushitem.objects.filter(id=thisid)
        if pagequerydict[0].type == 3:
            # if this is a comment, then get it's parent push
            pagequerydict = pushitem.objects.filter(comment= pagequerydict[0])
        related = pagequerydict[0].related()
        r = makepage(request,pagequerydict,{'item_id':request.GET['id'], 'showall': True,'title': pagequerydict[0].title,'related':related},template)
        return r
    except:
        return catalogue(request,LANGUAGE['Thatpushisnotfound'])

def iframe(request):    
    return item(request,'iframe.html')

@login_required
def add(request):
    def createimage(imagename,imagefieldname,placeholdername):
        try:
            thisimage = image(title = imagename , image = request.FILES[imagefieldname])
            thisimage.save()
        except:
            thisimage = image.objects.filter(title= placeholdername)[0]
        return thisimage

    def fileupload(request,fieldname,imagefieldname,versusplaceholder):     
        thisimage = createimage(request.POST[fieldname], imagefieldname,versusplaceholder)
        if not thisimage:
            return False
        return thisimage

    def type0(request):
        ''' yes no push '''
        r= []
        up = image.objects.filter(title= '_up')[0]
        down = image.objects.filter(title= '_down')[0]
        r.append({'name':'down' , 'image':down})
        r.append({'name':'up' , 'image':up})        
        return r

    def type1(request):
        ''' versus push '''
        r= []
        leftimg =fileupload(request,'versusleft','versusleftimage','_versus')
        rightimg =fileupload(request,'versusright','versusrightimage','_versus')
        
        #leftimg = image.objects.get(title= '_versus')
        #rightimg = image.objects.get(title= '_versus')

        r.append({'name':request.POST['versusleft'] , 'image':leftimg})
        r.append({'name': request.POST['versusright'] , 'image':rightimg})
        return r
    
    def type2(request):
        ''' multi push '''
        r= []        
        for im in range(1,30): # up to 30 ballot items to choose from
            try:
                im_str= str(im)
                fupload = fileupload(request,'multi'+im_str,'multi'+im_str+'image','_noimage')
                if request.POST['multi'+im_str]:
                    r.append({'name':request.POST['multi'+im_str] , 'image':fupload})
            except:
                pass
        return r

    def type3(request):
        ''' comment push '''
        r= []
        up = image.objects.filter(title= '_up')[0]
        down = image.objects.filter(title= '_down')[0]
        r.append({'name':'down' , 'image':down})
        r.append({'name':'up' , 'image':up})
        return r


    if request.method == 'POST': # If the form has been submitted...
        form = pushitemForm(request.POST or None) # A form bound to the POST data
        if request.POST and form.is_valid(): # All validation rules pass
            newpush = form.save(commit=False)
            #if 'pushimage' in request.FILES:
            #    newpush.pushimage = createimage(request.POST['title'], 'pushimage','_noimage')
            newpush.pushimage = createimage(request.POST['title'], 'pushimage','_noimage')
            newpush.type = request.POST['type']
            if(request.POST['type'] == '0'):
                newpush.ballotdata = type0(request)            
            if(request.POST['type'] == '1'):
                newpush.ballotdata = type1(request)
            if(request.POST['type'] == '2'):
                newpush.ballotdata = type2(request)
                if len(newpush.ballotdata)<3:
                    return HttpResponseRedirect('/multierror/') # Redirect after POST
            newpush.language = request.LANGUAGE_CODE
            newpush.owner = request.user
            newpush = form.save()
            taglist =request.POST.getlist('tag')
            tagstring = ' '
            for thistag in taglist:
                tagstring += str(thistag) +' '

            newpush.tags = tagstring
            newpush.save()
            return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
        form = pushitemForm() # An unbound form  
    q = pushitem.objects.none()
    r = makepage(request,q,
                {'title':LANGUAGE['addpushPage'],'form':form}
                ,'add.html')
    return r
    return render_to_response('add.html', {
        'form': form,      
        'title':LANGUAGE['Addapush']})

def user(request, user_id):
                  
    try:
        profileuser = User.objects.get(id = user_id)
        thisProfile = UserProfile.objects.get(user = profileuser)
        follow = pushitem.objects.filter(follow = user_id)
        comments=  pushitem.objects.filter(type = '3').filter(owner = profileuser)
        thispagequerydict = pushitem.objects.filter(owner = profileuser)
        
        contextoverridedict = {
                    'follow': follow,
                    'comments': comments,
                    'profileuser': profileuser,
                    'Profile':thisProfile,
                    }        
        #pagequerydict = pushitem.objects.all().order_by('-timestamp').exclude(Q(type = 3))
        r = makepage(   request,
                        thispagequerydict,
                        contextoverridedict
                       ,'user.html'
                        )
        return r
    except Exception, ex:
        logging.debug("salcat.views.user: Exception occurred: %s" % ex)
        pass
        
    return catalogue(request,LANGUAGE['usernotknown'])

def edituser(request):
    if not request.user.is_authenticated:
        return catalogue(request,LANGUAGE['Cannot edit user'])
    else:
        profile = get_object_or_404(UserProfile, user=request.user)
        if request.method == 'POST': # If the form has been submitted...
            form = UserProfileForm(data=request.POST, instance=profile) # A form bound to the POST data
            if request.POST and form.is_valid(): # All validation rules pass
                editeduser = form.save()
                return HttpResponseRedirect('/user/%d'%request.user.pk)
        else:
            form = UserProfileForm(instance=profile)
            
        return render_to_response('user_form.html', RequestContext(request,{'form': form,}))

@login_required
def vote(request,object_id):
    
    # keep track of the last ballot the user voted for on this push (if any)
    # so that we know which one to decrement in the DOM for an ajax vote
    old_ballot = {"id": None, "votes": None}
    logging.debug("In vote")
    def increment_vote(thisballot,request):
        ''' given a vote id , increment it '''
        thispush = pushitem.objects.get(id = thisballot.pushitem_id)
        thisballot.votes += 1
        thisballot.save()
        logging.debug("Incrementing ballot: %s" % thisballot.id)

        pushitem_voter.objects.create(user = request.user, pushitem = thispush,voted_for= thisballot)
    def decrement_votes(thispush,request):
        pvlist = pushitem_voter.objects.filter(user = request.user, pushitem = thispush)
        ballotlist=[]
        
        for thisvoter in pvlist:
            ballotlist.append(thisvoter.voted_for)
        for thisalreadyballot in ballotlist:
            thisalreadyballot.votes -= 1
            thisalreadyballot.save()
            logging.debug("Thisalreadyballot: %s" % thisalreadyballot)
            
            ballot_previously_voted = copy.deepcopy(thisalreadyballot)
            old_ballot['id'] = ballot_previously_voted.id
            old_ballot['votes'] = ballot_previously_voted.votes
            
        pushitem_voter.objects.filter(user = request.user, pushitem = thispush).delete()
        
    def useralreadyvotedforthispush(thispush,request):
        already = pushitem.objects.filter(voter__id = request.user.id,id = thispush.id).count()
        return already

    thisballot = ballotitem.objects.get(id = object_id)
    thispush = pushitem.objects.get(id = thisballot.pushitem_id)    
    if thispush.type == 3:
        # it's a comment: get parent
        thispushqueryset = pushitem.objects.filter(comment = thispush)
    else:
        thispushqueryset = pushitem.objects.filter(id = thisballot.pushitem_id)

    message = ''
    already_voted = useralreadyvotedforthispush(thispush,request)
    
    if already_voted:
        pvlist = pushitem_voter.objects.filter(user = request.user, pushitem = thispush)
        ballotlist=[]
        for thisvoter in pvlist:
            ballotlist.append(thisvoter.voted_for)
        if thisballot in ballotlist:
          #  message +=' voted for this push, and this ballot'
          pass
        else:
         #   message +=' voted for this push, but not this ballot'
            print "trayin to increment"
            decrement_votes(thispush,request)
            increment_vote(thisballot,request)
    else:
        #message +=' not voted yet'+ str(thispush.id)
        increment_vote(thisballot,request)
        thispush.votes_total += 1
        thispush.save()
    
    if request.is_ajax():
        logging.debug("Got ajax vote request for ballot# %s" % thisballot.id)
        json_dict = {'push': thispush.id,
                     'ballot': thisballot.id,
                     'votes': thisballot.votes}
        json_dict['old_ballot_id'] = old_ballot['id']
        json_dict['old_ballot_votes'] = old_ballot['votes']
        
        response = json.dumps(json_dict)
        
        logging.debug("Response: %s" % response)
        return HttpResponse(response,
                            content_type = 'application/javascript; charset=utf8')
        
    message = LANGUAGE['yourvotehasbeencounted'] % thispush.title #'Your vote for "'+thispush.title+'" has been counted'
    r = makepage(request,thispushqueryset,{'showall': 1,'message':message,})
    return r

def ajaxvote(request,object_id):
    r = vote(request,object_id)
    
    thisballot = ballotitem.objects.get(id = object_id)
    thispush = pushitem.objects.get(id = thisballot.pushitem_id)
    pagequerydict = pushitem.objects.filter(id= thispush.id)
    
    template = 'ajaxtemplate.html'
    r = makepage(request,pagequerydict,{'showall': True,'title': pagequerydict[0].title},template)
    #response = HttpResponse()
    #response['Content-Type'] = 'text'
    #response.write(r)
    #return response
    return r

@login_required
def follow(request,object_id):
    thispush = pushitem.objects.get(id = object_id)
    already = pushitem.objects.filter(follow__id = request.user.id,id = thispush.id).count()
    #follow = pushitem.objects.filter(follow = request.user.id)
    message= LANGUAGE["Okyournowfollowingthat"]
    if already:
        message=LANGUAGE["Yourealreadyfollowingthat"]
    thispush.follow.add(request.user)
    return catalogue(request,message)
    
@login_required
def report(request):
    ''' alert admin that the push is inappropriate'''
    if 'id' in request.GET:
        object_id = request.GET['id'].lower()
        thispush = pushitem.objects.get(id = object_id)
        already = pushitem.objects.filter(report__id = request.user.id,id = thispush.id).count()
        report = pushitem.objects.filter(report = request.user.id)
        message=_("Ok Thanks for reporting that")
        if already:
            message=_("You've already reported that! Thanks!")
        thispush.report.add(request.user)
        return catalogue(request,message)

def logoutview(request):
    logout(request)
    message = LANGUAGE['loggedout']
    return HttpResponseRedirect('/userlogout/') # Redirect after POST

    
def search(request):
    """Returns search of names and background"""
    if 'q' in request.GET:
        term = request.GET['q'].lower()
        thispushqueryset = pushitem.objects.filter(Q(searchfield__contains= term) )
        message = _('Searching for %s')%str(term)
    else:
        thispushqueryset = pushitem.objects.none()
        message = _('No search query specified')
    r = makepage(request,thispushqueryset,{'search_query':request.GET['q'].lower(), 'showall': 1,'message':message,}, template='search.html')
    return r


def pushinit(request):
    ''' restart the push/ user generated contents
    '''
    pushitem.objects.all().delete()
    ballotitem.objects.all().delete()  
    return catalogue(request,LANGUAGE['usergeneratedcontentdeleted'])

def init(request):
    '''
    Initialize the database
    '''
    from django.core import management
    management.call_command('reset','chunks' ,verbosity=1, interactive=False)
    management.call_command('reset','flatpages' ,verbosity=1, interactive=False)
    management.call_command('syncdb', verbosity=1, interactive=False)
    
    pushitem.objects.all().delete()
    ballotitem.objects.all().delete()
    image.objects.all().delete()
    pushimage.objects.all().delete()
    
    #User.objects.all().delete() # this keeps wiping me out of the DB!
    julz  = User.objects.create(
        username='julz',
        email='julian@example.com',
        password='sha1$3da70$0d38b7fe441f37aaf6f6c95ff6752a4d74378484', #ie type: 'pass'
        is_superuser=True,
        )
    julz= User.objects.get(username = "julz")
    
    thispush = pushitem(id = 1, title ="testpush",background ='bkk',type=0,owner=julz)
    up = ballotitem(name= '_up',pushitem=thispush,pushimage_id=1)
    down = ballotitem(name = '_down',pushitem=thispush,pushimage_id=2)
    thispush.tags = "a b c"
    im = pushimage(pushitem_id = 1)
    im.save()
    thispush.pushimage = im
    thispush.save()
    up.save()
    down.save()
    imagecreatelist = ['_up', '_down','_noimage','_versus','_agree','_disagree']
    for thisim in imagecreatelist:
        u = image(title= thisim)
        u.save()    
    Tag.objects.update_tags(thispush, LANGUAGE['defaulttagslist']) # 'house thing'
    thispush.save()
    return catalogue(request)


def add_user(request):
    
    if request.method == "POST":
        uform = UserForm(data = request.POST)
        pform = UserProfileForm(data = request.POST)
        if uform.is_valid() and pform.is_valid():
            user = uform.save()
            user.set_password(user.password)
            user.save()
            profile = UserProfile(user=user,
                                  country=pform.cleaned_data['country'],
                                  profile=pform.cleaned_data['profile'],
                                  dob=pform.cleaned_data['dob'])
            profile.save()
            return HttpResponseRedirect('/registration_success/') # Redirect after POST
    
    data, errors = {}, {}
    uform = UserForm()
    pform = UserProfileForm()
    pagequerydict = pushitem.objects.none()
    r = makepage(request,pagequerydict,{'title':LANGUAGE['Register'],
                                        'uform': uform,
                                        'pform': pform,
                                        'errors': {},},
                                        "registration/registration_form.html",
                                        )
    return r


def tag(request):
    try:
        thistag = Tag.objects.get(name= request.GET['tag'])        
        pagequerydict = TaggedItem.objects.get_by_model(pushitem, thistag)
        pagequerydict = pagequerydict.filter(language=request.LANGUAGE_CODE)
        message = LANGUAGE['taggedwith'] % str(thistag) # 'tagged with '+ str(thistag)
        r = makepage(request,pagequerydict,{'tag': request.GET['tag'], 'title':str(thistag),'showall':False, 'message': message,}, template='tags.html')
        return r
    except:
        return catalogue(request,LANGUAGE['notagspecified'])


def tagcloud(threshold=0, maxsize=1.75, minsize=.75):
    """usage:
        -threshold: Tag usage less than the threshold is excluded from
            being displayed.  A value of 0 displays all tags.
        -maxsize: max desired CSS font-size in em units
        -minsize: min desired CSS font-size in em units
    Returns a list of dictionaries of the tag, its count and
    calculated font-size.
    """
    counts, taglist, tagcloud = [], [], []
    tags = Tag.objects.all()
    for tag in tags:
        count = tag.items.count()
        count >= threshold and (counts.append(count), taglist.append(tag))
    maxcount = max(counts)
    mincount = min(counts)
    constant = log(maxcount - (mincount - 1))/(maxsize - minsize or 1)
    tagcount = zip(taglist, counts)
    for tag, count in tagcount:
        size = log(count - (mincount - 1))/constant + minsize
        tagcloud.append({'tag': tag, 'count': count, 'size': round(size, 7)})
    return tagcloud

@ajax_required
def is_field_available(request):
    """XMLHttpRequest with ?username='name_to_test' or ?email='email_to_test'
    returns True or False"""
    if request.method == "GET":
        get = request.GET.copy()
        if get.has_key('username'):
            name = get['username']
            if User.objects.filter(username__iexact=name):
                return HttpResponse(False)
            else:
                return HttpResponse(True)
        if get.has_key('email'):
            email = get['email']
            if User.objects.filter(email__iexact=email):
                return HttpResponse(False)
            else:
                return HttpResponse(True)

    return HttpResponseServerError(_("Requires username or email to test"))

def statistics(request, flip):
    flip = get_object_or_404(pushitem, pk=flip)
    if flip.type == 3:
        # if this is a comment, then get it's parent push
        flip = pushitem.objects.filter(comment=flip)
    context = {'push': flip,
               'showall': True,
               'title': flip.title,
               'ballotitems': flip.ballotitem_set.all()
               }
    
    # ballot items (names)
    ballots_name = [value['name'] for value in flip.ballotitem_set.all().values('name')]
    ballots_name_template = []
    
    by_total = {}
    by_country = {}
    by_age = {}
    by_gender = {}
     
    total_options = len(ballots_name)
    for name in ballots_name:
        if len(name) > 6:
            ballots_name_template.append(('%s...'%name[:3], name))
        else:
            ballots_name_template.append((name, name))
            
        by_total['counter'] = [0]*total_options
        by_total['percents'] = [0]*total_options

    total = flip.votes_total        
    by_total['total'] = total
        
    voters = pushitem_voter.objects.filter(pushitem=flip)
    
    unit_percent = (1*100.0/total)
    
    for voter in voters:
        option = voter.voted_for.name
        profile = voter.user.userprofile_set.all()[0] # getting profile
        
        if option in ballots_name:
            index = ballots_name.index(option)
        else:
            index = -1
            
        if index >= 0:
            # counting option
            by_total['counter'][index] += 1
            by_total['percents'][index] += unit_percent
            
            country = profile.get_country_display()
            gender = profile.get_gender_display()
            
            if country in by_country:
                by_country[country]['total'] += unit_percent
            else:
                by_country[country] = {'total': unit_percent, 'list': [0]*total_options}
            by_country[country]['list'][index] += unit_percent
                
            if gender in by_gender:
                by_gender[gender]['total'] += unit_percent
            else:
                by_gender[gender] = {'total': unit_percent, 'list': [0]*total_options}
            by_gender[gender]['list'][index] += unit_percent
            
            try:
                age = profile.age()
                if age in by_age:
                    by_age[age]['total'] += unit_percent
                else:
                    by_age[age] = {'total': unit_percent, 'list': [0]*total_options}
                by_age[age]['list'][index] += unit_percent
            except:
                pass
            
    # dict to list    
    by_age = [(key, by_age[key]['total'], by_age[key]['list']) for key in by_age]
    by_gender = [(key, by_gender[key]['total'], by_gender[key]['list']) for key in by_gender]
    by_country = [(key, by_country[key]['total'], by_country[key]['list']) for key in by_country]
    
    context['by_age'] = by_age
    context['by_total'] = by_total
    context['by_gender'] = by_gender
    context['by_country'] = by_country
    context['ballotnames'] = ballots_name_template
    
    return render_to_response('statistic.html', RequestContext(request, context))

