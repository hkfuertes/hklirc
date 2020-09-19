#!/usr/bin/env python3
import json, argparse
import import_keys as KeysHelper

KEYS_TO_REMOVE=[
    'KEY_MOD_LCTRL',
    'KEY_MOD_LSHIFT',
    'KEY_MOD_LALT',
    'KEY_MOD_LMETA',
    'KEY_MOD_RCTRL',
    'KEY_MOD_RSHIFT',
    'KEY_MOD_RALT',
    'KEY_MOD_RMETA',
    'KEY_NONE',
    'KEY_RO',
    'KEY_KATAKANAHIRAGANA',
    'KEY_YEN',
    'KEY_HENKAN',
    'KEY_MUHENKAN',
    'KEY_KPJPCOMMA',
    'KEY_HANGEUL',
    'KEY_HANJA',
    'KEY_KATAKANA',
    'KEY_HIRAGANA',
    'KEY_ZENKAKUHANKAKU',
    'KEY_LEFTCTRL',
    'KEY_LEFTSHIFT',
    'KEY_LEFTALT',
    'KEY_LEFTMETA',
    'KEY_RIGHTCTRL',
    'KEY_RIGHTSHIFT',
    'KEY_RIGHTALT',
    'KEY_RIGHTMETA',
    'KEY_MEDIA_STOPCD',
    'KEY_MEDIA_EJECTCD',
    'KEY_MEDIA_VOLUMEUP', # Already in a keyboard
    'KEY_MEDIA_VOLUMEDOWN', # Already in a keyboard
    'KEY_MEDIA_MUTE', # Already in a keyboard
    'KEY_MEDIA_WWW',
    'KEY_MEDIA_BACK',
    'KEY_MEDIA_FORWARD',
    'KEY_MEDIA_STOP',
    'KEY_MEDIA_FIND',
    'KEY_MEDIA_SCROLLUP',
    'KEY_MEDIA_SCROLLDOWN',
    'KEY_MEDIA_EDIT',
    'KEY_MEDIA_SLEEP',
    'KEY_MEDIA_COFFEE',
    'KEY_MEDIA_REFRESH',
    'KEY_MEDIA_CALC'
]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generates a key map for the daemon and server to be used.')
    parser.add_argument('filepath', metavar='filepath', help='Path to store the map', default="../standard_map.json")
    args = parser.parse_args()

    KEY_MAP = KeysHelper.readMap()
    toPrint = {}
    for key in KEY_MAP:
        toPrint[key] = {
            "key":key,
            "value": "0x{:02x}".format(KEY_MAP[key]),
            "keyboard": True
        }
    
    # We remove not used keys
    for element in KEYS_TO_REMOVE:
        del toPrint[element]

    '''
    2. Multimedia buttons: Report ID=2 : Backwards
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
    with open(args.filepath, 'w+') as f:
        # this would place the entire output on one line
        # use json.dump(lista_items, f, indent=4) to "pretty-print" with four spaces per indent
        json.dump(toPrint, f, indent=2)