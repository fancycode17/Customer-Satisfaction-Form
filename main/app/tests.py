
from django.test import TestCase
from django.urls import reverse


class PageTests(TestCase):
    def test_homepage_loads(self):
        response = self.client.get(reverse("main"))

        self.assertEqual(response.status_code, 200)

    def test_success_page_loads(self):
        response = self.client.get(reverse("success"))

        self.assertEqual(response.status_code, 200)
