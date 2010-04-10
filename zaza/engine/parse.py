import codecs
import operator
import sys

ratings_ = []
books_ = {}
users_ = {}

def LoadRatings(filename, skip_first=True):
  ratings = []
  f = codecs.open(filename, "r", "utf8")
  count = 0
  for line in f:
    count += 1
    if skip_first and count == 1:
      continue
    line = line.strip()
    tokens = line.split(";")
    if len(tokens) == 3:
      user, book, rating = tokens
    elif len(tokens) == 2:
      user, book = tokens
      rating = "0"
    else:
      continue
    user = user.strip("\"")
    book = book.strip("\"")
    rating = rating.strip("\"")
    try:
      rating = int(rating)
    except:
      continue
    ratings.append((user, book, rating))
  print "Ratings Loaded : %s" % len(ratings)
  f.close()
  return ratings

def LoadBooks(filename, skip_first=True):
  books = {}
  f = codecs.open(filename, "r", "utf8")
  count = 0
  for line in f:
    count += 1
    if skip_first and count == 1:
      continue
    line = line.strip()
    tokens = line.split(";")
    if len(tokens) >= 5:
      book, title, author, year, publisher = tokens[:5]
      book = book.strip("\"")
      title = title.strip("\"")
      author = author.strip("\"")
      year = year.strip("\"")
      publisher = publisher.strip("\"")
      if len(tokens) >=6:
        imgs = tokens[5].strip("\"")
      else:
        imgs = None
      if len(tokens) >=7:
        imgm = tokens[6].strip("\"")
      else:
        imgm = None
      if len(tokens) >=8:
        imgl = tokens[7].strip("\"")
      else:
        imgl = None
      books[book] = (book, title, author, year, publisher, imgs, imgm, imgl)
  print "Books Loaded : %s" % len(books.keys())
  f.close()
  return books

def LoadUsers(filename, skip_first=True):
  users = {}
  f = codecs.open(filename, "r", "utf8", "ignore")
  count = 0
  for line in f:
    count += 1
    if skip_first and count == 1:
      continue
    line = line.strip()
    tokens = line.split(";")
    if len(tokens) >= 3:
      # user, location, age
      user, location, age = tokens[:3]
      user = user.strip("\"")
      location = location.strip("\"")
      age = age.strip("\"")
      users[user] = (user, location, age)
  print "Users Loaded : %s" % len(users.keys())
  f.close()
  return users

def printBook(book):
  if book in books_:
    print "ISBN:%s\tTitle:%s\tAuthor:%s\tYear:%s\tPublisher:%s" % books_[book]
  else:
    print "Book not found : %s" % book

def printUser(user):
  if user in users_:
    print "User:%s\tLocation:%s\tAge:%s" % users_[user]
  else:
    print "User not found : %s" % user

def printRating(rating):
  printBook(rating[1])
  printUser(rating[0])
  print "Rating: %s\n" % rating[2]

def prune():
  print "Pruning dataset"
  books = {}
  users = {}
  selected_books = {}
  selected_users = {}
  for rating in ratings_:
    users[rating[0]] = users.get(rating[0], 0) + 1
    books[rating[1]] = books.get(rating[1], 0) + 1
  count = 1000
  f = codecs.open("data/books.csv", "w", "utf8")
  for book in sorted(books.iteritems(), key=operator.itemgetter(1), reverse=True):
    if count > 0:
      if book[0] not in books_:
        continue
      f.write("%s;%s;%s;%s;%s;%s;%s;%s\n" % books_[book[0]])
      selected_books[book[0]] = True
      count -= 1
    else:
      break
  f.close()
  count = 1000
  f = codecs.open("data/users.csv", "w", "utf8")
  for user in sorted(users.iteritems(), key=operator.itemgetter(1), reverse=True):
    if count > 0:
      if user[0] not in users_:
        continue
      f.write("%s;%s;%s\n" % users_[user[0]])
      selected_users[user[0]] = True
      count -= 1
    else:
      break
  f.close()
  f = codecs.open("data/ratings.csv", "w", "utf8")
  for rating in ratings_:
    if rating[0] in selected_users and rating[1] in selected_books:
      f.write("%s;%s;%s\n" % rating)
  f.close()


if __name__ == '__main__':
  ratings_ = LoadRatings("engine/data/BX-Book-Ratings.csv", True)
  books_ = LoadBooks("engine/data/BX-Books.csv", True)
  users_ = LoadUsers("engine/data/BX-Users.csv", True)
  prune()
else:
  ratings_ = LoadRatings("engine/data/ratings.csv", False)
  books_ = LoadBooks("engine/data/books.csv", False)
  users_ = LoadUsers("engine/data/users.csv", False)
