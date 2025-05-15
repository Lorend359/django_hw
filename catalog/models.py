from django.db import models

class Category(models.Model):
    name = models.CharField("Наименование", max_length=150)
    description = models.TextField("Описание", blank=True)

    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Категория",
    )
    name = models.CharField("Наименование", max_length=200)
    description = models.TextField("Описание", blank=True)
    image = models.ImageField("Изображение", upload_to="products/", blank=True)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)

    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)
    is_published = models.BooleanField(
        "Опубликовано",
        default=False,
        help_text="Отметьте, если товар уже готов к показу на сайте",
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["-created_at"]
        permissions = [
            ("can_unpublish_product", "Может отменять публикацию товара"),
        ]

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField("Тип контакта", max_length=100)   # например, "E-mail", "Телефон"
    value = models.CharField("Данные", max_length=255)        # сам e-mail или номер телефона

    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"

    def __str__(self):
        return f"{self.name}: {self.value}"
