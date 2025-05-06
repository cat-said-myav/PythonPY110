from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import DATABASE
from logic.services import filtering_category
from logic.control_cart import view_in_cart, add_to_cart, remove_from_cart

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
                    with open(f'app_store/product/{page}.html', encoding="utf-8") as f:
                        return HttpResponse(f.read())
            return HttpResponse(status=404)
        elif isinstance(page, int):
            data = DATABASE.get(str(page))
            if data:
                with open(f'app_store/product/{data["html"]}.html', encoding="utf-8") as f:
                    return HttpResponse(f.read())
        return HttpResponse(status=404)

def shop_view(request):
    if request.method == "GET":
        with open("app_store/shop.html", encoding="utf-8") as f:
            data = f.read()
        return HttpResponse(data)

def cart_view_json(request):
    if request.method == "GET":
        username = ""
        data = view_in_cart(username)
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                     'indent': 4})


def cart_add_view_json(request, id_product):
    if request.method == "GET":
        username = ""
        result = add_to_cart(id_product, username)
        if result:
            return JsonResponse({"answer": "Продукт успешно добавлен в корзину"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное добавление в корзину"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})


def cart_del_view_json(request, id_product):
    if request.method == "GET":
        username = ""
        result = remove_from_cart(id_product, username)
        if result:
            return JsonResponse({"answer": "Продукт успешно удалён из корзины"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное удаление из корзины"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})
# Create your views here.
