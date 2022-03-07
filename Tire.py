import pybullet as p


class Tire:
    def __init__(self, mass, radius, width, pos):
        self.mass = mass
        self.radius = radius
        self.width = width
        self.pos = pos


class TireList:
    def __init__(self, tires):
        self.masses = []
        self.collisionShapeIndices = []
        self.visualShapeIndices = []
        self.positions = []
        self.orientations = []
        self.inertialFramePositions = []
        self.inertialFrameOrientations = []
        self.indices = []
        self.jointTypes = []
        self.axis = []

        self.set_parameters(tires)

    def set_parameters(self, tires):
        vsi = 1  # visualShapeIndices
        tireOrientation = [1, 0, 0, 1]

        for tire in tires:
            self.masses.append(tire.mass)
            self.collisionShapeIndices.append(
                p.createCollisionShape(p.GEOM_CYLINDER, height=tire.width, radius=tire.radius))
            self.visualShapeIndices.append(vsi)
            vsi = vsi + 1
            self.positions.append(tire.pos)
            self.orientations.append(tireOrientation)
            self.inertialFramePositions.append([0, 0, 0])
            self.inertialFrameOrientations.append([0, 0, 0, 1])
            self.indices.append(0)
            self.jointTypes.append(p.JOINT_REVOLUTE)
            self.axis.append([0, 0, 1])
