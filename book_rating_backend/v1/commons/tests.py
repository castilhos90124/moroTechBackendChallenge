from rest_framework.test import APITestCase


class CustomAPITestCase(APITestCase):

    def assertExpectedFields(self, expected_fields, response_data):
        self.assertTrue(self.__is_subset(expected_fields, response_data))

    @classmethod
    def __is_subset(cls, expected_fields, response_data):
        obtained = set(response_data.keys())
        expected = set(expected_fields)
        return obtained.issubset(expected) and expected.issubset(obtained)