import shutil
import tempfile

from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.cache import cache

from posts.forms import PostForm, CommentForm
from posts.models import Post, Comment


TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
User = get_user_model()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostModelTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(
            username='HasNoName'
        )
        image = SimpleUploadedFile(
            'post_image.jpg',
            content=(
                b'\x47\x49\x46\x38\x39\x61\x02\x00'
                b'\x01\x00\x80\x00\x00\x00\x00\x00'
                b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
                b'\x00\x00\x00\x2C\x00\x00\x00\x00'
                b'\x02\x00\x01\x00\x00\x02\x02\x0C'
                b'\x0A\x00\x3B'
            ),
            content_type='image/jpg')
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.author,
            image=image,
        )

        cls.form = PostForm()
        cls.form = CommentForm()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        cache.clear()
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.author)

    def test_post_create_guest_client(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый текст',
        }
        response = self.guest_client.post(
            reverse('posts:create_post'),
            data=form_data,
            follow=True
        )
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertRedirects(response, reverse(
            'users:login') + '?next=' + reverse('posts:create_post'))

    def test_create_post(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый текст',
            'image': self.post.image,
        }
        response = self.authorized_client.post(
            reverse('posts:create_post'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse(
            'posts:profile', args=[self.author]))
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(
            Post.objects.filter(
                text=self.post.text,
                author=self.author,
                image='posts/post_image.jpg'
            ).exists()
        )

    def test_edit_post(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый текст',
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}),
            data=form_data,
            follow=True
        )
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertRedirects(response, reverse(
            'posts:post_detail', kwargs={'post_id': self.post.id}))
        self.assertTrue(
            Post.objects.filter(
                text=self.post.text,
                author=self.author,
            ).exists()
        )

    # def test_cached_post(self):
    #     cache.clear()
    #     posts_count = Post.objects.count()
    #     form_data = {
    #         'text': 'Тестовый текст',
    #     }
    #     response = self.authorized_client.post(
    #         reverse('posts:index'),
    #         data=form_data,
    #         follow=True
    #     )
    #     cache.clear()
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(Post.objects.count(), posts_count + 1)
        # cache.clear()
        # response = self.authorized_client.post(
        #     reverse('posts:index'),
        #     data=form_data,

        # # )
        # self.assertEqual(response.status_code, 200)
        # self.assertEqual(Post.objects.count(), posts_count + 1)



    # def test_comment_post(self):
    #     comment_count = Comment.objects.count()
    #     form_data = {
    #         'text': self.comment.text,
    #     }
    #     response = self.authorized_client.post(
    #         reverse('posts:post_detail', kwargs={'post_id': self.post.id}),
    #         data=form_data,
    #         follow=True
    #     )
    #     self.assertRedirects(response, reverse(
    #         'posts:post_detail', kwargs={'post_id': self.post.id}))
    #     self.assertEqual(Comment.objects.count(), comment_count + 1)
    #     self.assertTrue(
    #         Comment.objects.filter(
    #             text=self.post.text,
    #             author=self.author,
    #         ).exists()
    #     )

    # def test_comment_create_guest_client(self):
    #     posts_count = Post.objects.count()
    #     comment_count = Comment.objects.count()
    #     form_data = {
    #         'text': self.comment.text,
    #     }
    #     response = self.guest_client.post(
    #         reverse('posts:post_detail', kwargs={'post_id': self.post.id}),
    #         data=form_data,
    #         follow=True
    #     )
    #     self.assertEqual(Post.objects.count(), posts_count)
    #     self.assertEqual(Comment.objects.count(), comment_count)
    #     self.assertRedirects(response, reverse(
    #         'users:login') + '?next=' + reverse('posts:create_post'))
