import unittest
import nutritional_data


class TestNutrionalData(unittest.TestCase):

    def setUp(self):
        self.car = nutritional_data.BuildNutritionDB()
        self.test_list = ["Broccoli"]

    def test_attrs(self):
        self.assertEqual("uccIJar8k7Ps1nLu9PCJprLAPVgQWaO6MUWtVYM1", self.car.api_key)
        self.assertEqual("S:\THPMP Operations\Taylor Gosselin\Personal Projects\The-Optimalest-Salad/fooddb.csv", self.car.dbpath)

    def test_DB(self):
        self.assertEqual(nutritional_data.BuildNutritionDB.DB_Test(self.test_list),[[{'Name': 'Broccoli', 'Test1': 'xyz'}]])
if __name__ == '__main__':
    unittest.main()