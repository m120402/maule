# from __future__ import division

import numpy as np
import math
import Holtrop as h
import numpy as np
from scipy.optimize import minimize


# import gekko, pip install if needed
from gekko import GEKKO

# create new model
m = GEKKO()

LWL = 205 # length on waterline
LBP = 200 # length between perpendiculars
B = 32 # breadth moulded
Tf = 10 # draught moulded on F.P.
Ta = 10 # draught moulded on A.P.
Vol = 37500 # displacement volume moulded M^3
LCB_LBP = -2.02 # longitudinal centre of buoyancy % fwd of 1/2 LBP
Cm = 0.98 # midship section coefficient
Cwp = .75 # waterplane area coefficient
At = 16 # transom area m^2
Sapp = 50 # wetted area appendages m^2
Cstern = 10 # stern shape parameter
D = 8 # propeller diameter m
Z = 4 # number of propeUer blades	
Clearance = 0.2 # clearance propeller with keel line m
V = 25 #knots
V = V*0.514444 # m/s
g = 9.81 # m/s^2
rho = 1025 #kg/m^3
u_k = 9.37e7 #kinematic viscosity of seawater at 35 g/kg and 25 C

# Bulb Bow
Abt = 20 #m^2
hb = 4 #m


LCB = h.LCB_LBP_2_LCB_LWL(LWL, LBP, LCB_LBP) # longitudinal centre of buoyancy % fwd of 1/2 LWL
T = h.calc_T(Ta, Tf) #m
Rw = h.calc_Rw(V, LWL, g, rho, Vol, B, Ta, Tf, Cm, LCB, Cwp, At, Abt, hb)

Cb = h.calc_Cb(Vol, LWL, B, T)
Cp = h.calc_Cp(Cb, Cm)

Rv = h.calc_Rv(rho, V, LWL, u_k, B, T, Vol, Cp, LCB, Cstern, Cm, Cb, Cwp, Abt)
Ca = h.calc_Ca(LWL)

S = h.calc_S(LWL, T, B, Cm, Cb, Cwp, Abt)

R = h.calc_R(Rv, Rw, rho, V, Ca, S)

print('Relevant test calculations from 1982 Paper')

print('Rw: ' + str(Rw))
print('Rv: ' + str(Rv))
print('Ca: ' + str(Ca))
print('R: ' + str(R))



# print('')

# LWL = 50.00 #m
# B = 12.00 #m
# Tf = 3.10 #m
# Ta = 3.30 #m
# Vol = 900 #m^3
# Sapp = 50 #m^2
# Cstern = 0 #stern shape parameter

# Abt = 0
# iE = 25 #degrees
# Cm = 0.78
# LCB = -4.5 #% L fwd of 1/2L
# At = 10 #m2
# K2_1 = 3
# Cwp = 0.80

def calcWave(x, V, g, rho, Vol, Ta, Tf, Cm, LCB, Cwp, At, Abt, hb):
	LWL = x[0]
	B = x[1]
	Rw = h.calc_Rw(V, LWL, g, rho, Vol, B, Ta, Tf, Cm, LCB, Cwp, At, Abt, hb)
	return Rw

def calcLength(x):
	return x[0]

def objective(x, V = 12.861, g = 9.81, rho = 1025, Vol = 37500, Ta = 10, Tf = 10, Cm = 0.98, LCB = -0.75, Cwp = 0.75, At = 16, Abt = 20, hb = 4):
	return calcWave(x, V, g, rho, Vol, Ta, Tf, Cm, LCB, Cwp, At, Abt, hb)

def constraint1(x):
	return 400 - calcLength(x)

def constraint2(x):
	return calcLength(x)

bl = (100, 300)
bw = (20, 40)

bnds = (bl, bw)

cons = [{'type': 'ineq', 'fun':constraint1},{'type': 'ineq', 'fun':constraint2}]

lengthGuess = 205
widthGuess = 32

x0 = np.array([lengthGuess, widthGuess])

sol = minimize(objective,x0,method = 'SLSQP', bounds = bnds, constraints = cons, options ={'disp':True})

xOpt = sol.x
volumeOpt = -sol.fun

waveOpt = calcWave(xOpt, V, g, rho, Vol, Ta, Tf, Cm, LCB, Cwp, At, Abt, hb)

print('Length: ' + str(xOpt[0]))
print('Width: ' + str(xOpt[1]))
print('Rw: ' + str(waveOpt))



waveOpt = calcWave([205, 32], V, g, rho, Vol, Ta, Tf, Cm, LCB, Cwp, At, Abt, hb)

print('Rw: ' + str(waveOpt))
