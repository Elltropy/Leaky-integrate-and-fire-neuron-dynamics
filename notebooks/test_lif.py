import numpy as np 
from lif import simulate_lif

def test_resting_state():
    time = np.arange(0, 0.1, 1e-4)
    current = np.zeros_like(time)
    e_l = -65e-3

    v, spike_times = simulate_lif(
        time=time,
        current=current,
        v0=e_l,
        e_l=e_l,
        r_m=100e6,
        c_m=200e-12,
        v_threshold=-50e-3,
        v_reset=e_l,
        t_refractory=2e-3
    )

    np.testing.assert_allclose(v, e_l, rtol=0, atol=1e-12)
    assert spike_times.size == 0


def test_subthreshold_charging():
    time = np.arange(0, 0.1, 1e-4)
    i0 = 100e-12
    current = np.full_like(time, i0)

    e_l = -65e-3
    r_m = 100e6
    c_m = 200e-12

    v, spike_times = simulate_lif(
        time=time,
        current=current,
        v0=e_l,
        e_l=e_l,
        r_m=r_m,
        c_m=c_m,
        v_threshold=-50e-3,
        v_reset=e_l,
        t_refractory=2e-3
    )

    tau = r_m * c_m
    v_inf = e_l + r_m * i0
    expected = v_inf + (e_l - v_inf) * np.exp(-time / tau)

    np.testing.assert_allclose(v, expected, rtol=0, atol=1e-5)
    assert spike_times.size == 0


def test_spiking_and_refractory():
    time = np.arange(0, 0.1, 1e-4)
    i0 = 200e-12
    current = np.full_like(time, i0)

    e_l = -65e-3
    r_m = 100e6
    c_m = 200e-12

    v_reset = e_l
    v_threshold = -50e-3
    t_refractory = 2e-3

    v, spike_times = simulate_lif(
        time=time,
        current=current,
        v0=e_l,
        e_l=e_l,
        r_m=r_m,
        c_m=c_m,
        v_threshold=v_threshold,
        v_reset=v_reset,
        t_refractory=t_refractory
    )


    assert spike_times.size >= 2

    for spike_time in spike_times:
        refractory_mask = (
            (time >= spike_time)
            & (time < spike_time + t_refractory)
        )

        np.testing.assert_allclose(
            v[refractory_mask],
            v_reset,
            rtol=0,
            atol=1e-12
        )



    tau = r_m * c_m
    v_inf = e_l + r_m * i0

    dt = time[1] - time[0]

    expected_charge_time = tau * np.log(
        (v_inf - e_l) / (v_inf - v_threshold)
    )
    expected_interval = t_refractory + tau * np.log(
        (v_inf - v_reset) / (v_inf - v_threshold)
    )

    np.testing.assert_allclose(
        spike_times[0] - time[0],
        expected_charge_time,
        rtol=0,
        atol=dt
    )

    np.testing.assert_allclose(
        np.diff(spike_times),
        expected_interval,
        rtol=0,
        atol=2 * dt
    )


def test_invalid_inputs():
    time = np.arange(0, 0.1, 1e-4)
    current = np.zeros_like(time)

    valid_inputs = dict(
        time=time,
        current=current,
        v0=-65e-3,
        e_l=-65e-3,
        r_m=100e6,
        c_m=200e-12,
        v_threshold=-50e-3,
        v_reset=-65e-3,
        t_refractory=2e-3
    )

    invalid_cases = [
        {"current": current[:-1]},
        {
            "time": np.array([0, 1e-4, 3e-4]),
            "current": np.zeros(3)
        },
        {"c_m": 0},
        {"t_refractory": -1e-3},
        {"v_reset": -50e-3}
    ]

    for case in invalid_cases:
        inputs = valid_inputs.copy()
        inputs.update(case)

        with np.testing.assert_raises(ValueError):
            simulate_lif(**inputs)




if __name__ == "__main__":
    test_resting_state()
    test_subthreshold_charging()
    test_spiking_and_refractory()
    test_invalid_inputs()
    print("All four tests passed.")