from Truck_R580 import TruckR580
from Environment import Environment
from Helpers import  convert_kmt_ms, convert_ms_kmt
from Simulation import simulation, simulation_with_forced_gearing
from Graph import Graph

# Truck variables
Wr = 0.522
AR_6x4 = 2/6
AR_6x2 = 1/6
truckMass = 40000

# Gearing variables
gearing_time = 2

# Setup environ
TB_1 = Environment("TB_1")
TB_2 = Environment("TB_2")
TB_3 = Environment("TB_3")
envs = [TB_1, TB_2, TB_3]
# envs = [TB_3]


# Setup truck
R580_6x4 = TruckR580(truckMass, AR_6x4, Wr, 0, "R580_6x4", 0)
R580_6x2 = TruckR580(truckMass, AR_6x2, Wr, 0, "R580_6x2", 0)


def getTestVeloities(vlim):
    # Returns V0's in m/s
    _5 = convert_kmt_ms(5)
    _10 = convert_kmt_ms(10)

    return [vlim - _10, vlim - _5, vlim, vlim +_5, vlim + _10]

for env in envs:
    env.printTable()
    graph_6x2_env = Graph()
    graph_6x4_env = Graph()
    graph_6x2_gearing_env = Graph()
    graph_6x4_gearing_env = Graph()

    for V0 in getTestVeloities(env.Vlimit[0]):
    # for V0 in [convert_kmt_ms(40)]:
        graph_6x2 = Graph()
        graph_6x4 = Graph()
        graph_6x2_gearing = Graph()
        graph_6x4_gearing = Graph()

        for gear in R580_6x2.gearbox.getGearList():
            if R580_6x2.gearbox.gearCheck(V0, gear):
                R580_6x2.reset(V0, gear, "R580_6x2_GR" + str(R580_6x2.gearbox.getGearName(gear)))
                R580_6x4.reset(V0, gear, "R580_6x4_GR" + str(R580_6x4.gearbox.getGearName(gear)))
                # Run simulation without gearing
                simulation(R580_6x2, env)
                simulation(R580_6x4, env)
                # Collect data for graphs
                graph_6x2.collect_data(R580_6x2)
                graph_6x4.collect_data(R580_6x4)

                graph_6x2_env.collect_data(R580_6x2)
                graph_6x4_env.collect_data(R580_6x4)


                # Saving tot distance of env before resetting the trucks
                gearing_distance = R580_6x2.distances[len(R580_6x2.distances)-1] * 0.5
                R580_6x2.reset(V0, gear, "R580_6x2_GR" + str(R580_6x2.gearbox.getGearName(gear)))
                R580_6x4.reset(V0, gear, "R580_6x4_GR" + str(R580_6x4.gearbox.getGearName(gear)))
                # Run simulation with gearing
                newGR = R580_6x2.gearbox.gearDOWN(gear)
                simulation_with_forced_gearing(R580_6x2, env, gearing_distance, newGR, gearing_time)
                simulation_with_forced_gearing(R580_6x4, env, gearing_distance, newGR, gearing_time)
                # Collect data for graphs
                graph_6x2_gearing.collect_data(R580_6x2)
                graph_6x4_gearing.collect_data(R580_6x4)

                graph_6x2_gearing_env.collect_data(R580_6x2)
                graph_6x4_gearing_env.collect_data(R580_6x4)

        title = "Velocity. V0: {}. Environment: {}. Truck: ".format(convert_ms_kmt(V0), env.name)
        save_name = "VelocityGraph\V0_{}\Velocity_{}_".format(convert_ms_kmt(V0), env.name)

        graph_6x2.create_graph(title + "6x2", save_name + "6x2")
        graph_6x4.create_graph(title + "6x4", save_name + "6x4")
        graph_6x2_gearing.create_graph(title + "6x2 Forced GR down", save_name + "GearDOWN_6x2")
        graph_6x4_gearing.create_graph(title + "6x4 Forced GR down", save_name + "GearDOWN_6x4")

    title = "Velocity. Environment: {}. Truck: ".format(env.name)
    save_name = "VelocityGraph\Velocity_{}_".format(env.name)

    graph_6x2_env.create_graph(title + "6x2", save_name + "6x2")
    graph_6x4_env.create_graph(title + "6x4", save_name + "6x4")
    graph_6x2_gearing_env.create_graph(title + "6x2 Forced GR down", save_name + "GearDOWN_6x2")
    graph_6x4_gearing_env.create_graph(title + "6x4 Forced GR down", save_name + "GearDOWN_6x4")