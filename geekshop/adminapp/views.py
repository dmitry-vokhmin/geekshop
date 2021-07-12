from authapp.models import ShopUser
from django.shortcuts import get_object_or_404, render
from mainapp.models import Product, ProductCategory
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.urls import reverse
from authapp.forms import ShopUserRegisterForm
from .forms import ShopAdminEditForm, ProductCategoryEditForm, ProductCategoryCreateForm


@user_passes_test(lambda user: user.is_superuser)
def users(request):
    title = 'админка/пользователи'

    users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')

    context = {
        'title': title,
        'objects': users_list
    }

    return render(request, 'adminapp/users.html', context)


def user_create(request):
    title = "пользователь/создать"

    if request.method == "POST":
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse("admin_staff:users"))
    else:
        user_form = ShopUserRegisterForm()
    context = {
        "title": title,
        "user_form": user_form
    }
    return render(request, "adminapp/user_create.html", context)


def user_update(request, pk):
    title = "пользователь/редактировать"

    edit_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == "POST":
        user_form = ShopAdminEditForm(request.POST, request.FILES, instance=edit_user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse("admin_staff:user_update", args=[edit_user.id]))
    else:
        user_form = ShopAdminEditForm(instance=edit_user)
    context = {
        "title": title,
        "user_form": user_form
    }
    return render(request, "adminapp/user_update.html", context)


def user_delete(request, pk):
    title = "пользователь/удаление"

    user = get_object_or_404(ShopUser, pk=pk)
    if request.method == "POST":
        user.is_deleted = True
        user.save()
        return HttpResponseRedirect(reverse("admin_staff:users"))
    context = {
        "title": title,
        "user_to_delete": user
    }
    return render(request, "adminapp/user_delete.html", context)


@user_passes_test(lambda user: user.is_superuser)
def categories(request):
    title = 'админка/категории'

    categories_list = ProductCategory.objects.all()

    context = {
        'title': title,
        'objects': categories_list
    }

    return render(request, 'adminapp/categories.html', context)


def category_create(request):
    title = "категории/создать"

    if request.method == "POST":
        category_form = ProductCategoryCreateForm(request.POST)
        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse("admin_staff:categories"))
    else:
        category_form = ProductCategoryCreateForm()
    context = {
        "title": title,
        "category_form": category_form
    }
    return render(request, "adminapp/category_create.html", context)


def category_update(request, pk):
    title = "категории/редактировать"

    edit_category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == "POST":
        category_form = ProductCategoryEditForm(request.POST, instance=edit_category)
        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse("admin_staff:category_update", args=[edit_category.id]))
    else:
        category_form = ProductCategoryEditForm(instance=edit_category)
    context = {
        "title": title,
        "category_form": category_form
    }
    return render(request, "adminapp/category_update.html", context)


def category_delete(request, pk):
    title = "категории/удаление"

    category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == "POST":
        category.is_deleted = True
        category.save()
        return HttpResponseRedirect(reverse("admin_staff:categories"))
    context = {
        "title": title,
        "category_to_delete": category
    }
    return render(request, "adminapp/category_delete.html", context)


@user_passes_test(lambda user: user.is_superuser)
def products(request, pk):
    title = 'админка/продукт'

    category = get_object_or_404(ProductCategory, pk=pk)
    products_list = Product.objects.filter(category__pk=pk).order_by('name')

    context = {
        'title': title,
        'category': category,
        'objects': products_list,
    }

    return render(request, 'adminapp/products.html', context)


def product_create(request, pk):
    pass


def product_read(request, pk):
    pass


def product_update(request, pk):
    pass


def product_delete(request, pk):
    pass
