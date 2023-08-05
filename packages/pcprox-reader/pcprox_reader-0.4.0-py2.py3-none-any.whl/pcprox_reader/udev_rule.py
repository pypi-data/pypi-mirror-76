import subprocess
from os import path


def create_udev_rule():
    filename = "/etc/udev/rules.d/95-usb-perms.rules"
    print("You will need to run this script as sudo...")
    print("Checking if rule exists...")
    if path.exists(filename):
        print("All good, file already exists!")
        return 0
    else:
        try:
            txt = '''SUBSYSTEM=="usb", ATTRS{idVendor}=="0c27", ATTR{idProduct}=="3bfa", GROUP="plugdev", MODE="0666"'''
            print(f"Writing Rule to {filename}")
            f = open(filename, "w")
            f.write(txt)
            f.close()
            print("Rule written, updating udev...")
            subprocess.run("sudo udevadm trigger", shell=True)
            print(" udev rule triggered, unplug and plug device back in...")
            print(" ...and it should work!")
        except PermissionError:
            print("!!!")
            print("FAILED!")
            print("re-run script as sudo")
            print("!!!")


create_udev_rule()
