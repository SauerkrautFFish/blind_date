import json


from django.shortcuts import render
from main.utils.token import BDToken


def bd_login(func):
    def wrapper(*args, **kwargs):
        req = args[0]
        bd_token = req.META.get("HTTP_BD_TOKEN", None)
        bd = BDToken()
        user_id, bd_token, err_msg = bd.get_user_id_from_bd_token(bd_token)
        if user_id is None:
            return render(req, "login.html", context={"message": err_msg})

        req.session["user_id"] = user_id
        response = func(req)
        response.set_cookie(key="bd_token", value=bd_token)
        return response

    return wrapper


def bd_post(func):
    def wrapper(req):
        if req.method != "POST":
            raise Exception("非POST请求")
        if req.content_type != "application/json":
            raise Exception("Content-Type不是application/json")
        try:
            req.session["post_data"] = json.loads(req.body)
        except Exception as e:
            raise Exception(str(e))

        return func(req)

    return wrapper


def bd_get(func):
    def wrapper(req):
        if req.method != "GET":
            raise Exception("非GET请求")

        return func(req)

    return wrapper
