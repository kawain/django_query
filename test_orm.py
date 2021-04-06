import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_query.settings")

import django  # noqa
from django.db.models.functions import Concat  # noqa
from django.db.models import Count, TextField, CharField  # noqa
from django.db.models import Q, Value  # noqa
from tqdm import tqdm  # noqa
import random  # noqa


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


def f6():
    """適当な記事データを作成"""

    with open("data.txt", encoding="utf-8") as f:
        text = f.read()

    text = text.replace("―", "")
    text = text.replace("　", "")
    text = text.replace("「", "")
    text = text.replace("」", "")
    text = text.replace("\r", "")
    text = text.replace("\n", "")
    text_list = text.split("。")

    head = []
    body = []

    for v in text_list:
        if len(v) > 20:
            body.append(v)
        else:
            head.append(v)

    # headをシャッフルしておく
    random.shuffle(head)

    # カテゴリとタグをあらかじめ取得して記憶しておく
    cate_all = Category.objects.all()
    tag_all = Tag.objects.all()

    for v in tqdm(head):
        if v == "":
            continue

        # カテゴリを一つランダムに選ぶ
        cat = random.choice(cate_all)

        # ランダムに複数のタグを選択
        # 抽出数もランダム
        r = random.randint(1, 5)
        tags = random.sample(list(tag_all), r)

        # ランダムに複数のbodyを選択
        bodys = random.sample(body, r)

        # 記事オブジェクト作成
        obj = Article()
        obj.cat = cat
        obj.title = v
        obj.content = "。\n".join(bodys) + "。"
        obj.save()

        # 先にsaveする
        for t in tags:
            # タグの追加方法
            obj.tags.add(t)


def f7():
    """contentの検索"""

    word = "下人"

    count = Article.objects.filter(content__contains=word).count()
    qs = Article.objects.filter(content__contains=word)

    print(f"検索結果:{count}件")
    print("-" * 30)

    for v in qs:
        print(v.content)
        print("-" * 30)


def f8():
    """titleとcontentの普通の検索"""

    word = "下人"

    # and 検索
    qs = Article.objects.filter(title__contains=word, content__contains=word)
    for v in qs:
        print("タイトル：", v.title)
        print("内容：", v.content)
        print("-" * 30)

    print("-" * 80)

    # or 検索
    qs = Article.objects.filter(
        Q(title__contains=word) | Q(content__contains=word)
    )
    for v in qs:
        print("タイトル：", v.title)
        print("内容：", v.content)
        print("-" * 30)


def f9():
    """titleとcontentのannotate,Concat検索"""

    word = "下人"

    qs = Article.objects.annotate(
        search=Concat(
            'title',
            Value(' '),
            'content',
            output_field=TextField(),
        )
    ).filter(search__icontains=word)

    for v in qs:
        print("タイトル：", v.title)
        print("内容：", v.content)
        print("-" * 30)


def f10():
    """カテゴリから記事を抽出"""

    o = Category.objects.all()
    for v in o:
        print(v)
        print(v.article_set.all())
        print("-" * 30)


def f11():
    """cat,tags,title,contentのannotate,Concat検索"""

    word = "tag_10"

    qs = Article.objects.annotate(
        search=Concat(
            'cat__name',
            Value(' '),
            'tags__name',
            Value(' '),
            'title',
            Value(' '),
            'content',
            output_field=TextField(),
        )
    ).filter(search__icontains=word)

    for v in qs:
        print("id：", v.id)
        print("カテゴリ：", v.cat)
        print("タグ：", v.tags.all())
        print("タイトル：", v.title)
        print("内容：", v.content)
        print("-" * 30)


def f12():
    """スペースキーワード対応"""

    # 全角スペースと半角スペースを混ぜる（汚い入力の再現）
    keyword = "　下人　死人 老婆       "
    # keyword = "FORTRAN 屍骸 "
    # keyword = "羅生門 "
    # 入力された文字列の両端の空白を削除
    keyword = keyword.strip()
    # 入力された文字列の全角スペースを半角スペースに置換
    keyword = keyword.replace("　", " ")
    # 半角スペースで区切ってリスト化
    keyword_list = keyword.split()
    # リストの要素が0より大きいときだけ実行
    if len(keyword_list) == 0:
        return

    # Q オブジェクトを作成して
    q_object = Q()
    # キーワード分（リストの長さ分）
    for v in keyword_list:
        # and でつなげる
        q_object.add(Q(search__icontains=v), Q.AND)

    # q_objectを見るとこのようになっている
    # print(q_object)
    # (AND: ('search__icontains', '下人'), ('search__icontains', '死人'), ('search__icontains', '老婆'))

    # タグ以外用のクエリセット
    qs = Article.objects.annotate(
        search=Concat(
            'cat__name',
            Value(' '),
            'title',
            Value(' '),
            'content',
            output_field=TextField(),
        )
    ).filter(q_object)

    # # タグ用のクエリセット
    # q1 = Article.objects.filter(tags__name__in=keyword_list)

    # # クエリセット合算
    # qs = list(qs) + list(q1)
    # qs = set(qs)

    for v in qs:
        print("id：", v.id)
        print("カテゴリ：", v.cat)
        print("タグ：", v.tags.all())
        print("タイトル：", v.title)
        print("内容：", v.content)
        print("-" * 30)


f12()
