# Leaky Integrate-and-Fire Neuron Dynamics

A computational study of the leaky integrate-and-fire (LIF) neuron, from the passive membrane equation to spiking, firing-rate predictions, and responses to finite current pulses.

The project combines analytical derivations, forward Euler simulation, numerical validation, and parameter experiments.

## Model

Between spikes, the membrane voltage follows:

$$
-\frac{V-E_L}{R_m}+I(t).
$$

When voltage reaches threshold, a spike event is recorded and voltage resets to $$ V_{\mathrm{reset}}$$. During the absolute refractory period, voltage remains at reset.

The simulator uses SI units. Figures display time in milliseconds (ms), voltage in millivolts (mV), and current in picoamperes (pA).

## Notebooks

| Notebook | Main topic |
|---|---|
| [01  Passive membrane](notebooks/01_passive_membrane.ipynb) | Passive membrane dynamics, Analytical solution, Euler simulation and stability.|
| [02  Threshold and reset](notebooks/02_lif_threshold_reset.ipynb) | LIF Threshold, Reset, and Refractory Dynamics, Rheobase Current, Spike time and Frequency.|
| [03  F–I curve](notebooks/03_fi_curve.ipynb) | Rate–Current (F–I) Curve, Analytical presentation and Numerical validation |
| [04  Parameter sensitivity](notebooks/04_parameter_sensitivity.ipynb) | Parameter Sensitivity of the LIF Neuron, capacitance, resistance, and refractory duration |
| [05  Time-dependent input](notebooks/05_time_dependent_input.ipynb) | Finite current pulses, Pulse duration and spike counts |

The reusable numerical simulator is in `notebooks/lif.py`. Its automated tests are in `notebooks/test_lif.py`.

## Main results

For $$R_m=100\,\mathrm{M\Omega}$$, $$C_m=200\,\mathrm{pF}$$, $$E_L=V_{\mathrm{reset}}=-65\,\mathrm{mV}$$, and $$V_{\mathrm{threshold}}=-50\,\mathrm{mV}$$:

- The membrane time constant is **20 ms**, and rheobase is **150 pA**.
- Passive Euler simulations show approximately first-order convergence as the time step decreases.
- The F–I comparison at a **0.1 ms** time step over **2 s** gives a mean absolute error of **0.0929 Hz** and a maximum absolute error of **0.8188 Hz** across the tested currents.
- With a **2 ms** refractory period, the analytical high-current firing-rate limit is **500 Hz**.
- At **200 pA** with a **2 ms** refractory period, pulse durations of **20, 40, 85, and 150 ms** produce **0, 1, 2, and 5 spikes**, matching the analytical counts.

Notebook 2 also demonstrates a longer **20 ms** refractory period.

## Run the project

Clone the repository and install its dependencies:

```bash
git clone https://github.com/Elltropy/Leaky-integrate-and-fire-neuron-dynamics.git
cd Leaky-integrate-and-fire-neuron-dynamics
python -m pip install -r requirements.txt
python -m jupyterlab
```

Open the notebooks in numerical order. Each notebook should run independently from a fresh kernel.

Run the automated tests from the repository root:

```bash
python notebooks/test_lif.py
```

The tests cover resting behavior, subthreshold charging against the analytical solution, spike timing and refractory holding, and selected invalid inputs.

## Limitations

LIF represents spikes as threshold events followed by reset; it does not reproduce action-potential waveforms or voltage-dependent ion-channel dynamics.

Forward Euler introduces discretization error. Threshold detection and refractory release occur on the time grid, so spike times and firing rates depend on the chosen time step. The analytical constant-current predictions assume fixed model parameters.














# Leaky Integrate-and-Fire Neuron Dynamics

A computational study of the leaky integrate-and-fire (LIF) neuron, from the passive membrane equation to spiking, firing-rate predictions, and responses to finite current pulses.

The project combines analytical derivations, forward Euler simulation, numerical validation, and parameter experiments.

## Model

Between spikes, the membrane voltage follows:

-\frac{V-E_L}{R_m}+I(t).
$$

When voltage reaches threshold, a spike event is recorded and voltage resets to (V\_{\mathrm{reset}}). During the absolute refractory period, voltage remains at reset.

The simulator uses SI units internally. Figures display time in milliseconds, voltage in millivolts, and current in picoamperes.

## Notebooks

| Notebook                                                               | Main topic                                                  |
| ---------------------------------------------------------------------- | ----------------------------------------------------------- |
| [01 — Passive membrane](notebooks/01_passive_membrane.ipynb)           | Analytical solution, Euler convergence, and stability       |
| [02 — Threshold and reset](notebooks/02_lif_threshold_reset.ipynb)     | Spike timing, reset, refractoriness, and rheobase           |
| [03 — F–I curve](notebooks/03_fi_curve.ipynb)                          | Analytical and numerical firing-rate comparison             |
| [04 — Parameter sensitivity](notebooks/04_parameter_sensitivity.ipynb) | Effects of capacitance, resistance, and refractory duration |
| [05 — Time-dependent input](notebooks/05_time_dependent_input.ipynb)   | Finite pulses, charging and relaxation, and spike counts    |

The reusable numerical simulator is in `notebooks/lif.py`. Its automated tests are in `notebooks/test_lif.py`.

## Main results

For (R_m=100,\mathrm{M\Omega}), (C_m=200,\mathrm{pF}), (E_L=V\_{\mathrm{reset}}=-65,\mathrm{mV}), and (V\_{\mathrm{threshold}}=-50,\mathrm{mV}):

- The membrane time constant is **20 ms**, and rheobase is **150 pA**.
- Passive Euler simulations show approximately first-order convergence as the time step decreases.
- The F–I comparison at a **0.1 ms** time step over **2 s** gives a mean absolute error of **0.0929 Hz** and a maximum absolute error of **0.8188 Hz** across the tested currents.
- With a **2 ms** refractory period, the analytical high-current firing-rate limit is **500 Hz**.
- At **200 pA** with a **2 ms** refractory period, pulse durations of **20, 40, 85, and 150 ms** produce **0, 1, 2, and 5 spikes**, matching the analytical counts.

Notebook 2 also demonstrates a longer **20 ms** refractory period.

## Run the project

Clone the repository and install its dependencies:

```bash
git clone https://github.com/Elltropy/Leaky-integrate-and-fire-neuron-dynamics.git
cd Leaky-integrate-and-fire-neuron-dynamics
python -m pip install -r requirements.txt
python -m jupyterlab
```

Open the notebooks in numerical order. Each notebook should run independently from a fresh kernel.

Run the automated tests from the repository root:

```bash
python notebooks/test_lif.py
```

The tests cover resting behavior, subthreshold charging against the analytical solution, spike timing and refractory holding, and selected invalid inputs.

## Limitations

LIF represents spikes as threshold events followed by reset; it does not reproduce action-potential waveforms or voltage-dependent ion-channel dynamics.

Forward Euler introduces discretization error. Threshold detection and refractory release occur on the time grid, so spike times and firing rates depend on the chosen time step. The analytical constant-current predictions assume fixed model parameters.
