from .Function import Function
from .Environment import Environment
from .SolidMotor import SolidMotor
from .Rocket import Rocket
from .Flight import Flight

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib import pyplot as plt
import matplotlib
import matplotlib as mpl

from scipy.optimize import curve_fit

# Configure plot styles

# Sizes
mpl.rcParams['figure.figsize'] = [12.0, 6.0]
mpl.rcParams['figure.dpi'] = 120
mpl.rcParams['savefig.dpi'] = 120

# Font
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 22}
matplotlib.rc('font', **font)

# Style
plt.style.use(['science'])

Mandioca = SolidMotor(
    thrustSource="./data/mandioca/thrustCurve.csv",
    interpolationMethod='linear',
    burnOut=5.78,
    nozzleRadius=0.0335,
    throatRadius=0.0114,
    grainNumber=5,
    grainSeparation=0.010,
    grainDensity=1700,
    grainOuterRadius=0.047,
    grainInitialInnerRadius=0.016,
    grainInitialHeight=0.156
)

Mandioca.mass()

fit_func = lambda p, a, n: a*p**n
popt,y_ = curve_fit(fit_func, Mandioca.chamberPressure[:, 1], Mandioca.burnRate[:, 1])
a = popt[0]
n = popt[1]

plt.figure()
plt.scatter(1e-5*Mandioca.chamberPressure[:, 1], Mandioca.burnRate[:, 1]*1e3)
plt.plot(1e-5*Mandioca.chamberPressure[:, 1],1e3 * a*Mandioca.chamberPressure[:, 1]**n)
plt.xlabel('Pressure (bar)')
plt.ylabel('Burn rate (mm/s)')
plt.show()

Keron  = SolidMotor(
    thrustSource='./data/Keron/thrustCurve.csv',
    burnOut=5.3,
    reshapeThrustCurve= False,
    grainNumber=6,
    grainSeparation=6/1000,
    grainOuterRadius= 21.40/1000,
    grainInitialInnerRadius=9.65/1000,
    grainInitialHeight=120/1000,
    grainDensity= 1707,
    nozzleRadius=21.642/1000,
    throatRadius=8/1000,
    interpolationMethod='linear'
)

fit_func = lambda p, a, n: a*p**n
popt,y_ = curve_fit(fit_func, Keron.chamberPressure[:, 1], Keron.burnRate[:, 1])
a = popt[0]
n = popt[1]

plt.figure()
plt.plot(1e-5*Keron.chamberPressure[:, 1], Keron.burnRate[:, 1]*1e3)
plt.plot(1e-5*Keron.chamberPressure[:, 1],1e3 * a*Keron.chamberPressure[:, 1]**n)
plt.xlabel('Pressure (bar)')
plt.ylabel('Burn rate (mm/s)')
plt.show()

Pro75M1670.chamberPressure()
Pro75M1670.burnRate()

# Calisto = Rocket(
#     motor=Pro75M1670,
#     radius=127/2000,
#     mass=19.197-2.956,
#     inertiaI=6.60,
#     inertiaZ=0.0351,
#     distanceRocketNozzle=-1.255,
#     distanceRocketPropellant=-0.85704,
#     powerOffDrag='./data/calisto/powerOffDragCurve.csv',
#     powerOnDrag='./data/calisto/powerOnDragCurve.csv'
# )

# Calisto.setRailButtons([0.2, -0.5])

# def drogueTrigger(p, y):
#     # p = pressure
#     # y = [x, y, z, vx, vy, vz, e0, e1, e2, e3, w1, w2, w3]
#     # activate drogue when vz < 0 m/s.
#     return True if y[5] < 0 else False

# def mainTrigger(p, y):
#     # p = pressure
#     # y = [x, y, z, vx, vy, vz, e0, e1, e2, e3, w1, w2, w3]
#     # activate main when vz < 0 m/s and z < 800 m.
#     return True if y[5] < 0 and y[2] < 800 else False

# Main = Calisto.addParachute('Main',
#                             CdS=10.0,
#                             trigger=mainTrigger, 
#                             samplingRate=105,
#                             lag=1.5,
#                             noise=(0, 8.3, 0.5))

# Drogue = Calisto.addParachute('Drogue',
#                             CdS=1.0,
#                             trigger=drogueTrigger, 
#                             samplingRate=105,
#                             lag=1.5,
#                             noise=(0, 8.3, 0.5))