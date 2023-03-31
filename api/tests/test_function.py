import unittest

from module.driveTime.moduleMarketingProfiling import inputData

class TestInputData(unittest.TestCase):
    def test_inputData_with_valid_input(self):
        match = [1, 2, 3]
        expected_output = "'1','2','3'"
        self.assertEqual(inputData(match), expected_output)
    
    def test_inputData_with_empty_input(self):
        match = []
        expected_output = ""
        self.assertEqual(inputData(match), expected_output)
    
    def test_inputData_with_multiple_types_of_input(self):
        match = [1, '2', 3.0, "4"]
        expected_output = "'1','2','3.0','4'"
        self.assertEqual(inputData(match), expected_output)

