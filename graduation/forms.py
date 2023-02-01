import os

from django import forms
from django.core.mail import EmailMessage

from .models import *

class InquiryForm(forms.Form):
    name = forms.CharField(label="お名前", max_length=30)
    email = forms.EmailField(label="メールアドレス")
    title = forms.CharField(label="タイトル", max_length=30)
    message = forms.CharField(label="メッセージ", widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['placeholder'] = 'お名前をここに入力してください'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'メールアドレスをここに入力してください'
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['title'].widget.attrs['placeholder'] = 'タイトルをここに入力してください'
        self.fields['message'].widget.attrs['class'] = 'form-control'
        self.fields['message'].widget.attrs['placeholder'] = 'メッセージをここに入力してください'

    def send_email(self):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        title = self.cleaned_data['title']
        message = self.cleaned_data['message']

        subject = 'お問い合わせ {}'.format(title)
        message = '送信者名: {0}\nメールアドレス:{1}\nメッセージ:\n{2}'.format(name, email, message)
        from_email = os.environ.get('FROM_EMAIL')
        to_list = [
            os.environ.get('FROM_EMAIL')
        ]
        cc_list = [
            email
        ]

        message = EmailMessage(subject=subject, body=message, from_email=from_email, to=to_list, cc=cc_list)
        message.send()

# allauthからSignupFormをインポート
# このフォームでメールアドレスとパスワードを入力することができる

from allauth.account.forms import SignupForm

class UserSignupForm(SignupForm):
    name=forms.CharField(label="氏名", max_length=30)
    post=forms.CharField(label="郵便番号", max_length=7)
    address=forms.CharField(label="住所", max_length=100)
    age=forms.CharField(label="年齢")
    gendar = forms.fields.ChoiceField(
        choices = (
            ('XXXX', '男'),
            ('XXXX', '女'),
            ('XXXX', '未回答')
        ),
        label='性別',
        required=True,
        widget=forms.widgets.RadioSelect
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class GuideCourseForm(forms.ModelForm):
    
    class Meta:
        #対象モデルを指定
        model = GuideCourse
        #入力する項目を指定
        fields = ('start', 'picture', 'comment', 'stayTime', 'stayMinute')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #for文を使って全項目に同じクラス属性を設定
        #InquiryFormと同じように個別に設定するのがベスト
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class GuideCourse2Form(forms.Form):

    start = forms.ModelChoiceField(queryset=Place.objects.all())
    gc_picture = forms.ImageField()
    gc_comment = forms.CharField(widget=forms.Textarea)
    gc_stayTime = forms.IntegerField()
    gc_stayMinute = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #for文を使って全項目に同じクラス属性を設定
        #InquiryFormと同じように個別に設定するのがベスト
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class AddGuideCourseForm(forms.ModelForm):
    class Meta:
        #対象モデルを指定
        model = AddGuideCourse
        #入力する項目を指定
        fields = ('arrivalPoint', 'transportation', 'travelTime', 'travelMinute', 'picture', 'comment', 'stayTime', 'stayMinute')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class PlaceForm(forms.ModelForm):#場所
    class Meta:
        #対象モデルを指定
        model = Place
        #入力する項目を指定
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class DistrictForm(forms.ModelForm):#地区
    class Meta:
        #対象モデルを指定
        model = District
        #入力する項目を指定
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class TransportationForm(forms.ModelForm):#地区
    class Meta:
        #対象モデルを指定
        model = Transportation
        #入力する項目を指定
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
