import requests

class zibalPlatform:

    def __init__(self, access_token):
        self.access_token = access_token


    def sendRequestToZibal(self, path, parameters=None):
        url = "https://api.zibal.ir/" + path
        bearerToken = "Bearer " + self.access_token
        headers = {"Authorization": bearerToken }

        if path=='v1/wallet/list':
            response = requests.get(url=url, headers=headers)
        else:
            response = requests.post(url=url, json=parameters, headers=headers)

        return response.json()


    def platform_result(self, result):
        switcher = {
            1: "موفق",
            2: "API Key به درستی ارسال نشده است.",
            3: "API Key صحیح نیست.",
            4: "اجازه دسترسی به این سرویس صادر نشده‌است.",
            5: "callbackUrl نامعتبر است.",
            6: "یکی از فیلدهای اجباری ارسال نشده‌است. (در message نام فیلد مشخص می‌شود)",
            7: "IP ارسال‌کننده درخواست نامعتبر می‌باشد.",
            8: "API Key غیرفعال است.",
            9: "حداقل مبلغ باید 1000 ریال باشد.",
            10: "کیف پول انتخاب شده وجود ندارد.",
            11: "مبلغ درخواستی از موجودی کیف پول بیشتر است.",
            12: "حداقل مبلغ تسویه 10000 ریال است.",
            13: "تاخیر تسویه از حد مجاز اکانت شما کمتر است.",
            14: "درخواست تسویه مورد نظر وجود ندارد.",
            15: "این مقدار تاخیر تسویه برای حساب کاربری شما مجاز نمی‌باشد.",
            16: "دسترسی این نوع درخواست تسویه برای کیف پول مورد نظر وجود ندارد.",
            17: "امکان ثبت درخواست تسویه آنی برای مبالغ بیشتر از 50 میلیون تومان وجود ندارد.",
            18: "مرچنت درگاه مورد نظر مورد یافت نشد و یا غیر فعال است.",
            20: "نام وارد نشده‌است.",
            21: "شماره شبای وارد شده نامعتبر است (شروع با IR و 26 کاراکتر)",
            22: "ذی‌نفع قبلا ثبت شده است.",
            23: "ذی‌نفع نامعتبر است.",
            24: "ذی‌نفع غیرفعال است.",
            25: "ذی‌نفع غیرفعال است.",
            26: "امکان انجام ریفاند وجود ندارد."
        }
        return switcher.get(result, "خطا در پرداخت")
