from board.models import Word, Phrase
# from random import random

for word in Word.objects.all():
    #word.pos_x = random()*4000.
    #word.pos_y = random()*3000.
    word.used = False
    word.phrase = Phrase.objects.get(text='%No phrase%')
    word.save()