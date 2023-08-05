from onlinesimru.api import Api


class GetUser(Api):
    def balance(self):
        return self._get(f'/getBalance')

    def profile(self):
        return self._get(f'/getProfile', {'income': True})