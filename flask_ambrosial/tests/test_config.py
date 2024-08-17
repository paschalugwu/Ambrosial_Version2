#!/usr/bin/env python3
"""
Unit tests for the TestingConfig class in the flask_ambrosial.config module.
"""

import sys
import os
import unittest
from unittest.mock import patch

# Add the project root to the PYTHONPATH
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '../../')
    )
)

from flask_ambrosial.config import TestingConfig

class TestConfig(unittest.TestCase):
    """
    Test case for the TestingConfig class.
    """

    @patch.dict(os.environ, {
        'SECRET_KEY': os.environ.get('SECRET_KEY'),
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db',
        'EMAIL_USER': 'test@example.com',
        'EMAIL_PASS': 'password'
    })
    def test_config_values(self):
        """
        Test that the configuration values are correctly set.
        """
        self.assertEqual(
            TestingConfig.SECRET_KEY, os.environ.get('SECRET_KEY')
        )
        self.assertEqual(
            TestingConfig.SQLALCHEMY_DATABASE_URI, 'sqlite:///test.db'
        )
        self.assertEqual(
            TestingConfig.MAIL_USERNAME, 'test@example.com'
        )
        self.assertEqual(
            TestingConfig.MAIL_PASSWORD, 'password'
        )

if __name__ == '__main__':
    unittest.main()
