import math

P2 = 2 #KW
P5 = 20 #KW
total_propulsive_efficiency = 0.68 #Propulsive efficiency (~.7 for frigate*)* Transmission efficiency (~.97)
HotelLoads = 5 #kw
SprintTime = 240 #Hours

LHV_H2 = 120.21 #MJ/kg
hfc_efficiency = 0.59 #Percent of LHV of H2 delivered as electrical energy by Siemens FCM34
hydrogen_tank_specific_volume = 300.0 / 9.5  #Liters per Kg of hydrogen gas at 500 bar (stored in 300L canisters)
hydrogen_tank_specific_mass = 260.0/300 #Kg of tankage per 300L canister

energy_needed_kwh = ((P5 - P2)/total_propulsive_efficiency + HotelLoads) * SprintTime #Kwhr
energy_needed_MJ = energy_needed_kwh * 3.6 #MJ

hydrogen_mass = (energy_needed_MJ / hfc_efficiency) / LHV_H2 #kg H2 
tank_volume = hydrogen_mass * hydrogen_tank_specific_volume
tank_mass = tank_volume * hydrogen_tank_specific_mass

number_of_tanks = math.ceil(tank_volume / 300)
weight_of_tanks = number_of_tanks * 260 #kg
volume_of_tanks = number_of_tanks * 0.737 #m^3

print('Design requires', energy_needed_kwh, 'kwh of energy.')
print('This requires', hydrogen_mass, 'kg of H2 at 500 bar')
print('contained in', number_of_tanks, ' 300L tanks weighing', weight_of_tanks, 'kg and taking up', volume_of_tanks, 'm^3.')
