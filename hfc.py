import math

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

print('Design requires', round(energy_needed_kwh(),2), 'kwh of energy.')
print('This requires', round(hydrogen_needed_mass(),2), 'kg of H2 at 500 bar')
print('contained in', number_of_tanks(), ' 300L tanks weighing', round(weight_of_tanks(),2), 'kg and taking up', round(volume_of_tanks(),2), 'm^3.')
