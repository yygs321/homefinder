from django.shortcuts import render

def gangnam_view(request):
    return render(request, 'gangnam.html')

def seocho_view(request):
    return render(request, 'seocho.html')

def songpa_view(request):
    return render(request, 'songpa.html')