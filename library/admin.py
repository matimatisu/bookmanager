from django.contrib import admin
from .models import Book
from .models import Genre

admin.site.register(Book)
admin.site.register(Genre)

# Register your models here.
