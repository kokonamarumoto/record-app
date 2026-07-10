from django.contrib import messages

from django.shortcuts import get_object_or_404,render, redirect

# Create your views here.
from django.views import View

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from .forms import DiaryForm, StudyRecordForm, StudyRecordItemForm, StudyRecordItemFormSet

from django.views.generic import ListView,DeleteView, UpdateView,CreateView,TemplateView

from django.db.models import Q

from django.forms import inlineformset_factory

from django.utils import timezone
from django.db.models import Sum
from .models import StudyRecord, StudyRecordItem
from datetime import date, datetime, timedelta

from datetime import date as dt_date

from django.urls import reverse_lazy
from .models import Diary, StudyRecord

class DiaryListView(LoginRequiredMixin,ListView):
    model = Diary
    template_name = 'record/diary_list.html'
    context_object_name = 'diaries'

    def get_queryset(self):
        queryset = Diary.objects.filter(user=self.request.user)
        keyword = self.request.GET.get('keyword')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        sort = self.request.GET.get('sort', 'date_desc')

        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword) |
                Q(content__icontains=keyword) |
                Q(location__icontains=keyword)
            )

        if start_date:
            queryset = queryset.filter(date__gte=start_date)

        if end_date:
            queryset = queryset.filter(date__lte=end_date)

        if sort == 'date_asc':
            queryset = queryset.order_by('date')

        elif sort == 'favorite_sort':
            queryset = queryset.order_by('-favorite', '-date')
        elif sort == 'favorite_only':
            queryset = queryset.filter(favorite=True).order_by('-date')
        else:
            queryset = queryset.order_by('-date')
 
        return queryset
    
    

class StudyRecordListView(LoginRequiredMixin,ListView):
    model = StudyRecord
    template_name = 'record/studyrecord_list.html'
    context_object_name = 'studyrecords'

    def get_queryset(self):
        
        queryset =  StudyRecord.objects.filter(user=self.request.user).prefetch_related('items')

        keyword = self.request.GET.get('keyword')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        sort = self.request.GET.get('sort', 'date_desc')


        if keyword:
            queryset = queryset.filter(
                Q(items__subject__icontains=keyword) |
                Q(memo__icontains=keyword)
            ).distinct()

        if start_date:
            queryset = queryset.filter(date__gte=start_date)

        if end_date:
            queryset = queryset.filter(date__lte=end_date)

    
        if sort == 'date_asc':
            queryset = queryset.order_by('date')
        elif sort == 'favorite_sort':
            queryset = queryset.order_by('-favorite', '-date')
        elif sort == 'favorite_only':
            queryset = queryset.filter(favorite=True).order_by('-date')
        else:
            queryset = queryset.order_by('-date')

        return queryset

class InputView(LoginRequiredMixin, View):
    def get(self, request):
        #URLからデータを取る
        date_str = request.GET.get('date')
        focus = request.GET.get('focus')
     
        #初期値を入れる箱
        diary_initial = {}
        study_initial = {}
     
        if date_str:
            try:
                parsed_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                diary_initial['date'] = parsed_date
                study_initial['date'] = parsed_date
            except ValueError:
                pass




        diary_form = DiaryForm(initial=diary_initial)
        study_form = StudyRecordForm(initial=diary_initial)
        item_forms = [StudyRecordItemForm(prefix=str(i)) for i in range(3)]
        return render(request, 'record/input.html', {
            'diary_form': diary_form,
            'study_form': study_form,
            'item_forms': item_forms,
            'diary_message': '',
            'study_message': '',
            'focus': focus,
            
        })


    def post(self, request):
        date_str = request.POST.get('date')
        focus = request.POST.get('focus')


        diary_form = DiaryForm()
        study_form = StudyRecordForm()
        item_forms = [StudyRecordItemForm(request.POST, prefix=str(i)) for i in range(3)]

        diary_message = ''
        study_message = ''

        if 'save_diary' in request.POST:
            diary_form = DiaryForm(request.POST, request.FILES)
            if diary_form.is_valid():
                diary = diary_form.save(commit=False)
                diary.user = request.user
                diary.save()
                messages.success(request, '日記を保存しました。')
                diary_form = DiaryForm()
            else:
                messages.error(request, '日記の入力に誤りがあります。')




        elif 'save_study' in request.POST:
            study_form = StudyRecordForm(request.POST)


            if study_form.is_valid() :
                study = study_form.save(commit=False)
                study.user = request.user
                study.save()


                saved_any = False
                error_message = None

                for i in range(1, 4):
                    subject = request.POST.get(f'subject{i}')
                    study_time = request.POST.get(f'study_time{i}')

                   # 両方空ならスキップ
                    if not subject and not study_time:
                     continue

                    # 片方だけ入力されてたらエラー扱い
                    if not subject or not study_time:
                     
                     error_message = '科目と学習時間はセットで入力してください。'
                     break
                   
                   # モデルを直接保存
                    StudyRecordItem.objects.create(
                        record=study,
                        subject=subject,
                        study_time=study_time
                    )
                    saved_any = True


               
                if error_message:
                    study.delete()
                    messages.error(request, error_message)
                elif saved_any:
                    messages.success(request, '学習記録を保存しました。')
                else:
                 study.delete()
                 messages.error(request, '科目と学習時間を1つ以上入力してください。')


            else:     
                messages.error(request, '学習記録の入力に誤りがあります。')

        return render(request, 'record/input.html', {
            'diary_form': diary_form,
            'study_form': study_form,
             'item_forms': item_forms,
            'diary_message': diary_message,
            'study_message': study_message,
            'focus': focus,
        })


class DiaryDeleteView(LoginRequiredMixin,DeleteView):
    model = Diary
    template_name = 'record/diary_delete.html'
    success_url = reverse_lazy('diary_list')


    def get_queryset(self):
        return Diary.objects.filter(user=self.request.user)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(request, '日記を削除しました。')
        return super().post(request, *args, **kwargs)
    
    def get_success_url(self):
        return self.request.GET.get('next') or reverse_lazy('diary_list')


class StudyRecordDeleteView(LoginRequiredMixin, DeleteView):
    model = StudyRecord
    template_name = 'record/studyrecord_delete.html'

    def get_queryset(self):
        return StudyRecord.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(request, '学習記録を削除しました。')
        return super().post(request, *args, **kwargs)
    

    def get_success_url(self):
        return self.request.GET.get('next') or reverse_lazy('studyrecord_list')

class StudyRecordItemDeleteView(LoginRequiredMixin, DeleteView):
    model = StudyRecordItem
    template_name = 'record/studyrecorditem_delete.html'

    def get_queryset(self):
        return StudyRecordItem.objects.filter(record__user=self.request.user)


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(request, '学習記録を削除しました。')
        return super().post(request, *args, **kwargs)
    

    def get_success_url(self):
        return self.request.GET.get('next') or reverse_lazy('studyrecord_list')



class DiaryUpdateView(LoginRequiredMixin,UpdateView):
    model = Diary
    fields = ['date', 'title', 'content', 'image', 'location', 'favorite']
    template_name = 'record/diary_update.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, '日記を更新しました。')
        return response
    def get_success_url(self):
        return self.request.GET.get('next') or reverse_lazy('diary_list')

class StudyRecordUpdateView(LoginRequiredMixin,UpdateView):
    model = StudyRecord
    fields = ['date', 'memo', 'favorite' ]
    template_name = 'record/studyrecord_update.html'
    def get_success_url(self):
        return self.request.GET.get('next') or reverse_lazy('studyrecord_list')

class StudyRecordUpdateView(LoginRequiredMixin, View):
    template_name = 'record/studyrecord_update.html'

    def get(self, request, pk):
        record = get_object_or_404(StudyRecord, pk=pk, user=request.user)
        form = StudyRecordForm(instance=record)
        formset = StudyRecordItemFormSet(instance=record)
        return render(request, self.template_name, {
            'form': form,
            'formset': formset,
        })

    def post(self, request, pk):
        record = get_object_or_404(StudyRecord, pk=pk, user=request.user)
        form = StudyRecordForm(request.POST, instance=record)
        formset = StudyRecordItemFormSet(request.POST, instance=record)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, '学習記録を更新しました。')
            return redirect(request.GET.get('next') or 'studyrecord_list')

        return render(request, self.template_name, {
            'form': form,
            'formset': formset,
        })

class RecordLoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('top')




class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')





class StudyDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'record/study_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        period = self.request.GET.get('period', 'all')

        today = timezone.now().date()
        first_day_of_month = today.replace(day=1)
        week_start = today - timedelta(days=today.weekday())
        first_day_of_year = today.replace(month=1, day=1)
       

        items = StudyRecordItem.objects.filter(record__user=user)

        context['monthly_total'] = items.filter(record__date__gte=first_day_of_month).aggregate(
            total=Sum('study_time')
        )['total'] or 0

        context['weekly_total'] = items.filter(record__date__gte=week_start).aggregate(
            total=Sum('study_time')
        )['total'] or 0

        context['yearly_total'] = items.filter(record__date__gte=first_day_of_year).aggregate(
            total=Sum('study_time')
        )['total'] or 0

        context['all_total'] = items.aggregate(
            total=Sum('study_time')
        )['total'] or 0


        if period == 'week':
            start_date = today - timedelta(days=6)
            items = items.filter(record__date__gte=start_date)
        elif period == 'month':
            start_date = today.replace(day=1)
            items = items.filter(record__date__gte=start_date)
        elif period == 'year':
            start_date = today.replace(month=1, day=1)
            items = items.filter(record__date__gte=start_date)

       

        subject_totals = (
            items.values('subject')
            .annotate(total=Sum('study_time'))
            .order_by('-total')
        )
        

        context['period'] = period
        context['subject_labels'] = [item['subject'] for item in subject_totals]
        context['subject_data'] = [item['total'] for item in subject_totals]


        return context



class DiaryAlbumView(LoginRequiredMixin, ListView):
    model = Diary
    template_name = 'record/diary_album.html'
    context_object_name = 'albums'

    def get_queryset(self):
        return Diary.objects.filter(
            user=self.request.user,
            image__isnull=False
        ).exclude(image='').order_by('-favorite','-date')


class ToggleFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        diary = get_object_or_404(Diary, pk=pk, user=request.user)
        diary.favorite = not diary.favorite
        diary.save()
        return redirect(request.META.get('HTTP_REFERER', 'diary_album'))

class ToggleStudyRecordFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        record = get_object_or_404(StudyRecord, pk=pk, user=request.user)
        record.favorite = not record.favorite
        record.save()
        return redirect(request.META.get('HTTP_REFERER', 'studyrecord_list'))

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'record/top.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        diary_dates = Diary.objects.filter(user=user).values_list('date', flat=True).distinct()
        study_dates = StudyRecord.objects.filter(user=user).values_list('date', flat=True).distinct()

        events = []

        for d in diary_dates:
            events.append({
                'title': '日記',
                'start': d.isoformat(),
                'color': '#4CAF50',
                  'url':f"/daily/{d.isoformat()}/",
            })

        for s in study_dates:
            events.append({
                'title': '学習',
                'start': s.isoformat(),
                'color': '#2196F3',
                'url': f"/daily/{s.isoformat()}/",
            })

        context['calendar_events'] = events
        return context


def daily_detail(request, date):
    year, month, day = map(int, date.split('-'))
    target_date = dt_date(year, month, day)
    diary = Diary.objects.filter(user=request.user, date=target_date).first()
    study_record = StudyRecord.objects.filter(user=request.user, date=target_date).first()
    study_records = StudyRecordItem.objects.filter(record__user=request.user, record__date=target_date)
    total_study_time = study_records.aggregate(total=Sum('study_time'))['total'] or 0


    return render(request, 'record/daily_detail.html', {
         
                'target_date': target_date,
        'diary': diary,
        'study_record': study_record,
        'study_records': study_records,
        'total_study_time': total_study_time,
    })


class StudyMemoAlbumView(LoginRequiredMixin, ListView):
   model = StudyRecord
   template_name = 'record/studymemo.html'
   context_object_name = 'records'

   def get_queryset(self):
        return StudyRecord.objects.filter(
            user=self.request.user
        ).prefetch_related('items').order_by('-favorite','-date')


class StudyRecordFavoriteToggleView(LoginRequiredMixin, View):
    def post(self, request, pk):
        record = get_object_or_404(StudyRecord, pk=pk, user=request.user)
        record.favorite = not record.favorite
        record.save()
        return redirect(request.POST.get('next') or 'study_memo')
