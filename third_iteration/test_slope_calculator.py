import unittest
from slope_calculator import *


class TestSlopeCalculator(unittest.TestCase):
    def test_calc_slopes(self):
        point1 = [1.0, 1.0]
        point2 = [3.0, 3.0]
        expected_slope = 1.0
        self.assertAlmostEqual(calc_slope(point1,point2), expected_slope, 2)
        point1 = [1.0, 1.0]
        point2 = [3.0, 5.0]
        expected_slope = 2.0
        self.assertAlmostEqual(calc_slope(point1,point2), expected_slope, 2)
        point1 = [1.0, 1.0]
        point2 = [3.0, 1.0]
        expected_slope = 0.0
        self.assertAlmostEqual(calc_slope(point1,point2), expected_slope, 2)

    def test_calculate_slopes(self):
        test_points=[[1.0, 1], [3.0, 3.0], [5.0, 9.0], [6.0, 10.0], [8.0, 12.0], [4.0, 20.0]]
        expected_slopes = [1.0, 3.0, 1.0, 1.0, -2.0]
        pm_date = 2
        expected_r_slope = 1.0
        actual_r_slope, actual_slopes = calculate_slopes(test_points, pm_date)
        self.assertEqual(actual_r_slope, expected_r_slope)
        self.assertListEqual(actual_slopes, expected_slopes)

    def test_calc_distance(self):
        # The global MINIMUM is set to 10
        point1 = [1.0, 1.0]
        point2 = [2.0, 2.0]
        returned_point = calculate_distance(point1,point2)
        self.assertEqual(returned_point, None)
        point1 = [1.0, 1.0]
        point2 = [21.0, 21.0]
        returned_point = calculate_distance(point1, point2)
        self.assertEqual(returned_point, point1)

    def test_point(self):
        y_data = [0.0, 100.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0, 1000.0]
        peaks = [2.0, 4.0]
        valleys = [3.0, 5.0]
        start_date = 1
        expected_points = [(1, 0.0), (3.0, 200.0), (4.0, 300.0), (5.0, 400.0), (12, 1000.0)]
        points = find_points(y_data, peaks, valleys, start_date)
        self.assertListEqual(points, expected_points)


if __name__ == '__main__':
    unittest.main()
