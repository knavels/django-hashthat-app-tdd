from django.test import TestCase
from selenium import webdriver
from .form import HashForm
from .models import Hash
import hashlib

class FunctionalTestCase(TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.text = 'hello'
        self.hashed = '2CF24DBA5FB0A30E26E83B2AC5B9E29E1B161E5C1FA7425E73043362938B9824'.lower()

    def test_there_is_home_page(self):
        self.browser.get('http://localhost:8000')
        self.assertIn("Enter hash here:", self.browser.page_source)

    def test_hash_of_hello(self):
        self.browser.get('http://localhost:8000')
        text = self.browser.find_element_by_id('id_text')
        text.send_keys(self.text)
        self.browser.find_element_by_name('submit').click()
        self.assertIn(self.hashed, self.browser.page_source)

    def tearDown(self):
        self.browser.quit()


class UnitTestCase(TestCase):

    def setUp(self):
        self.text = 'hello'
        self.hashed = '2CF24DBA5FB0A30E26E83B2AC5B9E29E1B161E5C1FA7425E73043362938B9824'.lower()

    def test_home_homepage_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'hashing/home.html')

    def test_hash_form(self):
        form = HashForm(data={'text': self.text})
        self.assertTrue(form.is_valid)

    def test_hash_function_works_properly(self):
        text_hash = hashlib.sha256(self.text.encode('utf-8')).hexdigest()
        self.assertEqual(self.hashed, text_hash)

    def saveHash(self):
        hash = Hash()
        hash.text = self.text
        hash.hash = self.hashed
        hash.save()
        return hash

    def test_hash_object_working(self):
        hash = self.saveHash()

        pulled_hash = Hash.objects.get(hash=self.hashed)
        self.assertEqual(hash.text, pulled_hash.text)

    def test_viewing_hash(self):
        hash = self.saveHash()

        response = self.client.get('/hash/{}'.format(hash.hash))
        self.assertContains(response, hash.text)