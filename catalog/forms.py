from django import forms
from django.core.exceptions import ValidationError

from .models import Product

FORBIDDEN_WORDS = {
    "казино",
    "криптовалюта",
    "крипта",
    "биржа",
    "дешево",
    "бесплатно",
    "обман",
    "полиция",
    "радар",
}


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "image", "price", "category","is_published"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "is_published": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "image" in self.fields:
            self.fields["image"].label_suffix = ""

    def clean_name(self):
        name = self.cleaned_data["name"]
        lowered = name.lower()
        for bad in FORBIDDEN_WORDS:
            if bad in lowered:
                raise ValidationError(f"Поле «Наименование» не может содержать «{bad}»")
        return name

    def clean_description(self):
        desc = self.cleaned_data.get("description", "")
        lowered = desc.lower()
        for bad in FORBIDDEN_WORDS:
            if bad in lowered:
                raise ValidationError(f"Поле «Описание» не может содержать «{bad}»")
        return desc

    def clean_price(self):
        price = self.cleaned_data["price"]
        if price < 0:
            raise ValidationError("Цена не может быть отрицательной")
        return price

    def clean_image(self):
        """
        Дополнительное задание: проверяем формат и размер изображения.
        Поддерживаем как новый загруженный файл, так и уже существующий ImageFieldFile.
        """
        img = self.cleaned_data.get("image")
        if img is None or not hasattr(img, "content_type"):
            return img

        content_type = img.content_type
        size = img.size

        if content_type not in ("image/jpeg", "image/png"):
            raise ValidationError("Допускаются только JPEG и PNG изображения.")
        if size > 5 * 1024 * 1024:
            raise ValidationError("Размер изображения не должен превышать 5 МБ.")
        return img
