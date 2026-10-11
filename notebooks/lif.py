import numpy as np

def simulate_lif(
    time, 
    current,
    v0, 
    e_l, 
    r_m, 
    c_m,
    v_threshold, 
    v_reset, 
    t_refractory):


    """
    Simulate a leaky integrate-and-fire neuron using forward Euler.

    Inputs use SI units: seconds, amperes, volts, ohms, and farads.
    time and current must be matching one-dimensional arrays.
    time must be strictly increasing and uniformly spaced.
    The initial voltage is assumed to be below threshold.

    current[i] drives the interval from time[i] to time[i + 1].
    Threshold crossings are detected at time-grid endpoints.
    After a spike, voltage resets and remains fixed during refractoriness.
    Refractory release occurs at the first grid point at or after expiry.

    Returns:
    v : numpy array
        Membrane voltage at each time sample, in volts.
    spike_times : numpy array
        Detected spike times, in seconds.
    """


    parameters = [
        v0, e_l, r_m, c_m,
        v_threshold, v_reset, t_refractory
    ]

    if not np.all(np.isfinite(parameters)):
        raise ValueError("Model parameters must be finite.")

    if r_m <= 0 or c_m <= 0:
        raise ValueError("Resistance and capacitance must be positive.")

    if t_refractory < 0:
        raise ValueError("The refractory period cannot be negative.")

    if v_reset >= v_threshold:
        raise ValueError("Reset voltage must be below threshold.")



    tau = r_m * c_m



    time = np.asarray(time, dtype=float)
    current = np.asarray(current, dtype=float)

    if time.ndim != 1 or current.ndim != 1:
        raise ValueError("time and current must be one-dimensional.")

    if time.size < 2:
        raise ValueError("time must contain at least two samples.")

    if current.shape != time.shape:
        raise ValueError("time and current must have the same length.")

    if not np.all(np.isfinite(time)) or not np.all(np.isfinite(current)):
        raise ValueError("time and current must contain finite values.")

    steps = np.diff(time)
    dt = steps[0]

    if np.any(steps <= 0) or not np.allclose(steps, dt, rtol=1e-7, atol=0.0):
        raise ValueError("time must be increasing and uniformly spaced.")
    

    
    v = np.empty_like(time)
    v[0] = v0

    spike_times = []
    refractory_until = time[0]
    for i in range(time.shape[0] - 1):

        if time[i] < refractory_until:
            v[i+1] = v[i]
            continue

        dvdt = (-(v[i] - e_l) / tau + current[i] / c_m)
        v[i+1] = v[i] + dt * dvdt

        if v[i+1] >= v_threshold:
            v[i+1] = v_reset
            spike_times.append(time[i+1])
            refractory_until = time[i+1] + t_refractory

    spike_times = np.array(spike_times)

    return v, spike_times