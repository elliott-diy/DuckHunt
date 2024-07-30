import ctypes
import os

import keyboard
import time
import pywinusb.hid as hid

threshold = 0.50
char_sample = 20

last_time = time.time()
time_diffs = []
alerts = 0
auto_lock = False
keys_to_ignore = [
    'shift', 'ctrl', 'alt', 'caps lock', 'backspace', 'enter', 'tab', 'esc',
    'up', 'down', 'left', 'right', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7',
    'f8', 'f9', 'f10', 'f11', 'f12', 'insert', 'delete', 'home', 'end',
    'page up', 'page down', 'print screen', 'scroll lock', 'pause', 'num lock',
    'windows', 'right windows', 'menu', 'right menu', 'left windows', 'left menu',
    'left shift', 'right shift', 'left ctrl', 'right ctrl', 'left alt', 'right alt',
    'left arrow', 'right arrow', 'up arrow', 'down arrow', 'space', 'backspace',
    'enter', 'tab', 'esc', 'insert', 'delete', 'home', 'end', 'page up',
    'page down', 'print screen', 'scroll lock', 'pause', 'num lock', 'windows',
    'right windows', 'menu', 'right menu', 'left windows', 'left menu',
    'left shift', 'right shift', 'left ctrl', 'right ctrl', 'left alt', 'right alt',
    'left arrow', 'right arrow', 'up arrow', 'down arrow', 'space', 'w', 'a', 's', 'd'
]


def list_hid_devices():
    all_devices = hid.HidDeviceFilter().get_devices()
    device_list = []

    for device in all_devices:
        device_info = {
            "product_name": device.product_name,
            "vendor_name": device.vendor_name,
            "vendor_id": device.vendor_id,
            "product_id": device.product_id,
            "serial_number": device.serial_number
        }
        device_list.append(device_info)

    return device_list


initial_hid_devices = list_hid_devices()


def compare_hid_devices(initial_devices, current_devices):
    initial_set = {tuple(device.items()) for device in initial_devices}
    current_set = {tuple(device.items()) for device in current_devices}

    new_devices = current_set - initial_set
    if new_devices:
        message = "New HID devices detected:\n\n"
        for device in new_devices:
            device_info = dict(device)
            message += (
                f"Device: {device_info['product_name']}\n"
                f"Manufacturer: {device_info['vendor_name']}\n"
                f"Vendor ID: {device_info['vendor_id']}\n"
                f"Product ID: {device_info['product_id']}\n"
                f"Serial Number: {device_info['serial_number']}\n\n"
            )
        return message.strip()
    else:
        return None


def show_message_box(title, message):
    MB_ICONWARNING = 0x30
    MB_TOPMOST = 0x00040000
    MB_OK = 0x00000001
    MB_SYSTEMMODAL = 0x00001000

    ctypes.windll.user32.MessageBoxW(None, message, title, MB_OK | MB_ICONWARNING | MB_TOPMOST | MB_SYSTEMMODAL)


def alert_trigger():
    for i in range(150):
        keyboard.block_key(i)

    current_hid_devices = list_hid_devices()

    new_devices_info = compare_hid_devices(initial_hid_devices, current_hid_devices)

    if auto_lock == True:
        os.system("shutdown /l")

    if new_devices_info:
        message = (
            "### Security Alert ###\n\n"
            "Suspicious activity has been detected.\n\n"
            "Your keyboard input has been temporarily paused to protect your system from potential physical threats.\n"
            "A new USB HID device has been detected. This device might be attempting to act as a keyboard to execute potentially dangerous commands or actions.\n\n"
            "Details of the newly detected device(s):\n\n"
            f"{new_devices_info}\n\n"
            "A malicious USB device could pose a serious physical threat to your system. Such devices might mimic a keyboard to execute harmful commands without your knowledge.\n"
            "If you do not recognize these devices, it is strongly recommended to unplug them immediately.\n"
            "If you are unsure what this means or need help, please contact your system administrator for assistance.\n\n"
            "The system will resume normal operation in 30 seconds.\n\n"
            "If this alert occurs frequently, consider adjusting the detection settings:\n"
            "- **Lower the detection threshold** to increase sensitivity.\n"
            "- **Increase the character sample size** to improve accuracy.\n"
            "Consult the documentation or your system administrator for guidance on adjusting these settings."
        )
    else:
        message = (
            "### Security Alert ###\n\n"
            "Suspicious activity has been detected.\n\n"
            "Your keyboard input has been temporarily paused to protect your system from potential physical threats.\n"
            "No new USB HID devices were detected. This may be a false positive or the device might have been plugged in before the detection script was running.\n\n"
            "A malicious USB device could pose a serious physical threat to your system. If you are unsure what this means or need help, please contact your system administrator for assistance.\n\n"
            "The system will resume normal operation in 30 seconds.\n\n"
            "If this alert occurs frequently, consider adjusting the detection settings:\n"
            "- **Lower the detection threshold** to increase sensitivity.\n"
            "- **Increase the character sample size** to improve accuracy.\n"
            "Consult the documentation or your system administrator for guidance on adjusting these settings."
        )

    show_message_box("Security Alert", message)

    time.sleep(30)

    for i in range(150):
        keyboard.unblock_key(i)


def on_key_event(event):
    if event.event_type == 'down':
        if event.name in keys_to_ignore:
            return
        global last_time
        current_time = time.time()
        time_diff = current_time - last_time
        last_time = current_time

        time_diffs.append(time_diff)
        if len(time_diffs) > char_sample:
            time_diffs.pop(0)

        if len(time_diffs) == char_sample:
            avg_time_diff = sum(time_diffs) / len(time_diffs)
            if avg_time_diff == 0:
                return
            if all(abs(td - avg_time_diff) / avg_time_diff < threshold for td in time_diffs):
                global alerts
                alerts += 1
                if alerts > 2:
                    alert_trigger()


keyboard.hook(on_key_event)

keyboard.wait()
