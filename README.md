# HVAC Duct Sizing Calculator

**Version 0.4 — Preliminary HVAC Engineering Calculator**

An open-source Python tool for preliminary HVAC duct sizing, airflow velocity, and duct pressure-loss calculations. Designed as an educational project for MEP engineers and engineering students.

## Features

1. Round duct air velocity calculation
2. Rectangular duct air velocity calculation
3. Automatic round duct sizing
4. Automatic rectangular duct sizing
5. Round duct pressure-loss calculation
6. Rectangular duct pressure-loss calculation

## Pressure-Loss Calculations

The software calculates:

- Duct cross-sectional area and average air velocity
- Hydraulic diameter
- Reynolds number and estimated flow regime
- Darcy friction factor
- Straight duct friction loss using the Darcy–Weisbach equation
- Fitting losses based on a user-provided total K-value
- Total estimated pressure loss in pascals (Pa)

The turbulent friction factor is estimated using the Swamee–Jain approximation. Laminar friction uses 64/Re, while transitional flow uses approximate interpolation. Rectangular duct losses use the simplified hydraulic-diameter method.

## Engineering Assumptions

| Parameter | Value | Unit |
|---|---:|---|
| Air density | 1.20 | kg/m³ |
| Dynamic air viscosity | 1.81 × 10⁻⁵ | Pa·s |
| Absolute duct roughness | 0.15 | mm |
| Fitting loss coefficient | User input | Dimensionless |
| Maximum rectangular aspect ratio for auto-sizing | 4:1 | — |
| Rectangular sizing increments | 50 | mm |

Duct dimensions are assumed to be internal clear dimensions. Available size lists are illustrative and should be verified against actual manufacturers' data.

## How to Run

Requires Python 3. No additional Python packages are required.

1. Open the project in GitHub Codespaces or another Python environment.
2. Open a terminal in the repository folder.
3. Run `python3 duct_calculator.py`.
4. Select a calculation option from 1 to 7.
5. Enter the required calculation values.

## Example — Round Duct Pressure Loss

Inputs:

- Airflow: 1,000 m³/h
- Diameter: 400 mm
- Straight duct length: 20 m
- Total fitting K-value: 1.0

Outputs include duct velocity, Reynolds number, friction factor, straight-duct pressure loss, fitting pressure loss and total estimated pressure loss.

## Limitations and Engineering Disclaimer

**This software is intended for preliminary educational and conceptual engineering calculations only. It is not a certified or validated HVAC design tool.**

All calculated results must be independently verified before use in actual engineering designs, construction documents, equipment selections or safety-critical applications.

The simplified model does not fully represent rectangular duct friction, fitting geometry, different reference velocities, complete duct networks, acoustic requirements, leakage, or all fan-system effects.

Applicable engineering standards, actual material properties, manufacturers' data and project specifications must be considered.

## Future Development

- Version 0.5 — Detailed fitting losses and duct network calculations
- Version 0.6 — Fan pressure and system resistance calculations
- Version 1.0 — Web interface and downloadable calculation reports

## License

MIT License. See the `LICENSE` file for details.

## Project Status

Version 0.4 — Educational development project.
## Version 0.5 — Multi-Section Duct Route

## Version 0.5 — Multi-Section Duct Route

Version 0.5 retains all previous sizing and pressure-loss functions and adds:

- Individual user-entered fitting K-values
- Multiple connected round and rectangular duct sections
- Section-specific airflow, dimensions and duct length
- Section-specific Reynolds numbers and Darcy friction factors
- Individual fitting losses using local section velocity pressure
- Cumulative straight-duct friction and fitting losses
- Total pressure-loss summary for a specified duct path

### Engineering limitations

This version models one specified duct path, not a fully solved branched duct network. Fitting K-values must be selected using appropriate engineering references and reference velocities. Rectangular friction uses a simplified hydraulic-diameter method. Flow distribution, transition velocity-pressure effects, terminal losses, fan requirements and network balancing require additional analysis.

The program is intended for preliminary educational and conceptual engineering calculations only. Verify all results before use in actual engineering design.

### Running the program

Run `python3 duct_calculator.py` and select Option 7 for Multi-Section Duct Route. Option 8 exits the application.