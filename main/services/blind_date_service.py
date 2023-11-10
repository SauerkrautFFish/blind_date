import hashlib

from main.models import User, Candidate, BlindDateRecord


class BlindDateService(object):

    @staticmethod
    def register_user(account, password, username):
        h_password = hashlib.md5(password.encode()).hexdigest()
        User.objects.create(User(account=account, password=h_password, username=username))
        # 如果account冲突?

    @staticmethod
    def user_login(account, password):
        h_password = hashlib.md5(password.encode()).hexdigest()
        query_set = User.objects.filter(account=account, password=h_password)
        if not query_set.exists():
            return None, None

        obj = query_set[0]
        return obj.id, obj.username

    @staticmethod
    def get_candidates_by_user(user_id):
        resp_list = []
        query_set = Candidate.objects.filter(user_id=user_id)

        for obj in query_set:
            resp_list.append(
                {"candidate_id": obj.id, "candidate_name": obj.name, "image_url": obj.image_url}
            )

        return resp_list

    @staticmethod
    def candidate_in_list(user_id, candidate_id):
        # 是否是该用户的候选人
        candidate_list = BlindDateService.get_candidates_by_user(user_id)
        if candidate_id not in candidate_list:
            return False

        return True

    @staticmethod
    def get_blind_date_record_by_candidate(candidate_id):
        query_set = BlindDateRecord.objects.filter(candidate_id=candidate_id)

        resp_dict = {"user_record": [], "candidate_record": []}
        if not query_set.exists():
            return resp_dict

        obj = query_set[0]
        resp_dict = {"user_record": obj.user_record, "candidate_record": obj.candidate_record}

        return resp_dict

    @staticmethod
    def create_or_update_blind_date_record_by_candidate(candidate_id, user_record, candidate_record):
        query_set = BlindDateRecord.objects.filter(candidate_id=candidate_id)

        # 不存在则创建
        if not query_set.exists():
            BlindDateRecord.objects.create(BlindDateRecord(candidate_id=candidate_id, user_record=user_record,
                                                           candidate_record=candidate_record))
            return

        # 存在则更新
        obj = query_set[0]
        obj.user_record = user_record
        obj.candidate_record = candidate_record
        obj.save()

