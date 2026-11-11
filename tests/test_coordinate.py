import unittest

from coordinate import Coordinate

class CoordinateTest(unittest.TestCase):

    def test_coordinate_str(self):
        self.assertEqual(str(Coordinate(1,2)), "(1, 2)")

    def test_coordinate_repr(self):
        self.assertEqual(repr(Coordinate(1,2)), "(1, 2)")

    def test_coordinate_equality(self):
        self.assertEqual(Coordinate(1,2), Coordinate(1,2))

    def test_coordinate_inequality(self):
        self.assertNotEqual(Coordinate(1,2), Coordinate(2,2))

    def test_get_x(self):
        self.assertEqual(Coordinate(1,2).getX(), 1)

    def test_get_y(self):
        self.assertEqual(Coordinate(1,2).getY(), 2)

    def test_set_x(self):
        test = Coordinate(1,2)
        test.setX(3)
        self.assertEqual(test.getX(), 3)

    def test_set_y(self):
        test = Coordinate(1,2)
        test.setY(3)
        self.assertEqual(test.getY(), 3)

    def test_clamp_x(self):
        test1 = Coordinate(3,2)
        test1.clamp_x(2,4)
        self.assertEqual(test1.getX(), 3)
        test2 = Coordinate(1,2)
        test2.clamp_x(2,3)
        self.assertEqual(test2.getX(), 2)
        test3 = Coordinate(5,2)
        test3.clamp_x(3,4)
        self.assertEqual(test3.getX(), 4)

    def test_move(self):
        test1 = Coordinate(1, 2)
        test1.move(dx=5)
        test2 = Coordinate(6, 2)
        test2.move(dx=-5)
        self.assertEqual(test1.getX(), 6)
        self.assertEqual(test2.getX(), 1)
        test3 = Coordinate(1, 2)
        test3.move(dy=5)
        test4 = Coordinate(1, 7)
        test4.move(dy=-5)
        self.assertEqual(test3.getY(), 7)
        self.assertEqual(test4.getY(), 2)
