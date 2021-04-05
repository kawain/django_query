# Django の query の説明用

```
git clone https://github.com/kawain/django_query.git

cd django_query
```

## 新規に作る場合

```
django-admin startproject django_query .
```

settings.py の日本語日本時間設定

```
LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'
```

gitignore を作成

```
*.vscode
*__pycache__
*.sqlite3
```

データベース作成(Djangoで用意している11個のテーブルができる)

```
python manage.py migrate
```

スーパーユーザー作成

```
python manage.py createsuperuser
```

開発用サーバー起動

```
python manage.py runserver
```

http://127.0.0.1:8000/

スーパーユーザーでログイン

http://127.0.0.1:8000/admin/

