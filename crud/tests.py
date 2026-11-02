
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from .models import Product


class ProductCRUDTests(TestCase):

    def setUp(self):
        self.product = Product.objects.create(
            name="Laptop",
            price=Decimal("50000.00"),
            description="Lenovo laptop"
        )

    # 1. Создание товара
    def test_create_product(self):
        response = self.client.post(
            reverse("product_create"),
            {
                "name": "Phone",
                "price": "30000.00",
                "description": "Samsung phone"
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Product.objects.count(), 2)
        self.assertTrue(
            Product.objects.filter(name="Phone").exists()
        )

    # 2. Просмотр списка товаров
    def test_read_product(self):
        response = self.client.get(
            reverse("product_list")
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Laptop")

    # 3. Редактирование товара
    def test_update_product(self):
        response = self.client.post(
            reverse("product_update", args=[self.product.id]),
            {
                "name": "Updated Laptop",
                "price": "55000.00",
                "description": "Updated description"
            }
        )

        self.product.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.product.name, "Updated Laptop")
        self.assertEqual(
            self.product.price,
            Decimal("55000.00")
        )

    # 4. Удаление товара
    def test_delete_product(self):
        response = self.client.post(
            reverse("product_delete", args=[self.product.id])
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Product.objects.filter(id=self.product.id).exists()
        )

    # 5. Проверка модели товара
    def test_product_model(self):
        self.assertEqual(self.product.name, "Laptop")
        self.assertEqual(
            self.product.price,
            Decimal("50000.00")
        )
        self.assertEqual(str(self.product), "Laptop")

    # 6. Пустое название товара
    def test_create_product_empty_name(self):
        response = self.client.post(
            reverse("product_create"),
            {
                "name": "",
                "price": "1000.00",
                "description": "Test"
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Product.objects.count(), 1)

    # 7. Отрицательная цена
    def test_create_product_negative_price(self):
        response = self.client.post(
            reverse("product_create"),
            {
                "name": "Bad Product",
                "price": "-100.00",
                "description": "Invalid price"
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Product.objects.count(), 1)

    # 8. Несуществующий товар
    def test_update_nonexistent_product(self):
        response = self.client.get(
            reverse("product_update", args=[9999])
        )

        self.assertEqual(response.status_code, 404)

    # 9. Открытие формы создания
    def test_create_form_opens(self):
        response = self.client.get(
            reverse("product_create")
        )

        self.assertEqual(response.status_code, 200)

    # 10. GET-запрос не должен удалять товар
    def test_delete_get_does_not_remove_product(self):
        response = self.client.get(
            reverse("product_delete", args=[self.product.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            Product.objects.filter(id=self.product.id).exists()
        )
