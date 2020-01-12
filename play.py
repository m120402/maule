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

class Hull:
	def __init__(self, LWL, designSpeed = 2, gravity = 9.81, Abt = 0):
		self.V = designSpeed*0.514444 #knots -> m/s
		self.g = gravity #m/s^2
		self.Abt = Abt
		self.LWL = LWL
		

		# Internals
		self.Fn = p.calc_Fn(self.V, self.LWL, self.g)
		self.Cb = p.calc_Cb(self.Fn)
		self.Cm = p.calc_Cm(self.Fn)
		self.B = p.calc_B(self.LWL)
		self.T = p.calc_T(self.B, self.Cm)
		self.Cwp = p.calc_Cwp(self.Cb)
		self.D = p.calc_D(self.B)
		self.Cbd = p.calc_Cbd(self.Cb, self.D, self.T)
		self.Vi = p.calc_Vi(self.Cbd, self.LWL, self.B, self.D)
		self.displacement = p.calc_Disp(self.Cb, self.LWL, self.B, self.T)
		self.S = p.calc_S(self.LWL, self.T, self.B, self.Cm, self.Cb, self.Cwp, self.Abt)

	def setDims(self, LWL):
		self.LWL = LWL
		self.Fn = p.calc_Fn(self.V, self.LWL, self.g)
		self.Cb = p.calc_Cb(self.Fn)
		self.Cm = p.calc_Cm(self.Fn)
		self.B = p.calc_B(self.LWL)
		self.T = p.calc_T(self.B, self.Cm)
		self.Cwp = p.calc_Cwp(self.Cb)
		self.D = p.calc_D(self.B)
		self.Cbd = p.calc_Cbd(self.Cb, self.D, self.T)
		self.Vi = p.calc_Vi(self.Cbd, self.LWL, self.B, self.D)
		self.displacement = p.calc_Disp(self.Cb, self.LWL, self.B, self.T)
		self.S = p.calc_S(self.LWL, self.T, self.B, self.Cm, self.Cb, self.Cwp, self.Abt)

class Min_res:
	# def __init__(self, speed = 3, gravity = 9.81, density = 1025, kinematic_viscosity = 9.37e-7):
	def __init__(self, speed = 2, gravity = 9.81, density = 1025, kinematic_viscosity = 1.18832278e-6):
		self.V = speed*0.514444 #knots -> m/s
		self.g = gravity #m/s^2
		self.rho = density #kg/m^3
		self.u_k = kinematic_viscosity #m^2/s, default is kinematic viscosity of seawater at 35 g/kg and 25 C
		self.LCB = -0.75
		self.At = 16
		self.Abt = 0
		self.hb = 0
		self.Cstern = 10
		self.solar = s.Solar()
		self.hfc = s.FuelCell()
		self.deckArea = 0
		self.V2 = 2*0.514444 #knots -> m/s
		self.V5 = 5*0.514444 #knots -> m/s
		self.Rd2 = 0
		self.Rd5 = 0
		self.P2 = 0
		self.P5 = 0

		# Margins
		self.volumeMargin = 0.1


		self.hull = Hull(20)

	def objective(self, x, *args):
		self.hull.setDims(x)
		Vol = self.volume()
		# Currwntly the args dont matter since using self.xxx for inputs
		Abt = args[0]
		V = args[1] 
		u_k = args[2]
		rho = args[3]
		g = args[4]
		# visc = p.calc_Rv_Opt_Opt(x, Abt, Vol, V, u_k, rho, g) #, self.V, self.g, self.rho, self.LCB, self.Cwp, self.At, self.Abt, self.u_k, self.Cstern)
		self.Rd2 = p.calc_Rv_Opt(x, self.Abt, Vol, self.V2, self.u_k, self.rho, self.g) #, self.V, self.g, self.rho, self.LCB, self.Cwp, self.At, self.Abt, self.u_k, self.Cstern)
		self.Rd5 = p.calc_Rv_Opt(x, self.Abt, Vol, self.V5, self.u_k, self.rho, self.g) #, self.V, self.g, self.rho, self.LCB, self.Cwp, self.At, self.Abt, self.u_k, self.Cstern)
		
		self.P2 = self.Rd2*self.V2
		self.P5 = self.Rd2*self.V5
		visc = p.calc_Rv_Opt(x[0], self.Abt, Vol, self.V, self.u_k, self.rho, self.g) #, self.V, self.g, self.rho, self.LCB, self.Cwp, self.At, self.Abt, self.u_k, self.Cstern)
		# visc = x[0]
		# cor = self.calcCor(x) #, self.rho, self.V, self.Cwp, self.Abt)
		return (visc)/1000
		# return self.deckArea - self.solar.solar_area

	def kts_2_mps(self, kts):
		return kts * 0.514444

	def lbs_2_kg(self, lbs):
		return kts * 0.453592


	def volume(self):
		# Must Update to call the actual volume required!
		# ___________________________________________________________________________________________________
		return 177

	def weight(self):
		# Must Update to call the actual weight required!
		# ___________________________________________________________________________________________________
		container = 60000 # lbs
		hull = container * 3
		kg = self.lbs_2_kg(hull + contaier)
		return 

	def constraintVol(self, x):
		self.hull.setDims(x)
		Vol = (1+ self.volumeMargin) * self.hull.Vi - self.volume()
		return Vol

	def constraintArea(self, x):
		self.deckArea = p.calcDeckArea(x[0])
		res_2 = p.calc_Rv_Opt(x, self.Abt, self.volume(), self.kts_2_mps(2), self.u_k, self.rho, self.g)
		res_5 = p.calc_Rv_Opt(x, self.Abt, self.volume(), self.kts_2_mps(5), self.u_k, self.rho, self.g)
		self.solar.setRes(res_2,res_5)
		const = self.deckArea - self.solar.solar_area
		return const

	def constraintDisp(self, x):
		self.hull.setDims(x)
		Disp = self.hull.displacement - self.weight()
		return Vol


	def setBounds(self):
		bl = (10, 150)
		bnds = [bl]
		return bnds

	def setConstraints(self):
		conVol = {'type': 'ineq', 'fun': self.constraintVol}
		conArea = {'type': 'ineq', 'fun': self.constraintArea}

		cons = (conVol, conArea)
		return cons


	def minima(self,x0):
		bnds = self.setBounds()
		cons = self.setConstraints()
		solution = minimize(self.objective,x0,(self.Abt, self.V, self.u_k, self.rho, self.g),method = 'SLSQP', constraints = cons, bounds = bnds, options ={'disp':True,'maxiter':100})
		# self.deckArea = p.calcDeckArea(solution.x[0])
		return solution



if __name__ == "__main__":
	boat = Min_res()
	x0 = [20]
	res_2 = p.calc_Rv_Opt(x0[0], boat.Abt, boat.volume(), 2*0.514444, boat.u_k, boat.rho, boat.g)
	res_5 = p.calc_Rv_Opt(x0[0], boat.Abt, boat.volume(), 5*0.514444, boat.u_k, boat.rho, boat.g)
	boat.solar.setRes(res_2,res_5)
	# sol = Min_res().minima(x0)
	sol = boat.minima(x0)
	LWL = sol.x[0]

	print(LWL)
	print(p.calc_Rv_Opt(sol.x[0], boat.Abt, 177, boat.V, boat.u_k, boat.rho, boat.g))

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

	res_2 = p.calc_Rv_Opt(sol.x[0], boat.Abt, 177, 2*0.514444, boat.u_k, boat.rho, boat.g)
	res_5 = p.calc_Rv_Opt(sol.x[0], boat.Abt, 177, 5*0.514444, boat.u_k, boat.rho, boat.g)
	boat.solar.setRes(res_2,res_5)
	print('res_2: ' + str(res_2))
	print('res_5: ' + str(res_5))
	print('pow_2: ' + str(res_2*2*0.514444))
	print('pow_5: ' + str(res_5*5*0.514444))
	boat.solar.show()
	print(boat.deckArea)
	print(boat.solar.solar_area)





