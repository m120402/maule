# from __future__ import division

import numpy as np
import math
import Holtrop as h
from scipy.optimize import minimize

V = 5 #knots
V = V*0.514444 # m/s
g = 9.81 # m/s^2
rho = 1025 #kg/m^3
u_k = 9.37e-7 #kinematic viscosity of seawater at 35 g/kg and 25 C
# minVol = 55 #m^3



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

# def objective(x, V = 12.861, g = 9.81, rho = 1025, LCB = -0.75, Cwp = 0.75, At = 16, Abt = 0, hb = 0, u_k = 9.37e-7, Cstern = 10):
def objective(x, V = 1.543, g = 9.81, rho = 1025, LCB = -0.75, Cwp = 0.75, At = 16, Abt = 0, hb = 0, u_k = 9.37e-7, Cstern = 10):
	visc = calcVisc(x, V, g, rho, LCB, Cwp, At, Abt, u_k, Cstern)
	cor = calcCor(x, rho, V, Cwp, Abt)
	return (visc + cor)/10000


def constraintVol(x):
	Vol = calcVol(x) - 70
	return Vol

def constraintCpHigh(x):
	Fn = h.calc_Fn(V, x[0], g)
	Cp = calcCp(x)
	return (1.12666-1.722*Fn) - Cp

def constraintCpLow(x):
	Fn = h.calc_Fn(V, x[0], g)
	Cp = calcCp(x)
	return Cp - (1.0633-1.777*Fn)

def constraintCmLow(x):
	Cm = x[4]
	return Cm - 0.8

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

conVol = {'type': 'ineq', 'fun': constraintVol}
conCpLow = {'type': 'ineq', 'fun': constraintCpLow}
conCpHigh = {'type': 'ineq', 'fun': constraintCpHigh}
conCmLow = {'type': 'ineq', 'fun': constraintCmLow}
cons = (conVol, conCpLow, conCpHigh, conCmLow)

lengthGuess = 30
beamGuess = 7
draftGuess = 4
blockGuess = 0.8
midshipGuess = 0.98

x0 = np.array([lengthGuess, beamGuess, draftGuess, blockGuess, midshipGuess])

sol = minimize(objective,x0,method = 'SLSQP', constraints = cons, bounds = bnds, options ={'disp':True})

xOpt = sol.x
# volumeOpt = -sol.fun

#V = 12.861, g = 9.81, rho = 1025, Cm = 0.98, LCB = -0.75, Cwp = 0.75, At = 16, Abt = 0, hb = 0):

#x, V, g, rho, LCB, Cwp, At, Abt, u_k, Cstern
viscOpt = calcVisc(xOpt, 1.543, 9.81, 1025, -0.75, 0.75, 16, 0, 9.37e-7, 10)
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


print('Rv: ' + str(viscOpt))
print('Ra: ' + str(corOpt))
print('Rt: ' + str(viscOpt + corOpt))


k1_1 = h.calc_k1_1(xOpt[1], xOpt[0], xOpt[2], calcVol(xOpt),calcCp(xOpt), -0.75, 10)
S = h.calc_S(xOpt[0], xOpt[2], xOpt[1], xOpt[4], xOpt[3], 0.75, 0)
Ca = h.calc_Ca(xOpt[0])
Cf = h.calc_Cf(V,xOpt[0],u_k)


print('k1_1: ' + str(k1_1))
print('S: ' + str(S))
print('Ca: ' + str(Ca))
print('Cf: ' + str(Cf))




print('')
print('')
print('')


