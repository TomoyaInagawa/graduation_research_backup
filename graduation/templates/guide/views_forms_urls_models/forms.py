import os

from django import forms
from django.core.mail import EmailMessage

from .models import *

class GuideCourseForm(forms.ModelForm):
    
    class Meta:
        #対象モデルを指定
        model = GuideCourse
        #入力する項目を指定
        fields = ('title', 'explanation' ,'start', 'picture', 'comment', 'stayTime', 'stayMinute')

class AddGuideCourseForm(forms.ModelForm):
    # フィールド名の先頭につけるプレフィックス
    # ※他のフォームと区別したい場合に使える
    # prefix = "rd"

    class Meta:
        #対象モデルを指定
        model = AddGuideCourse
        #入力する項目を指定
        fields = ('arrivalPoint', 'transportation', 'travelTime', 'travelMinute', 'picture', 'comment', 'stayTime', 'stayMinute')

# 予約明細フォームセット
# ※同じフォームを複数使いたいときに使える
# ※参照元と参照先をセットで扱いたいとき:inlineformset_factory
# 　単独で扱いたいとき:modeformset_factory
# 　単なるフォームの時:fomset_factory
ReserveDetailFormSet = forms.inlineformset_factory(
    GuideCourse,    # 参照先モデル
    AddGuideCourse,  # 参照元モデル
    fields = ('arrivalPoint', 'transportation', 'travelTime', 'travelMinute', 'picture', 'comment', 'stayTime', 'stayMinute'),   # 参照元モデルの入力項目 
    extra=1,    # 初期フォーム数
    can_delete=False    # 削除可能（Falseにする）
)