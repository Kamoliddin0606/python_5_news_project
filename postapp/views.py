import imp
import numbers
from operator import imod
import re
from turtle import pos
from unicodedata import category
from venv import create
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from .models import *
from django.http import HttpResponseRedirect
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin
from django.views.decorators.csrf import csrf_exempt
def home(request):
    # objects = Post.objects.all()
    # pages = Paginator(object_list=objects, per_page=1)
    # paginator_page = request.GET.get('list')
    # page_objects = pages.get_page(paginator_page)
    objectcarousel = Post.objects.all().order_by('-created_date')[:7]
    objects = Post.objects.all().order_by('-created_date')[:7]
    objectstrend = Post.objects.all().order_by('-views')[:10]
    print(objectstrend)
    catsecond =''
    if Category.objects.all().count() <7 :
        catfirst = Category.objects.all()
    else:
        catfirst = Category.objects.all()[:6]
        catsecond = Category.objects.all()[6:]
    categories ={ 
        'catfirst':catfirst,
        'catsecond':catsecond,
        
    }


    context = {'objects':objects, 'objectcarousel':objectcarousel, 'categories':categories, 'objectstrend':objectstrend,}

    # return render(request=request, template_name='postapp/index.html', context={'objects':page_objects})

    return render(template_name='postapp/index.html',request=request, context=context)
# Create your views here.
@csrf_exempt
def detailPost(request ,pk):
   
    post = get_object_or_404(Post, pk=pk)
    category = Category.objects.get(pk = post.category_id)
   
    latestnews = Post.objects.filter(category=category)[:3]
   
    comments = post.PostComment.filter(parent_comment=None).order_by('-created')
    tags = post.tags.all()
    context = {'post':post, 'latestnews':latestnews, 'comments':comments,'tags':tags}
    

    hit_count = get_hitcount_model().objects.get_for_object(post)
    hits = hit_count.hits
   
    
  
    hit_count_response = HitCountMixin.hit_count(request, hit_count)

    
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk, 'hits':hits}
    if request.method == 'POST' and request.POST.get('body'):
        
        if request.POST.get('body'):
            parrentcomment = None
            
            if request.POST.get('parent_comment'):
                parrentcomment = Comment.objects.get(id=request.POST.get('parent_comment'))    
            comment =Comment.objects.create(author=request.user, parent_comment=parrentcomment, post = Post.objects.get(pk=pk),body = request.POST.get('body') )

            return HttpResponseRedirect(request.path_info)
    if request.method == 'POST':
        print('_____got ajax___')
        comment = Like.objects.get(post=post, author=request.user)
        if comment:
            if comment.like:
                
                return JsonResponse({'like': False})
            else:
                return JsonResponse({'like': True})
        else:
            # create new likeDislike

            return JsonResponse({'like':True})  

        print('______',request.POST)
            
     
    return render(request=request, template_name='postapp/single-blog.html', context=context)
  