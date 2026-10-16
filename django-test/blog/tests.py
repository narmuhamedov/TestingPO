from django.test import TestCase, Client
from django.urls import reverse
from blog.models import Blog

class BlogTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.blog = Blog.objects.create(
            title = 'Тестовый заголовок',
            description = 'Тестовое описание для проверки блога',
            image = 'blog/test_image.jpg',
            author = "Тестовый Автор"
        )
    def test_blog_model_creation(self):
        self.assertEqual(self.blog.title, 'Тестовый заголовок')
        self.assertEqual(self.blog.author, 'Тестовый Автор')

        self.assertEqual(str(self.blog), 'Тестовый заголовок')

    def test_blog_list_view(self):
        url = reverse('blog_list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'blog_list.html')

        self.assertContains(response, 'Тестовый заголовок')

    def test_blog_detail_not_found(self):
        url = reverse('blog_detail', args=[999])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_author_display_with_rank(self):
        default_blog = Blog.objects.create(
            title = 'Пост Иванова',
            description = 'Текст....',
            image = 'blog/test.jpg'
        )
        url = reverse('blog_detail', args=[default_blog.id])
        response = self.client.get(url)

        self.assertContains(response, "Ivanov Ivan (Главный редактор)")

    def test_blog_detail_server_error(self):
        url = reverse('blog_detail', args=[self.blog_id])
        response = self.client.get(url, raise_request_exception=False)
        self.assertEqual(response.status_code, 500)