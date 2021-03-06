from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Article(models.Model):
    cat = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        verbose_name="カテゴリ"
    )
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="タグ")
    title = models.CharField(max_length=255, verbose_name="タイトル")
    content = models.TextField(verbose_name="内容", blank=True, null=True)

    def __str__(self):
        return self.title
