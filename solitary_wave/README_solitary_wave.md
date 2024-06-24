# Solitary wave

Author: WaveHello
Date: 06/21/2024

# Information on the code

solitary_wave_analytical.ipynb
-------------------------------------

Initial analytical solution for the model. Is used to generate the boundary conditions for the xBeach model

NOTE: In wbctype = ts_nonh mode, the surface elevation input is the pertubation from the zs0 value. It is not the actual surface elevation.

 solitary_wave_compare_analy_xBeach.ipynb
-------------------------------------

Compares the analytical solution to the xBeach model.

1_sol_wave_nx_16000_tstop_250_CFL_075\solitary_wave_run_model.ipynb
-------------------------------------

Generates the boundary conditions and runs the ```1_sol_wave_nx_16000_tstop_250_CFL_075``` xBeach model


2_sol_wave_nx_16000_tstop_250_CFL_075_2_layer\solitary_wave_run_model.ipynb
-------------------------------------

Generates the boundary conditions and runs the ```2_sol_wave_nx_16000_tstop_250_CFL_075_2_layer``` xBeach model


# Info on the models

1_sol_wave_nx_16000_tstop_250_CFL_075
-------------------------------------

Solitary wave model with usual depth averaged model.

2_sol_wave_nx_16000_tstop_250_CFL_075_2_layer
-------------------------------------

Solitary wave model with pseudo-two layer xBeach model.




