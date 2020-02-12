from __future__ import division

import numpy as np
import math

def calc_Rn(V, LWL, u_k):
	return V*LWL/u_k

def LCB_LBP_2_LCB_LWL(LWL, LBP, LCB_LBP):
	return 100*(LWL/2-(LBP/2-LCB_LBP*LBP/100))/LWL

def calc_T(Ta, Tf):
	return (Ta+Tf)/2

def calc_Fn(V, LWL, g):
    return V/math.sqrt(g*LWL)

def calc_Cb(Vol, LWL, B, T):
	return Vol/(LWL*B*T)

def calc_Cp(Cb, Cm):
	return Cb/Cm

def calc_LR(LWL, Cp, LCB):
	return LWL*((1-Cp) + (0.06*Cp*LCB)/(4*Cp-1))

def calc_S(LWL, T, B, Cm, Cb, Cwp, Abt):
	return LWL*(2*T+B)*math.sqrt(Cm)*(0.453+0.4425*Cb-0.2862*Cm-0.003467*(B/T)+0.3696*Cwp)+2.38*(Abt/Cb)

def calc_c7(B, LWL):
	if B/LWL <0.11:
		c7 = 0.229577*(B/LWL)**(0.33333)
	elif B/LWL > 0.25:
		c7 = 0.5 - 0.0625*(LWL/B)
	else:
		c7 = B/LWL
	return c7

def calc_iE(LWL, B, Cwp, Cp, LCB, LR, Vol):
	return 1+89*math.exp(-(LWL/B)**(0.80856)*(1-Cwp)**(0.30484)*(1-Cp-0.0225*LCB)**(0.6367)*(LR/B)**(0.34574)*(100*Vol/(LWL**3))**(0.16302))

def calc_c1(c7, T, B, iE):
	return 2223105*c7**(3.78613)*(T/B)**(1.07961)*(90-iE)**(-1.37565)

def calc_c3(Abt, B, T, Tf, hb):
	return 0.56*Abt**(1.5)/(B*T*(0.31*math.sqrt(Abt)+Tf-hb))

def calc_c2(c3):
	return math.exp(-1.89*math.sqrt(c3))

def calc_c5(At, B, T, Cm):
	return 1-0.8*(At/(B*T*Cm))

def calc_c16(Cp):
	if Cp < 0.8:
		c16 = 8.07981*Cp-13.8673*Cp**2+6.984388*Cp**3
	else:
		c16 = 1.73014-0.7067*Cp
	return c16

def calc_m1(LWL, T, Vol, B, c16):
	return 0.0140407*(LWL/T)-1.75254*(Vol**(1/3)/LWL)-4.79323*(B/LWL)-c16

def calc_c15(LWL, Vol):
	if LWL**3/Vol<512:
		c15 = -1.69385
	elif LWL**3/Vol>1726.91:
		c15 = 0
	else:
		c15 = -1.69385+(LWL/Vol**(1/3)-8)/2.36
	return c15

def calc_m4(c15, Fn):
	return c15*0.4*math.exp(-0.034*Fn**(-3.29))

#Works up to Fn 0.4
def calc_lamb(Cp, LWL, B):
	if LWL/B < 12:
		lamb = 1.446*Cp-0.03*LWL/B
	else:
		lamb =1.446*Cp-0.36
	return lamb
def calc_d():
	return -0.9

def calc_Rw(V, LWL, g, rho, Vol, B, Ta, Tf, Cm, LCB, Cwp, At, Abt, hb):
	T = calc_T(Ta,Tf)
	Fn = calc_Fn(V, LWL, g)
	Cb = calc_Cb(Vol, LWL, B, T)
	Cp = calc_Cp(Cb, Cm)
	LR = calc_LR(LWL, Cp, LCB)
	c7 = calc_c7(B, LWL)
	iE = calc_iE(LWL, B, Cwp, Cp, LCB, LR, Vol)
	c1 = calc_c1(c7, T, B, iE)
	c3 = calc_c3(Abt, B, T, Tf, hb)
	c2 = calc_c2(c3)
	c5 = calc_c5(At, B, T, Cm)
	c16 = calc_c16(Cp)
	m1 = calc_m1(LWL, T, Vol, B, c16)
	c15 = calc_c15(LWL, Vol)
	d = calc_d()
	m4 = calc_m4(c15, Fn)
	lamb = calc_lamb(Cp, LWL, B)
	# print('c1: ' + str(c1))
	Rw = c1*c2*c5*Vol*rho*g*math.exp(m1*Fn**d+m4*math.cos(lamb*Fn**(-2)))
	return Rw

def calc_Rw_boat(boat,speeds):
	V = speeds
	LWL = boat.hull.LWL 
	g = boat.g 
	rho = boat.rho 
	Vol = boat.hull.displacement_volume
	B = boat.hull.B
	T = boat.hull.T
	Cm = boat.hull.Cm
	LCB = boat.hull.LCB
	Cwp = boat.hull.Cwp
	At = boat.At
	Abt = boat.Abt
	hb = boat.hb

	# print(f'V: {V}')
	# print(f'LWL: {LWL}')
	# print(f'g: {g}')
	# print(f'rho: {rho}')
	# print(f'Vol: {Vol}')
	# print(f'B: {B}')
	# print(f'T: {T}')
	# print(f'Cm: {Cm}')
	# print(f'LCB: {LCB}')
	# print(f'Cwp: {Cwp}')
	# print(f'At: {At}')
	# print(f'Abt: {Abt}')
	# print(f'hb: {hb}')



	Fn = calc_Fn(V, LWL, g)
	Cb = calc_Cb(Vol, LWL, B, T)
	Cp = calc_Cp(Cb, Cm)
	LR = calc_LR(LWL, Cp, LCB)
	c7 = calc_c7(B, LWL)
	iE = calc_iE(LWL, B, Cwp, Cp, LCB, LR, Vol)
	c1 = calc_c1(c7, T, B, iE)
	c3 = calc_c3(Abt, B, T, Tf, hb)
	c2 = calc_c2(c3)
	c5 = calc_c5(At, B, T, Cm)
	c16 = calc_c16(Cp)
	m1 = calc_m1(LWL, T, Vol, B, c16)
	c15 = calc_c15(LWL, Vol)
	d = calc_d()
	m4 = calc_m4(c15, Fn)
	lamb = calc_lamb(Cp, LWL, B)
	# print('c1: ' + str(c1))

	# print(f'Fn: {Fn}')
	# print(f'Cb: {Cb}')
	# print(f'Cp: {Cp}')
	# print(f'LR: {LR}')
	# print(f'c7: {c7}')
	# print(f'iE: {iE}')
	# print(f'c1: {c1}')
	# print(f'c3: {c3}')
	# print(f'c2: {c2}')
	# print(f'c5: {c5}')
	# print(f'c16: {c16}')
	# print(f'm1: {m1}')
	# print(f'c15: {c15}')
	# print(f'd: {d}')
	# print(f'm4: {m4}')
	# print(f'lamb: {lamb}')
	# print('')

	Rw = c1*c2*c5*Vol*rho*g*math.exp(m1*Fn**d+m4*math.cos(lamb*Fn**(-2)))
	return Rw

def calc_c14(Cstern):
	return 1+0.011*Cstern

def calc_k1_1(B, LWL, T, Vol, Cp, LCB, Cstern):
	c14 = calc_c14(Cstern)
	LR = calc_LR(LWL, Cp, LCB)
	k1_1 = 0.93+0.487118*c14*(B/LWL)**(1.06806)*(T/LWL)**(0.46106)*(LWL/LR)**(0.121563)*(LWL**3/Vol)**(0.36486)*(1-Cp)**(-0.604247)
	# print('k1_1: ' + str(k1_1) + ', LWL: ' + str(LWL) + ', B: ' + str(B) +', T: ' + str(T) +', Vol: ' + str(Vol)+ ', LR: ' + str(LR) + ', Cp: ' + str(Cp))
	return k1_1
def calc_Ca(LWL):
	if LWL < 100:
		Ca = 0.0010
	else:
		Ca = (1.8+260/LWL)*0.0001 #LWL in m
	return Ca
def calc_Ca_boat(boat):
	LWL = boat.hull.LWL
	if LWL < 100:
		Ca = 0.0010
	else:
		Ca = (1.8+260/LWL)*0.0001 #LWL in m
	return Ca


# ITTC-1957
def calc_Cf(V,LWL,u_k):
	return 0.075/(math.log10(calc_Rn(V,LWL,u_k))-2)**2

def calc_Rv(rho, V, LWL, u_k, B, T, Vol, Cp, LCB, Cstern, Cm, Cb, Cwp, Abt):
	Cf = calc_Cf(V,LWL,u_k)
	k1_1 = calc_k1_1(B, LWL, T, Vol, Cp, LCB, Cstern)
	S = calc_S(LWL, T, B, Cm, Cb, Cwp, Abt)
	Rv = 0.5*rho*(V**2)*Cf*k1_1*S
	return Rv

def calc_Rv_boat(boat, speeds):
	Cf = calc_Cf(speeds, boat.hull.LWL, boat.u_k)
	k1_1 = calc_k1_1(boat.hull.B, boat.hull.LWL, boat.hull.T, boat.hull.displacement_volume, boat.hull.Cp, boat.hull.LCB, boat.Cstern)
	S = calc_S(boat.hull.LWL, boat.hull.T, boat.hull.B, boat.hull.Cm, boat.hull.Cb, boat.hull.Cwp, boat.Abt)
	Rv = 0.5*boat.rho*(speeds**2)*Cf*k1_1*S
	return Rv

def calc_Ra(rho, V, Ca, S):
	return 0.5*rho*V**2*Ca*S

def calc_Ra_boat(boat,speeds):
	rho = boat.rho
	V = speeds
	Ca = calc_Ca_boat(boat)
	S = boat.hull.S
	return 0.5*rho*V**2*Ca*S

def calc_Rapp(rho, V, LWL, u_k, k2_1, Sapp):
	Cf = calc_Cf(V,LWL,u_k)
	return 0.5*rho*V**2*Sapp*k2_1*Cf

def calc_R(Rv, Rw, Ra):
	return Rv+Rw+Ra



LWL = 23.89
designSpeed = 5
V = designSpeed*0.514444
g = 9.81
density = 1025
rho = density
kinematic_viscosity = 1.18832278e-6
u_k = kinematic_viscosity
Abt = 0
B = 5.97
T = 2.29
Ta = 2.29
Tf = 2.29
Vol = 282.68
Cp = 0.869
LCB = -0.75
Cstern = 10
Cm = 0.997
Cb = 0.866
Cwp = 0.911
At = 0
hb = 0

Rv = calc_Rv(rho, V, LWL, u_k, B, T, Vol, Cp, LCB, Cstern, Cm, Cb, Cwp, Abt)
Rw = calc_Rw(V, LWL, g, rho, Vol, B, Ta, Tf, Cm, LCB, Cwp, At, Abt, hb)
print(f'Rv: {Rv}')
print(f'Rw: {Rw}')


print(f'Power: {(Rw+Rv)*V}')

# LWL: 			23.89 (m)
# B: 				5.97 (m)
# T: 				2.29 (m)
# D: 				3.32 (m)
# Disp: 			291.19 (tonnes)
# Disp Vol: 		282.68 (m^3)
# Internal Vol: 	413.45 (m^3)
# S: 				221.01 (m^2)

# Form Coefficients
# Fn: 	0.067
# Cb: 	0.866
# Cbd: 	0.873
# Cm: 	0.997
# Cwp: 	0.911
