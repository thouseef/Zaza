from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from zaza.ui.models import *
from django.contrib import auth
from django.core.paginator import Paginator, InvalidPage, EmptyPage

import datetime
import random



def index(request):
  context = {}
  if request.user.is_authenticated():
    user = request.user.get_profile()
    context = {'cuser':user,'cusername':request.user,'logged_in':True}
  else:
    context = {'logged_in':False}
  ratings = Rating.objects.all().order_by('rating')[:20]
  context['book1'] = ratings[random.randint(0,19)].book
  context['book2'] = ratings[random.randint(0,19)].book
  return render_to_response('zaza/index.html',context)

def logout(request):
  if request.user.is_authenticated():
    context = {'cuser':request.user}
    auth.logout(request)
    return render_to_response('zaza/logout.html',context)
  else:
    return HttpResponseRedirect('/')


def user(request):
  if not request.user.is_authenticated():
    return HttpResponseRedirect('/')
  user = request.user
  return show_user(request, user, user)

def other_user(request, uname):
  user = User.objects.filter(username=uname)[0]
  return show_user(request, request.user, user)

def show_user(request, cuser, user):
  context = {}
  recos = []
  if "page" in request.GET:
    page = int(request.GET["page"])
  else:
    page = 0
  #username = request.user
  #user = User.objects.get(username__exact=username)
  context['logged_in'] = True
  context['cusername'] = cuser
  context['cuser'] = cuser.get_profile()
  context['user'] = user.get_profile()
  ratings = user.rating_set.order_by('rating').reverse()
  if ((len(ratings)-1) / 5) > page:
    context['next'] = True
  context['npage'] = page+1
  if page > 0:
    context['prev'] = True
  context['ppage'] = page-1
  context['pages'] = (len(ratings) / 5) + 1
  context['ratings'] = ratings[5*page:5*(page+1)]
  recos = user.recommends_set.all()
  context['recos'] = []
  if len(recos) >= 1:
    recos=recos[0]
    context['recos'].append(recos.rec1)
    context['recos'].append(recos.rec2)
    context['recos'].append(recos.rec3)
    context['recos'].append(recos.rec4)
    context['recos'].append(recos.rec5)
  return render_to_response('zaza/user.html',context)


def user_reg(request):
  if request.method == 'POST':
    response = {}
    form = UserForm(request.POST)
    if form.is_valid():
      data = form.cleaned_data
      user = User.objects.create_user(data['username'], data['email'], data['password'])
      user.first_name = data['first_name']
      user.last_name = data['last_name']
      user.save()
      userprofile = UserProfile()
      userprofile.location = data['location']
      userprofile.age = data['age']
      userprofile.user = user
      userprofile.save()
      r = Recommends()
      r.user = user
      pbooks = userprofile.getPopularBooks()
      r.rec1 = Book.objects.get(isbn=pbooks[0][0])
      r.rec2 = Book.objects.get(isbn=pbooks[1][0])
      r.rec3 = Book.objects.get(isbn=pbooks[2][0])
      r.rec4 = Book.objects.get(isbn=pbooks[3][0])
      r.rec5 = Book.objects.get(isbn=pbooks[4][0])
      r.save()
      response.update({'success': True})
    else:
      response.update({'success': False})
      response.update({'errors':form.errors})
      response.update({'form':form})
    return render_to_response("registration/success.html",response)
  else:
    form = UserForm()
  return render_to_response("registration/register.html",{'form':form})


@login_required
def user_profile(request):
  user = request.user.get_profile()
  return render_to_response('zaza/profile.html',user)

def user_update(request):
  pass
  

def book_add():
  pass

def book_browse():
  pass

@login_required
def del_rating(request, isbn):
  context = {}
  u = request.user
  Rating.objects.get(user__username=u.username, book__isbn=isbn).delete()
  userp = u.get_profile()
  userp.stale=True
  userp.save()
  return user(request)
  

def book_rated(request):
  context = {}
  user = request.user
  context['logged_in'] = True
  context['cusername'] = user
  context['cuser'] = user.get_profile()
  ratings_list = user.rating_set.order_by('rating').reverse()
  paginator = Paginator(ratings_list,10)

  try:
    page = int(request.GET.get('page','1'))
  except ValueError:
    page = 1

  try:
    ratings = paginator.page(page)
  except (EmptyPage, InvalidPage):
    ratings = paginator.page(paginator.num_pages)

  context['rating'] = ratings
  return render_to_response('zaza/view_rated.html',context)

    
@login_required
def book_view(request, isbn):
  context = {}
  if "page" in request.GET:
    page = int(request.GET["page"])
  else:
    page = 0
  user = request.user.get_profile()
  book = Book.objects.get(isbn = isbn)
  context['logged_in'] = True
  context['cusername'] = request.user
  context['cuser'] = user
  context['book'] = book
  context['avgrating'] = "%.1f" % book.getMeanRating()
  context['comments'] = book.comments_set.order_by('date')
  ratings = book.rating_set.order_by('rating').reverse()
  if ((len(ratings)-1) / 5) > page:
    context['next'] = True
  context['npage'] = page+1
  if page > 0:
    context['prev'] = True
  context['ppage'] = page-1
  context['pages'] = (len(ratings) / 5) + 1
  context['ratings'] = ratings[5*page:5*(page+1)]
  return render_to_response("zaza/book.html",context)

def view_rating(request, isbn):
  context = {}
  user = request.user.get_profile()
  book = Book.objects.get(isbn = isbn)
  if user.isBookRated(isbn):
    context['rating'] = user.getBookRating(isbn)
  else:
    context['rating'] = 0
  return render_to_response("zaza/rating.html",context)

@login_required
def add_rating(request, isbn, rating):
  xhr = request.GET.has_key('xhr')
  user = request.user
  if user.get_profile().isBookRated(isbn):
    rating_obj = user.rating_set.get(book__isbn=isbn)
  else:
    rating_obj = Rating()
    rating_obj.book = Book.objects.get(isbn=isbn)
    rating_obj.user = user
  rating_obj.rating = rating
  rating_obj.save()
  userp = user.get_profile()
  userp.stale=True
  userp.save()
  if xhr:
    pass
  else:
    return HttpResponseRedirect("/book/"+isbn+"/rating")
  

@login_required
def add_comment(request, isbn):
  if request.method == 'POST':
    form = CommentsForm(request.POST)
    if form.is_valid():
      new_comment = form.save(commit=False)
      new_comment.user = request.user
      new_comment.book = Book.objects.get(isbn = isbn)
      new_comment.save()
      return HttpResponseRedirect("/book/"+isbn)
  else:
    form = CommentsForm()
  return render_to_response("zaza/comment.html",{'form':form})

def edit_comment(request, isbn, id):
  book = Book.objects.get(isbn = isbn)
  user = request.user
  comment = book.comments_set.get(id=id)
  if request.GET.get("action","edit") == 'edit':
    if request.method == 'POST':
      form = CommentsForm(request.POST,instance = comment)
      if form.is_valid():
        form.save()
        return HttpResponseRedirect("/book/"+isbn)
    else:
      form = CommentsForm(instance = comment)
      return render_to_response("zaza/comment.html",{'form':form})
  elif request.GET.get("action","edit") == 'delete':
    comment.delete()
    return HttpResponse("")


def search(request):
  context = {}
  if "page" in request.GET:
    page = int(request.GET["page"])
  else:
    page = 0
  if request.user.is_authenticated():
    user = request.user.get_profile()
    context = {'cuser':user,'cusername':request.user,'logged_in':True}
  else:
    context = {'logged_in':False}
  if request.method == 'GET':
    query = request.GET['query']
    context["query"] = query
    books = Book.objects.filter(Q(title__contains=query) | Q(author__contains=query)).distinct()
    if ((len(books)-1) / 5) > page:
      context['next'] = True
    context['npage'] = page+1
    if page > 0:
      context['prev'] = True
    context['ppage'] = page-1
    context['pages'] = (len(books) / 5) + 1
    context['books'] = books[5*page:5*(page+1)]
  else:
    return render_to_response("zaza/nosearch.html", context)

  return render_to_response("zaza/search.html", context)

