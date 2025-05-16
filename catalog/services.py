from django.core.cache import cache
from .models import Product

def products_for_category(cat_id: int, ttl: int = 300):
    """
    Возвращает *список* опубликованных товаров указанной категории,
    результат кешируется в Redis на `ttl` секунд.
    """
    key = f"category_products:{cat_id}"
    products = cache.get(key)
    if products is None:
        products = list(
            Product.objects
                   .filter(category_id=cat_id, is_published=True)
                   .select_related("category", "owner")
        )
        cache.set(key, products, ttl)
    return products