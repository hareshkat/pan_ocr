import unittest
from app import app
import io

class PanOcrTests(unittest.TestCase):
    def test_site_access(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_upload_text_file(self):
        tester = app.test_client(self)
        file_name = "dummy_text_file.txt"
        data = {
            'file': (io.BytesIO(b"This is test file"), file_name)
        }
        response = tester.post('/', data=data)
        self.assertEqual(response.status_code, 400)

    def test_upload_image_file(self):
        tester = app.test_client(self)
        image = "static/pancard.jpg"
        data = {
            'file': (open(image, 'rb'), image)
        }
        response = tester.post('/', data=data)
        self.assertEqual(response.status_code, 201)


if __name__ == "__main__":
    unittest.main()
