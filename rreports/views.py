from django.shortcuts import render
from . import translate_fn_3
from django.http import StreamingHttpResponse

def index(request):
    message = ''
    task = ''
    s_l = ''
    if request.method == 'POST':
        task = request.POST.get('myTextarea', '')
        s_l = request.POST.get('language', '')
        if task:
            message = translate_fn_3.translate_text(task, s_l)
    
    return render(request, "rreports/index.html", 
    {'original_text': task, 'translation': message})
