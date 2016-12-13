from django.contrib import admin

# Register your models here.

from .models import Phrase, Word

admin.site.register(Phrase)
admin.site.register(Word)