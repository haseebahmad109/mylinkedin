from os.path import join, normpath
from django.conf import settings

def handle_uploaded_file(f):
    with open(normpath(join(settings.SITE_ROOT, 'LinkedApp/media/uploads/' + f.name)), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


