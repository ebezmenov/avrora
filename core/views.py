# coding:utf8
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import user_passes_test
from avrora.catalog.models import Category
from avrora.core.forms import CSVUploadForm
from avrora.catalog.utils import handle_cvs_import_product

def home(request):
    categories = Category.objects.filter(parent = None)
    return render_to_response('base.html', { 'root_cat': categories})

#from django.views.decorators.csrf import csrf_exempt
#@csrf_exempt

def user_is_staff(user):
    return user.is_staff

@user_passes_test(user_is_staff)
def load_product(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            handle_cvs_import_product(request.FILES['file_cvs'])
            #обрабатываем форму
#            destination = open('myfile.csv', 'wb+')
#            for chunk in self.cleaned_data['file'].chunks():
#                destination.write(chunk)            
#            destination.close()
#            import csv
            #открываем и обрабатываем myfile.csv
    else:
        form = CSVUploadForm()
    return render_to_response('upload_csv.html',{'form': form,},
                              context_instance=RequestContext(request))