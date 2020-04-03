from django.test import TestCase
from django.test import Client
from django.contrib.auth import get_user_model

from posts.models import Post

User = get_user_model()


# Create your tests here.
class PostTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="sarah", email="connor.s@skynet.com", password="12345"
        )
        self.post = Post.objects.create(text="Testing post.", author=self.user)

    def test_profile(self):
        response = self.client.get("/sarah/")
        self.assertEqual(response.status_code, 200)

    def test_new_post_for_authorized_user(self):
        self.client.force_login(self.user)
        response = self.client.get("/new/")
        self.assertEqual(response.status_code, 200)

    def test_add_post_from_authorized_user(self):
        self.client.post("/new/", {"text": self.post.text})
        response_index = self.client.get("/")
        response_post = self.client.get(
            f"/{self.user.username}/{self.post.id}/")
        response_profile = self.client.get(f"/{self.user.username}/")
        self.assertContains(response_index, self.post)
        self.assertContains(response_post, self.post)
        self.assertContains(response_profile, self.post)

    def test_new_post_for_unauthorized_user(self):
        response = self.client.get("/new/", follow=True)
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.redirect_chain[0][0],
                         '/auth/login/?next=/new/')

    def test_edit_post_from_authorized_user(self):
        self.client.force_login(self.user)
        self.client.post("/new/", {
            "text": self.post.text})  # Создаем пост, который будем редактировать
        new_text = 'New testing text for post editing!'
        self.client.post(f"/{self.user.username}/{self.post.id}/edit/", {
            "text": new_text})
        response = self.client.get("/")
        self.assertContains(response, new_text)

    def tearDown(self):
        self.client.logout()
