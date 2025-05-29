from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render,redirect
from logic.control_cart import view_in_cart

def login_view(request):
    if request.method == "GET":
        return render(request, "login/login.html")

    if request.method == "POST":
        data = request.POST  # Получаем данный из post запроса
        user = authenticate(username=data["username"], password=data["password"])  # Понимаем, что за пользователь перед нами
        if user:
            login(request, user)
            view_in_cart(user.username)
            return redirect("/")
        return render(request, "login/login.html", context={"error": "Неверные данные"})

def logout_view(request):
    if request.method == "GET":
        logout(request)  # Функция разлогинивает пользователя
        return redirect("/")