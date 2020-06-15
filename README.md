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