import imp
import json
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
from .forms import ContactForm
def category(request, pk=None):
    
    objectcarousel = Category.objects.get(pk=pk).post.order_by('-created_date')[:7]
    objects = Category.objects.get(pk=pk).post.order_by('-created_date')[:7]
    objectstrend = Category.objects.get(pk=pk).post.order_by('-views')[:10]
    print('____________',objectcarousel, '____________')
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

    return render(template_name='postapp/category.html',request=request, context=context)
def home(request,pk=None):
    # objects = Post.objects.all()
    # pages = Paginator(object_list=objects, per_page=1)
    # paginator_page = request.GET.get('list')
    # page_objects = pages.get_page(paginator_page)
    
    if pk==None:
        objectcarousel = Post.objects.all().order_by('-created_date')[:7]
        objects = Post.objects.all().order_by('-created_date')[:7]
        objectstrend = Post.objects.all().order_by('-views')[:10]
    
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
    bgimages = BackGroundHeader.objects.all()
   

    context = {'objects':objects, 'objectcarousel':objectcarousel, 'categories':categories, 'objectstrend':objectstrend, 'bgimages':bgimages}

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
    print(post, request.user)
    likesentobj = Like.objects.filter(post=post, author=request.user)
    print(likesentobj)
    context = {'post':post, 'latestnews':latestnews, 'comments':comments,'tags':tags}
    if likesentobj:
        if likesentobj[0].like:
            context['like']=True
        elif  not likesentobj[0].like:
            context['like']=False
    else:
        context['like']=None
    print(context)
    hit_count = get_hitcount_model().objects.get_for_object(post)
    hits = hit_count.hits
   
    print(hits)
  
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    hitcontext = context['hitcount'] = {'pk': hit_count.pk, 'hits':hits}
    
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext = context['hitcount'] = {'pk': hit_count.pk, 'hits':hits}
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits
       
    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if request.POST.get('body'):
            parrentcomment = None
            
            if request.POST.get('parent_comment'):
                parrentcomment = Comment.objects.get(id=request.POST.get('parent_comment'))    
            comment =Comment.objects.create(author=request.user, parent_comment=parrentcomment, post = Post.objects.get(pk=pk),body = request.POST.get('body') )

            return HttpResponseRedirect(request.path_info)
        elif is_ajax:
            print('_____got ajax___')
            try:
                Likeobj = Like.objects.get(post=post, author=request.user)
            except:
                Likeobj=False
            print(Likeobj)
            if Likeobj:
                if Likeobj.like:
                    Likeobj.like = False
                    Likeobj.save()
                    return JsonResponse({'like': False})
                else:
                    Likeobj.delete()
                    
                    return JsonResponse({'like': None})
            else:
                # create new likeDislike
                Like.objects.create(post=post, author=request.user, like=True)
                return JsonResponse({'like':True})  

            print('______',request.POST)
                
     
    return render(request=request, template_name='postapp/single-blog.html', context=context)

    
def contact(request):
    if request.method =="GET":
        print('__post_')
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            form = ContactForm(request.GET)
            if form.is_valid():
                form.save()
                message = 'Your message is save to data base!'
                
                return JsonResponse({'result':True, 'message':message})
            print(form)
            print(request.GET)
            message = 'we must enter all dates'
           
            return JsonResponse({'result':False, 'message':message})
    return render(request=request, template_name='postapp/contact.html')   
