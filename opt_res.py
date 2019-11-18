# from __future__ import division

import numpy as np
import math
import Holtrop as h
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

V = 3 # kts
V = V*0.514444

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

def calcWave(x, V, g, rho, LCB, Cwp, At, Abt, hb):
	LWL = x[0]
	B = x[1]
	Ta = x[2]
	Tf = x[2]
	Cb = x[3]
	Cm = x[4]
	T = h.calc_T(Ta, Tf) #m
	Vol = LWL*B*T*Cb
	Rw = h.calc_Rw(V, LWL, g, rho, Vol, B, Ta, Tf, Cm, LCB, Cwp, At, Abt, hb)
	return Rw

def calcVisc(x, V, g, rho, LCB, Cwp, At, Abt, u_k, Cstern):
	LWL = x[0]
	B = x[1]
	Ta = x[2]
	Tf = x[2]
	Cb = x[3]
	Cm = x[4]
	Cp = calcCp(x)
	T = h.calc_T(Ta, Tf) #m
	Vol = LWL*B*T*Cb
	Rv = h.calc_Rv(rho, V, LWL, u_k, B, T, Vol, Cp, LCB, Cstern, Cm, Cb, Cwp, Abt)
	return Rv

def calcCor(x, rho, V, Cwp, Abt):
	B = x[1]
	Cb = x[3]
	Ta = x[2]
	Tf = x[2]
	Cm = x[4]
	T = h.calc_T(Ta, Tf) #m
	S = h.calc_S(x[0], T, B, Cm, Cb, Cwp, Abt)
	Ca = h.calc_Ca(x[0])
	Ra = h.calc_Ra(rho, V, Ca, S)
	return Ra

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

def calcCp(x):
	Cm = x[4]
	Cb = x[3]
	Cp = h.calc_Cp(Cb, Cm)
	return Cp

# def objective(x, V = 12.861, g = 9.81, rho = 1025, LCB = -0.75, Cwp = 0.75, At = 16, Abt = 0, hb = 0, u_k = 9.37e7, Cstern = 10):
def objective(x, V = 1.543, g = 9.81, rho = 1025, LCB = -0.75, Cwp = 0.75, At = 16, Abt = 0, hb = 0, u_k = 9.37e7, Cstern = 10):
	wave = calcWave(x, V, g, rho, LCB, Cwp, At, Abt, hb)
	visc = calcVisc(x, V, g, rho, LCB, Cwp, At, Abt, u_k, Cstern)
	cor = calcCor(x, rho, V, Cwp, Abt)
	return (wave + visc + cor)/10000

def constraint1(x):
	Lcons = 400 - calcLength(x)
	return Lcons

def constraint2(x):
	Lcons = calcLength(x)-250
	return Lcons

def constraintVol(x):
	Vol = calcVol(x) - 2500
	return Vol

def constraint4(x):
	B = calcBeam(x) - 9
	return B

def constraint5(x):
	T = calcDraft(x) - 2
	return T

def constraintCpHigh(x):
	Fn = h.calc_Fn(V, x[0], g)
	Cp = calcCp(x)
	return (1.12666-1.722*Fn) - Cp

def constraintCpLow(x):
	Fn = h.calc_Fn(V, x[0], g)
	Cp = calcCp(x)
	return Cp - (1.0633-1.777*Fn)

# bl = (100, 300)
# bw = (10, 40)
# bt = (1, 10)
# bcb = (0.5, 0.6)
# bcm = (0.5, 0.99)

bl = (20, 120)
bw = (2, 20)
bt = (1, 15)
bcb = (0.5, 0.6)
bcm = (0.5, 0.99)

bnds = (bl, bw, bt, bcb, bcm)

con1 = {'type': 'ineq', 'fun': constraint1}
con2 = {'type': 'ineq', 'fun': constraint2}
conVol = {'type': 'ineq', 'fun': constraintVol}
con4 = {'type': 'ineq', 'fun': constraint4}
con5 = {'type': 'ineq', 'fun': constraint5}
conCpLow = {'type': 'ineq', 'fun': constraintCpLow}
conCpHigh = {'type': 'ineq', 'fun': constraintCpHigh}
cons = (conVol, conCpLow, conCpHigh)

lengthGuess = 70
beamGuess = 7
draftGuess = 4
blockGuess = 0.57
midshipGuess = 0.98

x0 = np.array([lengthGuess, beamGuess, draftGuess, blockGuess, midshipGuess])

sol = minimize(objective,x0,method = 'SLSQP', constraints = cons, bounds = bnds, options ={'disp':True})

xOpt = sol.x
volumeOpt = -sol.fun

#V = 12.861, g = 9.81, rho = 1025, Cm = 0.98, LCB = -0.75, Cwp = 0.75, At = 16, Abt = 0, hb = 0):
# waveOpt = calcWave(xOpt, V, g, rho, LCB, Cwp, At, Abt, hb)
waveOpt = calcWave(xOpt, 1.543, 9.81, 1025, -0.75, 0.75, 0, 0, 0)
#x, V, g, rho, LCB, Cwp, At, Abt, u_k, Cstern
viscOpt = calcVisc(xOpt, 1.543, 9.81, 1025, -0.75, 0.75, 16, 0, 9.37e7, 10)
# x, rho, V, Cwp, Abt
corOpt = calcCor(xOpt, 1025, 1.543, 0.75, 0)

print('Length: ' + str(xOpt[0]))
print('Width: ' + str(xOpt[1]))
print('Draft: ' + str(xOpt[2]))
print('Cb: ' + str(xOpt[3]))
print('Cm: ' + str(xOpt[4]))
print('Vol: ' + str(calcVol(xOpt)))
print('Volcos: ' + str(constraintVol(xOpt)))
print('CpLow: ' + str(constraintCpLow(xOpt)))
print('CpHigh: ' + str(constraintCpHigh(xOpt)))
print('Fn: ' + str(h.calc_Fn(V, xOpt[0], g))) # should be between 0.12-0.3
print('Cp: ' + str(calcCp(xOpt)))


print('Rw: ' + str(waveOpt))
print('Rv: ' + str(viscOpt))
print('Ra: ' + str(corOpt))
print('Rt: ' + str(waveOpt + viscOpt + corOpt))



waveOpt = calcWave([205, 32, 10, 0.57, 0.98], 1.543, 9.81, 1025, -0.75, 0.75, 16, 0, 0)

print('Rw: ' + str(waveOpt))

print('')
print('')
print('')



LWL = xOpt[0]
B = xOpt[1]
Ta = xOpt[2]
Tf = xOpt[2]
Cb = xOpt[3]
Cm = xOpt[4]

LCB_LBP = -2.02
LBP = 200
LCB = h.LCB_LBP_2_LCB_LWL(205, LBP, LCB_LBP)
print('LCB: ' + str(LCB))


T = h.calc_T(Ta, Tf) #m
Vol = LWL*B*T*Cb
T = h.calc_T(Ta,Tf)
print('T: ' + str(T))
Fn = h.calc_Fn(V, LWL, g)
print('Fn: ' + str(Fn))
Cb = h.calc_Cb(Vol, LWL, B, T)
print('Cb: ' + str(Cb))
Cp = h.calc_Cp(Cb, Cm)
print('Cp: ' + str(Cp))
LR = h.calc_LR(LWL, Cp, LCB)
print('LR: ' + str(LR ))
c7 = h.calc_c7(B, LWL)
print('c7: ' + str(c7))
iE = h.calc_iE(LWL, B, Cwp, Cp, LCB, LR, Vol)
print('iE: ' + str(iE))
c1 = h.calc_c1(c7, T, B, iE)
print('c1: ' + str(c1))
c3 = h.calc_c3(Abt, B, T, Tf, hb)
print('c3: ' + str(c3))
c2 = h.calc_c2(c3)
print('c2: ' + str(c2))
c5 = h.calc_c5(At, B, T, Cm)
print('c5: ' + str(c5))
c16 = h.calc_c16(Cp)
print('c16: ' + str(c16))
m1 = h.calc_m1(LWL, T, Vol, B, c16)
print('m1: ' + str(m1))
c15 = h.calc_c15(LWL, Vol)
print('c15: ' + str(c15))
d = h.calc_d()
print('d: ' + str(d))
m4 = h.calc_m4(c15, Fn)
print('m4: ' + str(m4))
lamb = h.calc_lamb(Cp, LWL, B)
print('la,b: ' + str(lamb))
Rw = c1*c2*c5*Vol*rho*g*math.exp(m1*Fn**d+m4*math.cos(lamb*Fn**(-2)))
print('Rw: ' + str(Rw))




# h.calc_Rw(V, LWL, g, rho, Vol, B, Ta, Tf, Cm, LCB, Cwp, At, Abt, hb)

