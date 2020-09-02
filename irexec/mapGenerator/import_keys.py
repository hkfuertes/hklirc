def readMap ():
    file = open("usb_hid_keys.h", "r")
    retVal = {}
    for line in file:
        goodline = line[8:].split(" ")
        if line.startswith("#define ") and len(goodline)>1:
            key = goodline[0]
            value = ""
            for i in range(1, len(goodline)):
                if goodline[i] == "":
                    continue
                else:
                    value = goodline[i].rsplit()[0]
                    break

            # do whatever you wanna do with the scancode name, and its hex value
            #print("\"{}\": \"{}\",".format(key, value))
            retVal[key] = int(value,0)
    return retVal