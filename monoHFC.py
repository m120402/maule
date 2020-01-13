from __future__ import division

from scipy.optimize import minimize
import numpy as np
import math
  
import Parametric as p
import systems as s

import pandas as pd
import matplotlib.pyplot as plt
from pandas import ExcelWriter
from pandas import ExcelFile
import os.path
import sys
from import_values import get_PNA_weights
# To use the "boat" virtualenv:
# https://packagecontrol.io/packages/Virtualenv

options = {}
options['FIG_SIZE'] = [8,8]
options['FULL_RECALCULATE'] = False

print(type(options))

class Hull:
	def __init__(self, LWL, designSpeed = 2, gravity = 9.81, density = 1025, kinematic_viscosity = 1.18832278e-6, Abt = 0, shell_appendage_allowance = 0.005):
		self.V = designSpeed*0.514444 #knots -> m/s
		self.g = gravity #m/s^2
		self.rho = density
		self.u_k = kinematic_viscosity #m^2/s, default is kinematic viscosity of seawater at 35 g/kg and 15 C
		self.Abt = Abt
		self.shell_appendage_allowance = shell_appendage_allowance
		self.LWL = LWL
		self.Vol = 0
		

		# Internals
		self.Fn = p.calc_Fn(self.V, self.LWL, self.g)
		self.Cb = p.calc_Cb(self.Fn)
		self.Cm = p.calc_Cm(self.Cb)
		self.B = p.calc_B(self.LWL)
		self.T = p.calc_T(self.B, self.Cm)
		self.Cwp = p.calc_Cwp(self.Cb)
		self.D = p.calc_D(self.B)
		self.Cbd = p.calc_Cbd(self.Cb, self.D, self.T)
		self.Vi = p.calc_Vi(self.Cbd, self.LWL, self.B, self.D)
		self.displacement_volume = p.calc_Disp_Vol(self.Cb, self.LWL, self.B, self.T)
		self.displacement = p.calc_Disp(self.displacement_volume, self.rho, self.shell_appendage_allowance)
		self.S = p.calc_S(self.LWL, self.T, self.B, self.Cm, self.Cb, self.Cwp, self.Abt)
		self.K = p.calc_K(self.LWL, self.B, self.T, self.Cb)
		self.Cv = p.calc_Cv(self.LWL, self.B, self.T, self.Cb, self.V, self.u_k)

	def setDims(self, x):
		self.LWL = x[0]
		self.Fn = p.calc_Fn(self.V, self.LWL, self.g)
		self.Cb = p.calc_Cb(self.Fn)
		self.Cm = p.calc_Cm(self.Cb)
		self.Cp = p.calc_Cp(self.Cb,self.Cm)
		self.Cwp = p.calc_Cwp(self.Cb)
		self.B = p.calc_B(self.LWL)
		self.T = p.calc_T(self.B, self.Cm)
		self.D = p.calc_D(self.B)
		self.Cbd = p.calc_Cbd(self.Cb, self.D, self.T)
		self.Vi = p.calc_Vi(self.Cbd, self.LWL, self.B, self.D)
		self.displacement_volume = p.calc_Disp_Vol(self.Cb, self.LWL, self.B, self.T)
		self.displacement = p.calc_Disp(self.displacement_volume, self.rho, self.shell_appendage_allowance)
		self.S = p.calc_S(self.LWL, self.T, self.B, self.Cm, self.Cb, self.Cwp, self.Abt)
		self.K = p.calc_K(self.LWL, self.B, self.T, self.Cb)
		self.Cv = p.calc_Cv(self.LWL, self.B, self.T, self.Cb, self.V, self.u_k)

	def show(self):
		print('Main Characteristics')
		print('LWL: 			' + str(round(self.LWL,2)) + ' (m)')
		print('B: 				' + "%.2f" % round(self.B,2) + ' (m)')
		print('T: 				' + str(round(self.T,2)) + ' (m)')
		print('D: 				' + str(round(self.D,2)) + ' (m)')
		print('Disp: 			' + str(round(self.displacement/1000,2)) + ' (tonnes)')
		print('Disp Vol: 		' + str(round(self.displacement_volume,2)) + ' (m^3)')
		print('Internal Vol: 	' + str(round(self.Vi,2)) + ' (m^3)')
		print('S: 				' + str(round(self.S,2)) + ' (m^2)')

		print('')

		print('Form Coefficients')
		print('Fn: 	' + str(round(self.Fn,3)))
		print('Cb: 	' + str(round(self.Cb,3)))
		print('Cbd: 	' + str(round(self.Cbd,3)))
		print('Cm: 	' + str(round(self.Cm,3)))
		print('Cwp: 	' + str(round(self.Cwp,3)))
		print('Cp: 	' + str(round(self.Cp,3)))

		print('')

		print('Drag Coefficients')
		print('K: 		' + str(round(self.K,5)))
		print('Cv: 	' + str(round(self.Cv,5)))

		print('')


class Opt_Hull:
	# def __init__(self, speed = 3, gravity = 9.81, density = 1025, kinematic_viscosity = 9.37e-7):
	def __init__(self, speed = 2, gravity = 9.81, density = 1025, kinematic_viscosity = 1.18832278e-6, total_propulsive_efficiency = 0.68):
		self.V = speed*0.514444 #knots -> m/s
		self.g = gravity #m/s^2
		self.rho = density #kg/m^3
		self.u_k = kinematic_viscosity #m^2/s, default is kinematic viscosity of seawater at 35 g/kg and 15 C
		self.total_propulsive_efficiency = total_propulsive_efficiency
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

		self.total_estimated_weight = 0
		self.total_estimated_sys_volume = 0

		self.PNA_weight = get_PNA_weights().item()

		self.weights = {}
		self.volumes = {}
		self.areas = {}

		# Margins
		self.displacement_margin = 0.1
		self.solar_area_margin = 0.1
		self.volume_margin = 0.1

		self.hs = 438 # Number of hours of sprint capability 438 = 5% of a year

		self.hull = Hull(20)

	def objective(self, x, *args):
		self.update(x)
		# Currwntly the args dont matter since using self.xxx for inputs
		Abt = args[0]
		V = args[1] 
		u_k = args[2]
		rho = args[3]
		g = args[4]
		# visc = p.calc_Rv(x, Abt, Vol, V, u_k, rho, g) #, self.V, self.g, self.rho, self.LCB, self.Cwp, self.At, self.Abt, self.u_k, self.Cstern)

		visc = p.calc_Rv(self.rho, self.hull.S, self.V, self.hull.Cv) #, self.V, self.g, self.rho, self.LCB, self.Cwp, self.At, self.Abt, self.u_k, self.Cstern)
		# visc = x[0]
		# cor = self.calcCor(x) #, self.rho, self.V, self.Cwp, self.Abt)
		return (visc)/1000
		# return self.deckArea - self.solar.solar_area

	def show_weights(self):
		# plt.figure()
		slices = self.weights.values()
		labels = self.weights.keys()
		# colors = ['c','m','r']

		fig1, ax1 = plt.subplots()

		ax1.pie(slices, labels=labels, autopct='%1.1f%%', startangle=90)
		#draw circle
		centre_circle = plt.Circle((0,0),0.70,fc='white')
		fig = plt.gcf()
		fig.gca().add_artist(centre_circle)
		# Equal aspect ratio ensures that pie is drawn as a circle
		ax1.axis('equal')  


		# plt.pie(slices, 
		# 	labels = activities, 
		# 	startangle = 90, 
		# 	autopct = '%1.1f%%')
		plt.title(f'Ship Weights: Total = {round(sum(slices)/1000,2)} Tonnes')
		plt.tight_layout()
		plt.show()
		return
	def show_IV_const(self):
		data = [['Battery Volume', self.volumes.get("Battery Volume")], 
				['HFC Volume', self.volumes.get("HFC Volume")], 
				['Combined Volume', self.volumes.get("System Volume")], 
				['Internal Volume', self.volumes.get("Internal Volume")]]
		df2 = pd.DataFrame(data, columns=['Category', 'Volume'])
		df2.set_index("Category",drop=True,inplace=True)
		df2.plot.bar()
		plt.show()
		return 1

	def show_DA_const(self):
		data = [['Deck Area', self.areas.get("Deck Area")], 
				['Solar Area', self.areas.get("Solar Area")]]
		df2 = pd.DataFrame(data, columns=['Category', 'Area'])
		df2.set_index("Category",drop=True,inplace=True)
		df2.plot.bar()
		plt.show()
		return 1

	def show_Weight_const(self):
		data = [['Estimated Weight', self.total_estimated_weight], 
				['Displacement', self.hull.displacement]]

		df2 = pd.DataFrame(data, columns=['Category', 'Weight'])
		df2.set_index("Category",drop=True,inplace=True)
		df2.plot.bar()
		plt.show()

		print(f'weight estimate {self.total_estimated_weight}')

		return 1

	def show_constraints(self):
		self.show_IV_const()
		self.show_DA_const()
		self.show_Weight_const()
		return 1

	def show(self):
		self.show_weights()
		self.show_constraints()
		return

	def kts_2_mps(self, kts):
		return kts * 0.514444

	def lbs_2_kg(self, lbs):
		return lbs * 0.453592

	def calc_sys_weight(self):
		solar_weight = self.solar.solar_weight
		battery_weight = self.solar.weight_of_powerwalls
		hfc_weight = self.hfc.HFC_weight + self.hfc.HFC_Container_weight
		PNA_weight = self.PNA_weight

		cargo_weight = self.lbs_2_kg(60000)
		tmp_weight = solar_weight + battery_weight + hfc_weight + PNA_weight + cargo_weight
		hull_weight = tmp_weight
		sys_weight = solar_weight + battery_weight + hfc_weight + PNA_weight + cargo_weight + hull_weight
		self.weights['solar_weight'] = solar_weight
		self.weights['battery_weight'] = battery_weight
		self.weights['hfc_weight'] = hfc_weight
		self.weights['PNA_weight'] = PNA_weight
		self.weights['cargo_weight'] = cargo_weight
		self.weights['hull_weight'] = hull_weight
		# Must Update to actually account for hull and cargo and other weights!
		# ___________________________________________________________________________________________________
		
		# container = 60000 # lbs
		# hull = container * 3
		# kg = self.lbs_2_kg(hull + container)

		return sys_weight

	def calc_sys_volume(self):
		battery_volume = self.solar.volume_of_powerwalls
		hfc_volume = self.hfc.HFC_volume + self.hfc.HFC_Container_volume
		sys_volume = battery_volume + hfc_volume

		self.volumes['Battery Volume'] = battery_volume
		self.volumes['HFC Volume'] = hfc_volume
		self.volumes['System Volume'] = sys_volume


		# Must Update to account for binary decision to put cargo in hull!
		# ___________________________________________________________________________________________________
		return sys_volume


	def update(self, x):
		self.hull.setDims(x)

		self.deckArea = p.calcDeckArea(x[0], self.hull.B, self.hull.Cwp)
		# self.deckArea = self.hull.LWL * self.hull.B * 6

		Cv2 = p.calc_Cv(self.hull.LWL, self.hull.B, self.hull.T, self.hull.Cb, self.V2, self.u_k)
		Cv5 = p.calc_Cv(self.hull.LWL, self.hull.B, self.hull.T, self.hull.Cb, self.V5, self.u_k)
		self.Rd2 = p.calc_Rv(self.rho, self.hull.S, self.V2, Cv2) 
		self.Rd5 = p.calc_Rv(self.rho, self.hull.S, self.V5, Cv5) 
		
		self.P2 = self.Rd2 * self.V2 / self.total_propulsive_efficiency
		self.P5 = self.Rd2 * self.V5 / self.total_propulsive_efficiency

		self.solar.calc_Panel_Area(self.P2)
		self.solar.calc_Battery_Storage(self.P2)

		self.hfc.calc_HFC(self.P2, self.P5, self.hs)

		#Update Weight and Volume Estimates
		self.total_estimated_weight = self.calc_sys_weight()
		self.total_estimated_sys_volume = self.calc_sys_volume()

		self.volumes['Internal Volume'] = self.hull.Vi
		self.areas['Deck Area'] = self.deckArea
		self.areas['Solar Area'] = self.solar.solar_area


		return 1


	def constraintVol(self, x):
		self.update(x)
		Vol = (1+ self.volume_margin) * self.hull.Vi - self.total_estimated_sys_volume
		return Vol

	def constraintArea(self, x):
		
		self.update(x)
		const = self.deckArea - self.solar.solar_area
		return const

	def constraintDisp(self, x):
		self.update(x)
		Disp = self.hull.displacement - self.total_estimated_weight
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
	boat = Opt_Hull()
	x0 = [50]
	res_2 = 10
	res_5 = 20
	sol = boat.minima(x0)
	LWL = sol.x[0]

	boat.hull.show()
	boat.show()
	# boat.solar.show()


	# print(LWL)
	# print(p.calc_Rv(boat.rho, boat.hull.S, boat.kts_2_mps(2), boat.hull.Cv))

	# print(boat.rho)
	# print(boat.hull.S)
	# print(boat.kts_2_mps(2))
	# print(boat.hull.Cv)


	# B = p.calc_B(LWL)
	# Fn = p.calc_Fn(boat.V, LWL, boat.g)
	# Cb = p.calc_Cb(Fn)
	# Cm = p.calc_Cm(Fn)
	# T = p.calc_T(B, Cm)
	# Cwp = p.calc_Cwp(Cb)
	# S = p.calc_S(LWL, T, B, Cm, Cb, Cwp, boat.Abt)
	# Cv = p.calc_Cv(LWL, B, T, Cb, boat.V, boat.u_k)
	# Cp = p.calc_Cp(Cb,Cm)

	# print('LWL: ' + str(LWL))
	# print('B: ' + str(B))
	# print('Fn: ' + str(Fn))
	# print('Cb: ' + str(Cb))
	# print('Cm: ' + str(Cm))
	# print('T: ' + str(T))
	# print('Cwp: ' + str(Cwp))
	# print('S: ' + str(S))
	# print('Cv: ' + str(Cv))
	# print('Cp: ' + str(Cp))






	# res_2 = p.calc_Rv(sol.x[0], boat.Abt, 177, 2*0.514444, boat.u_k, boat.rho, boat.g)
	# res_5 = p.calc_Rv(sol.x[0], boat.Abt, 177, 5*0.514444, boat.u_k, boat.rho, boat.g)
	# boat.solar.setRes(res_2,res_5)
	# print('res_2: ' + str(res_2))
	# print('res_5: ' + str(res_5))
	print('pow_2: ' + str(boat.P2))
	print('pow_5: ' + str(boat.P5))

	# weight = get_PNA_weights().item()
	# print(weight)



