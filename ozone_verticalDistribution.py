from climt import Frierson06LongwaveOpticalDepth, GrayLongwaveRadiation, get_default_state, SlabSurface
from sympl import AdamsBashforth
import numpy as np
from matplotlib import pyplot as plt
import datetime

diagnostic = Frierson06LongwaveOpticalDepth(linear_optical_depth_parameter=-0.3,longwave_optical_depth_at_equator=7, longwave_optical_depth_at_poles=2.7)
slab = SlabSurface()
radiation = GrayLongwaveRadiation(tendencies_in_diagnostics=True)
state = get_default_state([radiation, diagnostic,slab])
time_stepper = AdamsBashforth([radiation, slab])
timestep = datetime.timedelta(hours=4)

for i in range(10):
	state.update(diagnostic(state))
	diagnostics, state = time_stepper(state,timestep)
	state.update(diagnostics)

longwaveTau = np.array(state['longwave_optical_depth_on_interface_levels'][:]).flatten()
#rad = np.array(state['longwave_'])
airPressure = np.array(state['air_pressure_on_interface_levels'][:])
ozoneDistribution = np.zeros(airPressure.shape)

airPressure = airPressure.flatten()
# Pulls out indexes of altitudes within ozone range
indices = [list(airPressure).index(i) for i in airPressure if i > 500 and i < 16000] 

heating = np.gradient(longwaveTau)
heat = [longwaveTau[i]-longwaveTau[i-1] for i in range(len(longwaveTau))]

upFlux = np.array(state['upwelling_longwave_flux_in_air']).flatten()[:28]
downFlux = np.array(state['downwelling_longwave_flux_in_air']).flatten()[:28]
netFlux = upFlux - downFlux
pres = np.array(state['air_pressure']).flatten()
plt.plot(upFlux,pres,label="up")
plt.plot(downFlux,pres,label="down")
plt.plot(netFlux,pres,label="net")
plt.legend()
plt.gca().invert_yaxis()
plt.show()