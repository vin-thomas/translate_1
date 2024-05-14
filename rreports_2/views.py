from django.shortcuts import render
from django.http import JsonResponse
from . import preprocess
from . import translate
from django.contrib.auth.decorators import login_required
from datetime import datetime

# Create your views here.
@login_required
def index(request):
    return render(request, "rreports_2/index.html", {})


def te(request):
    if request.method == 'POST':
        text = request.POST.get('text', '')
        target = request.POST.get('lang', '')

        print(text, target)

        if text:
            translation = preprocess.preprocess(text, target)
        with open("usage.log", "a+", encoding="utf-8") as log:
            log.seek(0)
            if len(log.read()) != 0:
                log.write("\n" + str(datetime.now()) + "   " +request.user.username + "    " +str(len(text)))
            else:
                log.write(str(datetime.now()) + "   " +request.user.username + "    " +str(len(text)))
            log.close()

        return JsonResponse({'translation': translation})
