import numpy as np
from matplotlib import pyplot as plt

""" Input quantities:
1. Solar constant
2. Zenith angle
3. Air Pressure
4. Ozone distribution (mole frac)


- ozone_moleFrac shape - (60,1,1)
- dI/dP = coefficient * o3
- ozone_moleFrac to be replaced with climt.init_ozone output (from initialization.py)
- downward integration is input to upward integration

"""

# Test 1: No absorption

def test1(ozone_moleFrac):
	ozone_moleFrac[:] = 0.
	return ozone_moleFrac


# Test 2: Linear absorption (15% increase in abundance w height)S

def test2(m, ozone_moleFrac):
	test2 = np.empty(ozone_moleFrac.shape)
	test2[0] = ozone_moleFrac[0]
	for elem in range(1,60):
		test2[elem] = test2[elem-1]*(1 + (0.01 * m))
	ozone_moleFrac = test2
	return ozone_moleFrac


# Test 3: Linear absorption (5%, 10%, 15% decrease in abundance w height)

def test3(m, ozone_moleFrac):
	test3 = np.empty(ozone_moleFrac.shape)
	test3[0] = ozone_moleFrac[0]
	for elem in range(1,60):
		test3[elem] = test3[elem-1]*(1 - (0.01 * m))
	ozone_moleFrac = test3
	return ozone_moleFrac


# Test 4: Constant absorption

def test4(ozone_moleFrac):
	ozone_moleFrac[:] = ozone_moleFrac[0]
	return ozone_moleFrac


# Test 5: Absorption at specific heights

def test5(ozone_moleFrac):
	meanOzone = np.mean(ozone_moleFrac)
	print(meanOzone)
	ozone_moleFrac[:] = 0.
	ozone_moleFrac[30] = meanOzone
	ozone_moleFrac[15] = meanOzone
	ozone_moleFrac[40] = meanOzone
	return ozone_moleFrac


def integrate_shortwave_downward(ozone_moleFrac):
	I = np.empty(ozone_moleFrac.shape)
	I[-1][:] = solarConstant
	for elem in range(58,-1,-1):
		dI = (airPressure[elem]) * ozone_moleFrac[elem] * attenuationCoefficient
		I[elem] = I[elem + 1]*(1 - dI)
	return I

def integrate_shortwave_upward(downFlux, surfaceAlbedo, ozone_moleFrac):
	I = np.empty(ozone_moleFrac.shape)
	I[0] = surfaceAlbedo * downFlux[0]
	for elem in range(1,60):
		dI = (airPressure[elem]) * ozone_moleFrac[elem] * attenuationCoefficient
		I[elem] = I[elem - 1] * (1 - dI)
	return I

def main(ozone_moleFrac):
	downFlux = integrate_shortwave_downward(ozone_moleFrac)
	upFlux = integrate_shortwave_upward(downFlux, surfaceAlbedo, ozone_moleFrac)
	print(downFlux.flatten())
	print(upFlux.flatten())
	netFlux = (upFlux - downFlux).flatten()
	return downFlux, upFlux, netFlux


# FOR TESTS 2 AND 3
def plotting_test_23(test, ozone_moleFrac):

	ozone_moleFrac = test(5, ozone_moleFrac)
	downFlux5, upFlux5, netFlux5 = main(ozone_moleFrac)
	ozone_moleFrac = test(10, ozone_moleFrac)
	downFlux10, upFlux10, netFlux10 = main(ozone_moleFrac)
	ozone_moleFrac = test(15, ozone_moleFrac)
	downFlux15, upFlux15, netFlux15 = main(ozone_moleFrac)

	downFluxes = [downFlux5, downFlux10, downFlux15]
	upFluxes = [upFlux5, upFlux10, upFlux15]
	netFluxes = [netFlux5, netFlux10, netFlux15]
	legend = ["5","10","15"]

	fig, ax = plt.subplots()
	for i in range(3):
		ax.plot(netFluxes[i].flatten(), airPressure.flatten(), label = legend[i])
	plt.ylabel("Pressure (Pa)")
	plt.xlabel("Net flux")
	ax.set_yscale('log')
	plt.gca().invert_yaxis()
	plt.legend()
	plt.savefig("graphs/" + test.__name__ + "/netFlux.png")


	fig, ax = plt.subplots()
	for i in range(3):
		ax.plot(downFluxes[i].flatten(), airPressure.flatten(), label = legend[i])
	plt.ylabel("Pressure (Pa)")
	plt.xlabel("Downward flux")
	ax.set_yscale('log')
	plt.gca().invert_yaxis()
	plt.legend()
	plt.savefig("graphs/" + test.__name__ + "/downFlux.png")

	fig, ax = plt.subplots()
	for i in range(3):
		ax.plot(upFluxes[i].flatten(), airPressure.flatten(), label = legend[i])
	plt.ylabel("Pressure (Pa)")
	plt.xlabel("Upward flux")
	ax.set_yscale('log')
	plt.gca().invert_yaxis()
	plt.legend()
	plt.savefig("graphs/" + test.__name__ + "/upFlux.png")


# FOR TESTS 1, 4, 5 - 
def plotting_test_145(test, ozone_moleFrac):
	ozone_moleFrac = test(ozone_moleFrac)
	downFlux, upFlux, netFlux = main(ozone_moleFrac)

	fig, ax = plt.subplots()
	ax.plot(netFlux, airPressure.flatten())
	plt.ylabel("Pressure (Pa)")
	plt.xlabel("Net flux")
	ax.set_yscale('log')
	plt.gca().invert_yaxis()
	plt.savefig("graphs/" + test.__name__ + "/netFlux.png")


	fig, ax = plt.subplots()
	ax.plot(downFlux.flatten(), airPressure.flatten())
	plt.ylabel("Pressure (Pa)")
	plt.xlabel("Downward flux")
	ax.set_yscale('log')
	plt.gca().invert_yaxis()
	plt.savefig("graphs/" + test.__name__ + "/downFlux.png")

	fig, ax = plt.subplots()
	ax.plot(upFlux.flatten(), airPressure.flatten())
	plt.ylabel("Pressure (Pa)")
	plt.xlabel("Upward flux")
	ax.set_yscale('log')
	plt.gca().invert_yaxis()
	plt.savefig("graphs/" + test.__name__ + "/upFlux.png")


solarConstant = 1360

mol_profiles = np.load('molecule_profiles.npz')
tp_profiles = np.load('thermodynamic_profiles.npz')

attenuationCoefficient = 0.6
surfaceAlbedo = 0.3
airPressure = tp_profiles['air_pressure'][:, np.newaxis, np.newaxis]
ozone_moleFrac = mol_profiles['ozone'][:, np.newaxis, np.newaxis]

plotting_test_145(test4, ozone_moleFrac)
plotting_test_23(test2, ozone_moleFrac)
plotting_test_23(test3, ozone_moleFrac)
plotting_test_145(test1, ozone_moleFrac)
plotting_test_145(test5, ozone_moleFrac)


# Instellation --> zenith angle (S cos theta)