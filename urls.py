from django.conf.urls.defaults import *
from social_auth import urls
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$','login.views.welcome'),
    (r'^login/$','login.views.userLogin'),
    (r'^logout/$','login.views.userLogout'),
    (r'^autheeror/$','login.views.autherror'),
    (r'^register/$','contest.views.register'),
    (r'^home/$','contest.views.home'),
    (r'^hitlist/$','contest.views.hitlist'),
    (r'^chalakudy/$','contest.views.allcontest'),
    (r'^passed/$','contest.views.passed'),
    (r'^contest/inc/$','contest.views.inc'),
    (r'^level/complete/$','contest.views.level_complete'),
    (r'^level/wrong/$','contest.views.wrong'),
    (r'^bonus/complete/$','contest.views.bonus_complete'),
    (r'^iitb/', include(admin.site.urls)),
    (r'',include(urls)),

)
