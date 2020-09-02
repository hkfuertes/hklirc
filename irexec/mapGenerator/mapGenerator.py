#!/usr/bin/env python3
import json
import import_keys as KeysHelper

if __name__ == "__main__":
    KEY_MAP = KeysHelper.readMap()
    toPrint = {}
    for key in KEY_MAP:
        toPrint[key] = {
            "key":key,
            "value": "0x{:02x}".format(KEY_MAP[key]),
            "keyboard": True
        }
    
    '''
    2.    Multimedia buttons: Report ID=2 : empezando del reves
    bit format: 7 reserved, 6 vol down(0x02), 5 vol up(0x01), 4 mute(0x04), 3 play/pause(0x08), 2 stop(0x10), 1 prev track(0x40), 0 next track(0x80)
    For example, 0x40 for volume down and 0x20 for volume up. 
    '''
    toPrint["KEY_VOLUMEUP"] = {
        "key":"KEY_VOLUMEUP",
        "value": "0x{:02x}".format(int('100000',2)),
        "keyboard": False
    }

    
    toPrint["KEY_VOLUMEDOWN"] = {
        "key":"KEY_VOLUMEDOWN",
        "value": "0x{:02x}".format(int('1000000',2)),
        "keyboard": False
    }

    toPrint["KEY_MUTE"] = {
        "key":"KEY_MUTE",
        "value": "0x{:02x}".format(int('10000',2)),
        "keyboard": False
    }

    toPrint["KEY_MEDIA_PLAYPAUSE"] = {
        "key":"KEY_MEDIA_PLAYPAUSE",
        "value": "0x{:02x}".format(int('1000',2)),
        "keyboard": False
    }

    toPrint["KEY_STOP"] = {
        "key":"KEY_STOP",
        "value": "0x{:02x}".format(int('100',2)),
        "keyboard": False
    }

    toPrint["KEY_MEDIA_PREVIOUSSONG"] = {
        "key":"KEY_MEDIA_PREVIOUSSONG",
        "value": "0x{:02x}".format(int('10',2)),
        "keyboard": False
    }

    toPrint["KEY_MEDIA_NEXTSONG"] = {
        "key":"KEY_MEDIA_NEXTSONG",
        "value": "0x{:02x}".format(int('1',2)),
        "keyboard": False
    }

    # note that output.json must already exist at this point
    with open('../standard_map.json', 'w+') as f:
        # this would place the entire output on one line
        # use json.dump(lista_items, f, indent=4) to "pretty-print" with four spaces per indent
        json.dump(toPrint, f, indent=4)