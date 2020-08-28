from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.conf import settings as ConfigSettings
from os import listdir
from os.path import isfile, join, basename, exists
import json, re
from ..models import Mapping

# Create your views here.
# form: https://www.youtube.com/watch?v=pH6X79wIgyY

def loadMap():
    return {}

def index(request):
    mappings = Mapping.objects.all()
    return render(request, "remote/mappings.html", {
        "mappings": mappings
    })

def detail(request, mapping_id):
    mapping = get_object_or_404(Mapping, pk=mapping_id)
    mapping_codes = loadMap()
    for key, value in json.loads(mapping.config).items():
        mapping_codes[key] = value
    print(mapping_codes)
    return render(request, "remote/mapping_detail.html", {
        "mapping": mapping,
        "mapping_codes": mapping_codes
    })