from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.core.exceptions import ValidationError

import re

# Create your models here.
    
@python_2_unicode_compatible
class Phrase(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('date published')
    text = models.CharField(max_length=255)
    def __str__(self):
        return self.text

@python_2_unicode_compatible 
class Word(models.Model):
    phrase = models.ForeignKey(Phrase, on_delete=models.DO_NOTHING, default='%No phrase%')
    text = models.SlugField(max_length=50)
    pos_x = models.FloatField(default=0)
    pos_y = models.FloatField(default=0)
    used = models.BooleanField(default=False)
    def __str__(self):
        return self.text
    def clean(self):
        if re.search(r"\s", self.text):
            raise ValidationError('spaces in text are not allowed')
