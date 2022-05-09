import math
from Helpers import convert_ms_kmt, convert_kmt_ms

class Gearbox:
    def __init__(self):
        self.gears = {
        '1': 9.16, '2': 7.33,
        '3': 5.82, '4': 4.66,
        '5LO': 3.75, '5HI': 3.00,
        '6LO': 2.44, '6HI': 1.96,
        '7LO': 1.55, '7HI': 1.24,
        '8LO': 1.00, '8HI': 0.80,
    }

    def getGearRatio(self, gear):
        return self.gears[gear]

    def getGearList(self):
        return list(self.gears.values())

    def getGearRange(self, GR):
        return {
            # 0.00: [0, 90],
            9.16: [0, 22.5],
            7.33: [0, 33.7],
            5.82: [7.5, 45],
            4.66: [15, 50.6],
            3.75: [22.5, 56.3],
            3.00: [30, 61.9],
            2.44: [37.5, 67.5],
            1.96: [45, 73.1],
            1.55: [52.5, 78.8],
            1.24: [60, 84.4],
            1.00: [67.5, 90],
            0.80: [75, 90],
        }[GR]

    def getGearName(self, GR):
        return {
            9.16: '1',
            7.33: '2',
            5.82: '3',
            4.66: '4',
            3.75: '5LO',
            3.00: '5HI',
            2.44: '6LO',
            1.96: '6HI',
            1.55: '7LO',
            1.24: '7HI',
            1.00: '8LO',
            0.80: '8HI',
        }[GR]

    def gearCheck(self, V0, GR):
        kmt = convert_ms_kmt(V0)
        range_list = self.getGearRange(GR)

        return kmt > range_list[0] and range_list[1] >= kmt

    def gearUP(self, GR):
        gears = self.getGearList()
        index = gears.index(GR)
        if index < len(gears)-1:
            return gears[index+1]
        return gears[index]

    def gearDOWN(self, GR):
        gears = self.getGearList()
        index = gears.index(GR)
        if index > 0:
            return gears[index-1]
        return gears[index]


class TruckR580:
    def __init__(self, mass, AR, Wr, V0, name, GR):
        self.DR = 3.42  # Differential ratio
        self.TE = 0.7   # Transmission efficiency (Value is guessed)
        self.ET = 2950  # Engine torque

        self.mass = mass
        self.AR = AR    # Weight distribution ratio over drive axle(s)
        self.Wr = Wr    # Wheel radius

        self.V = V0     # Current velocity
        self.a = 0      # Acceleration
        self.gearbox = Gearbox()

        # Data collecting
        self.V0 = V0    # Initial velocity
        self.GR = GR    # Gear ratio
        self.name = name
        self.velocities = [convert_ms_kmt(V0)]
        self.distances = [0]
        self.GRS = [GR]

    def getEngineForce(self):
        # GR = Gear ratio
        return (self.DR * self.TE * self.ET * self.GR) / self.Wr

    def getDZ(self):
        return -(math.pow(self.V0, 2))/(2*self.a)

    def getDGR(self, gearTime):
        return ((2*self.V0 + self.a*gearTime)*gearTime)/2

    def setVelocity(self, DS, Vlimit):
        self.V = min(math.sqrt(pow(self.V0, 2) + 2*self.a*DS), Vlimit + convert_kmt_ms(10))
        self.V0 = self.V

    def setAcceleration(self, F):
        self.a = F/self.mass

    def reset(self, V0, GR, name):
        self.velocities = [convert_ms_kmt(V0)]
        self.distances = [0]
        self.GRS = [GR]
        self.V0 = V0
        self.GR = GR
        self.name = name

    def gearCheck(self):
        kmt = convert_ms_kmt(self.V)
        range_list = {
            9.16: [0, 22.5],
            7.33: [0, 33.7],
            5.82: [7.5, 45],
            4.66: [15, 50.6],
            3.75: [22.5, 56.3],
            3.00: [30, 61.9],
            2.44: [37.5, 67.5],
            1.96: [45, 73.1],
            1.55: [52.5, 78.8],
            1.24: [60, 84.4],
            1.00: [67.5, 90],
            0.80: [75, 90],
        }[self.GR]
        return kmt > range_list[0] and range_list[1] >= kmt