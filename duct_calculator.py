
import math

# HVAC DUCT SIZING CALCULATOR - VERSION 0.3
# Educational engineering calculator

# Example selectable dimensions in mm.
# Verify actual product availability and internal sizes.
ROUND_SIZES = [
    100, 125, 160, 200, 250, 315, 355,
    400, 450, 500, 560, 630, 710, 800,
    900, 1000, 1120, 1250, 1400, 1600
]

RECT_SIZES = list(range(100, 1601, 50))
MAX_ASPECT_RATIO = 4.0


def get_positive_number(prompt):
    """Ask for a positive numeric value."""
    while True:
        try:
            value = float(input(prompt))
            if math.isfinite(value) and value > 0:
                return value
            print("Please enter a positive finite number.")
        except ValueError:
            print("Invalid number. Please try again.")


def round_area(diameter_mm):
    diameter_m = diameter_mm / 1000
    return math.pi * diameter_m**2 / 4


def rectangular_area(width_mm, height_mm):
    return (width_mm / 1000) * (height_mm / 1000)


def air_velocity(airflow_m3h, area_m2):
    return (airflow_m3h / 3600) / area_m2


def show_results(area, velocity):
    print("\n--- RESULTS ---")
    print(f"Duct area: {area:.4f} m2")
    print(f"Air velocity: {velocity:.2f} m/s")


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
    target_v = get_positive_number("Target velocity (m/s): ")

    required_area = (airflow / 3600) / target_v

    required_diameter = (
        math.sqrt(4 * required_area / math.pi) * 1000
    )

    selected = next(
        (d for d in ROUND_SIZES if d >= required_diameter),
        None
    )

    print("\n--- SIZING RESULTS ---")
    print(f"Required area: {required_area:.4f} m2")
    print(f"Calculated diameter: {required_diameter:.1f} mm")

    if selected is None:
        print("No suitable round size in the current list.")
        return

    actual_area = round_area(selected)
    actual_velocity = air_velocity(airflow, actual_area)

    print(f"Selected round diameter: {selected} mm")
    print(f"Selected area: {actual_area:.4f} m2")
    print(f"Actual velocity: {actual_velocity:.2f} m/s")


def automatic_rectangular_sizing():
    print("\nAUTOMATIC RECTANGULAR DUCT SIZING")

    airflow = get_positive_number("Airflow (m3/h): ")
    target_v = get_positive_number("Target velocity (m/s): ")

    required_area = (airflow / 3600) / target_v

    candidates = []

    for width in RECT_SIZES:
        for height in RECT_SIZES:
            if width < height:
                continue

            aspect_ratio = width / height

            if aspect_ratio > MAX_ASPECT_RATIO:
                continue

            area = rectangular_area(width, height)

            if area >= required_area:
                candidates.append(
                    (area, aspect_ratio, width, height)
                )

    print("\n--- SIZING RESULTS ---")
    print(f"Required area: {required_area:.4f} m2")

    if not candidates:
        print("No suitable rectangular size in the current list.")
        return

    # Pick minimum area; use aspect ratio as tie-breaker.
    best = min(candidates)
    actual_area, ratio, width, height = best

    actual_velocity = air_velocity(airflow, actual_area)

    print(f"Selected width: {width} mm")
    print(f"Selected height: {height} mm")
    print(f"Selected duct: {width} x {height} mm")
    print(f"Aspect ratio: {ratio:.2f}")
    print(f"Selected area: {actual_area:.4f} m2")
    print(f"Actual velocity: {actual_velocity:.2f} m/s")


def main():
    while True:
        print("\n==================================")
        print(" HVAC DUCT SIZING CALCULATOR V0.3")
        print("==================================")
        print("1. Round Duct Velocity")
        print("2. Rectangular Duct Velocity")
        print("3. Automatic Round Duct Sizing")
        print("4. Automatic Rectangular Duct Sizing")
        print("5. Exit")

        choice = input("Select option (1-5): ")

        if choice == "1":
            calculate_round_velocity()
        elif choice == "2":
            calculate_rectangular_velocity()
        elif choice == "3":
            automatic_round_sizing()
        elif choice == "4":
            automatic_rectangular_sizing()
        elif choice == "5":
            print("Thank you for using the calculator.")
            break
        else:
            print("Invalid option. Choose 1 to 5.")


if __name__ == "__main__":
    main()
