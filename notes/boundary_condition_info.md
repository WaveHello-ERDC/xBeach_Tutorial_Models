# Info on the boundary conditions from xBeach


## Flow Boundary Conditions

The labels in this section are: 
  --------------------------------
Flow boundary condition parameters:
* front    =  nonh_1d 
* left     =  neumann
* right    =  neumann
* back     =  abs_1d
* ARC      =  1       # Activate Reflection Compensation - Switch for active reflection compensation at seaward boundary. This should be on for nonh
* order    =  1.0000  # Controls if first or second order waves are on the boundary - Not sure how this interfaces with nonh
* highcomp =  0 (no record found, default value used)
* freewave =  0 (no record found, default value used)
* epsi =  -1.0000 (no record found, default value used)
* tidetype =  velocity (no record found, default value used)

<!-- Tables that define the flow conditions -->
<img src="boundary_condition_images\front_flow_boun_cond_table.png" alt="Open file image" style="width:600px; height:200px; display: block; margin-left: auto; margin-right: auto;" />

<img src="boundary_condition_images\back_flow_boun_cond_table.png" alt="Open file image" style="width:600px; height:200px; display: block; margin-left: auto; margin-right: auto;" />

<img src="boundary_condition_images\leftright_flow_boun_cond_table.png" alt="Open file image" style="width:600px; height:175px; display: block; margin-left: auto; margin-right: auto;" />

### NOTE: :warning: The wlevel option is deprecated :warning:

## Wave boundary conditions

#### wbctype Options
1) params
2) parametric
3) swan
4) vardens
5) off
6) jonstable
7) reuse
8) ts_1
9) ts_2
10) **ts_nonh**: This is the mode that should be used with nonh models and requres the boun_U.bcf file
