from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.forms import EmailField, SlugField, CharField, ValidationError, PasswordInput
from operator import itemgetter

from .models import Word, Phrase

def index(request, scroll_x=0, scroll_y=0):
    if request.user.is_authenticated():
        wordlist = Word.objects.all()
        colors = ['#1E90FF', '#6495ED', '#9932CC', '#5F9EA0', '#00BFFF',
                  '#7FFFD4', '#DB7093', '#00CED1', '#ADD8E6', '#1E90FF']
        phrasedict = {}
        for i, phrase in enumerate(Phrase.objects.all()):
            if phrase.word_set.count()>0 and phrase.text != '%No phrase%':
                phrasedict[phrase] = colors[i%10]
        context = {'wordlist': wordlist, 'phrasedict': phrasedict,
        'init_scroll_x': scroll_x, 'init_scroll_y': scroll_y}
        return render(request, 'board/index.html', context)
    else:
        return HttpResponseRedirect(reverse('board:login_form'))
        
def login_form(request, error_code=None):
    context = {'error_code': error_code}
    return render(request, 'board/login.html', context)
        
def auth_login(request, error_code):
    username = request.POST['login_name']
    password = request.POST['login_pass']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        scroll_x = 0
        scroll_y = 0
        return HttpResponseRedirect(reverse('board:index', args=(scroll_x, scroll_y)))
    else:
        error_code = 1
        return HttpResponseRedirect(reverse('board:login_form', args=(error_code, )))

def auth_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('board:login_form'))
        
def auth_register(request, error_code):
    username_f = SlugField(max_length=30)
    password_f = CharField(max_length=30, widget=PasswordInput)
    email_f = EmailField()
    username = request.POST.get('reg_name', None)
    password = request.POST.get('reg_pass', None)
    email = request.POST.get('reg_email', None)
    for field, value in [(username_f, username), (password_f, password), (email_f, email)]:
        try:
            field.clean(value)
        except ValidationError:
            error_code = 2
            return HttpResponseRedirect(reverse('board:login_form', args=(error_code, )))
            break
    else:
        if User.objects.filter(username=username).exists():
            error_code = 3
            return HttpResponseRedirect(reverse('board:login_form', args=(error_code, ))) 
        else:
            User.objects.create_user(username=username, email=email, password=password)
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect(reverse('board:index', args=(0, 0)))
            
def reposition(request):
    word = Word.objects.get(pk = request.POST.get('word_id'))
    word.pos_x = request.POST.get('pos_x')
    word.pos_y = request.POST.get('pos_y')
    word.save()
    scroll_x = request.POST.get('scroll_x')
    scroll_y = request.POST.get('scroll_y')
    return HttpResponseRedirect(reverse('board:index', args=(scroll_x, scroll_y)))

def add_or_del_phrase(request):
    mode = request.POST.get('mode')
    id_list = request.POST.get('phrase').split()
    scroll_x = request.POST.get('scroll_x_2')
    scroll_y = request.POST.get('scroll_y_2')
    if mode == 'add':
        words = []
        for el in id_list:
            word = Word.objects.get(pk=int(el))
            words.append([word.id, word.text, word.pos_x, word.pos_y])
        words_sorted = sorted(words, key=itemgetter(3,2)) # sort words in screen reading order
        for i, w in enumerate(words_sorted):
            if i == 0:
                phrase_text = w[1]
            else:
                phrase_text += (" "+w[1])
        phrase = Phrase(created_by=request.user, pub_date=timezone.now(),
        text=phrase_text)
        phrase.save()
        for el in id_list:
            word = Word.objects.get(pk=int(el))
            word.phrase = phrase
            word.used = True
            word.save()
    elif mode == 'del':
        for el in id_list:
            word = Word.objects.get(pk=int(el))
            word.used = False
            word.phrase = Phrase.objects.get(text='%No phrase%')
            word.save()
    return HttpResponseRedirect(reverse('board:index', args=(scroll_x, scroll_y)))
