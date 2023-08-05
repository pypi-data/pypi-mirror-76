## Djangosubscribe : Django Reusable app for Email Subscription.

**Djangosubscribe** is a **Reusable Django app** which provides a full featured Email Subscription Model. Djangosubscribe is rich features and powerful enough to start a **Blog** and **News website**, without installation of any 3rd party packages.
___

## Installation :
You can install **Djangosubscribe** from PyPI using **pip**.

``` pip install djangosubscribe ```
___

## Configuration :
***1\. Open the ```settings.py``` module of your project folder, And put djangosubscribe into ```INSTALLED_APPS```.***
```python
INSTALLED_APPS = (
    'djangosubscribe'
)
```

***2\. Open the ```urls.py``` module of your project folder, And include djangosubscribe URLs.***
```python
urlpatterns = [
    ...
    re_path(r'^post/', include('djangosubscribe.urls')),
    ...
]
```

***3\. Setup the Templates for djangosubscribe.***
>> ***Important Note***: djangosubscribe App is a part of Djangoengine project. And if you want to access UI part of Djangoadmin App, You need to configure some Reusable/global templates to your django project or you can create your own templates, It's very easy.
```python
TEMPLATES = [
    ...
    ...
    'DIRS': [os.path.join(BASE_DIR, 'templates'),],
    ...
    ...
]
```

Create the ```templates``` folder inside ```BASE_DIR``` and Then create ```djangoadmin``` folders inside the templates folder.
Then [download](https://www.dropbox.com/sh/na4tzfewub5mhe5/AABmyPHZ3KFZSpC7lH9Uvl5Ya?dl=0) the djangoadmin templates and put them inside the ```djangoadmin``` folder.

***4\. Static files configuration.***
Open your ```settings.py``` module and Configure Static files and media files or you can can use your own configuration.
```python
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static-local'),)
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static-root', 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static-root', 'media')
```

Create the ```static-local``` folder inside ```BASE_DIR```, Then create ```djangoadmin``` folders inside that ```static-local``` folder.
And also [download](https://www.dropbox.com/sh/1jjul5c7kauas3o/AACeEf_OqpnzTe_iqK-r3SNMa?dl=0) the djangoadmin static files and put them inside the ```djangoadmin``` folder.
___

## Complete the Djangosubscribe setup by running the following command in sequence.
```python
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
python manage.py runserver
```
___
