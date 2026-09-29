import unittest

from lambda_handler import ConfigurationError, invalidation_target


class InvalidationSwitchTest(unittest.TestCase):
    def test_off_by_default_even_with_a_distribution(self):
        self.assertIsNone(invalidation_target({}))
        self.assertIsNone(invalidation_target({"CLOUDFRONT_DISTRIBUTION_ID": "E123"}))
        self.assertIsNone(invalidation_target({"CLOUDFRONT_DISTRIBUTION_ID": "E123", "CLOUDFRONT_INVALIDATE": "0"}))

    def test_on_only_with_1(self):
        env = {"CLOUDFRONT_DISTRIBUTION_ID": " E123 ", "CLOUDFRONT_INVALIDATE": "1"}
        self.assertEqual(invalidation_target(env), "E123")

    def test_on_without_a_distribution_is_a_configuration_error(self):
        with self.assertRaises(ConfigurationError):
            invalidation_target({"CLOUDFRONT_INVALIDATE": "1"})
