
from __future__ import division

import math

import pandas as pd
import matplotlib.pyplot as plt
from pandas import ExcelWriter
from pandas import ExcelFile
import os.path
import sys
from import_values import get_PNA_loads


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
		self.LipoCellEnergy = 13.5 #kWh
		self.LipoCellVolume = 0.12763275 #m^3, Lipo cell
		self.LipoCellWeight = 114 #kg, Lipo cell

		# self.P2_ex=2.0 #Propulsive Power needed to go 2 knots
		# self.P5_ex=20.0 #Propulsive Power needed to go 5 knots


		# Initialize Variable Quantities
		self.res_2 = 0 # Resistance to go 2 kts (N)
		self.res_5 = 0 # Resistance to go 5 kts (N)

				# Must Update to call the actual HotelLoads required!
		# ___________________________________________________________________________________________________
		self.HotelLoads = get_PNA_loads().item()/1000 # Continuous Hotel Load (kW)
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
		print('Design requires ', round(self.solar_area,2), 'm^2 of solar panels, weighing ', self.solar_weight, 'kg.')
		# print('Design requires', round(self.PowerDelta,2), 'kw of additional capacity.')
		print('With Lithium Ion Powerwall, this means', self.number_of_powerwalls, "Powerwalls, taking up", self.volume_of_powerwalls, 'm^3')
		print('and weighing', self.weight_of_powerwalls, 'kg.\n')

	def calc_Panel_Area(self, P2):
		# Deck Area required for Solar Power to reliably sustain 2 kts 
		# Ads -= f(P2) + recharge factor + f(PeakPow - AvgPow)
		self.Power2 = P2/1000 + self.HotelLoads# Work with kW
		self.solar_area = (self.Power2 / self.solar_efficiency) / self.cell_rating
		self.solar_weight =  self.solar_area *self.panel_weight


	def calc_Battery_Storage(self, P2):
		# Calc # of Batteries required to sustain 2 kts and Hotel Loads for 3 days of no sunlight and 50% charge remaining

		# Must Update to actually account for correct fluctuation estimate!
		# ___________________________________________________________________________________________________
		# peak_hrs_lost = 1 # Assuming we get 1 less hour of peak solar output than expected in a day
		# energy_lost = self.solar_area * self.cell_rating * peak_hrs_lost #kWh
		
		self.Power2 = P2/1000 + self.HotelLoads# Work with kW
		self.battery_storage_energy = self.Power2 * 24 * 3 * 2 # 3 days of low speed propulsion and only 50% discharged
		self.number_of_powerwalls = math.ceil(self.battery_storage_energy/self.LipoCellEnergy)

		self.volume_of_powerwalls = self.number_of_powerwalls*self.LipoCellVolume
		self.weight_of_powerwalls = self.number_of_powerwalls*self.LipoCellWeight


	def calc_added_Battery(self, Vol, Weight):
		pass

	#This function required for compatability with play.py
	# def setRes(self, res_2, res_5):
	# 	self.res_2 = res_2
	# 	self.res_5 = res_5

	# 	self.Power2 = self.res_2*2*0.514444/1000/self.total_propulsive_efficiency + self.HotelLoads
	# 	self.Power5 = self.res_5*5*0.514444/1000/self.total_propulsive_efficiency + self.HotelLoads
	# 	self.solar_area = (self.Power2 / self.solar_efficiency) / self.cell_rating
	# 	self.solar_weight =  self.solar_area *self.panel_weight

	# 	self.PowerDelta = self.Power5 - self.Power2
	# 	self.number_of_cells = math.ceil(self.PowerDelta / self.BatteryCellOutput)
	# 	self.volume_of_cells = self.number_of_cells * self.CellVolume
	# 	self.weight_of_cells = self.number_of_cells * self.CellWeight
	# 	self.number_of_powerwalls = math.ceil(self.PowerDelta/self.LipoCellOutput)
	# 	self.volume_of_powerwalls = self.number_of_powerwalls*self.LipoCellVolume
	# 	self.weight_of_powerwalls = self.number_of_powerwalls*self.LipoCellWeight

class FuelCell:
	def __init__(self):

		# https://studylib.net/doc/18083455/sinavy-pem-fuel-cell

		# total_propulsive_efficiency = 0.68 #Propulsive efficiency (~.7 for frigate*)* Transmission efficiency (~.97)
		self.LHV_H2 = 120.21 #MJ/kg
		self.hfc_efficiency = 0.59 #Percent of LHV of H2 delivered as electrical energy by Siemens FCM34
		self.hydrogen_tank_fuel_mass = 9.5  # Kg of hydrogen gas at 500 bar (stored in 300L canisters)
		self.hydrogen_tank_mass = 260 # kg
		self.hydrogen_tank_volume = 300/1000 # m^3
		self.hydrogen_tank_specific_volume = 300.0 / 9.5  #Liters per Kg of hydrogen gas at 500 bar (stored in 300L canisters)
		self.hydrogen_tank_specific_mass = 260.0/300 #Kg of tankage per 300L canister
		self.ProvidedSolar_ex=2
		self.P5_ex=20
		# self.HotelLoads_ex = 5
		self.SprintTime_ex = 240

		self.FCM_34_Rated_Power = 34 #kW
		self.FCM_34_Volume = 0.48*0.48*1.45 #m^2
		self.FCM_34_Weight = 650 # kg

		# Note that FCM_120 can be run at 20% power (24kW) at 68% efficiency
		self.FCM_120_Rated_Power = 120 #kW
		self.FCM_120_Volume = 0.5*0.53*1.76 #m^2
		self.FCM_120_Weight = 900 # kg
		self.HFC_efficiency_design = 0.69 # Efficiency at 20% load
		self.hydrogen_structure = 5 #kg
		self.HotelLoads = get_PNA_loads().item()/1000 # Continuous Hotel Load (kW)
		self.HFC_efficiency_on_ave = 0.6
		self.HFC_efficiency_design = self.HFC_efficiency_on_ave
	def kJ_2_kWh(self, kJ):
		return kJ / 3600

	def calc_HFC(self, P2, P5, hs):
		# self.Pd = (P5 - P2)/ 1000 # kW
		self.Pd5 = (P5 / 1000) + self.HotelLoads# kW
		self.Pd = (P2 / 1000) + self.HotelLoads
		# self.Pd5 = (P5 + self.HotelLoads)/ 1000 # kW
		# self.Pd = (P2 + self.HotelLoads) / 1000
		self.HFC_Output = self.FCM_120_Rated_Power * 0.2
		# self.Num_HFC = math.ceil(self.Pd/self.HFC_Output) + 1 # Add a spare
		self.Num_HFC = math.ceil(self.Pd5/self.HFC_Output) + 1 # Add a spare
		self.HFC_weight = self.Num_HFC * self.FCM_120_Weight
		self.HFC_volume = self.Num_HFC * self.FCM_120_Volume

		# Cal Num Containers
		# HFC_Energy_Rec = self.Pd*hs
		HFC_Energy_Rec = self.Pd*365*24 +self.Pd5*hs
		HFC_Container_Energy_kJ = self.LHV_H2 * self.HFC_efficiency_design * self.hydrogen_tank_fuel_mass * 1000 # kJ 
		HFC_Container_Energy_kWh = self.kJ_2_kWh(HFC_Container_Energy_kJ) # kWh
		self.Num_HFC_Containers = math.ceil(HFC_Energy_Rec/HFC_Container_Energy_kWh)
		self.HFC_Container_weight = self.Num_HFC_Containers * (self.hydrogen_tank_mass + self.hydrogen_tank_fuel_mass + self.hydrogen_structure)
		self.HFC_Container_volume = self.Num_HFC_Containers * self.hydrogen_tank_volume

	def calc_HFC_Cat(self, P2, P5, hs):
		self.Pd = (P5 - P2)/ 1000 # kW
		# self.Pd5 = (P5 + self.HotelLoads)/ 1000 # kW
		# self.Pd = (P2 + self.HotelLoads) / 1000
		self.HFC_Output = self.FCM_120_Rated_Power * 0.2
		self.Num_HFC = math.ceil(self.Pd/self.HFC_Output) + 1 # Add a spare
		# self.Num_HFC = math.ceil(self.Pd5/self.HFC_Output) + 1 # Add a spare
		self.HFC_weight = self.Num_HFC * self.FCM_120_Weight
		self.HFC_volume = self.Num_HFC * self.FCM_120_Volume

		# Cal Num Containers
		HFC_Energy_Rec = self.Pd*hs
		# HFC_Energy_Rec = self.Pd*365*24 +self.Pd5*hs
		HFC_Container_Energy_kJ = self.LHV_H2 * self.HFC_efficiency_design * self.hydrogen_tank_fuel_mass * 1000 # kJ 
		HFC_Container_Energy_kWh = self.kJ_2_kWh(HFC_Container_Energy_kJ) # kWh
		self.Num_HFC_Containers = math.ceil(HFC_Energy_Rec/HFC_Container_Energy_kWh)
		self.HFC_Container_weight = self.Num_HFC_Containers * (self.hydrogen_tank_mass + self.hydrogen_tank_fuel_mass + self.hydrogen_structure)
		self.HFC_Container_volume = self.Num_HFC_Containers * self.hydrogen_tank_volume


	def calc_added_HFC(self, vol_avail, weight_avail):
		weight_constraint = math.floor(weight_avail / (self.hydrogen_tank_mass + self.hydrogen_tank_fuel_mass + self.hydrogen_structure))
		vol_constraint = math.floor(vol_avail / self.hydrogen_tank_volume)
		additional_containers = min(weight_constraint,vol_constraint) # Cant violate available mass or volume
		self.Num_HFC_Containers += additional_containers
		self.HFC_Container_weight += additional_containers * (self.hydrogen_tank_mass + self.hydrogen_tank_fuel_mass + self.hydrogen_structure)
		self.HFC_Container_volume += additional_containers * self.hydrogen_tank_volume
		print(f'# H2 Containers: {self.Num_HFC_Containers}')
		return 1

	def calc_endurance(self):
		# self.Pd = ((self.Pd * 1000) -self.HotelLoads)/1000 + self.HotelLoads 
		HFC_Container_Energy_kJ = self.LHV_H2 * self.HFC_efficiency_design * self.hydrogen_tank_fuel_mass * 1000 # kJ 
		HFC_Container_Energy_kWh = self.kJ_2_kWh(HFC_Container_Energy_kJ) # kWh
		HFC_energy_kWh = self.Num_HFC_Containers * HFC_Container_Energy_kWh
		hours_slow = HFC_energy_kWh / self.Pd
		days_slow = math.floor(hours_slow/24)
		# hours_fast = HFC_energy_kWh / self.Pd5
		# days_fast = math.floor(hours_fast/24)
		return days_slow

class IC:
	def __init__(self):

		# https://studylib.net/doc/18083455/sinavy-pem-fuel-cell

		# total_propulsive_efficiency = 0.68 #Propulsive efficiency (~.7 for frigate*)* Transmission efficiency (~.97)
		self.LHV_D = 12.67 #kWh/kg
		self.diesel_efficiency = 0.35 #Percent of LHV of fuel delivered as electrical energy by generator
		self.Generator_Rated_Power = 20 #kW
		self.Diesel_weight = 975 #kg weight of 20 kW generator
		self.Diesel_volume = 15.6 #m^3 volume
		self.hours_before_maintenance = 200
		self.Diesel_density = 846 # kg/m^3

	def calc_Diesel(self, P2, P5, hs):
		self.Pd = (P5 - P2)/ 1000 # kW
		self.Energy_Needed = self.Pd * hs # kWh
		self.Diesel_Energy_Capacity = self.Generator_Rated_Power * self.hours_before_maintenance
		
		self.Num_Diesel_power = math.ceil(self.Pd/self.Generator_Rated_Power) 
		self.Num_Diesel_energy = math.ceil(self.Energy_Needed/self.Diesel_Energy_Capacity) 
		self.Num_Diesel_time = math.ceil(hs/self.hours_before_maintenance) 

		self.Number_Generators_Needed = max(self.Num_Diesel_power,self.Num_Diesel_energy, self.Num_Diesel_time) + 1
		self.Volume_Generators = self.Number_Generators_Needed * self.Diesel_volume
		self.Weight_Generators = self.Number_Generators_Needed * self.Diesel_weight
		self.Weight_Fuel = self.Energy_Needed / self.LHV_D / self.diesel_efficiency
		self.Volume_Fuel = self.Weight_Fuel / self.Diesel_density

	def calc_added_Diesel(self, vol_avail, weight_avail):
		weight_constraint_m3 = math.floor(weight_avail / (self.Diesel_density))
		vol_constraint_m3 = math.floor(vol_avail)
		additional_fuel = min(weight_constraint_m3,vol_constraint_m3) # Cant violate available mass or volume
		self.Weight_Fuel += additional_fuel * self.Diesel_density
		self.Volume_Fuel += additional_fuel
		return 1

	def calc_endurance(self):
		Diesel_Energy_kWh = self.LHV_D * self.diesel_efficiency * self.Weight_Fuel # kWh
		hours_fast = Diesel_Energy_kWh / self.Pd
		days_fast = math.floor(hours_fast/24)
		return days_fast