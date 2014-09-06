from contest.models import Contestant
from django.contrib.auth.models import User
u=User.objects.all()
for i in u:
    try:
        c=Contestant.objects.get(user = i)
    except Exception as e:
        print e
        print i
        if i.is_staff:
            continue
        else:
            i.delete()
