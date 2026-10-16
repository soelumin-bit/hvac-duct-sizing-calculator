
import math

print("HVAC DUCT SIZING CALCULATOR")

airflow = float(input("Airflow (m3/h): "))
diameter = float(input("Duct diameter (mm): "))

if airflow <= 0 or diameter <= 0:
    print("Error: Enter positive values.")
else:
    area = math.pi * (diameter / 1000)**2 / 4
    velocity = (airflow / 3600) / area

    print("\n--- RESULTS ---")
    print(f"Duct Area: {area:.4f} m2")
    print(f"Air Velocity: {velocity:.2f} m/s")

