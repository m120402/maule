import math
total_propulsive_efficiency = 0.68 #Propulsive efficiency (~.7 for frigate*)* Transmission efficiency (~.97) 
solar_efficiency = 0.05 #Thumbrule - Only get 1/20th of rated solar over time
cell_rating = 105e-3 #Kilowatts per m^2 (typically ranges from 10-15 W/ft^2 or 105- 160 W / m^2)
BatteryDischargeRate = 150 #Amps over 24 hours
CellVoltage = 2 #Volts
CellVolume = .09 #m^3
CellWeight = 512 / 2.2 #kg
BatteryCellOutput = BatteryDischargeRate*CellVoltage*1e-3 #Kilowatts


def solar(P2=2.0, P5=20.0, HotelLoads = 5):
    Power2 = P2/total_propulsive_efficiency + HotelLoads
    Power5 = P5/total_propulsive_efficiency + HotelLoads
    solar_area = (Power2 / solar_efficiency) / cell_rating
    print('Design requires ', round(solar_area,2), 'm^2 of solar panels')

    PowerDelta = Power5 - Power2
    number_of_cells = math.ceil(PowerDelta / BatteryCellOutput)
    volume_of_cells = number_of_cells * CellVolume
    weight_of_cells = number_of_cells * CellWeight
    number_of_powerwalls = math.ceil(PowerDelta/5.0)
    volume_of_powerwalls = number_of_powerwalls*0.12763275
    weight_of_powerwalls = number_of_powerwalls*114

    print('Design requires', round(PowerDelta,2), 'kw of additional capacity.')
    print('With SVRLA Batteries, this means', number_of_cells, 'battery cells, taking up', round(volume_of_cells,2), 'm^3')
    print('and weighing', round(weight_of_cells,2), ' kg.')
    print('With Lithium Ion Powerwall, this means', number_of_powerwalls, "Powerwalls, taking up", volume_of_powerwalls, 'm^3')
    print('and weighing', weight_of_powerwalls, 'kg.')

solar()