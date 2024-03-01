from django.shortcuts import render
from . import preprocess
from . import translate

# Create your views here.

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
                
    return render(request, "rreports_2/index.html", 
    {'original_text': text, 'translation': message_1})
