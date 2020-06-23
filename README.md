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
    - In TEMPLATES, OPTIONS add: 
    ```python 
    'django.template.context_processors.media',
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

## Toasts
- Use toast templates in the includes
- Get the product item_id form the Product models in the bag views and display a success message through the else statement
- Display the message via base.html in a for loop and with statement with levels and use the script underneath it all in base.html
- Style the messages in the CSS

## Django Crispy Forms (For the checkout app in this case)
- `sudo pip3 install django-crispy-forms`
- In settings.py:
    - In INSTALLED_APPS:
        -   ```python
            # Other
            'crispy_forms',
            ```
    -   ```python
        CRISPY_TEMPLATE_PACK = 'bootstrap4'
        ```
    - In TEMPLATES: 
        -   ```python
            'builtins': [
                    'crispy_forms.templatetags.crispy_forms_tags',
                    'crispy_forms.templatetags.crispy_forms_field',
                ]
            ```
- `pip3 freeze > requirements.txt`

## Stripe 
- Get `<script src="https://js.stripe.com/v3/"></script>` from https://stripe.com/docs/payments/checkout/accept-a-payment and put it into the base.html head
- Do everything needed to do with the assistance of the stripe docs
- sudo pip3 install stripe

- Since we can't render Django template variables in external javascript files, we need to use a built-in template filter called json_script to render them here and then, we can access them in the external file: `{{ stripe_public_key|json_script:"id_stripe_public_key" }}` and `{{ client_secret|json_script:"id_client_secret" }}`
- These need to be added to the context in views.py as `stripe_public_key` and `client_secret`
- Their values should be seen in the script tag in the devtools
- Then, work on stripe_elements.js
- Use CSS from stripe JS docs too
- Make sure to add the JS throught script tag in checkout.html `<script src="{% static 'checkout/js/stripe_elements.js' %}"></script>`
- The payment input should be working with the card number turning red, if false, for example through 4000 0000 0000 0000
- After adjusting stripe in the views for it to get the bag's total value, use `sudo pip3 install stripe` and import stripe in views.py in the checkout app

- In settings.py:
    -   ```python
        STRIPE_CURRENCY = 'usd'
        STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY', '')
        STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', '')
        ```
- In env.py use the following structure:
    -   ```python 
        import os

        os.environ.setdefault('STRIPE_PUBLIC_KEY', '')
        os.environ.setdefault('STRIPE_SECRET_KEY', '')
        ```

- In views.py, set the secret key on stripe after creating the payment intent at the top of the function and create an intent variable besides the others too

- Add code in stripe_elements.js to handle form submit

### Testing if a payment worked
- Go to Stripe Dashboard > Developers > Events

## Checkout app
- In __init__.py, add `default_app_config = 'checkout.apps.CheckoutConfig'` for the signals to work from signals.py (make sure that apps.py imports it in a ready function)
- Restart the server for it to work, if it is already running

### Stripe testing
- 4242 4242 4242 4242 04 24 242 42424
- For extra authentication from stripe
    - 4000 0025 0000 3155 04 24 242 44242
- After adding the checkout success overlay with the loading icon, restart the server, if it is already running