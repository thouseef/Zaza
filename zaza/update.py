from django.core.management import setup_environ
import settings
setup_environ(settings)
from ui.models import *
import time

while True:
  users = UserProfile.objects.filter(stale=True)
  for userp in users:
    print "Updating recommendations for %s" % userp.user.username
    r =  userp.storeRecommendations()
    print "New recommendations are :"
    print " %s:%s" % (r.rec1.isbn, r.rec1.title)
    print " %s:%s" % (r.rec2.isbn, r.rec2.title)
    print " %s:%s" % (r.rec3.isbn, r.rec3.title)
    print " %s:%s" % (r.rec4.isbn, r.rec4.title)
    print " %s:%s" % (r.rec5.isbn, r.rec5.title)
    userp.stale = False
    userp.save()
  time.sleep(1)
