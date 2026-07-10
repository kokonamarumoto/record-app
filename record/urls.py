from . import views

from django.urls import path




from .views import DiaryAlbumView, DiaryDeleteView, DiaryListView, DiaryUpdateView, HomeView, InputView, RecordLoginView, SignUpView, StudyDashboardView, StudyMemoAlbumView, StudyRecordDeleteView, StudyRecordFavoriteToggleView, StudyRecordItemDeleteView, StudyRecordListView, StudyRecordUpdateView, ToggleFavoriteView, ToggleStudyRecordFavoriteView


from django.contrib.auth.views import LogoutView


urlpatterns = [
    
     path("", HomeView.as_view(), name="top"),

     path('daily/<str:date>/', views.daily_detail, name='daily_detail'),

    

    path('diaries/', DiaryListView.as_view(), name='diary_list'),
    path('studyrecords/', StudyRecordListView.as_view(), name='studyrecord_list'),
    path('input/', InputView.as_view(), name='input'),


    path('diary/<int:pk>/favorite/', ToggleFavoriteView.as_view(), name='toggle_favorite'),

    path('studyrecords/<int:pk>/favorite/', ToggleStudyRecordFavoriteView.as_view(), name='toggle_studyrecord_favorite'),

    

    path('diaries/<int:pk>/delete/', DiaryDeleteView.as_view(), name='diary_delete'),
    path('studyrecords/<int:pk>/delete/', StudyRecordDeleteView.as_view(), name='studyrecord_delete'),
    path('studyrecord-items/<int:pk>/delete/', StudyRecordItemDeleteView.as_view(), name='studyrecorditem_delete'),

    path('diaries/<int:pk>/edit/', DiaryUpdateView.as_view(), name='diary_update'),
    path('studyrecords/<int:pk>/edit/', StudyRecordUpdateView.as_view(), name='studyrecord_update'),

    path('studydashboard/', StudyDashboardView.as_view(), name='study_dashboard'),

    path('study-memo-album/', StudyMemoAlbumView.as_view(), name='study_memo'),

    path('study-record/<int:pk>/favorite-toggle/', StudyRecordFavoriteToggleView.as_view(), name='study_record_favorite_toggle'),

    

    path('diary-album/', DiaryAlbumView.as_view(), name='diary_album'),
    
    path('login/', RecordLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page="login"), name='logout'),

     path('signup/', SignUpView.as_view(), name='signup'),
]
