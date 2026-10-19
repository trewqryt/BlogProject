
from django.test import TestCase
from django.urls import reverse
from .models import Blog


class BlogTests(TestCase):

    def setUp(self):
        self.blog = Blog.objects.create(
            title="Test Blog",
            content="Test content"
        )

    # 1. List открывается
    def test_blog_list_status_code(self):
        response = self.client.get(reverse("blog_list"))
        self.assertEqual(response.status_code, 200)

    # 2. List содержит статью
    def test_blog_list_contains_content(self):
        response = self.client.get(reverse("blog_list"))
        self.assertContains(response, "Test Blog")
        self.assertContains(response, "Test content")

    # 3. У статьи есть ID
    def test_blog_has_id(self):
        self.assertIsNotNone(self.blog.id)

    # 4. Detail открывается
    def test_blog_detail_status_code(self):
        response = self.client.get(
            reverse("blog_detail", args=[self.blog.id])
        )
        self.assertEqual(response.status_code, 200)

    # 5. Несуществующая статья возвращает 404
    def test_blog_detail_wrong_id(self):
        response = self.client.get(
            reverse("blog_detail", args=[9999])
        )
        self.assertEqual(response.status_code, 404)

    # 6. Новая статья имеет 0 просмотров
    def test_new_blog_has_zero_views(self):
        blog = Blog.objects.create(
            title="New Blog",
            content="New content"
        )
        self.assertEqual(blog.views, 0)

    # 7. Первое открытие увеличивает просмотры до 1
    def test_blog_views_increase_after_detail(self):
        self.assertEqual(self.blog.views, 0)

        self.client.get(
            reverse("blog_detail", args=[self.blog.id])
        )

        self.blog.refresh_from_db()
        self.assertEqual(self.blog.views, 1)

    # 8. Два открытия дают 2 просмотра
    def test_blog_views_increase_twice(self):
        url = reverse("blog_detail", args=[self.blog.id])

        self.client.get(url)
        self.client.get(url)

        self.blog.refresh_from_db()
        self.assertEqual(self.blog.views, 2)
