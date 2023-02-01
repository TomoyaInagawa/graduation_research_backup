from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse_lazy
from .models import *
from graduation.models import *
import random

# allauthで提供される機能をカスタマイズするために使うクラス
#  @see https://itc.tokyo/django/customize-allauth-adapter/
#サインアップ時のユーザ登録処理を追加したり、ログイン後の移動先を変更したりできる
# @see https://github.com/pennersr/django-allauth/blob/master/allauth/account/adapter.py
class AccountAdapter(DefaultAccountAdapter):
    # サインアップ時のユーザ登録処理をオーバライド
    def save_user(self, request, user, form, commit=True):
        """
        This is called when saving user via allauth registration.
        We override this to set additional data on user object.
        """
        # Do not persist the user yet so we pass commit=False
        # (last argument)
        user = super(AccountAdapter, self).save_user(request, user, form, commit=False)

        # POSTで送信されたユーザタイプを設定
        user.userType = request.POST['user_type']

        if not user.userType:
            user.userType = 'consumer' # デフォルトのユーザ種別を設定

        # ユーザIDを取得するために一旦保存する
        user.save()

        # # ユーザタイプが店舗ユーザ
        # if user.userType == 'shopuser':
        #     # 店舗ユーザクラスのインスタンスを生成
        #     shopuser = ShopUser()
        #     # customuserフィールドにログインしているカスタムユーザを設定
        #     shopuser.customuser = user
        #     # shopフィールドに店舗クラスのデータを設定
        #     # 設定するデータは、formに入力された所属店舗
        #     shopuser.shop = form.cleaned_data['shop']
        #     # nameフィールドにformに入力された担当者名
        #     shopuser.name=form.cleaned_data['name']
        #     # saveメソッドでデータベースに保存
        #     shopuser.save()
        # # ユーザタイプが一般客ユーザ
        # else:
        #     # 一般客ユーザクラスのインスタンスを生成
        #     consumer = ConsumerUser()
        #     # customuserフィールドにログインしているカスタムユーザを設定
        #     consumer.customuser = user
        #     # nameフィールドにPOST送信された氏名を設定
        #     consumer.name = request.POST['consumer_name']
        #     # noフィールドにランダムに生成した数値を設定
        #     consumer.no=10000000+random.randint(1,10000)
        #     # pointsフィールドに初期値0を設定
        #     consumer.points=0
        #     # saveメソッドでデータベースに保存
        #     consumer.save()

    # ログイン後の移動先を指定するメソッド
    def get_login_redirect_url(self, request):
        # ログインしたユーザが店舗ユーザの場合
        # if request.user.userType=="shopuser":
        #     # 指定したURLにリダイレクト
        #     return reverse_lazy("sample_app:index")
        # # 店舗ユーザ以外（一般客ユーザ）の場合
        # else:
        #     # デフォルトのURLにリダイレクト
        #     return super().get_login_redirect_url(request)
        if request.user.userType=='customuser':
            return reverse_lazy("graduation:index")