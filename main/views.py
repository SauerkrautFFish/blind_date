from django.shortcuts import render

from main.services.blind_date_service import BlindDateService
from main.utils.bd_annotation import bd_login, bd_post
from logging import getLogger, INFO, ERROR, WARNING
from main.utils.constants import SUCCESS_CODE, ERR_CODE, BUSINESS_EXP_CODE, ERR_MSG
from main.utils.token import BDToken

logger = getLogger("main")


def login_html(req):
    return render(req, "login.html")


@bd_post
def register(req):
    try:
        # 获取参数
        post_data = req.session.get("post_data", {})
        account = post_data.get("re_account", None)
        password = post_data.get("re_password", None)
        username = post_data.get("re_username", None)
        print(account)
        print(password)
        print(username)
        # 简单校验
        if not all([account, password, username]):
            return {"code": BUSINESS_EXP_CODE, "message": "账号, 密码和用户名不能为空"}

        # 创建用户
        is_register = BlindDateService.register_user(account, password, username)
        if not is_register:
            return {"code": BUSINESS_EXP_CODE, "message": "注册失败, 账号重复"}

        return {"code": SUCCESS_CODE, "message": "注册成功!", "account": account}
    except Exception as e:
        logger.error(f"register err_msg: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"code": ERR_CODE, "message": ERR_MSG}


@bd_post
def login(req):
    try:
        # 获取参数
        post_data = req.session.get("post_data", {})
        account = post_data.get("account", None)
        password = post_data.get("password", None)

        # 获取候选人
        user_id, username = BlindDateService.user_login(account, password)
        if id is None:
            return {"code": BUSINESS_EXP_CODE, "message": "不存在该用户"}

        bd = BDToken()
        bd_token = bd.build_bd_token(user_id, username)

        return render(req, "main.html", context={"bd_token": bd_token})
    except Exception as e:
        logger.error(f"get_candidates err_msg: {str(e)}")
        return {"code": ERR_CODE, "message": ERR_MSG}


@bd_post
@bd_login
def get_candidates(req):
    try:
        # 获取参数
        user_id = req.session.get("user_id", None)

        # 获取候选人
        candidate_list = BlindDateService.get_candidates_by_user(user_id)
        return {"code": SUCCESS_CODE, "data": candidate_list}
    except Exception as e:
        logger.error(f"get_candidates err_msg: {str(e)}")
        return {"code": ERR_CODE, "message": ERR_MSG}


@bd_post
@bd_login
def get_candidate_record(req):
    try:
        # 获取参数
        post_data = req.session.get("post_data", {})
        user_id = req.session.get("user_id", None)
        candidate_id = post_data.get("candidate_id", None)

        # 判断是否是该用户的候选人
        if not BlindDateService.candidate_in_list(user_id, candidate_id):
            return {"code": BUSINESS_EXP_CODE, "message": "无权获取该候选人的数据"}
        # 获取候选人数据
        candidate_record = BlindDateService.get_blind_date_record_by_candidate(candidate_id)
        return {"code": SUCCESS_CODE, "data": candidate_record}
    except Exception as e:
        logger.error(f"get_candidates err_msg: {str(e)}")
        return {"code": ERR_CODE, "message": ERR_MSG}


@bd_post
@bd_login
def update_candidate_record(req):
    try:
        # 获取参数
        post_data = req.session.get("post_data", {})
        user_id = req.session.get("user_id", None)
        candidate_id = post_data.get("candidate_id", None)
        user_record = post_data.get("user_record", None)
        candidate_record = post_data.get("candidate_record", None)

        # 判断是否是该用户的候选人
        if not BlindDateService.candidate_in_list(user_id, candidate_id):
            return {"code": BUSINESS_EXP_CODE, "message": "无权更新该候选人的数据"}
        # 更新候选人数据
        BlindDateService.create_or_update_blind_date_record_by_candidate(candidate_id, user_record, candidate_record)

        return {"code": SUCCESS_CODE, "message": "更新成功"}
    except Exception as e:
        logger.error(f"update_candidate_record err_msg: {str(e)}")
        return {"code": ERR_CODE, "message": ERR_MSG}
