import math
import operator
import parse

meanUserRatings_ = {}
meanBookRatings_ = {}
userRatings_ = {}
bookRatings_ = {}
similarUsers_ = {}
threshold_ = 3

def LoadData():
  global meanUserRatings_
  global meanBookRatings_
  global userRatings_
  global bookRatings_
  count = 0
  for rating in parse.ratings_:
    user, book, vote = rating
    userRatings_.setdefault(user, {})[book] = vote
    bookRatings_.setdefault(book, {})[user] = vote
  for user, bookRating in userRatings_.iteritems():
    meanUserRatings_[user] = float(sum(bookRating.values())) / len(bookRating)
  for book, userRating in bookRatings_.iteritems():
    meanBookRatings_[book] = float(sum(userRating.values())) / len(userRating)

def FindSimilarUsers():
  global similarUsers_
  for user1 in parse.users_.iterkeys():
    similarUsers = {}
    for book in userRatings_.get(user1,{}).keys():
      for user2 in bookRatings_[book].keys():
        similarUsers.setdefault(user2, {})[book] = True
    for user2, books in similarUsers.iteritems():
      if len(books) < threshold_:
        continue
      num = 0
      den1 = 0
      den2 = 0
      for book in books.iterkeys():
        tmp1 = userRatings_[user1][book] - meanUserRatings_[user1]
        tmp2 = userRatings_[user2][book] - meanUserRatings_[user2]
        num += tmp1 * tmp2
        den1 += tmp1 * tmp1
        den2 += tmp2 * tmp2
      if den1 == 0.0 or den2 == 0.0:
        continue
      #print "user1=%s\tuser2=%s\tnum=%3.2f\tden1=%3.2f\tden2=%3.2f" % (user1, user2, num, den1, den2)
      similarUsers_.setdefault(user1, {})[user2] = num / math.sqrt(den1*den2)
      similarUsers_.setdefault(user2, {})[user1] = num / math.sqrt(den1*den2)

def GetRecommendations(user):
  bookScores = {}
  books = {}
  for user2, weight in similarUsers_.get(user,{}).iteritems():
    for book in userRatings_.get(user2,{}).iterkeys():
      books[book] = True
  for book in books.iterkeys():
    bookScores[book] = meanUserRatings_[user]
    for user2, weight in similarUsers_[user].iteritems():
      if user2 == user or book not in userRatings_[user2]:
        continue
      #print "  Checking user %s\tweight %3.2f\tbook=%s" % (user2, weight, book)
      bookScores[book] += weight * (userRatings_[user2][book]-meanUserRatings_[user2])
  return sorted(bookScores, key=operator.itemgetter(1), reverse=True)[:5]


print "Loading data"
LoadData()
print "Finding Similar Users"
FindSimilarUsers()

if __name__ == "__main__":
  print "Recommendations for 274301"
  books = GetRecommendations('274301')
  print "Current books and vote for user 274301"
  for book, score in userRatings_['274301'].iteritems():
    if book in parse.books_:
      print "%s : %s" % (parse.books_[book][1], score)
  print "\nRecommended books"
  for book in books:
    if book in parse.books_:
      print "%s" % (parse.books_[book][1])
