from .models import Product, Category
from collections import defaultdict


class ProductService:
    """Класс для бизнес-логики работы с продуктами."""

    @staticmethod
    def get_products_by_category(category_id):
        """Возвращает список всех продуктов в указанной категории по её ID."""
        return Product.objects.filter(category_id=category_id)
