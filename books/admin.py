from django.contrib import admin

# Register your models here.
from books.models import Publisher, Author, Book


class AuthorAdmin(admin.ModelAdmin):
    search_fields = ('first_name', 'last_name',)
    list_display = ('first_name', 'last_name', 'email',)


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'publisher', 'publication_date',)
    list_filter = ('publication_date',)
    date_hierarchy = 'publication_date'
    ordering = ('-publication_date', 'title',)
    fields = ('title', 'authors', 'publisher')
    filter_horizontal = ('authors',)
    raw_id_fields = ('publisher',)


admin.site.register(Publisher)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
