# from django.shortcuts import render
from django.shortcuts import render

from django.db.models import Q

from django.shortcuts import redirect

import logging

from django.urls import reverse_lazy

from django.views import generic

from .forms import *

from django.contrib import messages

from .models import *
from .forms import *

import random, string

logger = logging.getLogger(__name__)

# Create your views here.
class IndexView(generic.TemplateView):
    template_name = "index.html"

# class GourmetView(generic.TemplateView):
#     template_name = "gourmet.html"

# class Gourmet_searchView(generic.TemplateView):
#     template_name = "gourmet_search.html"

class InquiryView(generic.FormView):
    template_name = "inquiry.html"
    form_class = InquiryForm
    success_url = reverse_lazy('graduation:inquiry')

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'メッセージを送信しました')
        logger.info('Inquiry sent by {}'.format(form.cleaned_data['name']))
        return super().form_valid(form)

class GourmetView(generic.TemplateView):
    template_name = "gourmet/gourmet.html"


class Gourmet_searchView(generic.ListView):
    model = Gourmet
    template_name = "gourmet/gourmet_search.html"
    context_object_name = 'gourmet_list'
    # paginate_by = 1

    def post(self, request):
        query = request.POST.get("search")
        type = request.POST.get("chiku")

        id_list = Gourmet.objects.values_list("id", flat=True)
        name_list = []
        category_list = []
        result_list = []

        if query:
            for val in id_list:
                if Gourmet.objects.filter(Q(id=val) , Q(name__contains=query)):
                    name_list.append(val)
            
        if type:
            if type != 'すべて':
                for val in id_list:
                    if Gourmet.objects.filter(Q(id=val) , Q(category__name=type)):
                        category_list.append(val)
                        
            else:
                for val in id_list:
                    if Gourmet.objects.filter(Q(id=val)):
                        category_list.append(val)
        
        category_set = set(category_list)
        name_set = set(name_list)
        if query:
            if type:
                result_set = category_set & name_set
            else:
                result_set = name_set
        
        else:
            if type:
                result_set = category_set
            else:
                pass

        if query or type:
            result_list = list(result_set)
            result = Gourmet.objects.filter(id__in=result_list)
        else:
            result = Gourmet.objects.none()
        
        params = {
            'gourmet_list' : result,
        }

        return render(request, 'gourmet/gourmet_search.html', params)


        
class Gourmet_detailView(generic.DetailView):
    template_name = "gourmet/gourmet_detail.html"
    model = Gourmet
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data_list = Gourmet.objects.filter(pk=self.kwargs['pk']) # pkを指定してデータを絞り込む
        context['gourmet'] = data_list
        return context
    # context_object_name = "gourmet_detail"

class ShopView(generic.TemplateView):
    template_name = "shop/shop.html"

class ShopListView(generic.ListView):
    template_name = "shop/shop_list.html"
    model = Store

    def post(self, request):
        result = Store.objects.none()

        name = request.POST.get("search")
        if name:
            result = Store.objects.filter(place__name__contains = name)

        janru = request.POST.get("genre")
        if janru:
            result = Store.objects.filter(subCategory__storeCategory__name__contains = janru)

        params = {
            'store' : result,
        }
        return render(request, 'shop/shop_list.html', params)

        template_name = "shop/shop_list.html"
        model = Storesubcategory




# class ShopShosaiView(generic.TemplateView):
#     template_name = "shop/shop_shosai.html"

# class ShopGourmetView(generic.TemplateView):
#     template_name = "shop/shop_gourmet.html"
    
class AccountView(generic.TemplateView):
    template_name = "account.html"

# allauthからSignupVIewをインポート
# このビューで入力内容のチェックを行う

from allauth.account.views import SignupView

# ユーザ登録ページ
class UserSignupView(SignupView):
    template_name="user_signup.html"
    form_class=UserSignupForm

def randomname(n):
   randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
   return ''.join(randlst)


class Guide_rearchView(generic.ListView):
    template_name = "guide/guide_rearch.html"
    context_object_name = "Place_list"
    model = Place

    def get_context_data(self, **kwargs):
        context = super(Guide_rearchView, self).get_context_data(**kwargs)
        context.update({
            'Transportation_list': Transportation.objects.all(),
        })
        return context

    def get_queryset(self):
        return Place.objects.all()

class Guide_rearch_resultView(generic.ListView):
    template_name = "guide/guide_rearch_result.html"
    model = GuideCourse

    def post(self, request):
        place = request.POST.getlist("place")
        time = request.POST.get("time")
        tp = request.POST.getlist("tp")
        result = GuideCourse.objects.none()

        if place or time or tp:
            if place and tp:
                filter1 = GuideCourse.objects.filter(Q(start__in=place) | Q(AddGuideCourse__arrivalPoint__in=place),
                    Q(AddGuideCourse__transportation__name__in=tp))
            elif place and not tp:
                filter1 = GuideCourse.objects.filter(Q(start__in=place) | Q(AddGuideCourse__arrivalPoint__in=place))
            elif not place and tp:
                filter1 = GuideCourse.objects.filter(Q(AddGuideCourse__transportation__name__in=tp))
            elif not place and not tp:
                filter1 = GuideCourse.objects.all()

            if time:
                if time == '～1時間':
                    time2 = 0
                elif time == '1～2時間':
                    time2 = 1
                elif time == '2～3時間':
                    time2 = 2
                elif time == '4～5時間':
                    time2 = 4
                elif time == '6～7時間':
                    time2 = 6
                elif time == '8～9時間':
                    time2 = 8
                elif time == '10～11時間':
                    time2 = 10
                elif time == '12時間～':
                    time2 = 12

                for x in filter1:
                    if time2 == 0:
                        if GuideCourse.getAllTime(x) < 60:
                            result = result | x
                    elif 0 < time2 and time2 < 12:
                        if time2*60 <= GuideCourse.getAllTime(x) and GuideCourse.getAllTime(x) < (time2 + 1)*60:
                            result = result | x
                    elif time2 == 12:
                        if 720 <= GuideCourse.getAllTime(x):
                            result = result | x
            elif not time:
                result = filter1
        elif not place and not time and not tp:
            result = GuideCourse.objects.all()

        params = {
            'place' : place,
            'time' : time,
            'tp' : tp,
            'guidecourse' : result,
        }
        return render(request, 'guide/guide_rearch_result.html', params)

FORM_NUM = 1      # フォーム数 formsetを使うやつ
FORM_VALUES = {}  # 前回のPOST値

class Guide_addView(generic.FormView):
    template_name = 'guide/guide_add.html'
    success_url = reverse_lazy('graduation:guide_list')
    MemberFormSet = forms.formset_factory(
        form=AddGuideCourseForm,
        extra=1,
        max_num=10,
    )
    form_class = MemberFormSet

    def get_context_data(self, **kwargs):
        context = super(Guide_addView, self).get_context_data(**kwargs)
        context.update({
            'form2': GuideCourse2Form(),
        })
        return context

    def get_form_kwargs(self):
    # デフォルトのget_form_kwargsメソッドを呼び出す
        kwargs = super().get_form_kwargs()
        # FORM_VALUESが空でない場合（入力中のフォームがある場合）、dataキーにFORM_VALUESを設定
        if FORM_VALUES:
            kwargs['data'] = FORM_VALUES
        return kwargs

    def post(self, request, *args, **kwargs):
        global FORM_NUM
        global FORM_VALUES
        # 追加ボタンが押された時の挙動
        print(request.POST)
        if 'add_button' in request.POST:
            FORM_NUM += 1    # フォーム数をインクリメント
            FORM_VALUES = request.POST.copy()  # リクエストの内容をコピー
            FORM_VALUES['form-TOTAL_FORMS'] = FORM_NUM   # フォーム数を上書き
        return super().post(request, args, kwargs)
        # return redirect('graduation:guide_add')

    def form_valid(self, form):
        form2 = GuideCourse2Form(self.request.POST,self.request.FILES)
        if form2.is_valid():
            obj=GuideCourse()
            obj_id=randomname(12)

            while True:
                if GuideCourse.objects.filter(id=obj_id).count() == 0:
                    break
                else:
                    obj_id = randomname(12)

            obj.id = obj_id
            obj.start=form2.cleaned_data['start']
            obj.comment=form2.cleaned_data['gc_comment']
            obj.picture=form2.cleaned_data['gc_picture']
            obj.stayTime=form2.cleaned_data['gc_stayTime']
            obj.stayMinute=form2.cleaned_data['gc_stayMinute']

            obj.author = self.request.user

            obj.save()

            formset = self.MemberFormSet(self.request.POST,self.request.FILES)
            for val in formset:
                val.guidecourse = obj
                val.save()
            messages.success(self.request, 'ガイドコースを登録しました')
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form)
        messages.error(self.request, "エラー")
        return redirect('graduation:guide_add')

class Guide_detailView(generic.DetailView):
    model = GuideCourse
    template_name = "guide/guide_detail.html"

class Guide_listView(generic.ListView):
    model = GuideCourse
    template_name = "guide/guide_list.html"

    def get_queryset(self):
        gc = GuideCourse.objects.all()
        return gc


class Guide_deleteView(generic.ListView):
    model = GuideCourse
    template_name = "guide/guide_list.html"

    def get_queryset(self):
        gc = GuideCourse.objects.all()
        return gc

class Guide_favoriteView(generic.TemplateView):
    template_name = "guide/guide_favorite.html"

class Guide_place_detailView(generic.DetailView):
    template_name = "guide/guide_place_detail.html"
    model = Place

class DBTestView(generic.CreateView):
    model = Place
    template_name = "guide/dbtest.html"
    form_class = PlaceForm
    success_url = reverse_lazy('graduation:dbtest')

    def form_valid(self, form):
        guidecourse = form.save(commit=False)
        guidecourse.save()
        messages.success(self.request, '追加されました')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "エラー")
        return super().form_invalid(form)


class PlacetestView(generic.ListView):
    template_name = "guide/placetest.html"
    model = Place

    def get_queryset(self):
        return Place.objects.all()

class Shop_detailView(generic.DetailView):
    model = Store
    template_name = "shop/shop_shosai.html"
# 利用規約
class Terms_of_serviceView(generic.TemplateView):
    template_name = "terms_of_service.html"
