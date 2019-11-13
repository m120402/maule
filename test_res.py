from __future__ import division

import numpy as np
import math
import Holtrop as h


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


# print('Fn: ' + str(Fn))
# print('Cp: ' + str(Cp))
# print('LR: ' + str(LR))
# print('S: ' + str(S))
# print('c7: ' + str(c7))
# print('iE: ' + str(iE))
# print('c1: ' + str(c1))
# print('c3: ' + str(c3))
# print('c2: ' + str(c2))
# print('c5: ' + str(c5))
# print('m1: ' + str(m1))
# print('c15: ' + str(c15))
# print('Lambda: ' + str(lamb))
print('Rw: ' + str(Rw))
print('Rv: ' + str(Rv))
print('Ca: ' + str(Ca))
print('R: ' + str(R))



print('')

LWL = 50.00 #m
B = 12.00 #m
Tf = 3.10 #m
Ta = 3.30 #m
Vol = 900 #m^3
Sapp = 50 #m^2
Cstern = 0 #stern shape parameter

Abt = 0
iE = 25 #degrees
Cm = 0.78
LCB = -4.5 #% L fwd of 1/2L
At = 10 #m2
K2_1 = 3
Cwp = 0.80


