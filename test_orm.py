from tqdm import tqdm
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
    """カテゴリ１つ追加"""

    obj = Category()
    obj.name = "Python"
    obj.save()


def f2():
    """カテゴリまとめて追加"""

    a = [
        "Nim",
        "Rust",
        "JavaScript",
        "GO",
        "Java",
        "PHP",
        "C言語",
        "C++",
        "C#",
        "TypeScript",
        "Perl",
        "Swift",
        "Ruby",
        "R",
        "Kotlin",
        "Scala",
        "FORTRAN",
        "LISP",
    ]

    for v in tqdm(a):
        obj = Category()
        obj.name = v
        obj.save()


def f3():
    """カテゴリを全部見る"""

    qs = Category.objects.all()

    for v in qs:
        print(v.id)
        print(v.name)
        print("-" * 20)


def f4():
    """タグを適当に作る"""

    a = [f"tag_{v}" for v in range(1, 11)]

    for v in tqdm(a):
        obj = Tag()
        obj.name = v
        obj.save()


def f5():
    """タグを全部見る"""

    qs = Tag.objects.all()

    for v in qs:
        print(v.id)
        print(v.name)
        print("-" * 20)


f5()
