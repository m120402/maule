import math
P2 = 10 #KW
P5 = 20 #KW
total_propulsive_efficiency = 0.68 #Propulsive efficiency (~.7 for frigate*)* Transmission efficiency (~.97)
solar_efficiency = 0.05 #Thumbrule - Only get 1/20th of rated solar over time
cell_rating = 105e-3 #Kilowatts per m^2 (typically ranges from 10-15 W/ft^2 or 105- 160 W / m^2)
HotelLoads = 0.0 #Kilowatts
BatteryDischargeRate = 150 #Amps over 24 hours
CellVoltage = 2 #Volts
CellVolume = .09 #m^3

BatteryCellOutput = BatteryDischargeRate*CellVoltage*1e-3 #Kilowatts



def solar_size(Power2, Power5):
    Power2 = Power2/total_propulsive_efficiency + HotelLoads
    solar_area = (Power2 / solar_efficiency) / cell_rating
    print('Design requires ', solar_area, 'm^2 of solar panels')

def battery_size(Power2, Power5):
    Total_Power2 = Power2/total_propulsive_efficiency + HotelLoads
    Total_Power5 = Power5/total_propulsive_efficiency + HotelLoads
    PowerDelta = Total_Power5 - Total_Power2
    number_of_cells = PowerDelta / BatteryCellOutput
    volume_of_cells = number_of_cells * CellVolume
    print('Design requires', number_of_cells, 'battery cells, taking up', volume_of_cells, 'm^3')

solar_size(P2,P5)
battery_size(P2,P5)