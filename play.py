from __future__ import division

from scipy.optimize import minimize
import numpy as np
import math

import Parametric as p
import systems as s

options = {}
options['FIG_SIZE'] = [8,8]
options['FULL_RECALCULATE'] = False

print(type(options))

class Min_res:
	# def __init__(self, speed = 3, gravity = 9.81, density = 1025, kinematic_viscosity = 9.37e-7):
	def __init__(self, speed = 3, gravity = 9.81, density = 1025, kinematic_viscosity = 1.18832278e-6):
	  	self.V = speed*0.514444 #knots -> m/s
	  	self.g = gravity #m/s^2
	  	self.rho = density #kg/m^3
	  	self.u_k = kinematic_viscosity #m^2/s, default is kinematic viscosity of seawater at 35 g/kg and 25 C
	  	self.LCB = -0.75
	  	self.At = 16
	  	self.Abt = 0
	  	self.hb = 0
	  	self.Cstern = 10
	  	self.plant = s.Solar()
	  	self.deckArea = 0

	# def calcVisc(self, x): #, V, g, rho, LCB, Cwp, At, Abt, u_k, Cstern):
	# 	LWL = x[0]
	# 	B = x[1]
	# 	Ta = x[2]
	# 	Tf = x[2]
	# 	Cb = x[3]
	# 	Cm = x[4]
	# 	Cp = self.calcCp(x)
	# 	T = h.calc_T(Ta, Tf) #m
	# 	Vol = LWL*B*T*Cb
	# 	Rv = h.calc_Rv(self.rho, self.V, LWL, self.u_k, B, T, Vol, Cp, self.LCB, self.Cstern, Cm, Cb, self.Cwp, self.Abt)
	# 	return Rv

	# def calcVol(self, x):
	# 	LWL = x[0]
	# 	B = x[1]
	# 	Ta = x[2]
	# 	Tf = x[2]
	# 	Cb = x[3]
	# 	T = h.calc_T(Ta, Tf) #m
	# 	Vol = LWL*B*T*Cb
	# 	return Vol

	# def calcCp(self, x):
	# 	Cm = x[4]
	# 	Cb = x[3]
	# 	Cp = h.calc_Cp(Cb, Cm)
	# 	return Cp

	# def objective(x, V = 12.861, g = 9.81, rho = 1025, LCB = -0.75, Cwp = 0.75, At = 16, Abt = 0, hb = 0, u_k = 9.37e-7, Cstern = 10):
	# def objective(x, V = 1.543, g = 9.81, rho = 1025, LCB = -0.75, Cwp = 0.75, At = 16, Abt = 0, hb = 0, u_k = 9.37e-7, Cstern = 10):
	def objective(self, x, *args):
		# wave = self.calcWave(x)
		# self.deckArea = x
		Abt = args[0]
		Vol = 177
		V = args[1] 
		u_k = args[2]
		rho = args[3]
		g = args[4]
		visc = p.calc_Rv(x, Abt, Vol, V, u_k, rho, g) #, self.V, self.g, self.rho, self.LCB, self.Cwp, self.At, self.Abt, self.u_k, self.Cstern)
		# cor = self.calcCor(x) #, self.rho, self.V, self.Cwp, self.Abt)
		return (visc)/10000


	def constraintVol(self, x):
		# Vol = self.calcVol(x) - 60
		Vol = 100 - 60
		return Vol

	# def constraintVolHigh(self, x):
	# 	Vol = 8000 - self.calcVol(x)
	# 	return Vol

	# def constraintCpHigh(self, x):
	# 	Fn = h.calc_Fn(self.V, x[0], self.g)
	# 	Cp = self.calcCp(x)
	# 	return (1.12666-1.722*Fn) - Cp

	# def constraintCpLow(self, x):
	# 	Fn = h.calc_Fn(self.V, x[0], self.g)
	# 	Cp = self.calcCp(x)
	# 	return Cp - (1.0633-1.777*Fn)

	# def constraintCmLow(self, x):
	# 	Cm = x[4]
	# 	return Cm - 0.8

	# def constraintL(self, x):
	# 	L = x[0]
	# 	return L
	# def constraintB(self, x):
	# 	B = x[1]
	# 	return B
	# def constraintT(self, x):
	# 	T = x[2]
	# 	return T
	# def constraintCb(self, x):
	# 	Cb = x[3]
	# 	return Cb
	# def constraintCm(self, x):
	# 	Cm = x[4]
	# 	return Cm
	# def constraintCmCb(self, x):
	# 	Cb = x[3]
	# 	Cm = x[4]
	# 	return Cm-Cb
	# # New functions

	def setBounds(self):
		bl = (10, 120)
	# 	bw = (2, 20)
	# 	bt = (1, 15)
	# 	bcb = (0.5, 0.999)
	# 	bcm = (0.5, 0.999)

	# 	bnds = (bl, bw, bt, bcb, bcm)
		# bnds = (bl)
		bnds = [bl]
		return bnds

	def setConstraints(self):

		conVol = {'type': 'ineq', 'fun': self.constraintVol}
	# 	conVolHigh = {'type': 'ineq', 'fun': self.constraintVolHigh}
	# 	conCpLow = {'type': 'ineq', 'fun': self.constraintCpLow}
	# 	conCpHigh = {'type': 'ineq', 'fun': self.constraintCpHigh}
	# 	conCmLow = {'type': 'ineq', 'fun': self.constraintCmLow}

	# 	conL = {'type': 'ineq', 'fun': self.constraintL}
	# 	conB = {'type': 'ineq', 'fun': self.constraintB}
	# 	conT = {'type': 'ineq', 'fun': self.constraintT}
	# 	conCb = {'type': 'ineq', 'fun': self.constraintCb}
	# 	conCm = {'type': 'ineq', 'fun': self.constraintCm}

	# 	conCmCb = {'type': 'ineq', 'fun': self.constraintCmCb}

	# 	# cons = (conVol, conCpLow, conCpHigh, conCmLow)
		cons = (conVol)
	# 	cons = (conVol, conL, conB, conT, conCb, conCm, conCpLow, conCpHigh, conCmLow, conCmCb)
		return cons

	# def setInitial(self):
	# 	lengthGuess = 30
	# 	beamGuess = 7
	# 	draftGuess = 4
	# 	blockGuess = 0.8
	# 	midshipGuess = 0.98
	# 	x0 = np.array([lengthGuess, beamGuess, draftGuess, blockGuess, midshipGuess])
	# 	return x0

	def minima(self,x0):
		bnds = self.setBounds()
		cons = self.setConstraints()
		# return minimize(self.surrogateObj.predict, x0, method='Nelder-Mead', tol=1e-6, options ={'disp':True})
		# return minimize(self.predict,x0,method = 'SLSQP', constraints = cons, bounds = bnds, options ={'disp':True})
		solution = minimize(self.objective,x0,(self.Abt, self.V, self.u_k, self.rho, self.g),method = 'SLSQP', constraints = cons, bounds = bnds, options ={'disp':True})
		self.deckArea = p.calcDeckArea(solution.x[0])
		return solution



if __name__ == "__main__":
	x0 = [30]
	boat = Min_res()
	# sol = Min_res().minima(x0)
	sol = boat.minima(x0)
	LWL = sol.x[0]
	print(LWL)
	print(p.calc_Rv(sol.x[0], boat.Abt, 177, boat.V, boat.u_k, boat.rho, boat.g))

	B = p.calc_B(LWL)
	Fn = p.calc_Fn(boat.V, LWL, boat.g)
	Cb = p.calc_Cb(Fn)
	Cm = p.calc_Cm(Fn)
	T = p.calc_T(B, Cm)
	Cwp = p.calc_Cwp(Cb)
	S = p.calc_S(LWL, T, B, Cm, Cb, Cwp, boat.Abt)
	Cv = p.calc_Cv(LWL, T, 177, boat.V, boat.u_k)

	print('LWL: ' + str(LWL))
	print('B: ' + str(B))
	print('Fn: ' + str(Fn))
	print('Cb: ' + str(Cb))
	print('Cm: ' + str(Cm))
	print('T: ' + str(T))
	print('Cwp: ' + str(Cwp))
	print('S: ' + str(S))
	print('Cv: ' + str(Cv))

	res_2 = p.calc_Rv(sol.x[0], boat.Abt, 177, 2*0.514444, boat.u_k, boat.rho, boat.g)
	res_5 = p.calc_Rv(sol.x[0], boat.Abt, 177, 5*0.514444, boat.u_k, boat.rho, boat.g)
	boat.plant.setRes(res_2,res_5)
	print('res_2: ' + str(res_2))
	print('res_5: ' + str(res_5))
	boat.plant.show()
	print(boat.deckArea)





