from zaza.ui.models import *


def GetRecommendations(user):
  books = {}
  for user2, weight in user.getSimilarUsers():
    for book in user2.getBooks():
      books[book] = True
  for book in books.iterkeys():
    bookScores[book] = user.getMeanRating()
    for user2, weight in user.getSimilarUsers():
      if user2 == user or not user2.isBookRated(book):
        continue
      bookScores[book] += weight * (user2.getBookRating(book) - user2.getMeanRating())
  return sorted(bookScores, key = operator.itemgetter(1), reverse=True)[:5]
