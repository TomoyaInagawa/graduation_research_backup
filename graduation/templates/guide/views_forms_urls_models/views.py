# from django.shortcuts import render
import logging

from django.urls import reverse_lazy

from django.views import generic

from .forms import *

from django.contrib import messages

from .models import *

logger = logging.getLogger(__name__)

# Create your views here.
class IndexView(generic.TemplateView):
    template_name = "index.html"

from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import redirect

import random, string

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

        id_list = GuideCourse.objects.values_list("id", flat=True)
        place_list = []
        tp_list = []
        time_list = []
        result_list = []

        if place:
            for val in id_list:
                if GuideCourse.objects.filter(Q(id=val) , Q(start__name__in=place)):
                    place_list.append(val)
                else:
                    if AddGuideCourse.objects.filter(Q(guidecourse__id=val) , Q(arrivalPoint__name__in=place)):
                        place_list.append(val)
            place_set = set(place_list)
            
        if tp:
            for val in id_list:
                if AddGuideCourse.objects.filter(Q(guidecourse__id=val) , Q(transportation__name__in=tp)):
                    tp_list.append(val)
            tp_set = set(tp_list)

        if time:
            if time == '???1??????':
                time2 = 0
            elif time == '1???2??????':
                time2 = 1
            elif time == '2???3??????':
                time2 = 2
            elif time == '4???5??????':
                time2 = 4
            elif time == '6???7??????':
                time2 = 6
            elif time == '8???9??????':
                time2 = 8
            elif time == '10???11??????':
                time2 = 10
            elif time == '12?????????':
                time2 = 12
            
            for x in GuideCourse.objects.all():
                if time2 == 0:
                    if GuideCourse.getAllTime(x) < 60:
                        time_list.append(x.id)
                elif 0 < time2 and time2 < 12:
                    if time2*60 <= GuideCourse.getAllTime(x) and GuideCourse.getAllTime(x) < (time2 + 1)*60:
                        time_list.append(x.id)
                elif time2 == 12:
                    if 720 <= GuideCourse.getAllTime(x):
                        time_list.append(x.id)
            time_set = set(time_list)


        if place:
            if tp:
                if time:#ooo
                    result_set = place_set & tp_set & time_set
                else:#oox
                    result_set = place_set & tp_set
            else:
                if time:#oxo
                    result_set = place_set & time_set
                else:#oxx
                    result_set = place_set
        else:
            if tp:
                if time:#xoo
                    result_set = tp_set & time_set
                else:#xox
                    result_set = tp_set
            else:
                if time:#xxo
                    result_set = time_set
                else:#xxx
                    pass
                    
        if place or tp or time:
            result_list = list(result_set)
            result = GuideCourse.objects.filter(id__in=result_list)
        else:
            result = GuideCourse.objects.all()

        params = {
            'place' : place,
            'time' : time,
            'tp' : tp,
            'guidecourse' : result,
        }
        return render(request, 'guide/guide_rearch_result.html', params)

class Guide_addView(generic.TemplateView):
    template_name = 'guide/guide_add.html'
    success_url = reverse_lazy('graduation:guide_list')

        # ?????????????????????????????????????????????
    def post(self, request, *args, **kwargs):
        # ???????????????POST??????????????????????????????
        # ??????????????????????????????
        reserve_form=GuideCourseForm(request.POST, request.FILES)
        # ?????????????????????????????????????????????
        reserve_det_form=ReserveDetailFormSet(request.POST, request.FILES)

        # ??????????????????????????????????????????
        rf_is_valid=reserve_form.is_valid()
        rdf_is_valid=reserve_det_form.is_valid()

        # ???????????????????????????????????????
        if rf_is_valid and rdf_is_valid:
            # ???????????????????????????
            reserve=reserve_form.save(commit=False)
            reserve.author=self.request.user
            reserve.save()

            # ??????????????????????????????????????????
            reserve_det=reserve_det_form.save(commit=False)
            # ??????????????????????????????????????????????????????
            for rd in reserve_det:
                rd.guidecourse=reserve
                rd.save()

            return redirect(self.success_url)
        # ?????????????????????
        else:
            # ?????????????????????????????????????????????????????????????????????
            context = {
                'reserve_form': reserve_form,
                'reserve_det_form': reserve_det_form,
                'reserve_det_form_empty': ReserveDetailFormSet()
            }
            return render(request, self.template_name, context,)

    def get_context_data(self, **kwargs):
        ret = super().get_context_data(**kwargs)
        ret['reserve_form'] = GuideCourseForm()
        ret['reserve_det_form'] = ReserveDetailFormSet()
        # ??????????????????????????????????????????????????????????????????
        ret['reserve_det_form_empty'] = ReserveDetailFormSet()
        return ret


class Guide_detailView(generic.DetailView):
    model = GuideCourse
    template_name = "guide/guide_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        gc = GuideCourse.objects.get(pk=self.object.pk)
        user = GeneralUser.objects.get(customuser=self.request.user)
        gcl = GuideCourseLike.objects.filter(Q(generaluser=user), Q(guideCourse=gc))
        if gcl:
            context['favorite'] = True
        else:
            context['favorite'] = False
        return context


class Guide_listView(generic.ListView):
    model = GuideCourse
    template_name = "guide/guide_list.html"

    def get_queryset(self):
        return GuideCourse.objects.all()

    def post(self, request):
        sort = request.POST.get("sort")
        make = request.POST.get("make_select")
        name = request.POST.get("name_select")
        if sort == "0":
            if make == "0":
                result = GuideCourse.objects.order_by('addDateTime')
            elif make == "1":
                result = GuideCourse.objects.order_by('addDateTime').reverse()
        elif sort == "1":
            if name == "0":
                result = GuideCourse.objects.order_by('title')
            elif name == "1":
                result = GuideCourse.objects.order_by('title').reverse()
        params = {
            'guidecourse_list' : result,
        }
        return render(request, 'guide/guide_list.html', params)

class Guide_deleteView(generic.DeleteView):
    model = GuideCourse
    template_name = "guide/guide_delete.html"
    success_url = reverse_lazy('graduation:guide_list')

    #?????????????????????????????????
    def delete(self, request, *args, **kwargs):
        #???????????????????????????????????????
        #?????????????????????????????????????????????????????????????????????
        return super().delete(request, *args, **kwargs)

class Guide_favorite_listView(generic.ListView):
    model = GuideCourseLike
    template_name = "guide/guide_favorite_list.html"

    def get_queryset(self):
        user = GeneralUser.objects.get(customuser=self.request.user)
        return GuideCourseLike.objects.filter(generaluser=user)
    
    def post(self, request):
        sort = request.POST.get("sort")
        name = request.POST.get("name")
        user = GeneralUser.objects.get(customuser=self.request.user)

        if sort == 'search':
            result = GuideCourseLike.objects.filter(Q(generaluser=user),Q(guideCourse__title__contains=name))
        elif sort == 'register':
            result = GuideCourseLike.objects.filter(generaluser=user).order_by("pk")
        elif sort == 'name':
            result = GuideCourseLike.objects.filter(generaluser=user).order_by("guideCourse__title")
        else:
            result = GuideCourseLike.objects.filter(generaluser=user)
        params = {
            'object_list' : result,
        }
        return render(request, 'guide/guide_favorite_list.html', params)

def Guide_favoriteView(request, pk):
    gc = GuideCourse.objects.get(pk=pk)
    user = GeneralUser.objects.get(customuser=request.user)
    gcl = GuideCourseLike.objects.filter(Q(generaluser=user), Q(guideCourse=gc))
    if gcl:
        gcl.delete()
    else:
        favorite = GuideCourseLike(generaluser=user, guideCourse=gc)
        favorite.save()

    return redirect('graduation:guide_detail', pk=pk)

def Guide_favorite2View(request, pk):
    gc = GuideCourse.objects.get(pk=pk)
    user = GeneralUser.objects.get(customuser=request.user)
    gcl = GuideCourseLike.objects.filter(Q(generaluser=user), Q(guideCourse=gc))
    if gcl:
        gcl.delete()
    else:
        favorite = GuideCourseLike(generaluser=user, guideCourse=gc)
        favorite.save()

    return redirect('graduation:guide_favorite_list')


def Guide_place_favoriteView(request, pk):
    place = Place.objects.get(pk=pk)
    user = GeneralUser.objects.get(customuser=request.user)
    placelike = PlaceLike.objects.filter(Q(generalUser=user), Q(place=place))
    if placelike:
        placelike.delete()
    else:
        favorite = PlaceLike(generalUser=user, place=place)
        favorite.save()

    return redirect('http://127.0.0.1:8000/guide7/' + pk)

class Guide_place_detailView(generic.DetailView):
    template_name = "guide/guide_place_detail.html"
    model = Place

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        place = Place.objects.get(pk=self.object.pk)
        user = GeneralUser.objects.get(customuser=self.request.user)
        placelike = PlaceLike.objects.filter(Q(generalUser=user), Q(place=place))
        if placelike:
            context['favorite'] = True
        else:
            context['favorite'] = False
        return context