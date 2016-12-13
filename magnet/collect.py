import os

word_bank = []

for fname in os.listdir('./text'):
    if not ".py" in fname:
        with open('./text/'+fname) as f:
            content = f.readlines()
            for line in content:
                words = line.split()
                for word in words:
                    word_bank.append(word)
                
print word_bank

from board.models import Word, Phrase

for word in word_bank:
    w = Word(phrase=Phrase.objects.get(pk=1), text=word, pos_x=0, pos_y=0, used=False)
    w.save()