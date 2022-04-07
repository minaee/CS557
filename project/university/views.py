from django.shortcuts import render
from datetime import datetime

def uni_index(request):
    

    context = {
       
    }
    return render(request, 'university/uni_index.html', context)