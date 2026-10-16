
import math

print("================================")
print(" HVAC DUCT SIZING CALCULATOR V0.2")
print("================================")

print("1. Round Duct")
print("2. Rectangular Duct")

choice = input("Select duct type (1 or 2): ")

if choice == "1":
    print("\nROUND DUCT CALCULATION")

    airflow = float(input("Airflow (m3/h): "))
    diameter = float(input("Diameter (mm): "))

    if airflow <= 0 or diameter <= 0:
        print("Error: Enter positive values.")
    else:
        diameter_m = diameter / 1000
        area = math.pi * diameter_m**2 / 4
        velocity = (airflow / 3600) / area

        print("\n--- RESULTS ---")
        print(f"Duct Area: {area:.4f} m2")
        print(f"Air Velocity: {velocity:.2f} m/s")

elif choice == "2":
    print("\nRECTANGULAR DUCT CALCULATION")

    airflow = float(input("Airflow (m3/h): "))
    width = float(input("Width (mm): "))
    height = float(input("Height (mm): "))

    if airflow <= 0 or width <= 0 or height <= 0:
        print("Error: Enter positive values.")
    else:
        width_m = width / 1000
        height_m = height / 1000

        area = width_m * height_m
        velocity = (airflow / 3600) / area

        print("\n--- RESULTS ---")
        print(f"Duct Area: {area:.4f} m2")
        print(f"Air Velocity: {velocity:.2f} m/s")

else:
    print("Invalid selection. Please choose 1 or 2.")

