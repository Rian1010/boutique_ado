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

- Use `load static` for the base.html to get the static files
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
- Make sure to add the JS throught script tag in checkout.html `static 'checkout/js/stripe_elements.js'`
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

### Webhooks on Stripe
#### Localhost
- `brew cask install ngrok`
- `ngrok http 8000`
- Add the Forwarding link to ALLOWED_HOSTS and use the link
- Rerun that command every time the project gets started
- Use the command from the second step from https://ngrok.com/

- If not on Mac:
    - Go to https://ngrok.com/
    - Login with Github

## Country Fields In Models
- `sudo pip3 install django-countries`
- In models.py for the checkout app
    - `from django_countries.fields import CountryField`

## Login / Registration
- Go to templates/allauth/templates/account
- Edit its base.html, account_inactive.html, login.html and email_confirmation.html

## Heroku 
- Create a new app on Heroku
- In Resources, add the postgress add-on
- `sudo pip3 install dj_database_url`
- `sudo pip3 install psycopg2-binary`
- `pip3 freeze > requirements.txt`
- In settings.py:
    - import dj_database_url
    - Comment out DATABASES and make a new one:
        -   ```python
                DATABASES = {
                    'default': dj_database_url.parse(os.environ.get('DATABASE_URL(actual password NOT env.py'))
                }
            ```

- `python3 manage.py showmigrations`
- `python3 manage.py migrate`
- The order of the following is important, as products rely on categories
    - `python3 manage.py loaddata categories`
    - `python3 manage.py loaddata products`
- Again: `python3 manage.py createsuperuser`
- Comment out the new DATABASES in settings.py and get the old one back, then deploy to Github
- Change the DATABASES section in settings.py as:
    -   ```python 
        if 'DATABASE_URL' in os.environ:
            DATABASES = {
            '   default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
            }

        else:
            DATABASES = {
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
                }
            }
        ```

- `sudo pip3 install gunicorn`
- Create a Procfile and add in it: `web: gunicorn boutique_ado.wsgi:application`
- `pip3 freeze > requirements.txt`
- `heroku login` 
- To disable statics on Heroku:
    - `heroku config:set DISABLE_COLLECTSTATIC=1, --app rian-boutique-ado` (add the --add flag, if there is more than one app)
- Add ALLOWED_HOSTS for Heroku in settings.py

- Deploy to Github
- Deploy to Heroku:
    - `git push heroku master`
    - Initialize heroku git remote, if there is a fatal error: `heroku git:remote -a rian-boutique-ado`
    - Try again: `git push heroku master`
    - Check if the link to the heroku page works (statics won't work just yet and should be added later on)
        - In case it does not work, check if the config. vars on Heroku match with the env vars in env.py, if the requirements.txt file and Procfile are updated or visit: https://devcenter.heroku.com/articles/error-codes#:~:text=Whenever%20your%20app%20experiences%20an,error%20information%20to%20your%20logs.
        - MUST have a new secret key in Heroku config. vars
    - In settings.py, replace DEBUG with `DEBUG = 'DEVELOPMENT' in os.environment`, so DEBUG is only True, if there is a DEVELOPMENT variable
- Go to the 'Deployment' section on Heroku and set automatic deployment

## AWS
- Create a bucket unblocking publication
- Click on the bucket, go to CORS
- CORS configurations
    ```html
    <?xml version="1.0" encoding="UTF-8"?>
    <CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
    <CORSRule>
    <AllowedOrigin>*</AllowedOrigin>
    <AllowedMethod>GET</AllowedMethod>
    <AllowedMethod>HEAD</AllowedMethod>
    <MaxAgeSeconds>3000</MaxAgeSeconds>
    <AllowedHeader>Authorization</AllowedHeader>
    </CORSRule>
    </CORSConfiguration>
    ```
- Under Properties, click on static website hosting and input `index.html` and `error.html`
- Go to Permissions and click on Policy generator
- Select Type of Policy: S3 Bucket Policy, Principal: *, Amazon Resource Name (ARN): (get it from previous the permissions page), then click on Add Statement 
- Click on Generate Policy, copy the code and paste it into the Bucket Policy under Permissions
- Add /* at the end of the ARN Resource

- Under Public access and Group, click on 'Everyone' and select 'List objects' and the rest of the (4) checkboxes too
- Go to IAM, Group section and create a new Group for the user to live in
- Give it a reasonable name, such as: manage-boutique-ado
- Since there is no policy at this point, click on next step and create

- Then create an access policy giving the group access to the s3 bucket we created
- Click on Policies and then on Create policies
- Click on the JSON tab and import managed policy
- Search for S3 and import the AWS Managed Policy AmazonS3FullAccess
- Open S3 on a new tab, open the bucket, go to Permissions and Bucket Policy to copy the ARN
- Go back to the JSON tab and replace the Resource section with a list, in which one ARN needs to be added, and then the same ARN again, under it with /* at the end of it to have the bucket itself, and also another rule for all files/folders in the bucket
- Click on Review Policy
- Give it a name, like: rian-boutique-ado-policy
- Give it a description, such as: Access to S3 bucket for Boutique Ado static files
- Click on Groups, the group name, the Attach policy button, search for the policy just created and select it, then click on Attach Policy

- And finally, assign the user to the group so it can use the policy to access all our files.
- Go to the Users page, click on add user and give it a name, such as 'boutique-ado-staticfiles-user' 
- Select Programmatic access in Access type and click on Next: Permissions
- Now we can put the user in our group. Which as you can see here has our policy attached.
- Select the group name (manage-boutique-ado) and click on Next: Tags
- Click on Next: Review and then on Create User
- IMPORTANT!!! Download the csv. file which will contain this user's access key and secret access key, which should be used to authenticate them from the Django app
- IT CANNOT BE DOWNLOADED AGAIN, SO KEEP IT SAFE

- `sudo pip3 install boto3`
- `sudo pip3 install django-storages`
- `pip3 freeze > requirements.txt`

- In settings.py:
    - Add `'storages'` to the INSTALLED_APPS
    -   ```python 
        if 'USE_AWS' in os.environ:
            # Bucket Config
            AWS_STORAGE_BUCKET_NAME = 'rian-boutique-ado'
            AWS_S3_REGION_NAME = 'eu-central-1'
            AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
            AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
            AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
        ```
    - IMPORTANT!!! Variables MUST be hidden, otherwise someone else could get them and add things to the website, which would go on the AWS bill
- Add those variables on the config. vars on Heroku through the csv. file
- Add USE_AWS and set it to True in the Heroku config. vars

- Add a custom_storage.py file with the content it has in this project too
- Change the if statement in the settings.py to the following:
    ```python
    # IMPORTANT!!! 
    # Variables MUST be hidden, otherwise someone else could get them 
    # and add things to the website, which would go on the AWS bill
    if 'USE_AWS' in os.environ:
        # Cache control
        AWS_S3_OBJECT_PARAMETERS = {
            'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
            'CacheControl': 'max-age=94608000',
        }

        # Bucket Config
        AWS_STORAGE_BUCKET_NAME = 'rian-boutique-ado'
        AWS_S3_REGION_NAME = 'eu-central-1'
        AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
        AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
        AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

        # Static and media files
        STATICFILES_STORAGE = 'custom_storages.StaticStorage'
        STATICFILES_LOCATION = 'static'
        DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'
        MEDIAFILES_LOCATION = 'media'

        # Override static and media URLs in production
        STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATICFILES_LOCATION}/'
        MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIAFILES_LOCATION}/'
    ```
- Remove the DISABLE_COLLECTSTATIC variable from the config. vars on Heroku (django will collectstatic files automatically and upload them to s3, after deployment)
- Upload onto Github
- And then issue a git push, which will trigger an automatic deployment to Heroku
- Check the S3 Overview, there should be a static file, once uploaded onto Heroku 

## Python Refactoring on Gitpod
- `python3 -m flake8`
- This command should show all the pep8 errors
- Can ignore the errors on files that are automatically generated, such as migrations, since automatically generated files may intentionally ignore style rules for efficiency reasons, and because as developers we usually don't need to touch them.
- Unused imports can come from files that Django migrations generated that one may or may not be using, so depending on the usage, the file and import or just the import can be deleted

## S3 Media
- Add a media file next to the static file to add all of the images in there
- After adding the files, click on next and in the option dropdown, select 'Grant public read access to this object(s)'
- Then click next through to the end and click on upload

## Stripe Webhook new link
- Don't forget to add the new Heroku link with /checkout/wh/ to the webhook on the Stripe website, selecting 'receive all events' and add endpoint
- Add the Signing Secret to the Heroku config. vars with STRIPE_WE_SECRET as key, (So it needs to match with the variable in settings.py)
- Send a test handler to make sure that the webhook is working
    - Selecting the event type: 'account.external_account.created', should give the response, 'Unhandled webhook received: account.external_account.created'

## Gmail
- Got to Gmail
- Click on the settings button, then on the see all settings button
- Click on Accounts and Import and then 'Other Google Account settings'
- Click on Security and it the 2 step notification is on, (phone needed for verification), click on App password
- Add the 16 character long password to the Heroku config. vars, as for eg. EMAIL_HOST_PASS and also add EMAIL_HOST_USER set to my Gmail account
- Get rid of the DEFAULT_FROM_EMAIL and EMAIL_BACKEND variables in the settings.py file and add the following:
    -   ```python
        if 'DEVELOPMENT' in os.environ:
            EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
            DEFAULT_FROM_EMAIL = 'rtegally1098@gmail.com'
        else:
            EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
            EMAIL_USE_TLS = True
            EMAIL_PORT = 587
            EMAIL_HOST = 'smtp.gmail.com'
            EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
            EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASS')
            DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_HOST_USER')

        ```


## Side notes
- If needed to login with superuser on the website, comment out the two following lines of code (not sure if right or not, but it is) in the models.py of the profiles app:
    ```python
    # if created:
        UserProfile.objects.create(user=instance)
    # Existing users: just save the profile
    # instance.userprofile.save()
    ```
!!! Not sure if this or nothing (unclear from course) !!!