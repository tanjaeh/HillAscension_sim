import xlrd
from Helpers import convert_kmt_ms, convert_ms_kmt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Environment:
    def __init__(self, name):
        self.name = name
        self.g = 9.81

        self.gradient = []
        self.angle = []
        self.fric = []
        self.DS = []
        self.Vlimit = []


        # Gets excel file
        wb = xlrd.open_workbook('Environments.xlsx')
        lines = 0
        index = -1

        if name == "TB_1":
            lines = 1
            index = 0
        elif name == "TB_2":
            lines = 5
            index = 1
        elif name == "TB_3":
            lines = 10
            index = 2

        sheet = wb.sheet_by_index(index)
        i = 0
        while (i < lines):
            self.gradient.append(sheet.cell_value(1 + i, 0))# gradient %
            self.angle.append(sheet.cell_value(1 + i, 1) )  # Angle degrees
            self.fric.append(sheet.cell_value(1 + i, 2))    # Friction coefficient
            self.DS.append(sheet.cell_value(1 + i, 3))      # State distance
            self.Vlimit.append(convert_kmt_ms(sheet.cell_value(1 + i, 4)))  # Speed limit m/s

            i = i+1

    def printTable(self):
        fig, ax = plt.subplots()

        # hide axes
        fig.patch.set_visible(False)
        ax.axis('off')
        ax.axis('tight')

        # Data setup
        distance = [0]
        for ds in self.DS:
            distance.append(distance[len(distance)-1] + ds)

        data = [self.gradient, self.angle, self.fric, distance[1:], [convert_ms_kmt(vlim) for vlim in self.Vlimit]]
        data2 = np.transpose(data)


        df = pd.DataFrame(np.array(data2).round(2), columns=['Gradient', 'Angle', 'Friction coefficient', 'DS', 'Vlimit'])
        df.round(2)

        ax.table(cellText=df.values, colLabels=df.columns, loc='center')

        fig.tight_layout()

        plt.savefig('EnvTable\ ' + self.name,
                    bbox_inches='tight',
                    dpi=500)

        plt.show()
