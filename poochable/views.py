from django.http import HttpResponse
from django.shortcuts import render
from poochable.forms import UploadFileForm

def pooch_list(request):
    context = {}
    return render(request, 'poochable/pooch_list.html', context)

def pooch_detail(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             handle_uploaded_file(request.FILES['file'])
            
    return HttpResponse("Thanks!")




