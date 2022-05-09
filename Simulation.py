import math
from Truck_R580 import TruckR580
from Helpers import convert_ms_kmt


def force_check(truck, env, part):
    Fg = truck.mass * env.g * math.sin(math.radians(env.angle[part]))
    Ff = truck.mass * env.g * math.cos(math.radians(env.angle[part])) * env.fric[part] * truck.AR
    Fe = truck.getEngineForce()

    return min(Ff, Fe) - Fg


def speed_gain(truck, DS, Vlimit):
    truck.setVelocity(DS, Vlimit)


def speed_reduction(truck, DS, Vlimit):
    DZ = truck.getDZ()
    if (DZ >= DS):
        truck.setVelocity(DS, Vlimit)
    else:
        truck.V = 0
        truck.V0 = 0


def driving(truck, F, D, Vlim):
    truck.setAcceleration(F)

    if F >= 0:
        speed_gain(truck, D, Vlim)
    else:
        speed_reduction(truck, D, Vlim)


def collect_data(truck, D):
    truck.distances.append(truck.distances[len(truck.distances)-1] + D)
    truck.velocities.append(convert_ms_kmt(truck.V))
    truck.GRS.append(truck.GR)


def simulation(truck: TruckR580, env):
    for part in range(len(env.angle)):
        F = force_check(truck, env, part)
        driving(truck, F, env.DS[part], env.Vlimit[part])

        collect_data(truck, env.DS[part])

def simulation_with_forced_gearing(truck: TruckR580, env, gearing_distance, newGR, gearing_time):
    extra_distance = 0

    for part in range(len(env.angle)):
        traveled_D = truck.distances[len(truck.distances)-1]
        if traveled_D <= gearing_distance and gearing_distance < traveled_D + env.DS[part]:
            # Truck will gear during this part
            DG = gearing_distance - traveled_D

            if not traveled_D == gearing_distance:
                # Simulate driving until DG
                F = force_check(truck, env, part)
                driving(truck, F, DG, env.Vlimit[part])
                collect_data(truck, DG)

            # Cluching
            truck.GR = 0.0
            F = force_check(truck, env, part)
            truck.setAcceleration(F)

            DGR = truck.getDGR(gearing_time)
            if DG + DGR > env.DS[part]:
                # Gearing state goes into next part of simulation
                # Simulate to end of this part
                DS_DG = env.DS[part] - DG
                speed_reduction(truck, DS_DG, env.Vlimit[part])
                collect_data(truck, DS_DG)

                # Simulate to end of gearing
                speed_reduction(truck, DGR - DS_DG, env.Vlimit[part])
                truck.GR = newGR
                collect_data(truck, DGR - DS_DG)

                extra_distance = DG + DGR - env.DS[part]
                continue
            else:
                # Simulate to end of gearing
                speed_reduction(truck, DGR, env.Vlimit[part])
                truck.GR = newGR
                collect_data(truck, DGR)

                extra_distance = DG + DGR

        # Simulate to end of part
        DS = env.DS[part] - extra_distance
        extra_distance = 0
        F = force_check(truck, env, part)
        driving(truck, F, DS, env.Vlimit[part])
        collect_data(truck, DS)