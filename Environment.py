import xlrd

class Enviorment:
    def __init__(self, name):
        self.name = name

        self.angle = []
        self.fric = []
        self.DS = []
        self.Vlimit = []

        # Gets excel file
        wb = xlrd.open_workbook('Enviorments.xlsx')
        lines = 0
        index = -1

        if name == "TB_1":
            lines = 1
            index = 0
        elif name == "TB_2":
            lines = 5
            index = 1

        sheet = wb.sheet_by_index(index)
        i = 0
        while (i < lines):
            self.angle.append(sheet.cell_value(1 + i, 1) )  # Angle degrees
            self.fric.append(sheet.cell_value(1 + i, 2))    # Friction coefficient
            self.DS.append(sheet.cell_value(1 + i, 3))      # State distance

            i = i+1

