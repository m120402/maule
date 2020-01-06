
from __future__ import division

import math


class Solar:
	# def __init__(self, speed = 3, gravity = 9.81, density = 1025, kinematic_viscosity = 9.37e-7):
	def __init__(self):

		self.total_propulsive_efficiency = 0.68 #Propulsive efficiency (~.7 for frigate*)* Transmission efficiency (~.97) 
		# self.solar_efficiency = 0.05 #Thumbrule - Only get 1/20th of rated solar over time
		self.solar_efficiency = (5/24) # 5 hours of peak solar rating.
		self.cell_rating = 200e-3 #Kilowatts per m^2 (typically ranges from 10-15 W/ft^2 or 105- 200 W / m^2)
		self.panel_weight = 18.6/1.63 #kg/m^2
		self.BatteryDischargeRate = 150 #Amps over 24 hours, gel-type lead acid battery cell
		self.CellVoltage = 2 #Volts, gel-type lead acid battery cell
		self.CellVolume = .09 #m^3, gel-type lead acid battery cell
		self.CellWeight = 512 / 2.2 #kg, gel-type lead acid battery cell
		self.BatteryCellOutput = self.BatteryDischargeRate*self.CellVoltage*1e-3 #Kilowatts
		# Lipo Values
		self.LipoCellOutput = 5 #Kilowatts
		self.LipoCellVolume = 0.12763275 #m^3, Lipo cell
		self.LipoCellWeight = 5114 #kg, Lipo cell

		# self.P2_ex=2.0 #Propulsive Power needed to go 2 knots
		# self.P5_ex=20.0 #Propulsive Power needed to go 5 knots

		# Must Update to call the actual HotelLoads required!
		# ___________________________________________________________________________________________________
		self.HotelLoads_ex = 5

		# Initialize Variable Quantities
		self.res_2 = 0 # Resistance to go 2 kts (N)
		self.res_5 = 0 # Resistance to go 5 kts (N)
		self.HotelLoads = 0 # Continuous Hotel Load (kW)
		self.Power2 = 0 # Propulsive Power required to move 2 kts (kW)
		self.Power5 = 0 # Propulsive Power required to move 5 kts(kW)
		self.solar_area = 0 # Area of solar pannels to power 2 kts though water continuously (m^2)
		self.solar_weight =  0 # Weight of solar panels (kg)

		self.PowerDelta = 0 # Difference between power to push vessel at 5 vs 2 kts (kW)
		self.number_of_cells = 0 # Number of battery cells required to instantaneously supply the power delta between 2 and 5 kts
		self.volume_of_cells = 0 # Volume of lead acid battery cells (m^3)
		self.weight_of_cells = 0 # Weight of lead acid battery cells (kg)
		self.number_of_powerwalls = 0
		self.volume_of_powerwalls = 0
		self.weight_of_powerwalls = 0

	def show(self):
		if self.res_2:
			self.setRes(self.res_2,self.res_5)
			print('Design requires ', round(self.solar_area,2), 'm^2 of solar panels, weighing ', self.solar_weight, 'kg.')
			print('Design requires', round(self.PowerDelta,2), 'kw of additional capacity.')
			print('With SVRLA Batteries, this means', self.number_of_cells, 'battery cells, taking up', round(self.volume_of_cells,2), 'm^3')
			print('and weighing', round(self.weight_of_cells,2), ' kg.')
			print('With Lithium Ion Powerwall, this means', self.number_of_powerwalls, "Powerwalls, taking up", self.volume_of_powerwalls, 'm^3')
			print('and weighing', self.weight_of_powerwalls, 'kg.')
		else:
			print('Must setRes First')

	def setRes(self, res_2, res_5):
		self.res_2 = res_2
		self.res_5 = res_5

		# Must Update to call the actual HotelLoads required!
		# ___________________________________________________________________________________________________
		self.HotelLoads = self.HotelLoads_ex
		self.Power2 = self.res_2*2/1000/self.total_propulsive_efficiency + self.HotelLoads
		self.Power5 = self.res_5*5/1000/self.total_propulsive_efficiency + self.HotelLoads
		self.solar_area = (self.Power2 / self.solar_efficiency) / self.cell_rating
		self.solar_weight =  self.solar_area *self.panel_weight

		self.PowerDelta = self.Power5 - self.Power2
		self.number_of_cells = math.ceil(self.PowerDelta / self.BatteryCellOutput)
		self.volume_of_cells = self.number_of_cells * self.CellVolume
		self.weight_of_cells = self.number_of_cells * self.CellWeight
		self.number_of_powerwalls = math.ceil(self.PowerDelta/self.LipoCellOutput)
		self.volume_of_powerwalls = self.number_of_powerwalls*self.LipoCellVolume
		self.weight_of_powerwalls = self.number_of_powerwalls*self.LipoCellWeight

class FuelCell:
	def __init__(self):

		total_propulsive_efficiency = 0.68 #Propulsive efficiency (~.7 for frigate*)* Transmission efficiency (~.97)
LHV_H2 = 120.21 #MJ/kg
hfc_efficiency = 0.59 #Percent of LHV of H2 delivered as electrical energy by Siemens FCM34
hydrogen_tank_specific_volume = 300.0 / 9.5  #Liters per Kg of hydrogen gas at 500 bar (stored in 300L canisters)
hydrogen_tank_specific_mass = 260.0/300 #Kg of tankage per 300L canister
ProvidedSolar_ex=2
P5_ex=20
HotelLoads_ex = 5
SprintTime_ex = 240

	def energy_needed_kwh(ProvidedSolar=ProvidedSolar_ex, P5=P5_ex, HotelLoads = HotelLoads_ex, SprintTime = SprintTime_ex):
	    return ((P5 - ProvidedSolar)/total_propulsive_efficiency + HotelLoads) * SprintTime #Kwhr

	def hydrogen_needed_mass(ProvidedSolar=ProvidedSolar_ex, P5=P5_ex, HotelLoads = HotelLoads_ex, SprintTime = SprintTime_ex):
	    energy_needed_MJ = energy_needed_kwh(ProvidedSolar,P5,HotelLoads,SprintTime) * 3.6 #MJ
	    return ((energy_needed_MJ / hfc_efficiency) / LHV_H2) #kg H2

	def hydrogen_needed_volume(ProvidedSolar=ProvidedSolar_ex, P5=P5_ex, HotelLoads = HotelLoads_ex, SprintTime = SprintTime_ex):
	    return (hydrogen_needed_mass(ProvidedSolar,P5,HotelLoads,SprintTime) * hydrogen_tank_specific_volume)


	def number_of_tanks(ProvidedSolar=ProvidedSolar_ex, P5=P5_ex, HotelLoads = HotelLoads_ex, SprintTime = SprintTime_ex):
	    return (math.ceil(hydrogen_needed_volume(ProvidedSolar,P5,HotelLoads,SprintTime) / 300) )

	def weight_of_tanks(ProvidedSolar=ProvidedSolar_ex, P5=P5_ex, HotelLoads = HotelLoads_ex, SprintTime = SprintTime_ex):
	    return (number_of_tanks(ProvidedSolar,P5,HotelLoads,SprintTime) * 260) #kg

	def volume_of_tanks(ProvidedSolar=ProvidedSolar_ex, P5=P5_ex, HotelLoads = HotelLoads_ex, SprintTime = SprintTime_ex):
	    return (number_of_tanks(ProvidedSolar,P5,HotelLoads,SprintTime) * 0.737) #m^3

	def show(self):

		print('Design requires', round(energy_needed_kwh(),2), 'kwh of energy.')
		print('This requires', round(hydrogen_needed_mass(),2), 'kg of H2 at 500 bar')
		print('contained in', number_of_tanks(), ' 300L tanks weighing', round(weight_of_tanks(),2), 'kg and taking up', round(volume_of_tanks(),2), 'm^3.')


# plant = Solar()
# plant.solar()