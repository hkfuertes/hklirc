# hkLirc
This is a simple project for a Raspberry Pi that aims to bridge the **gpio-ir** interface with a **HID device**.

There are 3 parts to the project, the [gadget](gadget) configuration part, the [server](server) to manage the mappings and the actual python [daemon](daemon_python) that will trigger the actual keystrokes in the connected PC.

## Installation
`wget -O - https://raw.githubusercontent.com/hkfuertes/hklirc/master/hklirc-installer.sh | bash`

