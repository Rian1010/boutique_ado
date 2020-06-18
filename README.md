# Boutique Ado

## Django 3.7
### Allauth
- After starting a django project and creating a super-user: `sudo pip3 install django-allauth`
- Get the following from django-allauth documentation into the `settings.py` file:
    - `AUTHENTICATION-BACKENDS`
    - `INSTALLED-APPS`: 
        - `'django.contrib.sites',`
        - `'allauth',`
        - `'allauth.account',`
        - `'allauth.socialaccount', `   
- Use the following code in settings.py:
```python
SITE_ID = 1

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = True
ACCOUNT_USERNAME_MIN_LENGTH = 4
LOGIN_URL = 'accounts/login/'
LOGIN_REDIRECT_URL = '/'
```
- Copy and paste the `allauth` folder from the venv file into the `templates` folder

- Add the following meta tag into the base.html file:
```html
<!-- This will allow support of older Internet Explorer versions and eliminate validation errors when validating the HTML -->
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
```

- Use `{% load static %}` for the base.html to get the static files
- Move the scripts to the head for them to load as early as possible

## After setting up base.html and the home django-app (with its url.py)
- In settings.py
    - Add `home` to INSTALLED_APPS
    - Add the following in TEMPLATES:
    ```python
    'DIRS': [
        os.path.join(BASE_DIR, 'templates'),
        os.path.join(BASE_DIR, 'templates', 'allauth'),
    ],
    ```
- Test the project: `python3 manage.py runserver`

## Media and Statics
- Use font awesome with link tag and a font awesome kit (Through login) with script tag in base.html
- Use media and static files
- In settings.py:
```python
STATIC_URL = '/static/'
# Tells Django where the static files are located at
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

# Where all uploaded media files go
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```
- In the main urls.py file:
```python 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## After migrating the models from the products app
- Use the fixtures: `python3 manage.py loaddata categories`
- Start with `categories` since the products need to know which category to go in
- Then upload all products: `python3 manage.py loaddata products`

## For Clothing sizes
- migrate `has_sizes = models.BooleanField(default=False, null=True, blank=True)`
- `python3 manage.py shell`
- `In [1]: from products.models import Product`
- `kdbb = ['kitchen_dining', 'bed_bath']` (To get the products that need to be excluded)
- `clothes = Product.objects.exclude(category__name__in=kdbb)` (Excludes kdbb categories)
- `clothes.count()` should show how many products are available for sizes
- ```python
    In [5]: for item in clothes: 
   ...:     item.has_sizes=True 
   ...:     item.save() 
   ...: 
   ```
- Check if the right amount of clothes have sizes: `In [6]: Product.objects.filter(has_sizes=True).count()`
- Exit the shell: `exit()`
- Use a with statement, like in product_detail.html