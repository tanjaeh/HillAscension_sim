import pybullet as p
import time
import pybullet_data
from Tire import Tire, TireList

# Environment
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.createCollisionShape(p.GEOM_PLANE)
p.createMultiBody(0, 0)

# Trailer sizes (m) Currently a box
trailer_x = 10
trailer_y = 1.6
trailer_z = 2
trailer_mass = 40000  # KG
amount_tires = 6

# Tire size
radius = 0.25
width = 0.3
tire_z = -((trailer_z/2)+radius*1.1)
tire_mass = 5 # KG


visualShapeId = -1

# Creates a sphere
# colSphereId = p.createCollisionShape(p.GEOM_SPHERE, radius=trailer_x) # Creates a sphere
# sphereUid = p.createMultiBody(mass, colSphereId, visualShapeId, basePosition, baseOrientation)

# Creates a box
colBoxId = p.createCollisionShape(p.GEOM_BOX, halfExtents=[trailer_x/2, trailer_y/2, trailer_z/2])
# Creates a cylinder
colCylinderId = p.createCollisionShape(p.GEOM_CYLINDER, height=width, radius=radius)

#Create object
basePosition = [0, 0, 5]
baseOrientation = [0, 0, 0, 1]
tireOrientation = [1, 0, 0, 1]

#Tires
tire_pos = [[5, -0.8, tire_z], [5, 0.8, tire_z],
            [-5, -0.8, tire_z], [-5, 0.8, tire_z],
            [-4, -0.8, tire_z], [-4, 0.8, tire_z]]
tires = []
for pos in tire_pos:
    tires.append( Tire(tire_mass, radius, width, pos) )

link_list = TireList(tires)
link_Masses = link_list.masses
linkCollisionShapeIndices = link_list.collisionShapeIndices
linkVisualShapeIndices = link_list.visualShapeIndices
linkPositions = link_list.positions
linkOrientations = link_list.orientations
linkInertialFramePositions = link_list.inertialFramePositions
linkInertialFrameOrientations = link_list.inertialFrameOrientations
indices = link_list.indices
jointTypes = link_list.jointTypes
axis = link_list.axis


# Multiple parts
# link_Masses = [1, 1]
# linkCollisionShapeIndices = [colCylinderId, colCylinderId]
# linkVisualShapeIndices = [1, 2]
# linkPositions = [[0, 0, tire_z], [5, 0, tire_z]]
# linkOrientations = [tireOrientation, tireOrientation]
# linkInertialFramePositions = [[0, 0, 0], [0, 0, 0]]
# linkInertialFrameOrientations = [[0, 0, 0, 1], [0, 0, 0, 1]]
# indices = [0, 0]
# jointTypes = [p.JOINT_REVOLUTE, p.JOINT_REVOLUTE]
# axis = [[0, 0, 1], [0, 0, 1]]
# cylinderUid = p.createMultiBody(tire_mass, colCylinderId, visualShapeId, basePosition, tireOrientation)

# p.changeDynamics(cylinderUid,
#                  -1,
#                  spinningFriction=0.001,
#                  rollingFriction=0.2,
#                  linearDamping=0.0)

boxUid = p.createMultiBody(trailer_mass,
                           colBoxId,
                           visualShapeId,
                           basePosition,
                           baseOrientation,
                           linkMasses=link_Masses,
                           linkCollisionShapeIndices=linkCollisionShapeIndices,
                           linkVisualShapeIndices=linkVisualShapeIndices,
                           linkPositions=linkPositions,
                           linkOrientations=linkOrientations,
                           linkInertialFramePositions=linkInertialFramePositions,
                           linkInertialFrameOrientations=linkInertialFrameOrientations,
                           linkParentIndices=indices,
                           linkJointTypes=jointTypes,
                           linkJointAxis=axis)

# p.changeDynamics(boxUid,
#                  -1,
#                  spinningFriction=0.001,
#                  rollingFriction=0.2,
#                  linearDamping=0.0)


# for joint in range(p.getNumJoints(sphereUid)):
#     p.setJointMotorControl2(sphereUid, joint, p.VELOCITY_CONTROL, targetVelocity=1, force=10)

p.setGravity(0, 0, -9.81)
p.setRealTimeSimulation(1)

# p.getNumJoints(sphereUid)
# for i in range(p.getNumJoints(sphereUid)):
#   p.getJointInfo(sphereUid, i)

while (1):
  keys = p.getKeyboardEvents()
  # print(keys)

  time.sleep(0.01)