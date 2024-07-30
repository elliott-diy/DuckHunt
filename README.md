
# DuckHunt | USB HID Security Monitor

This program is designed to monitor keyboard input and detect any suspicious activity indicative of a potential USB HID (Human Interface Device) attack. It works by analyzing the typing rhythm and detecting new HID devices that might be attempting to mimic keyboard input to execute unauthorized commands on the system. When suspicious activity is detected, the program temporarily blocks keyboard input and alerts the user.

## Features

- **Detection of Suspicious Typing Patterns**: Analyzes typing rhythm to detect unusual patterns that may indicate a script or unauthorized hardware device.
- **USB HID Device Monitoring**: Checks for newly connected USB devices that could pose a threat to system security.
- **Automatic System Lock**: Optionally locks the system if suspicious activity is detected.
- **Visual Alerts**: Provides on-screen alerts when suspicious activity is detected.

## Installation

To run this program, you'll need Python installed on your Windows system, along with a few Python packages. Follow the steps below to install the necessary components:

### Prerequisites

- **Python**: Make sure you have Python installed. You can download it from the official [Python website](https://www.python.org/downloads/).
- **Pip**: Ensure that pip is installed to manage Python packages.

### Install Required Packages

Open a command prompt and run the following command to install the required Python packages:

```bash
pip install keyboard pywinusb
```

## Usage

Once you have installed the necessary packages, you can run the program by executing the Python script. The program will begin monitoring your keyboard input and connected USB devices for any suspicious activity.

### Running the Program

```bash
python main.py
```


### How It Works

1. **Typing Pattern Analysis**: The program calculates the average time difference between consecutive keystrokes and compares it against a predefined threshold. If the keystroke timing is consistent and suspicious, it raises an alert.
2. **USB HID Device Detection**: It continuously monitors USB HID devices connected to the system. If a new device is detected, it checks whether it is a potential threat and alerts the user.
3. **Security Alerts**: If a potential threat is detected, the program will:
   - Block all keyboard input for 30 seconds.
   - Display a security alert message box with details about the detected threat.
   - Optionally lock the system to prevent unauthorized access.

### Configuration Options

- **Threshold**: Adjust the sensitivity of typing pattern detection. The lower the threshold, the more sensitive the detection.
- **Character Sample**: The number of keystrokes used to calculate the average typing speed. Increasing this number may improve accuracy but delay detection.

### Code Configuration

You can modify the following variables in the script to adjust the behavior of the program:

```python
threshold = 0.50   # Sensitivity threshold for typing pattern detection
char_sample = 20   # Number of keystrokes to analyze for typing pattern

auto_lock = False  # Set to True to enable automatic system lock on alert
```

### Adjusting Detection Sensitivity

- **Increase Sensitivity**: Lower the `threshold` value to make the program more sensitive to typing patterns.
- **Decrease Sensitivity**: Raise the `threshold` value to reduce sensitivity, which may help reduce false positives.

### Keyboard Keys to Ignore

The program ignores certain keys when analyzing typing patterns. You can customize the list of keys to ignore in the `keys_to_ignore` list in the script.

```python
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
```

### Example Alert Message

When a new USB HID device is detected, the following alert message is displayed:

```
### Security Alert ###

Suspicious activity has been detected.

Your keyboard input has been temporarily paused to protect your system from potential physical threats.
A new USB HID device has been detected. This device might be attempting to act as a keyboard to execute potentially dangerous commands or actions.

Details of the newly detected device(s):

Device: <Device Name>
Manufacturer: <Manufacturer Name>
Vendor ID: <Vendor ID>
Product ID: <Product ID>
Serial Number: <Serial Number>

A malicious USB device could pose a serious physical threat to your system. Such devices might mimic a keyboard to execute harmful commands without your knowledge.
If you do not recognize these devices, it is strongly recommended to unplug them immediately.
If you are unsure what this means or need help, please contact your system administrator for assistance.

The system will resume normal operation in 30 seconds.

If this alert occurs frequently, consider adjusting the detection settings:
- **Lower the detection threshold** to increase sensitivity.
- **Increase the character sample size** to improve accuracy.
Consult the documentation or your system administrator for guidance on adjusting these settings.
```

## Contributing

If you wish to contribute to the development of this project, please feel free to submit a pull request or report any issues you encounter. Contributions are always welcome!

## License

This project is licensed under the MIT License. You can freely use, modify, and distribute the software according to the terms of the license.

