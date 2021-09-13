from django.shortcuts import render
import os
from django.http import HttpResponse
from django.db import connections
from django.views.decorators.cache import cache_page
import json
import requests
import logging
from django.core.paginator import Paginator
from ratelimit.decorators import ratelimit
# Create your views here.
# Create the loggers object
logger = logging.getLogger('__name__')

@cache_page(10 * 1)

@ratelimit(key='user', rate='2/10s')
#@ratelimit(key='user', rate='1000/d')

def stack_overflow(request):

    stklnk = []
    PARAMS = {}
    url='https://api.stackexchange.com/2.3/search/advanced?site=stackoverflow'
    logger.error(request.GET)
    print(request.GET)
    if 'title' in request.GET and request.GET['title'] != '':
        PARAMS['title'] = request.GET['title']
    if 'user' in request.GET and request.GET['user'] != '':
        PARAMS['user'] = request.GET['user']
    if 'tagged' in request.GET and request.GET['tagged'] != '':
        PARAMS['tagged'] = request.GET['tagged']
    if 'nottagged' in request.GET and request.GET['nottagged'] != '':
        PARAMS['nottagged'] = request.GET['nottagged']
    if 'sort' in request.GET and request.GET['sort'] != '':
        PARAMS['sort'] = request.GET['sort']
    if 'order' in request.GET and request.GET['order'] != '':
        PARAMS['order'] = request.GET['order']
    try:
       response_api = requests.get(url, verify=False,params = PARAMS)
       json_data = json.loads(response_api.text)
       for a in json_data['items']:
           values = [a['title'],a['link'],a['owner']['display_name']]
           stklnk.append(values)
    except:
        print("Invalid request")
    paginator = Paginator(stklnk, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print(page_obj)
    return render(request, 'teamwave.html', {'stklnk': page_obj})
