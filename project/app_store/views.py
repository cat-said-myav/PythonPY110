from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from .models import DATABASE
from logic.services import filtering_category
from logic.control_cart import view_in_cart, add_to_cart, remove_from_cart
from django.shortcuts import render,redirect
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required



def product_view_json(request):
    if request.method == "GET":
        id_ = request.GET.get("id")
        if id_:
            if DATABASE.get(id_, False) is not False:
                return JsonResponse(DATABASE[id_], json_dumps_params={'ensure_ascii': False,
                                                                'indent': 4})
            else:
                return HttpResponse("Данного продукта нет в базе данных")
        category_key = request.GET.get("category")
        if ordering_key := request.GET.get("ordering"):
            reverse = request.GET.get("reverse")
            if reverse and reverse.lower() == 'true':
                data = filtering_category(DATABASE, category_key, ordering_key, reverse=True)
            else:
                data = filtering_category(DATABASE, category_key, ordering_key)
        else:
            data = filtering_category(DATABASE, category_key)
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False,
                                                                 'indent': 4})
def product_page_view(request, page):
    if request.method == "GET":
        if isinstance(page, str):
            for data in DATABASE.values():
                if data['html'] == page:
                    data_other_products = list(filter(lambda x: x is not data,
                                                      filtering_category(DATABASE, data['category'])))[:5]
                    return render(request, 'app_store/product.html', context={'product': data,
                                                                              'other_products': data_other_products})

        elif isinstance(page, int):
            data = DATABASE.get(str(page))  # Получаем какой странице соответствует данный id
            if data:  # Если по данному page было найдено значение
                data_other_products = list(filter(lambda x: x is not data,
                                                  filtering_category(DATABASE, data['category'])))[:5]
                return render(request, 'app_store/product.html', context={'product': data,
                                                                          'other_products': data_other_products})

        return HttpResponse(status=404)


def shop_view(request):
    if request.method == "GET":
        category_key = request.GET.get("category")
        if ordering_key := request.GET.get("ordering"):
            if request.GET.get("reverse") in ('true', 'True'):
                data = filtering_category(DATABASE, category_key, ordering_key, True)
            else:
                data = filtering_category(DATABASE, category_key, ordering_key)
        else:
            data = filtering_category(DATABASE, category_key)
        return render(request, 'app_store/shop.html',
                      context={"products": data,
                               "category": category_key})

@login_required(login_url='app_login:login_view')
def cart_view_json(request):
    if request.method == "GET":
        username = get_user(request).username
        data = view_in_cart(username)
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                     'indent': 4})

@login_required(login_url='app_login:login_view')
def cart_add_view_json(request, id_product):
    if request.method == "GET":
        username = get_user(request).username
        result = add_to_cart(id_product, username)
        if result:
            return JsonResponse({"answer": "Продукт успешно добавлен в корзину"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное добавление в корзину"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})

@login_required(login_url='app_login:login_view')
def cart_del_view_json(request, id_product):
    if request.method == "GET":
        username = get_user(request).username
        result = remove_from_cart(id_product, username)
        if result:
            return JsonResponse({"answer": "Продукт успешно удалён из корзины"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное удаление из корзины"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})
@login_required(login_url='app_login:login_view')
def cart_view(request):
    if request.method == "GET":
        username = get_user(request).username
        data = view_in_cart(username)[username]

        products = []
        for product_id, quantity in data['products'].items():
            product = DATABASE[product_id]  # Получаем информацию о продукте
            product["quantity"] = quantity  # Реализуйте
            product["price_total"] = round(quantity * product['price_after'], 2)  # Реализуйте
            products.append(product)

        return render(request, "app_store/cart.html", context={"products": products})

def coupon_check_view(request, name_coupon):
    DATA_COUPON = {
        "coupon": {
            "discount": 10,
            "is_valid": True},
        "coupon_old": {
            "discount": 20,
            "is_valid": False},
    }
    if request.method == "GET":
        if name_coupon in DATA_COUPON.keys():
            return JsonResponse(DATA_COUPON[name_coupon], json_dumps_params={'ensure_ascii': False,
                                                                             'indent': 4})
        return HttpResponseNotFound("Неверный купон")

def delivery_estimate_view(request):
    DATA_PRICE = {
        "Россия": {
            "Москва": {"price": 90},
            "Санкт-Петербург": {"price": 78},
            "fix_price": 100,
        },
    }
    if request.method == "GET":
        data = request.GET
        country = data.get('country')
        city = data.get('city')
        if country in DATA_PRICE.keys():
            if city in DATA_PRICE[country].keys():
                return JsonResponse(DATA_PRICE[country][city], json_dumps_params={'ensure_ascii': False,
                                                                                  'indent': 4})
            else:
                return JsonResponse({"price":DATA_PRICE[country]["fix_price"]}, json_dumps_params={'ensure_ascii': False,
                                                                                  'indent': 4})
        return HttpResponseNotFound("Неверные данные")

def cart_buy_now_view(request, id_product):
    if request.method == "GET":
        username = get_user(request).username
        result = add_to_cart(id_product, username)
        if result:
            return redirect("app_store:cart_view")

        return HttpResponseNotFound("Неудачное добавление в корзину")

def cart_remove_view(request, id_product):
    if request.method == "GET":
        username = get_user(request).username
        result = remove_from_cart(id_product, username)  # TODO Вызвать функцию удаления из корзины
        if result:
            return redirect("app_store:cart_view") # TODO Вернуть перенаправление на корзину

        return HttpResponseNotFound("Неудачное удаление из корзины")

# Create your views here.
