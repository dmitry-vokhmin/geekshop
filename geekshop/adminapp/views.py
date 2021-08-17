from django.contrib.auth.decorators import user_passes_test
from django.db.models import F
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from .forms import ShopAdminEditForm, ProductCategoryEditForm, ProductCategoryCreateForm, ProductEditForm
from mainapp.models import Product, ProductCategory
from django.dispatch import receiver
from django.db.models.signals import pre_save


class UserListView(ListView):
    model = ShopUser
    template_name = "adminapp/users.html"
    context_object_name = "objects"
    paginate_by = 3

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context["title"] = "admin/users"
        return context

    def get_queryset(self):
        return ShopUser.objects.all().order_by('is_deleted', '-is_superuser', '-is_staff', 'username')


class UserCreateView(CreateView):
    model = ShopUser
    form_class = ShopUserRegisterForm
    template_name = "adminapp/user_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "user/create"
        return context

    def get_success_url(self):
        return reverse("admin_staff:users")


class UserUpdateView(UpdateView):
    model = ShopUser
    form_class = ShopAdminEditForm
    template_name = "adminapp/user_update.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "user/edit"
        return context

    def get_success_url(self):
        return reverse("admin_staff:user_update", kwargs={"pk": self.object.pk})


class UserDeleteView(DeleteView):
    model = ShopUser
    template_name = "adminapp/user_delete.html"

    def get_success_url(self):
        return reverse("admin_staff:users")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.is_deleted = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class CategoryListView(ListView):
    model = ProductCategory
    template_name = "adminapp/categories.html"
    ordering = ["is_deleted"]

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context["title"] = 'admin/categories'
        return context


class CategoryCreateView(CreateView):
    model = ProductCategory
    template_name = "adminapp/category_create.html"
    form_class = ProductCategoryCreateForm
    success_url = reverse_lazy("admin_staff:categories")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "category/create"
        return context


class CategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = "adminapp/category_update.html"
    form_class = ProductCategoryEditForm

    def get_success_url(self):
        return reverse("admin_staff:category_update", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "category/edit"
        return context

    def form_valid(self, form):
        if "discount" in form.cleaned_data:
            discount = form.cleaned_data["discount"]
            if discount:
                self.object.product_set.update(price=F("price") * (1 - discount / 100))
        return super().form_valid(form)


class CategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = "adminapp/category_delete.html"
    success_url = reverse_lazy("admin_staff:categories")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_deleted = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "category/delete"
        return context


class ProductsListView(ListView):
    model = Product
    template_name = "adminapp/products.html"

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context["title"] = 'admin/product'
        context["category"] = self.kwargs["pk"]
        return context

    def get_queryset(self):
        return Product.objects.filter(category__pk=self.kwargs["pk"]).order_by("is_deleted", "name")


class ProductCreateView(CreateView):
    model = Product
    template_name = "adminapp/product_create.html"
    form_class = ProductEditForm

    def get_success_url(self):
        return reverse("admin_staff:products", kwargs={"pk": self.object.category_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "product/create"
        context["category"] = self.kwargs["pk"]
        return context

    def get_initial(self):
        initial = super().get_initial()
        initial["category"] = ProductCategory.objects.filter(pk=self.kwargs["pk"]).get()
        return initial


class ProductDetailView(DetailView):
    model = Product
    template_name = "adminapp/product_read.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "product/details"
        return context


class ProductUpdateView(UpdateView):
    model = Product
    template_name = "adminapp/product_update.html"
    form_class = ProductEditForm

    def get_success_url(self):
        return reverse("admin_staff:products", kwargs={"pk": self.object.category_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "product/edit"
        return context


class ProductDeleteView(DeleteView):
    model = Product
    template_name = "adminapp/product_delete.html"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_deleted = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("admin_staff:products", kwargs={"pk": self.object.category_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "product/delete"
        return context


@receiver(pre_save, sender=ProductCategory)
def product_is_active_update_product_category_save(sender, instance, **kwargs):
    if instance.pk:
        if instance.is_deleted:
            instance.product_set.update(is_deleted=True)
        else:
            instance.product_set.update(is_deleted=False)
