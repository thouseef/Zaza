from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from zaza.ui.models import *

import datetime



def index(request):
  return render_to_response('zaza/index.html')


@login_required
def user(request):
  context = {}
  recos = []
  #username = request.user
  #user = User.objects.get(username__exact=username)
  user = request.user
  context['username'] = user
  context['user'] = user.get_profile()
  context['ratings'] = user.rating_set.order_by('rating').reverse()
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
      r.rec1, r.rec2, r.rec3, r.rec4, r.rec5 = Book.objects.all().extra(order_by=['rating'])[:5]
      r.save()
      return HttpResponseRedirect("/user/")
  else:
    form = UserForm()
  return render_to_response("registration/register.html",{'form':form})


@login_required
def user_profile(request):
  user = request.user.get_profile()
  return render_to_response('zaza/profile.html',user)

def user_profile_edit(request):
  pass

def book_add():
  pass

def book_browse():
  pass

@login_required
def book_view(request, isbn):
  context = {}
  user = request.user.get_profile()
  book = Book.objects.get(isbn = isbn)
  context['username'] = request.user
  context['user'] = user
  context['book'] = book
  context['comments'] = book.comments_set.order_by('date')
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

def results_search():
  pass
