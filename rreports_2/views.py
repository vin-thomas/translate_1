from django.shortcuts import render
from . import preprocess
from . import translate
from django.contrib.auth.decorators import login_required
from datetime import datetime

# Create your views here.
@login_required
def index(request):
    text = ''
    message_1 = ''
    message_2 = ''
    message_3 = ''
    if request.method == 'POST':
        text = request.POST.get('textToTranslate', '')
        target = request.POST.get('language', '')

        if text:
            message_1 = preprocess.preprocess(text, target)
        with open("usage.log", "a+", encoding="utf-8") as log:
            log.seek(0)
            if len(log.read()) != 0:
                log.write("\n" + str(datetime.now()) + "   " +request.user.username + "    " +str(len(text)))
                print("log 1")
            else:
                log.write(str(datetime.now()) + "   " +request.user.username + "    " +str(len(text)))
                print("log 2")
            log.close()
    return render(request, "rreports_2/index.html", 
    {'original_text': text, 'translation': message_1})
