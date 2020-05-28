import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

def compute_rotation_matrix(angle):
    rotation = np.zeros((2,2))

    rotation[0,0] = np.cos(angle)
    rotation[0,1] = -np.sin(angle)
    rotation[1,0] = np.sin(angle)
    rotation[1,1] = np.cos(angle)

    return rotation



print("---------------------------------------------------- Start")
print("Point definitions")
a_0 = np.array([0,        0])
b_0 = np.array([62.5,     0])
c_0 = np.array([350,      0])
d_0 = np.array([350,     50])
e_0 = np.array([62.5, -62.5])
f_0 = np.array([56,    -374])

print("Define froces in points")
force_d = np.array([0, 85*1.6*9.81])

print("Define discretization")
num_steps = 50
angle = np.linspace(0,3.14*0.55,num_steps)

force_e = np.zeros((num_steps, 2))

for i, alpha in enumerate(angle):
    rotation = compute_rotation_matrix(alpha)

    d = rotation.dot(d_0)
    e = rotation.dot(e_0)
    e_unit = e /  np.linalg.norm(e)
	
    fe = e - f_0
    fe_unit = fe /  np.linalg.norm(fe)
 
    sin_theta = np.cross(e_unit, fe_unit)

    force_e_norm = (np.cross(d,force_d))/ (np.linalg.norm(e)*sin_theta)
    force_e[i] =force_e_norm * fe_unit


# Plot force by components X and Y at point e
"""plt.rc('text', usetex=True)
plt.rc('font', family='serif')
fig, ax1 = plt.subplots()
plt.plot(angle, force_e[:,0], label='x')
plt.plot(angle, force_e[:,1], label='y')
ax1.set_ylabel(r'Force N')
ax1.set_xlabel(r'Angle in rad')
plt.legend()
plt.show()
"""

# Start animation
fig2, ax = plt.subplots()
#ax.set_xlim(np.min(force_e[:,1]), np.max(force_e[:,1]))
#ax.set_ylim(np.min(force_e[:,1]), np.max(force_e[:,1]))
ax.set_xlim(-300, 300)
ax.set_ylim(-300, 300)
angle_template = r'angle = %.3f $^\circ$'
angle_text = ax.text(0.75, 0.9, '', transform=ax.transAxes)

xdata = np.zeros((1,2))
ydata = np.zeros((1,2))
line_force_e, = plt.plot([], [], '-r')

data = np.zeros((2,5))
body, = plt.plot([], [], '-r')

def init():
    #line.set_data([],[])
    line_force_e.set_data([],[])
    angle_text.set_text('')
    return line_force_e, angle_text

def update(i):

    data[0,0] =(compute_rotation_matrix(angle[i]).dot(a_0))[0]
    data[0,1] =(compute_rotation_matrix(angle[i]).dot(d_0))[0]
    data[0,2] =(compute_rotation_matrix(angle[i]).dot(c_0))[0]
    data[0,3] =(compute_rotation_matrix(angle[i]).dot(e_0))[0]
    data[0,4] =(compute_rotation_matrix(angle[i]).dot(a_0))[0]

    data[1,0] =(compute_rotation_matrix(angle[i]).dot(a_0))[1]
    data[1,1] =(compute_rotation_matrix(angle[i]).dot(d_0))[1]
    data[1,2] =(compute_rotation_matrix(angle[i]).dot(c_0))[1]
    data[1,3] =(compute_rotation_matrix(angle[i]).dot(e_0))[1]
    data[1,4] =(compute_rotation_matrix(angle[i]).dot(a_0))[1]

    body.set_data(data[0], data[1])
 
    xdata[0,1] = force_e[i,0]
    ydata[0,1] = force_e[i,1]
    #line_force_e.set_data(xdata, ydata)

    angle_text.set_text(angle_template % np.degrees(angle[i]))
    return line_force_e,

ani = FuncAnimation(fig2, update, num_steps,
                    init_func=init, blit=False)
plt.show()

