# Django Generic Awards #

Django app to create and manage Awards for your Model objects.


## Quick start ##

1. Add `django.contrib.sites`, `tof` and `django_generic_awards.apps.DjangoGenericAwardsConfig` to your INSTALLED_APPS setting like this:
    ```python
    INSTALLED_APPS = [
        ...
        'django.contrib.sites',
        'tof',
        'django_generic_awards',
    ]
    ```
2. Make sure that you have `SITE_ID` in your `settings.py`:
    ```python
    SITE_ID = XX
   ```
3. Run `python manage.py migrate sites` to create example site for your project.

4. Run `python manage.py migrate` to create the django_generic_awards models.

5. Start the development server and visit http://127.0.0.1:8000/admin/
   to setup Awardable models and add new Awards.

## Optional ##

- Run tests with `python runtests.py` command


## Special Thanks ##

To [**winePad GmbH**](https://winepad.at/) for initiating and sponsoring of this project.
