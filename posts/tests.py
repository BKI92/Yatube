import time

from django.shortcuts import get_object_or_404
from django.test import TestCase, override_settings
from django.test import Client
from django.contrib.auth import get_user_model
from yatube import settings

from posts.models import Post, Group, Follow, Comment

User = get_user_model()


# Create your tests here.
class PostTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="sarah", email="connor.s@skynet.com", password="12345"
        )
        self.group = Group.objects.create(title='Test Group', slug='tg',
                                          description='testing group')
        self.post = Post.objects.create(text="Testing post.", author=self.user)

        self.user1 = User.objects.create_user(
            username="Василий", email="basil@yandex.ru",
            password="2444666668888888"
        )
        self.user2 = User.objects.create_user(
            username="terminator", email="Ill_be_back@yahoo.com",
            password="skynet"
        )

    def test_profile(self):
        self.client.force_login(self.user)
        response = self.client.get("/sarah/")
        self.assertEqual(response.status_code, 200)

    def test_new_post_for_authorized_user(self):
        self.client.force_login(self.user)
        response = self.client.get("/new/")
        self.assertEqual(response.status_code, 200)

    def test_add_post_from_authorized_user(self):
        self.client.force_login(self.user)
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

    @override_settings(CACHES=settings.TEST_CACHES)
    def test_edit_post_from_authorized_user(self):
        self.client.force_login(self.user)
        self.client.post("/new/", {
            "text": self.post.text})  # Создаем пост, который будем редактировать
        new_text = 'New testing text for post editing!'
        self.client.post(f"/{self.user.username}/{self.post.id}/edit/", {
            "text": new_text})
        response = self.client.get("/")
        self.assertContains(response, new_text)

    @override_settings(CACHES=settings.TEST_CACHES)
    def test_post_with_img(self):
        self.client.force_login(self.user)
        with open("media/posts/test.jpg", mode='rb') as image:
            self.client.post("/new/",
                             {"text": 'Testing post with image',
                              'image': image})
        post_id = Post.objects.last().id
        response = self.client.get(f"/{self.user.username}/{post_id}/")
        self.assertContains(response, 'img')

    @override_settings(CACHES=settings.TEST_CACHES)
    def test_post_with_img_everywhere(self):
        self.client.force_login(self.user)
        with open('media/posts/test.jpg', 'rb') as img:
            self.client.post('/new/', {'text': 'new text', 'image': img,
                                       'group': self.group.id})
        response_index = self.client.get(f"/")
        response_profile = self.client.get(f"/{self.user.username}/")
        response_group = self.client.get(f"/group/{self.group.slug}/")
        self.assertContains(response_index, 'img')
        self.assertContains(response_profile, 'img')
        self.assertContains(response_group, 'img')

    @override_settings(CACHES=settings.TEST_CACHES)
    def test_post_with_non_graphic_files(self):
        self.client.force_login(self.user)
        with open('manage.py', 'rb') as file:
            self.client.post('/new/', {'text': 'new text', 'image': file})
        post = Post.objects.last()
        with self.assertRaises(ValueError):
            post.image.open()

    def test_check_cache(self):
        self.client.force_login(self.user)
        self.client.post('/new/', {'text': 'new text for testing cash',
                                   'group': self.group.id})
        response = self.client.get("/")
        self.assertNotContains(response, 'new text for testing cash')
        time.sleep(20)
        response_2 = self.client.get("/")
        self.assertContains(response_2, 'new text for testing cash')

    @override_settings(CACHES=settings.TEST_CACHES)
    def test_follow_unfollow_authorized_user(self):
        self.client.force_login(self.user1)
        followers = Follow.objects.filter(author=self.user2.id).count()
        following = Follow.objects.filter(user=self.user1.id).count()
        self.assertEqual(followers, 0)
        self.assertEqual(following, 0)
        self.client.get(f"/{self.user2.username}/follow/")
        followers = Follow.objects.filter(author=self.user2).count()
        following = Follow.objects.filter(user=self.user1).count()
        self.assertEqual(followers, 1)
        self.assertEqual(following, 1)
        self.client.get(f"/{self.user2.username}/unfollow/")
        followers = Follow.objects.filter(author=self.user2).count()
        following = Follow.objects.filter(user=self.user1).count()
        self.assertEqual(followers, 0)
        self.assertEqual(following, 0)

    def test_check_new_post_from_follower(self):
        Follow.objects.create(user=self.user1, author=self.user2)
        self.client.force_login(self.user2)
        self.client.post("/new/", {"text": 'test follower text'})
        self.client.force_login(self.user1)
        response = self.client.get('/follow/')
        self.assertContains(response, 'test follower text')

    def test_authorized_user_comments_posts(self):
        self.client.force_login(self.user1)
        self.client.post(f'/{self.user.username}/{self.post.id}/comment/',
                         {'text': 'new comment'})
        comment = Comment.objects.filter(post=self.post.id).last().text
        self.assertEqual(comment, 'new comment')

    def tearDown(self):
        self.client.logout()
