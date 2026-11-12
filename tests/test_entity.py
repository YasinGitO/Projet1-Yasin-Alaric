import unittest

from entity import Entity

class EntityTest(unittest.TestCase):

    def test_is_alive_and_damage(self):
        entitee1 = Entity(1,2,3,4)
        self.assertTrue(entitee1.is_alive())
        entitee2 = Entity(1,2,0,4)
        self.assertFalse(entitee2.is_alive())
        entitee3 = Entity(1,2,3,4)
        self.assertEqual(entitee3.get_hp(), 3)
        entitee3.take_damage(3)
        self.assertEqual(entitee3.get_hp(), 0)
        self.assertFalse(entitee3.is_alive())

