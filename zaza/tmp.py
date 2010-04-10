from zaza.ui.models import *

user = User.objects.get(username="274301")
books = user.get_profile().getRecommendations()
print "\nRecommended books"
for book in books:
  tmp = Book.objects.filter(isbn=book)
  if len(tmp)<1:
    continue
  print "%s:%s" % (tmp[0].isbn,tmp[0].title)
