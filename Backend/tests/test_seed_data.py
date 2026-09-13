import unittest

from scripts.seed_drugs import DRUGS


class SeedDataTest(unittest.TestCase):
    def test_drug_seed_data_is_complete_and_unique(self):
        names = [item["name"] for item in DRUGS]
        self.assertEqual(len(names), len(set(names)))
        self.assertTrue(
            all(
                {"name", "spec", "unit", "unit_price"} == set(item)
                and item["unit_price"] > 0
                for item in DRUGS
            )
        )


if __name__ == "__main__":
    unittest.main()
