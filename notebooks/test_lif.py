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


if __name__ == "__main__":
    test_resting_state()
    test_subthreshold_charging()
    print("Both tests passed.")