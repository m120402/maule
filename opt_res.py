# from __future__ import division

import numpy as np
import math
import Holtrop as h
import numpy as np
from scipy.optimize import minimize


# # import gekko, pip install if needed
# from gekko import GEKKO

# # create new model
# m = GEKKO()

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


# LCB = h.LCB_LBP_2_LCB_LWL(LWL, LBP, LCB_LBP) # longitudinal centre of buoyancy % fwd of 1/2 LWL
# T = h.calc_T(Ta, Tf) #m
# Rw = h.calc_Rw(V, LWL, g, rho, Vol, B, Ta, Tf, Cm, LCB, Cwp, At, Abt, hb)

# Cb = h.calc_Cb(Vol, LWL, B, T)
# Cp = h.calc_Cp(Cb, Cm)

# Rv = h.calc_Rv(rho, V, LWL, u_k, B, T, Vol, Cp, LCB, Cstern, Cm, Cb, Cwp, Abt)
# Ca = h.calc_Ca(LWL)

# S = h.calc_S(LWL, T, B, Cm, Cb, Cwp, Abt)

# Ra = h.calc_Ra(rho, V, Ca, S)

# R = h.calc_R(Rv, Rw, Ra)

# print('Relevant test calculations from 1982 Paper')

# print('Rw: ' + str(Rw))
# print('Rv: ' + str(Rv))
# print('Ca: ' + str(Ca))
# print('R: ' + str(R))



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

def calcWave(x, V, g, rho, Cm, LCB, Cwp, At, Abt, hb):
	LWL = x[0]
	B = x[1]
	Ta = x[2]
	Tf = x[2]
	Cb = x[3]
	T = h.calc_T(Ta, Tf) #m
	Vol = LWL*B*T*Cb
	Rw = h.calc_Rw(V, LWL, g, rho, Vol, B, Ta, Tf, Cm, LCB, Cwp, At, Abt, hb)
	return Rw

def calcLength(x):
	return x[0]

def calcBeam(x):
	return x[1]

def calcDraft(x):
	return x[2]

def calcVol(x):
	LWL = x[0]
	B = x[1]
	Ta = x[2]
	Tf = x[2]
	Cb = x[3]
	T = h.calc_T(Ta, Tf) #m
	Vol = LWL*B*T*Cb
	return Vol

def objective(x, V = 12.861, g = 9.81, rho = 1025, Cm = 0.98, LCB = -0.75, Cwp = 0.75, At = 16, Abt = 0, hb = 0):
	return calcWave(x, V, g, rho, Cm, LCB, Cwp, At, Abt, hb)/100000

def constraint1(x):
	Lcons = 400 - calcLength(x)
	return Lcons

def constraint2(x):
	Lcons = calcLength(x)-250
	return Lcons

def constraint3(x):
	Vol = calcVol(x) - 37500
	return Vol

def constraint4(x):
	B = calcBeam(x) - 9
	return B

def constraint5(x):
	T = calcDraft(x) - 2
	return T

bl = (100, 300)
bw = (10, 40)
bt = (1, 20)
bcb = (0.5, 0.6)

bnds = (bl, bw, bt, bcb)

con1 = {'type': 'ineq', 'fun': constraint1}
con2 = {'type': 'ineq', 'fun': constraint2}
con3 = {'type': 'ineq', 'fun': constraint3}
con4 = {'type': 'ineq', 'fun': constraint4}
con5 = {'type': 'ineq', 'fun': constraint5}
cons = (con3)

lengthGuess = 200
beamGuess = 30
draftGuess = 10
blockGuess = 0.57

x0 = np.array([lengthGuess, beamGuess, draftGuess, blockGuess])

sol = minimize(objective,x0,method = 'SLSQP', constraints = cons, bounds = bnds, options ={'disp':True})

xOpt = sol.x
volumeOpt = -sol.fun

#V = 12.861, g = 9.81, rho = 1025, Cm = 0.98, LCB = -0.75, Cwp = 0.75, At = 16, Abt = 0, hb = 0):
# waveOpt = calcWave(xOpt, V, g, rho, Cm, LCB, Cwp, At, Abt, hb)
waveOpt = calcWave(xOpt, 12.861, 9.81, 1025, 0.98, -0.75, 0.75, 16, 0, 0)

print('Length: ' + str(xOpt[0]))
print('Width: ' + str(xOpt[1]))
print('Draft: ' + str(xOpt[2]))
print('Cb: ' + str(xOpt[3]))
print('Vol: ' + str(calcVol(xOpt)))
print('Volcos: ' + str(constraint3(xOpt)))
print('Fn: ' + str(h.calc_Fn(V, xOpt[0], g))) # should be between 0.12-0.3

print('Rw: ' + str(waveOpt))



waveOpt = calcWave([205, 32, 10, 0.57], 12.861, 9.81, 1025, 0.98, -0.75, 0.75, 16, 0, 0)

print('Rw: ' + str(waveOpt))
