from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.conf import settings as ConfigSettings
from os import listdir
from os.path import isfile, join, basename, exists
import json, re
from ..models import Mapping
from ..util.LircdParser import parse as parseLirc
from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def loadMap():
    return {}

def index(request):
    mappings = Mapping.objects.all()
    return render(request, "remote/mappings.html", {
        "mappings": mappings
    })

def detail(request, mapping_id):
    mypath = ConfigSettings.LIRCD_PATH
    remotes = parseLirc(mypath)

    available_keys = []
    for _, value in remotes.items():
        for key in value['codes']:
            if key not in available_keys:
                available_keys.append(key)
    print(available_keys)

    mapping = get_object_or_404(Mapping, pk=mapping_id)
    return render(request, "remote/mapping_detail.html", {
        "mapping": mapping,
        "mapping_codes": json.loads(mapping.config),
        "remotes": remotes,
        "available_keys": available_keys
    })