import inspect

if 'ryu' in inspect.stack()[-1].filename:
    import os
    import django

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mike.settings")
    django.setup()
