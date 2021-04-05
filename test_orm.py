import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_query.settings")

import django  # noqa
from django.db.models.functions import Concat  # noqa
from django.db.models import Count, TextField  # noqa
from django.db.models import Q, Value  # noqa

django.setup()

# ※注意　モデルのインポートは ↓ django.setup()の後にする
from blog.models import Category, Tag, Article  # noqa


#
# Django ORMの勉強
#

def f1():
    obj = Category()
    obj.name = "Python"
    obj.save()


def f2():
    qs = Category.objects.all()
    print(qs)
    print(qs[0].id)
    print(qs[0].name)


f2()
