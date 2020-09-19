## Mapping file generator
Simple python script to translate the standard C `usb_hid_keys.h` header file into the mapping standard used by **hkLirc**, including modifying the media keys to work with the consumer device.
Also and as the system does not allow modifiers, those keys are also removed.

### Keys removed:
```python
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
```

## Execution
To run the program:
```
$ python3 ./mapGenerator.py [mapping_file]
```
If no `mapping_file` is pass the file will be generated in `../standard_map.json` 