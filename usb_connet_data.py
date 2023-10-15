import pyudev
import os
import subprocess
import getpass
from cryptography.fernet import Fernet
import sys
from usbCheckStatus import * 

# Define the expected password
EXPECTED_PASSWORD = 'pankaj'
# Initialize the password as None
password = None

def bind_usb_device(device_node):
    global password
    for _ in range(3):  # Allow up to 3 password attempts
        if password is None:
            print("Please enter the password to unlock the USB device:")
            entered_password = getpass.getpass()
            
            if entered_password == EXPECTED_PASSWORD:
                print("|=> You Entered correct password")
                print("|=> Plase wait for some time to bind your USb ...")
                encryption_command = f'encrypt_usb --device {device_node} --password {entered_password}'
                # Run the encryption/decryption command
                try:
                    subprocess.run(encryption_command, shell=True, check=True)
                    print("USB device bound successfully.")
                    break  # Exit the loop on success
                except subprocess.CalledProcessError as e:
                    print(f"Error binding USB device: {e}")
            else:
                print("Incorrect password. Please try again.")
        else:
            print("A password is already set. USB device not bound.")
            
    else:
        print("Maximum password attempts reached. USB device not bound.")
        sys.exit(1)
            
     



def alert_on_usb_insert(action, device):
    print("---------------------")
    print(action)
    print(device)
    print("---------------------")
    if  action == 'add' :
        print("USB device inserted:")
        print(f"Device Name: {device.device_node}")
        print(f"Device ID: {device.get('ID_SERIAL_SHORT', 'N/A')}")
        bind_usb_device(device.device_node)
        # You can replace the print statements with your alert mechanism, e.g., sending a notification

def main():
    context = pyudev.Context()

    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem='usb')
    # monitor.filter_by(subsystem='usb_device')

    observer = pyudev.MonitorObserver(monitor, alert_on_usb_insert)
    observer.start()

    try:
        print("Monitoring for USB devices. Press Ctrl+C to exit.")
        observer.join()
    except KeyboardInterrupt:
        observer.stop()
        observer.join()

if __name__ == "__main__":
    main()
