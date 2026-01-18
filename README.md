- Check list of devices that are supported by seabreeze
- If your device is supported by cseabreeze, then no other step is required
- If your device is supported only via pyseabreeze, then you need to do the following
    - Set up pyOceanOpticsSpectrometer so that it uses pyseabreeze
    - Install pip install pyusb
    - Install pip install libusb
    - You might need to manually add a .dll file to your system. Go here https://libusb.info/, Downloads -> Latest Windows Binaries. In the zip file, enter either the folder MinGW64/dll or MinGW32/dll (depending on your OS). Copy the file  libusb-1.0.dll into C:\Windows\System32

# pyOceanopticsSpectrometer

```pyOceanopticsSpectrometer``` is a Python library/GUI interface to control several models of spectrometers from Ocean Optics. The package is composed of two parts, a
low-level driver to perform basic operations, and high-level GUI, written with PyQt5, which can be easily embedded into other GUIs. It heavily relies on the package [python-seabreeze](https://github.com/ap--/python-seabreeze).

The interface can work either as a stand-alone CLI or GUI application, or as a module of [ergastirio](https://github.com/MicheleCotrufo/ergastirio).

The list of devices supported can be found in the table in the readme file of [python-seabreeze](https://github.com/ap--/python-seabreeze), with either the `cseabreeze' or 'pyseabreeze (usb)' backend.

## Table of Contents
 - [Installation](#installation)
 <!---
  - [Usage via the low-level driver](#usage-via-the-low-level-driver)
	* [Examples](#examples)
 - [Usage as a stand-alone GUI interface](#usage-as-a-stand-alone-GUI-interface)
 - [Embed the GUI within another GUI](#embed-the-gui-within-another-gui)
-->

## Installation

Use the package manager pip to install,

```bash
pip install pyOceanopticsSpectrometer
```
The package ```python-seabreeze``` uses two different backends (`cseabreeze` and `pyseabreeze (usb)`), and some devices are compatible with only one backend (see table in readme file of [python-seabreeze](https://github.com/ap--/python-seabreeze)). By default, ```pyOceanopticsSpectrometer``` uses the backend `pyseabreeze (usb)`, which is referred to as just `pyseabreeze` in the code. To change this to  `cseabreeze`, after installation, go to the directory which contains the code of ```pyOceanopticsSpectrometer```, open the file `config.json`, and change the value of "backend" from `pyseabreeze` to `cseabreeze`.


 <!---
**Important:** in order to be accessible from this library, the console needs to be set to "PM100D NI-VISA" modality, and not to
"TLPM modality". Typically, if you used recent Thorlabs software to acquire from a console, that will automatically set the console to "TLPM modality".
You can use the utility [Power Meter Driver Switcher](https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=OPM) to switch between modalities.

## Usage via the low-level driver

`pyThorlabsPM100x` provides also a low-level driver, based on the library `pyvisa`, to directly interface with the powermeter console.

```python
from pyThorlabsPM100x.driver import ThorlabsPM100x
powermeter = ThorlabsPM100x()
available_devices = powermeter.list_devices()
print(available_devices)
powermeter.connect_device(device_addr = available_devices[0][0])
print(powermeter.power)
powermeter.disconnect_device()
```
The method `list_devices()` returns a list, with each element representing one available device in the format `[address,identity,model]`. The string `address` contains 
the physical address of the device. The line `powermeter.connect_device(device_addr = available_devices[0][0])` establishes a connection to the first device found.
We then print the power currently read by the console, and finally disconnect from it.

The class `ThorlabsPM100x` supports several properties and methods to communicate with the console and to read/change its settings. Some of the properties are read-only, while others can be set. A full list of properties and methods is available here below

**Properties**

| Property | Type | Description | <div style="width:300px"> Can be set?</div> | Notes |
| --- | --- | --- | --- | --- |
| `power` | (float,str) | First element of list is the power currently read by the console, second element is the power units. | No |
| `power_units` | str | Power units | No |
| `wavelength` | int | Operating wavelength (in nanometers) of the console. | Yes | Each powermerter head has a different range of acceptable wavelengths. The driver will **not** return an error when trying to set a wavelength outside of this range. |
| `power_range` | float | Current power range, defined as the maximum power measurable in the current range | Yes | When setting this property to a particular value X, the console will change the power range to the smallest power range which allows to measure the desired power X. |
| `min_power_range` | float | Minimum power range available. | No | For the same console/head, this value might vary for different wavelengths. |
| `max_power_range` | float | Maximum power range available. | No | For the same console/head, this value might vary for different wavelengths. |
| `auto_power_range`| bool | Determines whether the consol is in auto power range or not. | Yes | |
| `being_zeroed`| bool | It is True if zero of the device is currently being set. | No | The property `power` will return (None,'') if read while `being_zeroed==True` |

**Methods**
| Method | Returns | Description  |
| --- | --- | --- | 
| `list_devices()` | list |  Returns a list of all available devices. Each element of the list identifies a different device, and it is a three-element list in the form `[address,identity,model]`. The string `address` contains the physical address of the device. The string `idn` contains the 'identity' of the device (which is the answer of the device to the visa query '*IDN?'). The string `model` contains the device model (either 'PM100A' or 'PM100D').| 
| `connect_device(device_addr: str)` | (str,int) |  Attempt to connect to the device identified by the address in the string  `device_addr`. It returns a list of two elements. The first element is a string containing either the ID number of the connected device or an error message. The second element is an integer, equal to 1 if connection was succesful or to 0 otherwise. | 
| `disconnect_device()` | (str,int)  | Attempt to disconnect the currently connected device. If no device is currently connected, it raises a `RuntimeError`. It returns a list of two elements. The first element is a string containing info on succesful disconnection or an error message. The second element is an integer, equal to 1 if disconnection was succesful or to 0 otherwise.  |
| `read_min_max_wavelength()` | (float,float) |  Returns the minimum and maximum operating wavelengths for the connected device. If no device is currently connected, it raises a `RuntimeError`. | 
| `set_zero()` | int | Set the zero to the currently connected (if any) console. The returned value is 1 if the operation was successful, or 0 if any error occurred. | 
| `move_to_next_power_range(direction: int)`| None | It increases or decreases the power range of the console, depending on whether the input parameter is `direction=+1` or `direction=-1`. | 


### Examples
```python
from pyThorlabsPM100x.driver import ThorlabsPM100x
powermeter = ThorlabsPM100x()
available_devices = powermeter.list_devices() #Check which devices are available
print(available_devices)
powermeter.connect_device(device_addr = available_devices[0][0]) #Connect to the first available device
print(powermeter.power) #print the power currently read
print(powermeter.wavelength) #print the operating wavelength
(minWL,maxWL) = powermeter.read_min_max_wavelength() #read max and min available wavelengths
powermeter.wavelength = maxWL #set wavelength to the max
print(powermeter.power_range) #print current power range
powermeter.move_to_next_power_range(direction=+1) #increaase power range
print(powermeter.power_range) #print new power range
powermeter.disconnect_device() #disconnect the device
```

## Usage as a stand-alone GUI interface
The installation should set up an entry point for the GUI. Just typing
```bash
pyThorlabsPM100x
```
in the command prompt will start the GUI.

## Embed the GUI within another GUI
The GUI controller can also be easily integrated within a larger graphical interface, as shown in the example [here](https://github.com/MicheleCotrufo/pyThorlabsPM100x/blob/master/examples/embedding_in_gui.py).

-->