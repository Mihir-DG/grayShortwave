from matplotlib import pyplot as plt
import numpy as np

fig = plt.figure()
x = np.linspace(-(np.pi)/2,(np.pi)/2,180)
y = np.cos(x+(np.pi)*1.07)+0.5
plt.xlabel("Latitude (Degrees)")
plt.ylabel("Variation in Vertical Profile")
plt.plot(360*x/(2*np.pi),y)
plt.savefig("ozone_horizontalAnomaly")
plt.show()

# HORIZONTAL DISTRIBUTION:
# y = 150 cos(x + 1.07pi) + 375 (For Dobson Units)
# x = {-pi/2, +pi/2}

# HORIZONTAL ANOMALY: cos(x + 1.07pi) + 0.5