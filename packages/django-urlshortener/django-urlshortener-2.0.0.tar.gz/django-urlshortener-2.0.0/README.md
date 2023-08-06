**Django-URLShortener** is a **Reusable Django App**, and a full featured **URLShortener Application**. The **Django-URLShortener** is rich features and powerful enough, You can start with **Django-URLShortener** without installation of any 3rd party packages.
___


## Installation :
You can install **Django-URLShortener** from PyPI using **pip**.

``` pip install django-urlshortener ```
___


## Configuration :
***1. Open the ```settings.py``` module of your project, And put urlshortener into ```INSTALLED_APPS```.***  
```python
INSTALLED_APPS = (
    'urlshortener'
)
```

***2. Open the ```urls.py``` module of your project, And include urlshortener URLs.***  
```python
urlpatterns = [
    ...
    re_path(r'', include('urlshortener.urls')),
    ...
]
```

***3. Setup the Templates.***
>> ***Important Note***: You need to configure some Reusable/global templates to your django project or you can create your own templates, It's very easy.  
```python
TEMPLATES = [
    ...
    ...
    'DIRS': [os.path.join(BASE_DIR, 'templates'),],
    ...
    ...
]
```

***4. Static files configuration.***
Open your ```settings.py``` module and Configure Static files and media files or you can can use your own configuration.  
```python
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static-local'),)
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static-root', 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static-root', 'media')
```
___


## Complete the Djangocontact setup by running the following command one by one in the sequence.  
```python
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
python manage.py runserver
```