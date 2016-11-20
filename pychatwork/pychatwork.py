import requests


class ChatworkClient:
    BASE_URL = 'https://api.chatwork.com/v1/'

    def __init__(self, token: str):
        """
        Set ChatWork's API token.
        """
        self._token = token

    def set_token(self, token: str):
        """
        Set another ChatWork's API token.
        """
        self._token = token

    def post_messages(self, message: str, room_id: int) -> dict:
        """
        Posts a message to a room.
        """
        res = requests.post(
            self._make_url('rooms/{}/messages'.format(room_id)),
            headers=self._make_headers(self._token),
            params=self._make_body(message)
            )
        return self._check_res(res)

    def get_messages(self, room_id: int, force: bool=False) -> list:
        """
        Gets new messages from a room.
        If you set force=True, you can get older messages.
        """
        forceflg = '?force=1' if force else '?force=0'
        res = requests.get(
            self._make_url('rooms/{}/messages'.format(room_id) + forceflg),
            headers=self._make_headers(self._token)
            )
        return self._check_res(res)

    def _make_url(self, endpoint):
        return self.BASE_URL + endpoint

    def _make_headers(self, token):
        if token is None:
            raise Exception('please set token')
        else:
            return {'X-ChatWorkToken': token}

    def _make_body(self, message):
        return {'body': message}

    def _check_res(self, res):
        if res.ok:
            return self._check_status_code(res)
        else:
            message = res.json()
            raise Exception(message['errors'])

    def _check_status_code(self, res):
        if res.status_code == 200:
            return res.json()
        elif res.status_code == 204:
            return []
        else:
            res.raise_for_status()
