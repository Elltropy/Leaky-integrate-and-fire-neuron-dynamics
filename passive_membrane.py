import numpy as np 
import matplotlib.pyplot as plt 

# c_m * dv/dt = i0 - g_l(v - e_l)
# tau * dv/dt = i0 * r_m - v + e_l

e_l = -65e-3   # V
v0  = -65e-3   # V
r_m = 100e6    # ohm
c_m = 200e-12  # F
i0  = 100e-12  # A

t = np.linspace(0, 0.1, 500)  # seconds


def passive_voltage(t, v0, i0, e_l, r_m, c_m):
    tau = r_m * c_m
    v_inf = e_l + r_m * i0
    v = v_inf + (v0 - v_inf) * np.exp(-t/tau)
    return v, v_inf, tau


y, v_inf, tau = passive_voltage(t, v0, i0, e_l, r_m, c_m)

def f(v, v_inf, tau):
    dvdt = -(v - v_inf)/tau
    return dvdt


v = np.linspace(-45, -65, 25)
t_field = np.linspace(0, 100, 25)
V, T = np.meshgrid(v, t_field)

X = np.ones_like(V)
Y = f(V, v_inf * 1e3, tau * 1e3)
N = np.sqrt(X**2 + Y**2)
X = X/N
Y = Y/N

#plt.figure()
#plt.quiver(T, V, X, Y, scale_units = 'xy', angles = 'xy', scale = 0.38)
#plt.xlim(0, 100)
#plt.ylim(-65, -45)
#plt.xlabel('Time (ms)')
#plt.ylabel('Membrane potential (mV)')
#plt.grid(alpha = 0.3)
#plt.plot(t * 1e3, y * 1e3)
#plt.show()


plt.figure()
errors = []
#dts = np.array([1e-3, 0.5e-3, 0.1e-3, 0.05e-3, 0.01e-3])
dts = np.array([10, 20, 30, 40, 45]) * 1e-3
for dt in dts:      
    t_end = 0.3   
    t = np.arange(0, t_end + dt, dt)

    vv = np.empty_like(t)
    vv[0] = v0

    for i in range(t.shape[0] - 1):
        dvdt = f(vv[i], v_inf, tau)
        vv[i+1] = vv[i] + dvdt * dt

    yy, v_inf, tau = passive_voltage(t, v0, i0, e_l, r_m, c_m)

    plt.plot(t * 1e3, vv * 1e3, marker='o', label=f'dt = {dt * 1e3} ms')

    #plt.figure()
    #plt.plot(t * 1e3, vv * 1e3, '--', label = 'Euler, dt = 1 ms')
    #plt.plot(t * 1e3, yy * 1e3, label = 'Analytical')
    #plt.show()

    max_er = np.max(np.abs(yy - vv))
    errors.append(float(max_er * 1e3))
plt.axhline(v_inf * 1e3, linestyle = '--', color = "#267E99")
plt.xlabel('Time (ms)')
plt.ylabel('Membrane potential (mV)')
plt.grid(alpha=0.3)
plt.legend()
plt.show()

er = np.array(errors)
slope, intercept = np.polyfit(np.log(dts), np.log(er), 1)

k = np.exp(intercept)
er_estm = k * (dts)**slope

#print(np.mean(np.abs(er - er_estm)))
#plt.loglog(dts, er)
#plt.show()

