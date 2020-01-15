from __future__ import division

import numpy as np
import math

def calc_Disp_Vol(Cb, L, B, T):
	return Cb * L * B * T

def calc_Disp(Disp_Vol, rho, shell_appendage_allowance):
	return Disp_Vol * rho * (1+shell_appendage_allowance)

def calc_Fn(V, LWL, g):
    return V/math.sqrt(g*LWL)

def calc_Cb(Fn):
	# Watson and Gilfillan Mean Line
	return 0.7 + 0.125* math.atan2((23-100*Fn),4)
# 
# Attributed to Kerlen in Schneekluth and Bertram
# May be too large if L/B not large enough
def calc_Cm(Cb):
	return 1.006 - 0.0056 * (Cb**(-3.56))

def calc_Cp(Cb, Cm):
	return Cb/Cm

def calc_Ws(LWL, B, T, D, Cb):
	E = LWL*(B+T) + 0.85*LWL*(D-T)
	Cb_prime = Cb + (1-Cb)*(0.8*D - T) / (3*T)
	K = 0.045
	Ws = K * E**(1.36) * (1 + 0.5 * (Cb_prime - 0.7))
	return Ws*1000 #tonnes -> kg

# Series 60 min wetted surface area (Saunders)
def calc_T(B, Cm):
	return B/(5.93 - 3.33 * Cm)

# Average hulls, Riddlesworth (2)
# Average between V shaped and U shaped hulls. 
# CWP = 0.175 + 0.875 CP could be used since it represents a single screw, cruiser stern
# Check out SNAME_DES Fig 11.12
def calc_Cwp(Cb):
	return (1+2*Cb)/3

# Watson and Gilfillan Suggestion
def calc_B(LWL):
	if LWL < 30:
		B = LWL/4
	elif LWL <130:
		B = LWL/(4 + 0.025 * (LWL - 30))
	else:
		B = LWL/6.5
	return B


def calc_K(LWL, B, T, Cb):
	# simple_k = 19*(Vol/((LWL**2)*T))**2 
	# Watanabe empirical formula
	L2B = LWL/B
	B2T = B/T
	k = -0.095 + 25.6 * Cb / (L2B**2 * math.sqrt(B2T))
	return k

def calc_Cf(Rn):
	# ITTC-57 Formula
	Cf = 0.075/(math.log10(Rn) - 2)**2
	return Cf

def calc_Rn(LWL, V, v):
	return LWL*V/v

def calc_Cv(LWL, B, T, Cb, V, v):
	K = calc_K(LWL, B, T, Cb)
	Rn = calc_Rn(LWL, V, v)
	Cf = calc_Cf(Rn)
	Cv = Cf*(1+K)
	return Cv

def calc_Rv_Opt(LWL, T, Vol, V, v, rho):
	B = calc_B(LWL)
	Fn = calc_Fn(V, LWL, g)
	Cb = calc_Cb(Fn)
	Cm = calc_Cm(Fn)
	T = calc_T(B, Cm)
	Cwp = calc_Cwp(Cb)
	S = calc_S(LWL, T, B, Cm, Cb, Cwp, Abt)
	Cv = calc_Cv(LWL, T, Vol, V, v)
	# print(Cv)
	Rv = 0.5*rho*S*(V**2)*Cv
	return Rv # (N)

def calc_Rv(rho, S, V, Cv):
	Rv = 0.5*rho*S*(V**2)*Cv
	return Rv # (N)

# Holtrop
def calc_S(LWL, T, B, Cm, Cb, Cwp, Abt):
	return LWL*(2*T+B)*math.sqrt(Cm)*(0.453+0.4425*Cb-0.2862*Cm-0.003467*(B/T)+0.3696*Cwp)+2.38*(Abt/Cb)

def calcDeckArea(LWL, B, Cwp):
		# Must Update to use Mono/Cat as applicable!
		# ___________________________________________________________________________________________________
	# return LWL**2*0.1
	return LWL * B * Cwp

def calc_D(B):
	return B/1.8

def calc_Cbd(Cb, D, T):
	return Cb + (1 - Cb) * (0.8 * D - T)/(3 * T)

def calc_Vi(Cbd, LWL, B, D):
	return Cbd * LWL * B * D

# Combination functions

# def calc_Internal_V(V, g, LWL):
# 	Fn = calc_Fn(V, LWL, g)
# 	Cb = calc_Cb(Fn)
# 	Cm = calc_Cm(Fn)
# 	B = calc_B(LWL)
# 	T = calc_T(B, Cm)
# 	D = calc_D(B)
# 	Cbd = calc_Cbd(Cb, D, T)
# 	Vi = calc_Vi(Cbd, LWL, B, D)
# 	return Vi

# print(calc_Cb(0.1))
# print(calc_Cb(0.2))
# print(calc_Cb(0.3))

# print(calc_K(10,1,0.5,4.95))
# print(calc_K(10,1,0.5,4.75))
# print(calc_K(10,1,0.5,4.5))

# print(calc_Cf(1e6))

# print(calc_Rv(LWL, T, B, Cm, Cwp, Abt, Vol, V, v, rho))
