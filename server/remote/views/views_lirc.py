from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.conf import settings as ConfigSettings
from os import listdir, remove
from os.path import isfile, join, basename, exists
import json, re
from ..util.LircdParser import parse as parseLirc
from ..forms import UploadFileForm

# Create your views here.
# form: https://www.youtube.com/watch?v=pH6X79wIgyY

def index(request):
    return render(request, "remote/empty.html", {})

def handle_uploaded_file(f, folder):
    with open(join(folder, f.name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def lircd_remotes(request):
    mypath = ConfigSettings.LIRCD_PATH
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            print(file) # handle_uploaded_file
            handle_uploaded_file(file, mypath)
            # return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    
    remotes = parseLirc(mypath)
    return render(request, "remote/lircd_remotes.html", {
        'remotes': remotes,
        'lircd_path': mypath,
        'file_form': form    
    })

def lircd_remote(request, remote_file):
    remote_file_path = ConfigSettings.LIRCD_PATH + basename(remote_file)
    print(remote_file_path)
    remotes = parseLirc(remote_file_path)
    file = open(remote_file_path,"r")
    config = file.read()
    file.close()
    return render(request, "remote/lircd_remote.html", {
        'remote': {"config":config, "filename":remote_file}, "remotes": remotes
    })

def lircd_remote_download(request, remote_file):
    remote_file_path = ConfigSettings.LIRCD_PATH + basename(remote_file)
    if exists(remote_file_path):
        with open(remote_file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + basename(remote_file_path)
            return response
    raise Http404

def lircd_remote_delete(request, remote_file):
    remote_file_path = ConfigSettings.LIRCD_PATH + basename(remote_file)
    if exists(remote_file_path):
        remove(remote_file_path)
        return redirect('lircd_remotes')
    raise Http404