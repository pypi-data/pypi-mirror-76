from onlinesimru.api import Api


class GetFree(Api):
    def countries(self):
        return self._get(f'/getFreeCountryList')

    def numbers(self, country: int = 7):
        return self._get(f'/getFreePhoneList', {'country': country})

    def messages(self, phone: int, page: int = 1):
        return self._get(f'/getFreePhoneList', {'phone': phone, 'page': page})