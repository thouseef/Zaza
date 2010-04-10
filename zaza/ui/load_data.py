import sys
import zaza.engine.parse as parse
import zaza.engine.recommend as recommend
import zaza.ui.models as models
from django.contrib.auth.models import User
from django.contrib.auth.models import UserManager

def AddBook(book):
  print "Adding book %s" % parse.books_[book][0]
  newbook = models.Book()
  newbook.isbn = parse.books_[book][0]
  newbook.title = parse.books_[book][1]
  newbook.author = parse.books_[book][2]
  newbook.year = parse.books_[book][3]
  newbook.publisher = parse.books_[book][4]
  newbook.imgs = parse.books_[book][5]
  newbook.imgm = parse.books_[book][6]
  newbook.imgl = parse.books_[book][7]
  newbook.save()

def AddUser(username):
  print "Adding user %s" % username
  user = User.objects.create_user(parse.users_[username][0], 'a@b.com', 'password')
  userp = models.UserProfile()
  userp.user = user
  userp.location = parse.users_[username][1]
  if type(parse.users_[username][2]) == type(0):
    userp.age = int(parse.users_[username][2])
  else:
    userp.age = 0
  userp.save()

def AddRating(user, book, rating):
  print "Adding rating %s:%s:%s" % (user, book, rating)
  newrating = models.Rating()
  try:
    bookobj = models.Book.objects.get(isbn__exact=book)
    userobj = User.objects.get(username__exact=user)
    newrating.user = userobj
    newrating.book = bookobj
    newrating.rating = rating
    newrating.save()
  except Exception:
    print >>sys.stderr, "Skipping %s:%s:%s" % (user, book, rating)

def LoadData():
  for user in parse.users_:
    AddUser(user)
  for book in parse.books_:
    AddBook(book)
  for user, book, rating in parse.ratings_:
    AddRating(user, book, rating)

def LoadRecommendations():
  for user in parse.users_:
    print "Generating recommendations for user %s" % user
    books = recommend.GetRecommendations(user)
    recommends = models.Recommends()
    recommends.user = User.objects.get(username__exact=user)
    if len(books) >= 1:
      recommends.rec1 = models.Book.objects.get(isbn__exact=books[0])
    if len(books) >= 2:
      recommends.rec2 = models.Book.objects.get(isbn__exact=books[1])
    if len(books) >= 3:
      recommends.rec3 = models.Book.objects.get(isbn__exact=books[2])
    if len(books) >= 4:
      recommends.rec4 = models.Book.objects.get(isbn__exact=books[3])
    if len(books) >= 5:
      recommends.rec5 = models.Book.objects.get(isbn__exact=books[4])
    recommends.save()

LoadData()
LoadRecommendations()
