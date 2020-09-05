from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.conf import settings as ConfigSettings
from os import listdir, kill
from os.path import isfile, join, basename, exists
import json, re
from ..models import Mapping
from ..util.LircdParser import parse as parseLirc
from django.template.defaulttags import register
import signal

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def loadMap(file):
    all_keys = []
    with (open(file, "r")) as f:
        all_keys = json.loads(f.read()).keys()
    return all_keys

def index(request):
    mappings = Mapping.objects.all()
    return render(request, "remote/mappings.html", {
        "mappings": mappings,
    })

def detail(request, mapping_id):
    if mapping_id == 'NEW':
        mapping = Mapping(config="{}")
    else:
        mapping = get_object_or_404(Mapping, pk=mapping_id)
    
    if (request.POST.get("submitted", None) is not None):
        new_mapping = {}
        print(request.POST.dict())
        for key, value in request.POST.dict().items():
            if key.startswith("mapping_") and value is not "":
                new_mapping[key.replace("mapping_","")] = value
            if key == 'general_name':
                mapping.name = value
        mapping.config = json.dumps(new_mapping)
        mapping.save()
        if (mapping.active):
            # We update the mapping in the daemon
            signal_daemon(ConfigSettings.DAEMON_FILE)
        return redirect('mapping_index')
    

    mypath = ConfigSettings.LIRCD_PATH
    remotes = parseLirc(mypath)
    available_keys = []
    for _, value in remotes.items():
        for key in value['codes']:
            if key not in available_keys:
                available_keys.append(key)

    
    return render(request, "remote/mapping_detail.html", {
        "mapping": mapping,
        "mapping_codes": json.loads(mapping.config),
        "remotes": remotes,
        "available_keys": available_keys,
        "all_keys": loadMap(str(ConfigSettings.BASE_DIR) + "/../standard_map.json")
    })

def activate(request, mapping_id):
    mappings = Mapping.objects.all()
    for m in mappings:
        # Just one can be active
        m.active = (str(m.id) == str(mapping_id))
        m.save()

    # We update the mapping in the daemon
    signal_daemon(ConfigSettings.DAEMON_FILE)

    return redirect('mapping_index')

def delete(request, mapping_id):
    mapping = get_object_or_404(Mapping, pk=mapping_id)
    mapping.delete()
    return redirect('mapping_index')

def update_map(request):
    # We update the mapping in the daemon
    signal_daemon(ConfigSettings.DAEMON_FILE)
    return redirect('index')


def signal_daemon(pid_file):
    if exists(pid_file):
        with open(pid_file,'r') as f:
            pid = int(f.read())
            kill(pid, signal.SIGUSR1)