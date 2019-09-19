CFL3D
=
A structured-grid, cell-centered, upwind-biased, Reynolds-averaged Navier-Stokes (RANS) code



## Description

Originally Developed by NASA Langley Computation Fluid Lab (CFL). It can be run in parallel on multiple grid zones with point-matched, patched, overset, or embedded connectivities. Both multigrid and mesh sequencing are available in time-accurate or steady-state modes.
The most up-to-date information can be found on the web at: https://cfl3d.larc.nasa.gov.

Copyright 2001 United States Government as represented by the Administrator of the National Aeronautics and Space Administration. All Rights Reserved.

Based on the CFL3D 6.7.0, this repository continue to develop some useful features to facilitate its applications. All rights Reserved.

The CFL3D platform is licensed under the Apache License, Version 2.0 (the "LICENSE"); you may not use this file except in compliance with the LICENSE. You may obtain a copy of the LICENSE at http://www.apache.org/licenses/LICENSE-2.0. Unless required by applicable law or agreed to in writing, software distributed under the LICENSE is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the LICENSE for the specific language governing permissions and limitations under the License.



## Develop-Release Note

#### CFL3D 6.7.2
- [x] Added some bash files to facilitate the installation under Linux
#### CFL3D 6.7.1
- [x] To facilitate the ICEM-CFL3D workflow, the formatted 'cfl3d.grd' mesh file format is dropped, instead unformated 'cfl3d.xyz' is used. (Modified source/cfl3d/dist/main.F Line 548)
#### CFL3D 6.7.0
- [x] Original version inherited from NASA CFL3D opensource version

