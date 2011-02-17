from myproject.salcat.models import pushitem, ballotitem, Tag
from myproject.salcat.forms import commentForm
from django import template
from django.conf import settings
from django.db.models import Q
from django.template import Library, Node
import logging
import random

register = template.Library()

# configure logger
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')

@register.inclusion_tag('format_list_tag.html')
def format_list(input_list):
    return { 'unformatted_list':input_list, }

@register.inclusion_tag('format_pushitem_tag.html', takes_context=True)
def format_push_item(context):
    '''
    is this an extensive push item,(is showall is true,) or is it a summary? (=0)
    
    Retrieves parameters from the existing template context. Expects:
    
    push: The push to render
    user: The user viewing the page, not the push owner. Can be anonymous.
    showall: False will truncate push background
    '''
    # instead of taking parameters, we pull from the original context
    # (takes_context=True in registration tag)
    push=context['push']
    user=context['user']
    showall=context['showall']
    
    logging.debug("Rendering push item %s" % push)
    logging.debug("User: %s" % user)
    if user and user.is_authenticated():
        logging.debug("%s Is authenticated" % user)
    else:
        logging.debug("%s is NOT authenticated" % user)
    
    commentform = commentForm() # A form bound to the POST data
    
    showballotsummary = True
    if (push.type == 2 or push.type == 1) and showall: # for the multi push, don't show the small ballot area in the full view (it's shown in full later)
        showballotsummary = False

    thiscommentqueryset = push.comment.all()
    comment_count = thiscommentqueryset.count()
    opposingcomments = push.opposingcomments(user)
    
    return { 
             'input_push':push,
             'showall' : showall,
             'commentform':commentform,
             'MEDIA_URL':settings.MEDIA_URL,
             'SITE_URL':settings.SITE_URL,
             'showballotsummary':showballotsummary,
             'commentset': thiscommentqueryset,
             'opposingcomments': opposingcomments,
             'user': user,
             'comment_count':comment_count,
            }

@register.inclusion_tag('most_popular.html')
def most_popular(lang):
    '''
        Most popular list
    '''
    from django.db.models import Max
    listings = pushitem.objects.all().filter(language=lang[:2]).order_by('-votes_total')[:10]    
    return{
        'listings': listings,
        'title': 'pushidlist',
        'url': settings.SITE_URL + '/item/',
        }


maxsize =220 # maximum size of the most popular tag
minsize = 55 # minimum size of the least popular tag

class LatestTagsNode(Node):
        def gen_clouds(self):
                p=Tag.objects.all()
                #max1=max([int(p-item.video_set.count()) for p-item in p])
                max1=2

                for i in range(p.count()):
                        size =int(round(int(p[i].video_set.count())*maxsize/max1))
                        if size<minsize:
                                size=minsize
                        cloudsize =str(size) +"%"
                        p[i].cloudsize=cloudsize
                return p

        def render(self, context):
                self.__init__()
                context['content_tagclouds'] = self.gen_clouds()
                return ''

def get_latest_cloudtag(parser, token):

        return LatestTagsNode()
get_latest_cloudtag= register.tag(get_latest_cloudtag)

######################
# from django tagging

from django.db.models import get_model

class TagCloudForModelNode(Node):
    def __init__(self, model, context_var, **kwargs):
        self.model = model
        self.context_var = context_var
        self.kwargs = kwargs

    def render(self, context):
        model = get_model(*self.model.split('.'))
        if model is None:
            raise TemplateSyntaxError(_('tag_cloud_for_model tag was given an invalid model: %s') % self.model)
        context[self.context_var] = \
            Tag.objects.cloud_for_model(model, **self.kwargs)[:10]
        return ''

def do_tag_cloud_for_model(parser, token):
    """
    Retrieves a list of ``Tag`` objects for a given model, with tag
    cloud attributes set, and stores them in a context variable.

    Usage::

       {% tag_cloud_for_model [model] as [varname] %}

    The model is specified in ``[appname].[modelname]`` format.

    Extended usage::

       {% tag_cloud_for_model [model] as [varname] with [options] %}

    Extra options can be provided after an optional ``with`` argument,
    with each option being specified in ``[name]=[value]`` format. Valid
    extra options are:

       ``steps``
          Integer. Defines the range of font sizes.

       ``min_count``
          Integer. Defines the minimum number of times a tag must have
          been used to appear in the cloud.

       ``distribution``
          One of ``linear`` or ``log``. Defines the font-size
          distribution algorithm to use when generating the tag cloud.

    Examples::

       {% tag_cloud_for_model products.Widget as widget_tags %}
       {% tag_cloud_for_model products.Widget as widget_tags with steps=9 min_count=3 distribution=log %}

    """
    bits = token.contents.split()
    len_bits = len(bits)
    if len_bits != 4 and len_bits not in range(6, 9):
        raise TemplateSyntaxError(_('%s tag requires either three or between five and seven arguments') % bits[0])
    if bits[2] != 'as':
        raise TemplateSyntaxError(_("second argument to %s tag must be 'as'") % bits[0])
    kwargs = {}
    if len_bits > 5:
        if bits[4] != 'with':
            raise TemplateSyntaxError(_("if given, fourth argument to %s tag must be 'with'") % bits[0])
        for i in range(5, len_bits):
            try:
                name, value = bits[i].split('=')
                if name == 'steps' or name == 'min_count':
                    try:
                        kwargs[str(name)] = int(value)
                    except ValueError:
                        raise TemplateSyntaxError(_("%(tag)s tag's '%(option)s' option was not a valid integer: '%(value)s'") % {
                            'tag': bits[0],
                            'option': name,
                            'value': value,
                        })
                elif name == 'distribution':
                    if value in ['linear', 'log']:
                        kwargs[str(name)] = {'linear': LINEAR, 'log': LOGARITHMIC}[value]
                    else:
                        raise TemplateSyntaxError(_("%(tag)s tag's '%(option)s' option was not a valid choice: '%(value)s'") % {
                            'tag': bits[0],
                            'option': name,
                            'value': value,
                        })
                else:
                    raise TemplateSyntaxError(_("%(tag)s tag was given an invalid option: '%(option)s'") % {
                        'tag': bits[0],
                        'option': name,
                    })
            except ValueError:
                raise TemplateSyntaxError(_("%(tag)s tag was given a badly formatted option: '%(option)s'") % {
                    'tag': bits[0],
                    'option': bits[i],
                })
    return TagCloudForModelNode(bits[1], bits[3], **kwargs)

register.tag('tag_cloud_for_model1', do_tag_cloud_for_model)