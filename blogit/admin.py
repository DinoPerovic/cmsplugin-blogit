# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from hvad.admin import TranslatableAdmin
from cms.admin.placeholderadmin import PlaceholderAdmin

from blogit.models import AuthorLink, Author, Category, Tag, TaggedPost, Post
from blogit.utils.image import thumb


class AuthorLinkInline(admin.TabularInline):
    model = AuthorLink
    extra = 0


class AuthorAdmin(TranslatableAdmin, PlaceholderAdmin):
    list_display = ('get_full_name', 'slug', 'all_translations', 'get_image')
    inlines = (AuthorLinkInline,)

    def __init__(self, *args, **kwargs):
        super(AuthorAdmin, self).__init__(*args, **kwargs)
        self.fieldsets = (
            (None, {
                'fields': ('slug', 'user'),
                'description': _(
                    'These fields are the same across all languages.'),
            }),
            (_('Personal Info'), {
                'fields': ('first_name', 'last_name', 'email', 'picture'),
                'description': _(
                    'These fields are the same across all languages.'),
            }),
            (None, {
                'fields': ('description',),
            }),
            (_('Bio'), {
                'fields': ('bio',),
                'classes': ('plugin-holder', 'plugin-holder-nopage'),
            }),
        )

    def get_image(self, obj):
        # Returns a thumbnail to display in list_display.
        if obj.picture:
            return '<img src="{}">'.format(thumb(obj.picture, '72x72'))
        return None
    get_image.short_description = _('picture')
    get_image.allow_tags = True

    def get_full_name(self, obj):
        # Returns authors full name.
        return obj.get_full_name()
    get_full_name.short_description = _('full name')


class CategoryAdmin(TranslatableAdmin, PlaceholderAdmin):
    list_display = (
        'get_title', 'get_slug', 'date_created', 'last_modified',
        'all_translations')
    list_filter = ('date_created', 'last_modified')
    readonly_fields = ('last_modified',)

    def __init__(self, *args, **kwargs):
        super(CategoryAdmin, self).__init__(*args, **kwargs)
        self.prepopulated_fields = {'slug': ('title',)}
        self.fieldsets = (
            (None, {
                'fields': ('title', 'slug'),
            }),
            (_('Common Settings'), {
                'fields': ('parent',),
                'description': _(
                    'These fields are the same across all languages.'),
            }),
            (_('Date Information'), {
                'fields': ('date_created', 'last_modified'),
                'classes': ('collapse',),
                'description': _(
                    'These fields are the same across all languages.'),
            }),
        )

    def get_title(self, obj):
        # Returns translated title field.
        return obj.__str__()
    get_title.short_description = _('title')

    def get_slug(self, obj):
        # Returns translated slug field.
        return obj.get_slug()
    get_title.short_description = _('slug')


class TaggedPostInline(admin.TabularInline):
    model = TaggedPost
    extra = 0


class TagAdmin(admin.ModelAdmin):
    inlines = (TaggedPostInline,)


class PostAdmin(TranslatableAdmin, PlaceholderAdmin):
    list_display = (
        'get_title', 'get_slug', 'date_published', 'author',
        'all_translations', 'get_image', 'get_is_public')
    list_filter = ('date_published', 'date_created', 'last_modified', 'author')
    readonly_fields = ('date_created', 'last_modified',)
    actions = ['make_public', 'make_hidden']

    def __init__(self, *args, **kwargs):
        super(PostAdmin, self).__init__(*args, **kwargs)
        self.prepopulated_fields = {'slug': ('title',)}
        self.fieldsets = (
            (None, {
                'fields': ('title', 'slug', 'is_public'),
            }),
            (None, {
                'fields': ('subtitle', 'description', 'tags'),
            }),
            (_('Common Settings'), {
                'fields': (
                    'category', 'author', 'featured_image'),
                'description': _(
                    'These fields are the same across all languages.'),
            }),
            (_('Date Information'), {
                'fields': ('date_published', 'date_created', 'last_modified'),
                'classes': ('collapse',),
                'description': _(
                    'These fields are the same across all languages.'),
            }),
            (_('SEO Settings'), {
                'fields': ('meta_title', 'meta_description', 'meta_keywords'),
                'classes': ('collapse',),
            }),
            (_('Content'), {
                'fields': ('content',),
                'classes': ('plugin-holder', 'plugin-holder-nopage'),
            }),
        )

    def get_image(self, obj):
        # Returns a thumbnail to display in list_display.
        if obj.featured_image:
            return '<img src="{}">'.format(thumb(obj.featured_image, '72x72'))
        return None
    get_image.short_description = _('featured image')
    get_image.allow_tags = True

    def get_title(self, obj):
        # Returns translated title field.
        return obj.__str__()
    get_title.short_description = _('title')

    def get_slug(self, obj):
        # Returns translated slug field.
        return obj.get_slug()
    get_slug.short_description = _('slug')

    def get_is_public(self, obj):
        # Returns translated slug field.
        return obj.is_public
    get_is_public.boolean = True
    get_is_public.short_description = _('is public')

    def make_public(self, request, queryset):
        # Marks selected posts as public.
        for obj in queryset:
            obj.is_public = True
            obj.save()
    make_public.short_description = _('Mark selected posts as public')

    def make_hidden(self, request, queryset):
        # Marks selected posts as hidden.
        for obj in queryset:
            obj.is_public = False
            obj.save()
    make_hidden.short_description = _('Mark selected posts as hidden')


admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
