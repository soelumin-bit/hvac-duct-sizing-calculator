
import math

# HVAC DUCT SIZING CALCULATOR V0.4
# Educational preliminary engineering tool

# Air properties and duct roughness
AIR_DENSITY = 1.20          # kg/m3
AIR_VISCOSITY = 1.81e-5    # Pa.s
ROUGHNESS = 0.00015        # metres

# Illustrative selectable internal duct sizes (mm)
ROUND_SIZES = [
    100, 125, 160, 200, 250, 315, 355,
    400, 450, 500, 560, 630, 710, 800,
    900, 1000, 1120, 1250, 1400, 1600
]

RECT_SIZES = list(range(100, 1601, 50))
MAX_ASPECT_RATIO = 4.0


# ==========================================
# COMMON CALCULATION FUNCTIONS
# ==========================================

def get_positive_number(prompt):
    while True:
        try:
            value = float(input(prompt))
            if math.isfinite(value) and value > 0:
                return value
            print("Enter a positive finite number.")
        except ValueError:
            print("Invalid number. Please try again.")


def get_nonnegative_number(prompt):
    while True:
        try:
            value = float(input(prompt))
            if math.isfinite(value) and value >= 0:
                return value
            print("Enter zero or a positive number.")
        except ValueError:
            print("Invalid number. Please try again.")


def round_area(diameter_mm):
    d = diameter_mm / 1000
    return math.pi * d**2 / 4


def rectangular_area(width_mm, height_mm):
    return width_mm * height_mm / 1000000


def air_velocity(airflow_m3h, area_m2):
    return airflow_m3h / 3600 / area_m2


def hydraulic_diameter(width_mm, height_mm):
    w = width_mm / 1000
    h = height_mm / 1000
    return 2 * w * h / (w + h)


def show_results(area, velocity):
    print("\n--- RESULTS ---")
    print(f"Duct area: {area:.4f} m2")
    print(f"Air velocity: {velocity:.2f} m/s")


# ==========================================
# VERSION 0.3: EXISTING CALCULATIONS
# ==========================================

def calculate_round_velocity():
    print("\nROUND DUCT VELOCITY")
    airflow = get_positive_number("Airflow (m3/h): ")
    diameter = get_positive_number("Diameter (mm): ")

    area = round_area(diameter)
    velocity = air_velocity(airflow, area)
    show_results(area, velocity)


def calculate_rectangular_velocity():
    print("\nRECTANGULAR DUCT VELOCITY")
    airflow = get_positive_number("Airflow (m3/h): ")
    width = get_positive_number("Width (mm): ")
    height = get_positive_number("Height (mm): ")

    area = rectangular_area(width, height)
    velocity = air_velocity(airflow, area)
    show_results(area, velocity)


def automatic_round_sizing():
    print("\nAUTOMATIC ROUND DUCT SIZING")
    airflow = get_positive_number("Airflow (m3/h): ")
    target = get_positive_number("Target velocity (m/s): ")

    required_area = airflow / 3600 / target
    required_d = math.sqrt(
        4 * required_area / math.pi
    ) * 1000

    selected = next(
        (d for d in ROUND_SIZES if d >= required_d),
        None
    )

    print("\n--- SIZING RESULTS ---")
    print(f"Required area: {required_area:.4f} m2")
    print(f"Calculated diameter: {required_d:.1f} mm")

    if selected is None:
        print("No suitable diameter in size list.")
        return

    area = round_area(selected)
    velocity = air_velocity(airflow, area)

    print(f"Selected diameter: {selected} mm")
    show_results(area, velocity)


def automatic_rectangular_sizing():
    print("\nAUTOMATIC RECTANGULAR SIZING")
    airflow = get_positive_number("Airflow (m3/h): ")
    target = get_positive_number("Target velocity (m/s): ")

    required_area = airflow / 3600 / target
    candidates = []

    for width in RECT_SIZES:
        for height in RECT_SIZES:
            if width < height:
                continue

            ratio = width / height
            if ratio > MAX_ASPECT_RATIO:
                continue

            area = rectangular_area(width, height)

            if area >= required_area:
                candidates.append(
                    (area, ratio, width, height)
                )

    print("\n--- SIZING RESULTS ---")
    print(f"Required area: {required_area:.4f} m2")

    if not candidates:
        print("No suitable rectangular duct size.")
        return

    area, ratio, width, height = min(candidates)
    velocity = air_velocity(airflow, area)

    print(f"Selected duct: {width} x {height} mm")
    print(f"Aspect ratio: {ratio:.2f}")
    show_results(area, velocity)


# ==========================================
# VERSION 0.4: PRESSURE LOSS FUNCTIONS
# ==========================================

def reynolds_number(velocity, diameter_m):
    return (
        AIR_DENSITY * velocity * diameter_m
        / AIR_VISCOSITY
    )


def turbulent_friction_factor(re, diameter_m):
    # Swamee-Jain approximation
    relative_roughness = ROUGHNESS / diameter_m

    term = (
        relative_roughness / 3.7
        + 5.74 / re**0.9
    )

    return 0.25 / math.log10(term)**2


def darcy_friction_factor(re, diameter_m):
    if re < 2300:
        return 64 / re, "Laminar"

    if re >= 4000:
        f = turbulent_friction_factor(re, diameter_m)
        return f, "Turbulent"

    # Transitional flow: illustrative interpolation
    f_low = 64 / 2300
    f_high = turbulent_friction_factor(4000, diameter_m)
    fraction = (re - 2300) / (4000 - 2300)
    f = f_low + fraction * (f_high - f_low)

    return f, "Transitional (approximation)"


def calculate_pressure_loss(area, dh, airflow, length, k):
    velocity = air_velocity(airflow, area)
    re = reynolds_number(velocity, dh)

    friction_factor, regime = darcy_friction_factor(
        re, dh
    )

    dynamic_pressure = 0.5 * AIR_DENSITY * velocity**2

    friction_loss = (
        friction_factor * length / dh * dynamic_pressure
    )

    fitting_loss = k * dynamic_pressure
    total_loss = friction_loss + fitting_loss

    print("\n--- PRESSURE LOSS RESULTS ---")
    print(f"Duct area: {area:.4f} m2")
    print(f"Hydraulic diameter: {dh:.4f} m")
    print(f"Air velocity: {velocity:.2f} m/s")
    print(f"Reynolds number: {re:.0f}")
    print(f"Flow regime: {regime}")
    print(f"Darcy friction factor: {friction_factor:.5f}")
    print(f"Dynamic pressure: {dynamic_pressure:.2f} Pa")

    if regime.startswith("Transitional"):
        print("WARNING: Transitional-flow friction is uncertain.")

    if length > 0:
        print(
            f"Straight friction rate: "
            f"{friction_loss / length:.3f} Pa/m"
        )

    print(f"Straight duct loss: {friction_loss:.2f} Pa")
    print(f"Fitting K total: {k:.2f}")
    print(f"Fitting loss: {fitting_loss:.2f} Pa")
    print(f"TOTAL PRESSURE LOSS: {total_loss:.2f} Pa")

    print("\nPreliminary estimate only.")
    print("Verify fittings and actual duct construction.")


def round_pressure_loss():
    print("\nROUND DUCT PRESSURE LOSS")

    airflow = get_positive_number("Airflow (m3/h): ")
    diameter = get_positive_number("Diameter (mm): ")
    length = get_nonnegative_number("Duct length (m): ")
    k = get_nonnegative_number("Total fitting K-value: ")

    area = round_area(diameter)
    dh = diameter / 1000

    calculate_pressure_loss(area, dh, airflow, length, k)


def rectangular_pressure_loss():
    print("\nRECTANGULAR DUCT PRESSURE LOSS")

    airflow = get_positive_number("Airflow (m3/h): ")
    width = get_positive_number("Width (mm): ")
    height = get_positive_number("Height (mm): ")
    length = get_nonnegative_number("Duct length (m): ")
    k = get_nonnegative_number("Total fitting K-value: ")

    area = rectangular_area(width, height)
    dh = hydraulic_diameter(width, height)

    calculate_pressure_loss(area, dh, airflow, length, k)

    print("NOTE: Rectangular friction uses")
    print("a simplified hydraulic-diameter model.")


# ==========================================
# MAIN MENU
# ==========================================

def main():
    while True:
        print("\n=================================")
        print(" HVAC DUCT SIZING CALCULATOR V0.4")
        print("=================================")

        print("1. Round Duct Velocity")
        print("2. Rectangular Duct Velocity")
        print("3. Automatic Round Duct Sizing")
        print("4. Automatic Rectangular Duct Sizing")
        print("5. Round Duct Pressure Loss")
        print("6. Rectangular Duct Pressure Loss")
        print("7. Exit")

        choice = input("Select option (1-7): ")

        if choice == "1":
            calculate_round_velocity()
        elif choice == "2":
            calculate_rectangular_velocity()
        elif choice == "3":
            automatic_round_sizing()
        elif choice == "4":
            automatic_rectangular_sizing()
        elif choice == "5":
            round_pressure_loss()
        elif choice == "6":
            rectangular_pressure_loss()
        elif choice == "7":
            print("Thank you for using the calculator.")
            break
        else:
            print("Invalid choice. Please select 1-7.")


if __name__ == "__main__":
    main()
