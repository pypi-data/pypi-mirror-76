import os


def env(request):
    context = dict(os.environ)
    for key, value in os.environ.items():
        key = key.replace('DJANGO_', '')
        context[key] = value
    return context
