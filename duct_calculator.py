
import math

# ==========================================
# HVAC DUCT SIZING CALCULATOR - VERSION 0.5
# Preliminary educational calculations
# ==========================================

AIR_DENSITY = 1.20          # kg/m3
AIR_VISCOSITY = 1.81e-5    # Pa.s
ROUGHNESS = 0.00015        # metres

# Illustrative duct internal sizes (mm)
ROUND_SIZES = [
    100, 125, 160, 200, 250, 315, 355,
    400, 450, 500, 560, 630, 710, 800,
    900, 1000, 1120, 1250, 1400, 1600
]

RECT_SIZES = list(range(100, 1601, 50))
MAX_ASPECT_RATIO = 4.0


# ==========================================
# INPUT FUNCTIONS
# ==========================================

def get_positive_number(prompt):
    while True:
        try:
            number = float(input(prompt))
            if math.isfinite(number) and number > 0:
                return number
        except ValueError:
            pass
        print("Enter a positive finite number.")


def get_nonnegative_number(prompt):
    while True:
        try:
            number = float(input(prompt))
            if math.isfinite(number) and number >= 0:
                return number
        except ValueError:
            pass
        print("Enter zero or a positive number.")


def get_positive_integer(prompt):
    while True:
        text = input(prompt)
        try:
            number = int(text)
            if number > 0:
                return number
        except ValueError:
            pass
        print("Enter a positive whole number.")


# ==========================================
# GEOMETRY AND VELOCITY
# ==========================================

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
# VERSION 0.3 FEATURES - RETAINED
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
# VERSION 0.4 - FRICTION AND PRESSURE LOSS
# ==========================================

def reynolds_number(velocity, diameter_m):
    return (
        AIR_DENSITY * velocity * diameter_m
        / AIR_VISCOSITY
    )


def turbulent_friction_factor(re, diameter_m):
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
        return (
            turbulent_friction_factor(re, diameter_m),
            "Turbulent"
        )

    # Simplified transitional interpolation
    f_low = 64 / 2300
    f_high = turbulent_friction_factor(
        4000, diameter_m
    )

    fraction = (re - 2300) / 1700
    f = f_low + fraction * (f_high - f_low)

    return f, "Transitional (approximation)"


# Return results as a dictionary.
# This enables reuse in duct-network calculations.
def pressure_loss_data(area, dh, airflow, length, k):
    velocity = air_velocity(airflow, area)

    re = reynolds_number(velocity, dh)

    friction_factor, regime = darcy_friction_factor(
        re, dh
    )

    dynamic_pressure = (
        0.5 * AIR_DENSITY * velocity**2
    )

    friction_loss = (
        friction_factor * length / dh
        * dynamic_pressure
    )

    fitting_loss = k * dynamic_pressure
    total_loss = friction_loss + fitting_loss

    return {
        "area": area,
        "dh": dh,
        "velocity": velocity,
        "re": re,
        "regime": regime,
        "f": friction_factor,
        "dynamic_pressure": dynamic_pressure,
        "friction_loss": friction_loss,
        "fitting_loss": fitting_loss,
        "total_loss": total_loss,
        "length": length,
        "k": k
    }


def print_pressure_results(result):
    print("\n--- PRESSURE LOSS RESULTS ---")

    print(f"Duct area: {result['area']:.4f} m2")
    print(f"Hydraulic diameter: {result['dh']:.4f} m")
    print(f"Air velocity: {result['velocity']:.2f} m/s")
    print(f"Reynolds number: {result['re']:.0f}")
    print(f"Flow regime: {result['regime']}")
    print(f"Darcy factor: {result['f']:.5f}")

    print(
        f"Dynamic pressure: "
        f"{result['dynamic_pressure']:.2f} Pa"
    )

    if result["length"] > 0:
        friction_rate = (
            result["friction_loss"] / result["length"]
        )
        print(f"Friction rate: {friction_rate:.3f} Pa/m")

    print(
        f"Straight duct loss: "
        f"{result['friction_loss']:.2f} Pa"
    )
    print(f"Total fitting K: {result['k']:.3f}")
    print(
        f"Fitting loss: "
        f"{result['fitting_loss']:.2f} Pa"
    )
    print(
        f"TOTAL PRESSURE LOSS: "
        f"{result['total_loss']:.2f} Pa"
    )

    if result["regime"].startswith("Transitional"):
        print("WARNING: Transitional friction is uncertain.")


def round_pressure_loss():
    print("\nROUND DUCT PRESSURE LOSS")

    airflow = get_positive_number("Airflow (m3/h): ")
    diameter = get_positive_number("Diameter (mm): ")
    length = get_nonnegative_number("Length (m): ")
    k = get_nonnegative_number("Total fitting K: ")

    result = pressure_loss_data(
        round_area(diameter),
        diameter / 1000,
        airflow, length, k
    )

    print_pressure_results(result)


def rectangular_pressure_loss():
    print("\nRECTANGULAR DUCT PRESSURE LOSS")

    airflow = get_positive_number("Airflow (m3/h): ")
    width = get_positive_number("Width (mm): ")
    height = get_positive_number("Height (mm): ")
    length = get_nonnegative_number("Length (m): ")
    k = get_nonnegative_number("Total fitting K: ")

    result = pressure_loss_data(
        rectangular_area(width, height),
        hydraulic_diameter(width, height),
        airflow, length, k
    )

    print_pressure_results(result)
    print("Rectangular friction is approximate.")


# ==========================================
# VERSION 0.5 - INDIVIDUAL FITTING LOSSES
# ==========================================

def input_fittings():
    print("\nINDIVIDUAL FITTINGS")
    print("Enter K from verified fitting references.")
    print("Use the local section velocity pressure.")

    count = get_nonnegative_integer(
        "Number of fittings: "
    )

    fittings = []

    for i in range(count):
        print(f"\nFitting {i + 1}")

        name = input("Fitting name: ").strip()
        if not name:
            name = f"Fitting {i + 1}"

        k = get_nonnegative_number(
            "Fitting K-value: "
        )

        fittings.append({
            "name": name,
            "k": k
        })

    return fittings


def get_nonnegative_integer(prompt):
    while True:
        try:
            number = int(input(prompt))
            if number >= 0:
                return number
        except ValueError:
            pass
        print("Enter zero or a positive whole number.")


def create_duct_section(number):
    print(f"\n====== DUCT SECTION {number} ======")

    while True:
        shape = input(
            "Shape (1=Round, 2=Rectangular): "
        ).strip()

        if shape in ("1", "2"):
            break

        print("Choose 1 or 2.")

    airflow = get_positive_number("Airflow (m3/h): ")
    length = get_nonnegative_number("Length (m): ")

    if shape == "1":
        diameter = get_positive_number(
            "Internal diameter (mm): "
        )

        area = round_area(diameter)
        dh = diameter / 1000
        description = f"Round D{diameter:g} mm"

    else:
        width = get_positive_number(
            "Internal width (mm): "
        )
        height = get_positive_number(
            "Internal height (mm): "
        )

        area = rectangular_area(width, height)
        dh = hydraulic_diameter(width, height)
        description = (
            f"Rectangular {width:g} x {height:g} mm"
        )

    fittings = input_fittings()

    total_k = sum(
        fitting["k"] for fitting in fittings
    )

    result = pressure_loss_data(
        area, dh, airflow, length, total_k
    )

    return {
        "number": number,
        "shape": description,
        "airflow": airflow,
        "fittings": fittings,
        "result": result
    }


def calculate_duct_route():
    print("\nMULTI-SECTION DUCT ROUTE V0.5")
    print("Calculate ONE specified duct path.")
    print("Do not add parallel branch losses together.")

    count = get_positive_integer(
        "Number of duct sections: "
    )

    sections = []

    for number in range(1, count + 1):
        section = create_duct_section(number)
        sections.append(section)

    cumulative_loss = 0.0
    total_friction = 0.0
    total_fittings = 0.0
    total_length = 0.0

    print("\n================================")
    print(" SECTION-BY-SECTION PRESSURE LOSS")
    print("================================")

    for section in sections:
        result = section["result"]

        cumulative_loss += result["total_loss"]
        total_friction += result["friction_loss"]
        total_fittings += result["fitting_loss"]
        total_length += result["length"]

        print(f"\nSECTION {section['number']}")
        print(f"Duct: {section['shape']}")
        print(f"Airflow: {section['airflow']:.1f} m3/h")
        print_pressure_results(result)

        print("\nIndividual fitting losses:")

        if not section["fittings"]:
            print("No fittings entered.")

        for fitting in section["fittings"]:
            loss = (
                fitting["k"]
                * result["dynamic_pressure"]
            )

            print(
                f"  {fitting['name']}: "
                f"K={fitting['k']:.3f}, "
                f"Loss={loss:.2f} Pa"
            )

        print(
            f"CUMULATIVE LOSS: "
            f"{cumulative_loss:.2f} Pa"
        )

    print("\n================================")
    print(" TOTAL DUCT ROUTE SUMMARY")
    print("================================")

    print(f"Number of sections: {count}")
    print(f"Total duct length: {total_length:.2f} m")
    print(f"Total friction loss: {total_friction:.2f} Pa")
    print(f"Total fitting loss: {total_fittings:.2f} Pa")

    print(
        f"TOTAL ROUTE PRESSURE LOSS: "
        f"{cumulative_loss:.2f} Pa"
    )

    print("\nIMPORTANT:")
    print("This is a preliminary path loss estimate.")
    print("Verify K-values and reference velocities.")
    print("Account separately for branches,")
    print("terminal devices, coils and fan effects.")
    print("Check velocity changes and transitions.")
    print("Use validated methods for final design.")


# ==========================================
# MAIN MENU - VERSION 0.5
# ==========================================

def main():
    while True:
        print("\n===================================")
        print(" HVAC DUCT SIZING CALCULATOR V0.5")
        print("===================================")

        print("1. Round Duct Velocity")
        print("2. Rectangular Duct Velocity")
        print("3. Automatic Round Duct Sizing")
        print("4. Automatic Rectangular Duct Sizing")
        print("5. Round Duct Pressure Loss")
        print("6. Rectangular Duct Pressure Loss")
        print("7. Multi-Section Duct Route (NEW)")
        print("8. Exit")

        choice = input("Select option (1-8): ").strip()

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
            calculate_duct_route()
        elif choice == "8":
            print("Thank you for using the calculator.")
            break
        else:
            print("Invalid option. Please choose 1-8.")


if __name__ == "__main__":
    main()
