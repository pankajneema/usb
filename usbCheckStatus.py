# Author: Mr.Hacker
# Date: Oct 1, 2023
# Description: This is a Python script for USB deletion tool.    


#import module
import pyudev
import os
import subprocess
import getpass
import threading
import platform
import sys, traceback

#check operating system
_operatingSystem_ = platform.system() 
_operatingSystemVersion_ = platform.version() 
print(f"||=> Your System Details -> OS:{_operatingSystem_}, Details:{_operatingSystemVersion_} <||")

#this class for linux 
class linux:

    def __init__(self,mount_path):
        self.mount_path = mount_path

    def __str__(self) -> str:
        print(f"Your Mount {self.mount_path}")
        pass    

    def __CheckAutoMount__(self):
        print(f"USB auto Mount Enable staus Checking  ... ")
        try:
            # Use systemctl to check the status of udisks2 service
            output = subprocess.check_output(["systemctl", "is-active", "udisks2"])
            # print(output)
            if output.strip().decode("utf-8") == "active":
                return True
        except subprocess.CalledProcessError as suberr:
            return False
        except Exception as e:
            print(f"Exception:-> {e}")
            error = f"{e}"
            return error
            
        
    def __stopAutoMount__(self):
        try:
            output = subprocess.check_output(["systemctl", "stop", "udisks2"])
            print(output)
            print(f"Mount Path = {self.mount_path} to stop auto monut")
            return True
        except Exception as e:
            print(f"Some Error Occred -> {e}")
    
if _operatingSystem_.lower() == "linux":
    print(f"||-> COME IN  =>{_operatingSystem_}")

    #get mount path  now hardcoded but it will be dynamic 
    device_path_to_check = '/dev/sdb2' 

    #get automount status -> make object of linux class for __CheckAutoMount__  this 
    _linuxObj_ = linux(device_path_to_check)
    autoMountStatus = _linuxObj_.__CheckAutoMount__()
    print(f"Your USB auto mount status is {autoMountStatus}")
    # sys.exit()
    if autoMountStatus == True:
        StopMount = _linuxObj_.__stopAutoMount__()
        if StopMount == True:
            print("Stop Auto mount done")
        else:    
            print(f"Some error -> {StopMount}")
    elif autoMountStatus == False: 
         print(" Auto mount Alredy Stopped")  
    else:
        print("Some Error Occored : {StopMount}")     
    


    













# # Define the expected password
# EXPECTED_PASSWORD = 'pankaj'

# # Initialize the password as None
# password = None

# # Lock to synchronize access to the password variable
# password_lock = threading.Lock()

# # Flag to indicate whether the USB device is bound
# usb_device_bound = False

# def bind_usb_device(device_node):
#     global password, usb_device_bound
#     with password_lock:
#         if password is not None and not usb_device_bound:
#             if password == EXPECTED_PASSWORD:
#                 # Perform encryption/decryption operations here using the password
#                 # For example, you can use a tool like cryptsetup for device encryption
#                 # Replace 'your_encryption_command' with the actual command for your use case
#                 encryption_command = f'your_encryption_command --device {device_node} --password {password}'

#                 # Run the encryption/decryption command
#                 try:
#                     subprocess.run(encryption_command, shell=True, check=True)
#                     print("USB device bound successfully.")
#                     usb_device_bound = True
#                 except subprocess.CalledProcessError as e:
#                     print(f"Error binding USB device: {e}")

# def monitor_usb():
#     context = pyudev.Context()
#     monitor = pyudev.Monitor.from_netlink(context)
#     monitor.filter_by(subsystem='usb')

#     observer = pyudev.MonitorObserver(monitor, alert_on_usb_add)
#     observer.start()

#     try:
#         print("Monitoring for USB devices. Press Ctrl+C to exit.")
#         observer.join()
#     except KeyboardInterrupt:
#         observer.stop()
#         observer.join()

# def alert_on_usb_add(action, device):
#     print("---------------------")
#     print(action)
#     print(device)
#     print("---------------------")
#     if  action == 'add' :
#         print("USB device inserted:")
#         print(f"Device Name: {device.device_node}")
#         print(f"Device ID: {device.get('ID_SERIAL_SHORT', 'N/A')}")
#         bind_usb_device(device.device_node)
#         # You can replace the print statements with your alert mechanism, e.g., sending a notifica
#         if not usb_device_bound:
#             enter_password()

# def enter_password():
#     global password
#     with password_lock:
#         if password is None:
#             print("Please enter the password to unlock the USB device:")
#             entered_password = getpass.getpass()
#             password = entered_password

# if __name__ == "__main__":
#     # Start the USB monitoring process in a separate thread
#     usb_monitor_thread = threading.Thread(target=monitor_usb)
#     usb_monitor_thread.daemon = True
#     usb_monitor_thread.start()

#     try:
#         # Start the password entry process in the main thread
#         enter_password()
        
#         while True:
#             # Continue running the main program until terminated by the user
#             pass
#     except KeyboardInterrupt:
#         pass
