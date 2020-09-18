from django.core.management.base import BaseCommand, CommandError
from remote.models import Mapping
import json

class Command(BaseCommand):
    help = 'Creates an example mapping.'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        new_mapping={
            'CIRCLE':'KEY_VOLUMEUP',
            'CROSS':'KEY_VOLUMEDOWN',
            'R3':'KEY_MUTE'
        }
        mapping = Mapping(config=json.dumps(new_mapping), name="Music", active=True, id=1)
        mapping.save()
        self.stdout.write(self.style.SUCCESS('Successfully created example mapping!'))
