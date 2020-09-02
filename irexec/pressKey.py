#!/usr/bin/python3
import argparse
from MappingHelper import loadMap, getMappingFromDB # Used for DB/dJango

############################################################################## HID HELPERS ##
# Descriptor:
#   05010906a1018501050719e029e71500250175019508810295017508810395057501050819012905910295017
#   503910395067508150025650507190029658100c0050C0901A1018502050C150025017501950709B509B609B7
#   09CD09E209E909EA810295068101C0

KEYBOARD_ID = chr(0x01)
CONSUMER_ID = chr(0x02)
NULL_CHAR = chr(0)

def write_report(report, file = '/dev/hidg0' ):
    with open(file, 'rb+') as fd:
        fd.write(report.encode())

def sendKey(key, file = '/dev/hidg0'):
    write_report(KEYBOARD_ID+NULL_CHAR*2+chr(key)+NULL_CHAR*5, file)
    write_report(KEYBOARD_ID+NULL_CHAR*8, file)

def sendMultimediaKey(key, file = '/dev/hidg0'):
    write_report(CONSUMER_ID+chr(key)+NULL_CHAR, file)
    write_report(CONSUMER_ID+NULL_CHAR*2, file)
#############################################################################################

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Sends keystrokes to usb-gadget keyboard device.')
    parser.add_argument('code', metavar='KEY_CODE', help='key code to be sent')
    parser.add_argument('--dev', dest='device',default="/dev/hidg0", help='device to be used (defaults to /dev/hidg0)')
    args = parser.parse_args()

    KEY_MAP = loadMap('../standard_map.json')
    user_mapping = getMappingFromDB('../hklirc.db')
    if(args.code in KEY_MAP):
        if(KEY_MAP[args.code]['keyboard']):
            sendKey(int(KEY_MAP[args.code]['value'],0), args.device)
        else:
            sendMultimediaKey(int(KEY_MAP[args.code]['value'],0), args.device)

    #print (args.code + args.device)