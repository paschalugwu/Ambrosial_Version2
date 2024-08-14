#!/usr/bin/env python3

import os
import unittest
from unittest.mock import patch, MagicMock
from flask_ambrosial.users.utils import save_picture

class TestUtils(unittest.TestCase):

    @patch('flask_ambrosial.users.utils.current_app')
    @patch('flask_ambrosial.users.utils.Image.open')
    def test_save_picture(self, mock_image_open, mock_current_app):
        # Mock the form_picture
        mock_form_picture = MagicMock()
        mock_form_picture.filename = 'test.jpg'
        
        # Mock current_app.root_path
        mock_current_app.root_path = '/fake/path'
        
        # Mock the Image.open and save methods
        mock_image = MagicMock()
        mock_image_open.return_value = mock_image
        
        # Call the function
        result = save_picture(mock_form_picture)
        
        # Assertions
        self.assertTrue(result.endswith('.jpg'))
        self.assertTrue(len(result) > len('.jpg'))
        mock_image.thumbnail.assert_called_with((125, 125))
        mock_image.save.assert_called_with(os.path.join('/fake/path', 'static/profile_pics', result))

if __name__ == '__main__':
    unittest.main()
