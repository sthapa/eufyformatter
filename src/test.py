import datetime
import unittest
import convert_eufy


class TestConvertEufy(unittest.TestCase):
    lb_to_kg_factor = 0.45359237
    def test_fieldname_conversion(self):
        mappings = {
            "Time": "time",
            "WEIGHT (kg)": "weight",
            "WEIGHT (lbs)": "weight",
            "BMI": "bmi",
            "BODY FAT %": "body_fat",
            "HEART RATE (bpm)": "heart_rate",
            "MUSCLE MASS (kg)": "muscle_mass",
            "MUSCLE MASS (lbs)": "muscle_mass",
            "MUSCLE MASS %": "muscle_mass_percent",
            "BMR": "bmr",
            "WATER": "water",
            "BODY FAT MASS (kg)": "body_fat_mass",
            "BODY FAT MASS (lbs)": "body_fat_mass",
            "LEAN BODY MASS (kg)": "lean_body_mass",
            "LEAN BODY MASS (lbs)": "lean_body_mass",
            "BONE MASS (kg)": "bone_mass",
            "BONE MASS (lbs)": "bone_mass",
            "BONE MASS %": "bone_mass_percent",
            "VISCERAL FAT": "visceral_fat_percentage",
            "PROTEIN %": "protein_percentage",
            "SKELETAL MUSCLE MASS (kg)": "skeletal_muscle_mass",
            "SKELETAL MUSCLE MASS (lbs)": "skeletal_muscle_mass",
            "SUBCUTANEOUS FAT %": "subcutaneous_fat_percentage",
            "BODY AGE": "body_age",
            "BODY TYPE": "body_type",
            "HEAD SIZE (cm)": "head_size"
        }
        for k,v in mappings.items():
            name = convert_eufy.convert_fieldname(k)
            self.assertEqual(name, v)  # add assertion here

    def test_csv_read_conversion_imperial(self):
        """
        Test conversion from imperial to metric units when reading a csv file
        """
        fname = "./test_data/test_read_imperial.csv"
        output = convert_eufy.read_eufyfile(fname)
        entry = output[0]
        expected_time = datetime.datetime(2025, 5, 1, 11, 6, 55)
        self.assertEqual(entry.time,
                         expected_time,
                         f"Date entry in {fname} does not match {entry.time} vs {expected_time}")
        expected = round(79.01 * self.lb_to_kg_factor, 1)
        self.assertEqual(entry.weight,
                         expected,
                         f"Weight entry in {fname} does not match {entry.weight} vs {expected}")
        self.assertEqual(entry.bmi, 27.1,
                         f"BMI entry in {fname} does not match {entry.bmi} vs 27.1")
        self.assertEqual(entry.body_fat, 26.3,
                         f"Body fat entry in {fname} does not match {entry.body_fat} vs 26.3")
        self.assertEqual(entry.heart_rate, 97.0,
                         f"Heart rate entry in {fname} does not match {entry.heart_rate} vs 97.0")
        expected = round(35.44 * self.lb_to_kg_factor, 1)
        self.assertEqual(entry.muscle_mass, expected,
                         f"Muscle mass in {fname} does not match {entry.skeletal_muscle_mass} vs {expected}")
        self.assertEqual(entry.muscle_mass_percent,
                         70.0,
                         f"Muscle mass % in {fname} does not match {entry.muscle_mass_percent} vs 70.0")
        self.assertEqual(entry.bmr, 1541,
                         f"BMR in {fname} does not match {entry.bmr} vs 1541")
        self.assertEqual(entry.water, 50.4,
                         f"Water % in {fname} does not match {entry.water} vs 50.4")
        expected = round(6.95 * self.lb_to_kg_factor, 1)
        self.assertEqual(entry.body_fat_mass, expected,
                         f"Body Fat Mass in {fname} does not match {entry.body_fat_mass} vs {expected}")
        expected = round(2.49 * self.lb_to_kg_factor, 1)
        self.assertEqual(entry.lean_body_mass,
                         expected,
                         f"Lean Body Mass in {fname} does not match {entry.lean_body_mass} vs {expected}")
        expected = round(1.61 * self.lb_to_kg_factor, 1)
        self.assertEqual(entry.bone_mass,
                         expected,
                         f"Bone Mass in {fname} does not match {entry.bone_mass} vs {expected}")
        self.assertEqual(entry.bone_mass_percentage,
                         3.7,
                         f"Bone Mass Percentage in {fname} does not match {entry.bone_mass_percentage} vs 3.7")
        expected = round(14.000000, 1)
        self.assertEqual(entry.visceral_fat_percentage,
                         expected,
                         f"Visceral Fat Mass in {fname} does not match {entry.visceral_fat_percentage} vs {expected}")
        self.assertEqual(entry.protein_percentage,
                         15.5,
                         f"Protein Percentage in {fname} does not match {entry.protein_percentage} vs 15.5")
        expected = round(33.32 * self.lb_to_kg_factor, 1)
        self.assertEqual(entry.skeletal_muscle_mass,
                         expected,
                         f"Skeletal Muscle Mass in {fname} does not match {entry.skeletal_muscle_mass} vs "
                         f"{expected}")
        self.assertEqual(entry.subcutaneous_fat_percentage,
                         22.7,
                         f"Subcutaneous Fat Percentage in {fname} does not match "
                         f"{entry.subcutaneous_fat_percentage} vs 22.7")
        self.assertEqual(entry.body_age,
                         23.0,
                         f"Body Age in {fname} does not match {entry.body_age} vs 49.0")
        self.assertEqual(entry.body_type,
                         "Average",
                         f"Body Type in {fname} does not match -{entry.body_type}- vs Average")
        self.assertEqual(entry.head_size,
                         0.0,
                         f"Head Size in {fname} does not match {entry.head_size} vs 0.0")

    def test_csv_read_imperial(self):
        """
        Test reading from imperial csv file
        """
        fname = "./test_data/test_read_imperial.csv"
        output = convert_eufy.read_eufyfile(fname)
        entries = []
        entry = convert_eufy.WeightEntry(time = datetime.datetime(2025, 5, 1, 11, 6, 55),
                                         weight = round(79.01 * self.lb_to_kg_factor, 1),
                                         bmi = 27.1)
        entry.body_fat = 26.3
        entry.heart_rate = 97.0
        entry.muscle_mass = round(35.44 * self.lb_to_kg_factor, 1)
        entry.muscle_mass_percent = 70.0
        entry.bmr = 1541.0
        entry.water = 50.4
        entry.body_fat_mass = round(6.95 * self.lb_to_kg_factor, 1)
        entry.lean_body_mass = round(2.49 * self.lb_to_kg_factor, 1)
        entry.bone_mass = round(1.61 * self.lb_to_kg_factor, 1)
        entry.bone_mass_percentage = 3.7
        entry.skeletal_muscle_mass = round(33.32 * self.lb_to_kg_factor, 1)
        entry.subcutaneous_fat_percentage = 22.7
        entry.visceral_fat_percentage =  round(14.000000, 1)
        entry.protein_percentage = 15.5
        entry.body_age = 23.0
        entry.body_type = "Average"
        entry.head_size = 0.0
        entries.append(entry)

        entry = convert_eufy.WeightEntry(time = datetime.datetime(2025, 4, 29, 5, 38, 45),
                                         weight = round(81.21 * self.lb_to_kg_factor, 1),
                                         bmi = 27.4)
        entry.body_fat = 27.0
        entry.heart_rate = 77.0
        entry.muscle_mass = round(35.88 * self.lb_to_kg_factor, 1)
        entry.muscle_mass_percent = 69.4
        entry.bmr = 1556.0
        entry.water = 50.00
        entry.body_fat_mass = round(8.72 * self.lb_to_kg_factor, 1)
        entry.lean_body_mass = round(12.49 * self.lb_to_kg_factor, 1)
        entry.bone_mass = round(6.61 * self.lb_to_kg_factor, 1)
        entry.bone_mass_percentage = 3.6
        entry.visceral_fat_percentage =  round(18.000000, 1)
        entry.skeletal_muscle_mass = round(17.51 * self.lb_to_kg_factor, 1)
        entry.subcutaneous_fat_percentage = 23.20
        entry.protein_percentage = 15.300
        entry.body_age = 73.0
        entry.body_type = "Average"
        entry.head_size = 0.0
        entries.append(entry)

        self.assertEqual(output[0], entries[0])
        self.assertEqual(output[1], entries[1])

    def test_csv_read_conversion_metric(self):
        """
        Test conversion from metric units when reading a csv file.  Probably not needed
        """
        fname = "./test_data/test_read_metric.csv"
        output = convert_eufy.read_eufyfile(fname)
        entry = output[0]
        expected_time = datetime.datetime(2025, 1, 17, 18, 47, 20)
        self.assertEqual(entry.time,
                         expected_time,
                         f"Date entry in {fname} does not match {entry.time} vs {expected_time}")
        self.assertEqual(entry.weight,
                         93.35,
                         f"Weight entry in {fname} does not match {entry.weight} vs {93.35}")
        self.assertEqual(entry.bmi, 17.800000,
                         f"BMI entry in {fname} does not match {entry.bmi} vs 17.800000")
        self.assertEqual(entry.body_fat, 19.5,
                         f"Body fat entry in {fname} does not match {entry.body_fat} vs 19.5")
        self.assertEqual(entry.heart_rate, 54.0,
                         f"Heart rate entry in {fname} does not match {entry.heart_rate} vs 54.0")
        self.assertEqual(entry.muscle_mass, 45.4,
                         f"Muscle mass in {fname} does not match {entry.skeletal_muscle_mass} vs 45.4")
        self.assertEqual(entry.muscle_mass_percent,
                         48.9,
                         f"Muscle mass % in {fname} does not match {entry.muscle_mass_percent} vs 48.9")
        self.assertEqual(entry.bmr, 1572,
                         f"BMR in {fname} does not match {entry.bmr} vs 1572")
        self.assertEqual(entry.water, 50.6,
                         f"Water % in {fname} does not match {entry.water} vs 50.6")
        self.assertEqual(entry.body_fat_mass, 12.9,
                         f"Body Fat Mass in {fname} does not match {entry.body_fat_mass} vs 12.9")
        self.assertEqual(entry.lean_body_mass,
                         50.44,
                         f"Lean Body Mass in {fname} does not match {entry.lean_body_mass} vs 50.44")
        self.assertEqual(entry.bone_mass,
                         3,
                         f"Bone Mass in {fname} does not match {entry.bone_mass} vs 3")
        self.assertEqual(entry.bone_mass_percentage,
                         4.6,
                         f"Bone Mass Percentage in {fname} does not match {entry.bone_mass_percentage} vs 4.6")
        self.assertEqual(entry.visceral_fat_percentage,
                         24.0,
                         f"Visceral Fat Mass in {fname} does not match {entry.visceral_fat_percentage} vs 24.0")
        self.assertEqual(entry.protein_percentage,
                         18.3,
                         f"Protein Percentage in {fname} does not match {entry.protein_percentage} vs 18.3")
        self.assertEqual(entry.skeletal_muscle_mass,
                         36.6,
                         f"Skeletal Muscle Mass in {fname} does not match {entry.skeletal_muscle_mass} vs 36.6")
        self.assertEqual(entry.subcutaneous_fat_percentage,
                         36.8,
                         f"Subcutaneous Fat Percentage in {fname} does not match "
                         f"{entry.subcutaneous_fat_percentage} vs 36.8")
        self.assertEqual(entry.body_age,
                         23.0,
                         f"Body Age in {fname} does not match {entry.body_age} vs 23.0")
        self.assertEqual(entry.body_type,
                         "Average",
                         f"Body Type in {fname} does not match -{entry.body_type}- vs Average")
        self.assertEqual(entry.head_size,
                         0.0,
                         f"Head Size in {fname} does not match {entry.head_size} vs 0.0")

    def test_csv_read_metric(self):
        """
        Test reading from metric csv file
        """
        fname = "./test_data/test_read_metric.csv"
        output = convert_eufy.read_eufyfile(fname)
        entries = []
        entry = convert_eufy.WeightEntry(time = datetime.datetime(2025, 1, 17, 18, 47, 20),
                                         weight = 93.35,
                                         bmi = 17.800000)
        entry.body_fat = 19.500000
        entry.heart_rate = 54.00
        entry.muscle_mass = 45.4
        entry.muscle_mass_percent = 48.9
        entry.bmr = 1572.00
        entry.water = 50.600000
        entry.body_fat_mass = 12.9
        entry.lean_body_mass = 50.44
        entry.bone_mass = 3
        entry.bone_mass_percentage = 4.600000
        entry.skeletal_muscle_mass = 36.6
        entry.subcutaneous_fat_percentage = 36.800000
        entry.visceral_fat_percentage =  24.000000
        entry.protein_percentage = 18.300000
        entry.body_age = 23.000000
        entry.body_type = "Average"
        entry.head_size = 0.0
        entries.append(entry)

        entry = convert_eufy.WeightEntry(time = datetime.datetime(2025, 1, 18, 8, 54, 8),
                                         weight = 33.2,
                                         bmi = 37.700000)
        entry.body_fat = 10.500000
        entry.heart_rate = 60.000000
        entry.muscle_mass = 32.4
        entry.muscle_mass_percent = 28.900000
        entry.bmr = 1571.000000
        entry.water = 30.600000
        entry.body_fat_mass = 32.8
        entry.lean_body_mass = 70.4
        entry.bone_mass = 3
        entry.bone_mass_percentage = 2.600000
        entry.visceral_fat_percentage =  44.000000
        entry.protein_percentage = 21.500000
        entry.skeletal_muscle_mass = 27.5
        entry.subcutaneous_fat_percentage = 12.700000
        entry.body_age = 73.0
        entry.body_type = "Average"
        entry.head_size = 0.0
        entries.append(entry)

        self.assertEqual(output[0], entries[0])
        self.assertEqual(output[1], entries[1])


if __name__ == '__main__':
    unittest.main()
