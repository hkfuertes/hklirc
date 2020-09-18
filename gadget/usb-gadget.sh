#!/bin/bash
gadget=/sys/kernel/config/usb_gadget/raspberrypi

usb_version="0x0200" # USB 2.0
device_class="0xEF"
device_subclass="0x02"
bcd_device="0x0100" # v1.0.0
device_protocol="0x01"
vendor_id="0x1d50"
product_id="0x60c7"
manufacturer="HKF"
product="RPi USB Gadget"
serial="fedcba9876543211"
attr="0x80" # Bus powered
power="250"
config1="RNDIS"
config2="CDC"
ms_vendor_code="0xcd" # Microsoft
ms_qw_sign="MSFT100" # also Microsoft (if you couldn't tell)
ms_compat_id="RNDIS" # matches Windows RNDIS Drivers
ms_subcompat_id="5162001" # matches Windows RNDIS 6.0 Driver
mac="01:23:45:67:89:ab"
dev_mac="02$(echo ${mac} | cut -b 3-)"
host_mac="12$(echo ${mac} | cut -b 3-)"

mkdir -p ${gadget}
echo "${usb_version}" > ${gadget}/bcdUSB
echo "${device_class}" > ${gadget}/bDeviceClass
echo "${device_subclass}" > ${gadget}/bDeviceSubClass
echo "${vendor_id}" > ${gadget}/idVendor
echo "${product_id}" > ${gadget}/idProduct
echo "${bcd_device}" > ${gadget}/bcdDevice
echo "${device_protocol}" > ${gadget}/bDeviceProtocol

mkdir -p ${gadget}/strings/0x409
echo "${manufacturer}" > ${gadget}/strings/0x409/manufacturer
echo "${product}" > ${gadget}/strings/0x409/product
echo "${serial}" > ${gadget}/strings/0x409/serialnumber

mkdir ${gadget}/configs/c.1
echo "${attr}" > ${gadget}/configs/c.1/bmAttributes
echo "${power}" > ${gadget}/configs/c.1/MaxPower
mkdir -p ${gadget}/configs/c.1/strings/0x409
echo "${config1}" > ${gadget}/configs/c.1/strings/0x409/configuration

mkdir -p ${gadget}/os_desc
echo "1" > ${gadget}/os_desc/use
echo "${ms_vendor_code}" > ${gadget}/os_desc/b_vendor_code
echo "${ms_qw_sign}" > ${gadget}/os_desc/qw_sign

mkdir -p ${gadget}/functions/rndis.usb0
echo "${dev_mac}" > ${gadget}/functions/rndis.usb0/dev_addr
echo "${host_mac}" > ${gadget}/functions/rndis.usb0/host_addr
echo "${ms_compat_id}" > ${gadget}/functions/rndis.usb0/os_desc/interface.rndis/compatible_id
echo "${ms_subcompat_id}" > ${gadget}/functions/rndis.usb0/os_desc/interface.rndis/sub_compatible_id

# HID
mkdir -p ${gadget}/functions/hid.usb0
echo 1 > ${gadget}/functions/hid.usb0/protocol
echo 1 > ${gadget}/functions/hid.usb0/subclass
echo 8 > ${gadget}/functions/hid.usb0/report_length
echo "05010906a1018501050719e029e71500250175019508810295017508810395057501050819012905910295017503910395067508150025650507190029658100c0050C0901A1018502050C150025017501950a09B509B609B709CD09E209E909EA0A23020A94010A9201810295068101C0" | xxd -r -ps > ${gadget}/functions/hid.usb0/report_desc

ln -s ${gadget}/configs/c.1 ${gadget}/os_desc
ln -s ${gadget}/functions/rndis.usb0 ${gadget}/configs/c.1
ln -s ${gadget}/functions/hid.usb0 ${gadget}/configs/c.1/

ls /sys/class/udc > ${gadget}/UDC
udevadm settle -t 5 || :
ifup usb0
ifconfig usb0 10.42.0.1 netmask 255.255.255.252 up
#service dnsmasq restart

chmod 777 /dev/hidg0
