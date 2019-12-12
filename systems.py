
from __future__ import division

import math


class Solar:
    # def __init__(self, speed = 3, gravity = 9.81, density = 1025, kinematic_viscosity = 9.37e-7):
    def __init__(self,speed = 3, gravity = 9.81, density = 1025, kinematic_viscosity = 1.18832278e-6):

        self.total_propulsive_efficiency = 0.68 #Propulsive efficiency (~.7 for frigate*)* Transmission efficiency (~.97) 
        self.solar_efficiency = 0.05 #Thumbrule - Only get 1/20th of rated solar over time
        self.cell_rating = 196e-3 #Kilowatts per m^2 (typically ranges from 10-15 W/ft^2 or 105- 200 W / m^2)
        self.panel_weight = 18.6/1.63 #kg/m^2
        self.BatteryDischargeRate = 150 #Amps over 24 hours
        self.CellVoltage = 2 #Volts
        self.CellVolume = .09 #m^3
        self.CellWeight = 512 / 2.2 #kg
        self.BatteryCellOutput = self.BatteryDischargeRate*self.CellVoltage*1e-3 #Kilowatts
        # self.P2_ex=2.0 #Propulsive Power needed to go 2 knots
        # self.P5_ex=20.0 #Propulsive Power needed to go 5 knots
        self.HotelLoads_ex = 5

        self.res_2 = 0
        self.res_5 = 0
        self.HotelLoads = 0
        self.Power2 = 0
        self.Power5 = 0
        self.solar_area = 0
        self.solar_weight =  0

        self.PowerDelta = 0
        self.number_of_cells = 0
        self.volume_of_cells = 0
        self.weight_of_cells = 0
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

        self.HotelLoads = self.HotelLoads_ex
        self.Power2 = self.res_2*2/1000/self.total_propulsive_efficiency + self.HotelLoads
        self.Power5 = self.res_5*5/1000/self.total_propulsive_efficiency + self.HotelLoads
        self.solar_area = (self.Power2 / self.solar_efficiency) / self.cell_rating
        self.solar_weight =  self.solar_area *self.panel_weight

        self.PowerDelta = self.Power5 - self.Power2
        self.number_of_cells = math.ceil(self.PowerDelta / self.BatteryCellOutput)
        self.volume_of_cells = self.number_of_cells * self.CellVolume
        self.weight_of_cells = self.number_of_cells * self.CellWeight
        self.number_of_powerwalls = math.ceil(self.PowerDelta/5.0)
        self.volume_of_powerwalls = self.number_of_powerwalls*0.12763275
        self.weight_of_powerwalls = self.number_of_powerwalls*114


# plant = Solar()
# plant.solar()