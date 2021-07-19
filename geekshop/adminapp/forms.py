from authapp.forms import ShopUserEditForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product
from django import forms


class ShopAdminEditForm(ShopUserEditForm):
    class Meta:
        model = ShopUser
        fields = ("username", "first_name", "email", "age", "avatar", "is_active", "is_deleted")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == "is_active" or field_name == "is_deleted":
                field.widget.attrs["style"] = "-webkit-appearance: auto;"
            field.widget.attrs["class"] = "form-control"
            field.help_text = ""
            if field_name == "password":
                field.widget = forms.HiddenInput()


class ProductCategoryEditForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == "is_deleted":
                field.widget.attrs["style"] = "-webkit-appearance: auto;"
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class ProductCategoryCreateForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = "name", "description"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class ProductEditForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == "is_deleted":
                field.widget.attrs["style"] = "-webkit-appearance: auto;"
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
