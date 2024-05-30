import matplotlib.pyplot as plt
from seabreeze.spectrometers import Spectrometer, list_devices

l = list_devices()
print(l)

spec =  Spectrometer(l[0])
#spec.open()

spec = Spectrometer.from_first_available()

wavelengths = spec.wavelengths()
print(wavelengths)
intensities = spec.intensities()
print(intensities)
fig, ax = plt.subplots()
ax.plot(wavelengths, intensities)



spec._dev.f.spectrometer.get_integration_time_micros_limits()
spec.integration_time_micros(100000)
spec._dev.f.thermo_electric.enable_tec(True)
spec._dev.f.thermo_electric.read_temperature_degrees_celsius()
spec._dev.f.thermo_electric.set_temperature_setpoint_degrees_celsius(-30)

import seabreeze.cseabreeze as csb
api = csb.SeaBreezeAPI()
api.supported_models()

#%%
from pyOceanopticsSpectrometer import driver

device = driver.OceanopticsSpectrometer()

device.list_devices()

device.connect_device('NQ5500252')
device.connect_device('HR4C4675')
device.disconnect_device()

device.wavelengths

device.spectrum

device.TEC_Temperature

device.TEC_Temperature = -30

device.integration_time_limits_microseconds

device.integration_time_microseconds = 1600000001