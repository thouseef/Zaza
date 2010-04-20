import operator
import math
import random
from django.db import models
from django.forms import ModelForm, CharField, IntegerField, Textarea, PasswordInput, EmailField
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
from django.db.models import Avg, Count

class UserProfile(models.Model):
  user = models.ForeignKey(User, unique=True)
  #uid = models.IntegerField(blank = True,unique = True)
  location = models.CharField(max_length = 80)
  age = models.IntegerField(blank = True)
  stale = models.BooleanField(True)
  
  def __unicode__(self):
    return self.user.username

  def getBooks(self):
    books = Book.objects.filter(rating__user__username = self.user.username)
    return map(lambda x:x.isbn, books)

  def isBookRated(self, book):
    if len(self.user.rating_set.filter(book__isbn = book)) < 1:
      return False
    return True
    
  def getBookRating(self, book):
    return self.user.rating_set.get(book__isbn = book).rating

  def getMeanRating(self):
    avg = self.user.rating_set.all().aggregate(Avg('rating')).get('rating__avg', 0.0)
    if not avg:
      avg = 0.0
    if avg > 5:
      return avg - 0.5
    else:
      return avg + 0.5
    

  def getSimilarUsers(self):
    def getSimilarUsers_(books, susers, threshold):
      users = susers.filter(common_book_count__gt=threshold)
      users = users.exclude(username = self.user.username)
      return users
    sim_users = {}
    books = Book.objects.filter(rating__user__username = self.user.username)
    susers = User.objects.filter(rating__book__in = books)
    susers = susers.annotate(common_book_count=Count('username'))
    threshold = 0
    print "  Finding an optimal user threshold..."
    i = 0
    while i < 100:
      if i == 0:
        i += 1
      else:
        i *= 2
      threshold = i
      users = getSimilarUsers_(books, susers, threshold)
      if users.count() < 10:
        threshold = (3 * i) / 4
        users = getSimilarUsers_(books, susers, threshold)
        if users.count() < 5:
          threshold = i / 2
          users = getSimilarUsers_(books, susers, threshold)
        break
    if threshold == 0 and users.count() == 0:
      return sim_users
    if users.count() == 0:
      threshold -= 1
      users = getSimilarUsers_(books, susers, threshold)
    print "   found threshold = %s" % threshold
    for user in users:
      num = den1 = den2 = 0
      for book in Book.objects.select_related('rating').filter(rating__user__username = self.user.username,
                                                               rating__user__username = user.username):
        if not self.isBookRated(book.isbn) or not user.get_profile().isBookRated(book.isbn):
          continue
        rating1 = self.getBookRating(book.isbn)
        rating2 = user.get_profile().getBookRating(book.isbn)
        tmp1 = rating1 - self.getMeanRating()
        tmp2 = rating2 - user.get_profile().getMeanRating()
        num += tmp1 * tmp2
        den1 += tmp1 * tmp1
        den2 += tmp2 * tmp2
      if num == 0.0 or den1 == 0.0 or den2 == 0.0:
        continue
      sim_users[user] = num / math.sqrt(den1*den2)
    print "    number of similar users is  %s" % len(sim_users)
    return sim_users

  def getRecommendations(self):
    books = {}
    bookScores = {}
    similarUsers = self.getSimilarUsers()
    for user2, weight in similarUsers.iteritems():
      for book in user2.get_profile().getBooks():
        books[book] = books.get(book, 0) + 1
    print "  Considering %s books" % len(books),
    for i in range(50):
      threshold = i
      newbooks = filter(lambda x: x[1]>threshold, books.iteritems())
      if len(newbooks) < 50:
        break
    if len(newbooks) == 0:
      threshold -= 1
      newbooks = filter(lambda x: x[1]>threshold, books.iteritems())
    print " pruned to %s books using threshold %s" % (len(newbooks), threshold)
    for book, count in newbooks:
      if self.isBookRated(book):
        continue
      bookScores[book] = self.getMeanRating()
      for user2, weight in similarUsers.iteritems():
        if user2 == self.user or not user2.get_profile().isBookRated(book):
          continue
        bookScores[book] += weight * (user2.get_profile().getBookRating(book) - user2.get_profile().getMeanRating())
    return sorted(bookScores.iteritems(), key = operator.itemgetter(1), reverse=True)[:5]

  def storeRecommendations(self):
    books = self.getRecommendations()
    if len(books) < 5:
      pbooks = self.getPopularBooks()
      for i in range(len(pbooks)):
        if len(books) < 5:
          books.append(pbooks[i])
        else:
          break
    recommends = Recommends.objects.filter(user__username=self.user.username)
    if len(recommends) < 1:
      recommends = Recommends()
    else:
      recommends = recommends[0]
    recommends.user = self.user
    if len(books) >= 1:
      recommends.rec1 = Book.objects.get(isbn__exact=books[0][0])
    if len(books) >= 2:
      recommends.rec2 = Book.objects.get(isbn__exact=books[1][0])
    if len(books) >= 3:
      recommends.rec3 = Book.objects.get(isbn__exact=books[2][0])
    if len(books) >= 4:
      recommends.rec4 = Book.objects.get(isbn__exact=books[3][0])
    if len(books) >= 5:
      recommends.rec5 = Book.objects.get(isbn__exact=books[4][0])
    recommends.save()
    return recommends

  def getPopularBooks(self):
    index = []
    while len(index) < 5:
      rand = random.randint(0,19)
      if rand not in index:
        index.append(rand)
    pbooks = Book.objects.all().extra(order_by=['rating'])[:20]
    books = []
    for i in sorted(index):
      books.append((pbooks[i].isbn, 1))
    return books


class UserForm(ModelForm):
  username = CharField(max_length=16)
  password = CharField(max_length=16,widget=PasswordInput)
  email = EmailField(required=True)
  location = CharField(max_length=128)
  age = IntegerField()
  class Meta:
    model = User
    fields = ('username', 'first_name', 'last_name', 'email')


class Book(models.Model):
  isbn = models.CharField(max_length = 20, unique = True)
  title = models.CharField(max_length = 50)
  author = models.CharField(max_length = 50)
  year = models.CharField(max_length = 10)
  publisher = models.CharField(max_length = 50)
  imgs = models.CharField(max_length=512)
  imgm = models.CharField(max_length=512)
  imgl = models.CharField(max_length=512)


  def __unicode__(self):
    return self.title

  def getMeanRating(self):
    return self.rating_set.all().aggregate(Avg('rating')).get('rating__avg', 0.0)


class Rating(models.Model):
  book = models.ForeignKey('Book')
  user = models.ForeignKey(User)
  rating = models.IntegerField(max_length = 2)
  
  def __unicode__(self):
    return self.user.username + ":" + self.book.isbn + ":" + str(self.rating)


class Recommends(models.Model):
  user = models.ForeignKey(User, unique=True)
  rec1 = models.ForeignKey('Book', related_name='rec1_set', null=True)
  rec2 = models.ForeignKey('Book', related_name='rec2_set', null=True)
  rec3 = models.ForeignKey('Book', related_name='rec3_set', null=True)
  rec4 = models.ForeignKey('Book', related_name='rec4_set', null=True)
  rec5 = models.ForeignKey('Book', related_name='rec5_set', null=True)

  def __unicode__(self):
    return self.user.username


class Comments(models.Model):
  book = models.ForeignKey('Book')
  user = models.ForeignKey(User)
  title = models.CharField(max_length = 50)
  body = models.CharField(max_length = 300)
  date = models.DateField(auto_now_add=True)

  def __unicode__(self):
    return self.book.title

class CommentsForm(ModelForm):
  title = CharField(max_length=100)
  body = CharField(widget=Textarea)
  class Meta:
    model = Comments
    fields = ('title','body')
