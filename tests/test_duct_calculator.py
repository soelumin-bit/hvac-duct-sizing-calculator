
import math
import unittest
from io import StringIO
from contextlib import redirect_stdout
from unittest.mock import patch

import duct_calculator as dc

class TestHVACCalculator(unittest.TestCase):

    def test_round_duct_area(self):
        area = dc.round_area(400)
        expected = math.pi * 0.4**2 / 4
        self.assertAlmostEqual(area, expected)

    def test_rectangular_duct_area(self):
        area = dc.rectangular_area(500, 250)
        self.assertAlmostEqual(area, 0.125)

    def test_air_velocity(self):
        velocity = dc.air_velocity(1800, 0.125)
        self.assertAlmostEqual(velocity, 4.0)

    def test_hydraulic_diameter(self):
        diameter = dc.hydraulic_diameter(500, 250)
        self.assertAlmostEqual(diameter, 1 / 3)

    def test_reynolds_number(self):
        re = dc.reynolds_number(4.0, 1 / 3)
        expected = 1.20 * 4.0 * (1 / 3) / 1.81e-5
        self.assertAlmostEqual(re, expected)

    def test_laminar_friction(self):
        factor, regime = dc.darcy_friction_factor(
            1000, 0.4
        )
        self.assertEqual(regime, "Laminar")
        self.assertAlmostEqual(factor, 0.064)

    def test_turbulent_friction(self):
        factor, regime = dc.darcy_friction_factor(
            100000, 0.4
        )
        self.assertEqual(regime, "Turbulent")
        self.assertGreater(factor, 0)
        self.assertLess(factor, 0.1)

    def test_round_pressure_loss(self):
        result = dc.pressure_loss_data(
            dc.round_area(400), 0.4, 1000, 20, 1.0
        )
        self.assertAlmostEqual(
            result["total_loss"], 6.10, delta=0.10
        )

    def test_rectangular_pressure_loss(self):
        area = dc.rectangular_area(500, 250)
        dh = dc.hydraulic_diameter(500, 250)
        result = dc.pressure_loss_data(
            area, dh, 1800, 20, 1.0
        )
        self.assertAlmostEqual(
            result["total_loss"], 21.43, delta=0.15
        )

    def test_individual_fitting_losses(self):
        result = dc.pressure_loss_data(
            0.125, 1 / 3, 1800, 15, 1.0
        )
        elbow = 0.4 * result["dynamic_pressure"]
        damper = 0.6 * result["dynamic_pressure"]

        self.assertAlmostEqual(elbow, 3.84)
        self.assertAlmostEqual(damper, 5.76)
        self.assertAlmostEqual(
            elbow + damper, result["fitting_loss"]
        )

    def test_two_section_route(self):
        inputs = [
            "2",
            "1", "1800", "10", "400",
            "2", "Elbow", "0.3", "Damper", "0.2",
            "2", "1800", "15", "500", "250",
            "2", "Elbow", "0.4", "Damper", "0.6"
        ]

        output = StringIO()
        with patch("builtins.input", side_effect=inputs):
            with redirect_stdout(output):
                dc.calculate_duct_route()

        self.assertIn(
            "TOTAL ROUTE PRESSURE LOSS: 27.90 Pa",
            output.getvalue()
        )

    def test_positive_input_validation(self):
        with patch(
            "builtins.input",
            side_effect=["abc", "-5", "100"]
        ):
            with redirect_stdout(StringIO()):
                value = dc.get_positive_number("Airflow: ")

        self.assertEqual(value, 100.0)

    def test_zero_fittings(self):
        with patch("builtins.input", return_value="0"):
            with redirect_stdout(StringIO()):
                fittings = dc.input_fittings()

        self.assertEqual(fittings, [])


if __name__ == "__main__":
    unittest.main()