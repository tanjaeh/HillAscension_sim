import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from Helpers import convert_kmt_ms
from Truck_R580 import Gearbox

class Graph:
    def __init__(self):
        self.velocities = []
        self.distances = []
        self.truck_names = []
        self.GRS = []

    def collect_data(self, truck):
        self.velocities.append(truck.velocities)
        self.distances.append(truck.distances)
        self.truck_names.append(truck.name)
        self.GRS.append(truck.GRS)

    def get_truck_index_list(self):
        valid_index_list = []
        gearbox = Gearbox()
        for truck_index in range(len(self.velocities)):
            gear_check_results = []
            for index in range(len(self.velocities[truck_index])):
                kmt = self.velocities[truck_index][index]
                GR = self.GRS[truck_index][index + 1] if self.GRS[truck_index][index] == 0 else self.GRS[truck_index][index]

                gear_check_results.append(gearbox.gearCheck(convert_kmt_ms(kmt), GR))

            if all (gear_check_results):
                valid_index_list.append(truck_index)

        return valid_index_list

    def combine_overlapping_graphs(self, index_list):
        for truck_i_1 in index_list:
            for truck_i_2 in index_list:
                if self.truck_names[truck_i_1] == self.truck_names[truck_i_2]\
                        and self.velocities[truck_i_1] == self.velocities[truck_i_2]:
                    continue

                if self.velocities[truck_i_1] == self.velocities[truck_i_2]:
                    self.truck_names[truck_i_1] = self.truck_names[truck_i_1] + self.truck_names[truck_i_2][8:]
                    index_list.remove(truck_i_2)

    def create_graph(self, title, save_name):
        fig, ax = plt.subplots(figsize=(12, 8))
        index_list = self.get_truck_index_list()

        velocity = []
        distance = []
        if index_list:
            self.combine_overlapping_graphs(index_list)
            for index in index_list:
                x = self.distances[index]
                y = self.velocities[index]
                distance.append(self.distances[index])
                velocity.append(self.velocities[index])

                plt.plot(x, y, label=self.truck_names[index])
        else:
            index_list = list(range(0, len(self.velocities), 1))
            self.combine_overlapping_graphs(index_list)
            title = title + "_FAILED"
            save_name = save_name + "_FAILED"
            for index in index_list:
                x = self.distances[index]
                y = self.velocities[index]
                distance.append(self.distances[index])
                velocity.append(self.velocities[index])

                plt.plot(x, y, label=self.truck_names[index])

        max_velocity_list = [max(V) for V in self.velocities]
        plt.ylim(-2, max(max_velocity_list) + 5)

        txt = "{value:.2f}"
        for truck_index in range(len(velocity)):
            for index in range(len(velocity[truck_index])):
                plt.annotate(txt.format(value=velocity[truck_index][index]), xy=(distance[truck_index][index], velocity[truck_index][index]))

        ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        plt.xlabel("Distance [m]")
        plt.ylabel("Velocity [km/t]")

        plt.title(title)
        plt.legend()
        plt.savefig(save_name, bbox_inches='tight', dpi=500)

        plt.show()
