import time
import jwt
from datetime import datetime

class BDToken(object):

    def __init__(self):
        self.secret = "IT666"
        self.alg = "HS256"
        self.expire_interval = 3600
        self.update_threshold = 1800

    def build_bd_token(self, user_id, username):
        header = {"alg": self.alg, "typ": "JWT"}
        payload = {"user_id": user_id, "username": username, "exp": int(time.time()) + self.expire_interval}

        bd_token = jwt.encode(headers=header, payload=payload, key=self.secret, algorithm=self.alg)

        return bd_token

    def get_user_id_from_bd_token(self, bd_token):
        try:
            payload = jwt.decode(bd_token, self.secret, algorithms=[self.alg], options={"verify_exp": True})

            user_id = payload.get("user_id")

            exp = payload.get("exp")
            now = int(time.time())

            if self.update_threshold > exp - now:
                username = payload.get("username")
                bd_token = self.build_bd_token(user_id, username)

            return user_id, bd_token, None

        except jwt.ExpiredSignatureError:
            return None, None, "token过期, 请重新登录"
        except jwt.InvalidTokenError:
            return None, None, "无效token"


if __name__ == '__main__':
    bd = BDToken()
    # a = bd.build_bd_token("123", "!@3")
    # print(a)

    b, c = bd.get_user_id_from_bd_token("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMTIzIiwidXNlcm5hbWUiOiIhQDMiLCJleHAiOjE2OTk2MjY0Mzd9.UUy86liX6VPEtoXL7Lncd2PMEnfvV-VqCoe8rOAEHGA")
