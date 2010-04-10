from django.core.management import setup_environ
from zaza import settings
from zaza.ui.models import *
import time

setup_environ(settings)

while True:
  users = User.objects.filter(stale=True)
  for user in users:
    print "Updating recommendations for %s" % user.username
    user.storeRecommendations()
    user.stale = False
    user.save()
  time.sleep(10)
