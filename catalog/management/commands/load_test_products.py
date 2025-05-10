from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Category, Product
from django.conf import settings
from pathlib import Path

class Command(BaseCommand):
    help = "Перезаливает тестовые категории и товары из fixtures/initial_data.json"

    def handle(self, *args, **options):
        self.stdout.write("⚙️  Очищаем старые данные…")
        Product.objects.all().delete()
        Category.objects.all().delete()

        fixture_path = Path(settings.BASE_DIR) / "catalog" / "fixtures" / "initial_data.json"
        self.stdout.write(f"📥  Загружаем данные из {fixture_path.name}…")
        call_command("loaddata", fixture_path)

        self.stdout.write(self.style.SUCCESS("✅ Данные успешно загружены!"))
