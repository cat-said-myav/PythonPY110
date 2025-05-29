import json
import os
from app_store.models import DATABASE

PATH_WISHLIST = 'wishlist.json'


def view_in_wishlist(username: str = '') -> dict:
    """
    Просматривает содержимое корзины 'wishlist.json', если пользователя с именем username нет в корзине, то создает его там

    :param username: Имя пользователя
    :return: Содержимое 'wishlist.json'
    """
    empty_user_wishlist = {'products': []}

    if os.path.exists(PATH_WISHLIST):
        with open(PATH_WISHLIST, encoding='utf-8') as f:
            wishlist = json.load(f)
            if username not in wishlist:
                wishlist[username] = empty_user_wishlist
    else:
        wishlist = {username: empty_user_wishlist}

    with open(PATH_WISHLIST, mode='w', encoding='utf-8') as f:
        json.dump(wishlist, f)

    return wishlist

def add_to_wishlist(id_product: str, username: str = '') -> bool:
    """
    Добавляет продукт в избраное. Если в избраном нет данного продукта, то добавляет его.

    :param id_product: Идентификационный номер продукта в виде строки.
    :param username: Имя пользователя

    :return: Возвращает True в случае успешного добавления, а False в случае неуспешного добавления(товара по id_product
    не существует).
    """
    wishlist = view_in_wishlist(username)
    if DATABASE.get(id_product, None) is None:
        return False
    else:
        user_wishlist = wishlist[username]["products"]
        if id_product not in user_wishlist:
            user_wishlist.append(id_product)

    with open(PATH_WISHLIST, mode='w', encoding='utf-8') as f:
        json.dump(wishlist, f)
    return True


def remove_from_wishlist(id_product: str, username: str = '') -> bool:
    """
    Добавляет позицию продукта из избраного. Если в корзине есть такой продукт, то удаляется ключ в словаре
    с этим продуктом.

    :param id_product: Идентификационный номер продукта в виде строки.
    :param username: Имя пользователя

    :return: Возвращает True в случае успешного удаления, а False в случае неуспешного удаления(товара по id_product
    не существует).
    """
    wishlist = view_in_wishlist(username)
    user_wishlist = wishlist[username]["products"]
    if id_product not in user_wishlist:
        return False
    else:
        user_wishlist.remove(id_product)
    with open(PATH_WISHLIST, mode='w', encoding='utf-8') as f:
        json.dump(wishlist, f)
    return True


