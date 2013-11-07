# -*- coding: utf-8 -*-
from django.http import Http404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils.translation import get_language, ugettext_lazy as _
from easy_thumbnails.files import get_thumbnailer


def thumb(image, size, crop=True, upscale=True):
    """
    Returns a thumbnail.
    """
    if image:
        options = {
            'size': size.split('x'),
            'crop': crop,
            'upscale': upscale,
        }
        thumbnailer = get_thumbnailer(image)
        thumb = thumbnailer.get_thumbnail(options)
        return thumb.url
    else:
        return None


def paginate(queryset, request, items_per_page=10, orphans=0):
    """
    Paginates given queryset.
    """
    paginator = Paginator(queryset, items_per_page, orphans)
    page = request.GET.get('page')

    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    return queryset


def get_translation(default, translations, language=None):
    """
    Returns the correct translation for the given list of tuples.
    """
    if not language:
        language = get_language()

    if translations:
        for item in translations:
            if item[0] == language:
                return item[1]

        return translations[0][1]
    else:
        return default
