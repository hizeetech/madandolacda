from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='registration'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('events/', views.events, name='events'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('pay_levy/<int:levy_id>/', views.pay_levy, name='pay_levy'),
    path('committees/<int:committee_id>/', views.committee_detail, name='committee_detail'),
    path('adverts/', views.advert_list, name='advert_list'),
    path('adverts/<int:pk>/', views.advert_detail, name='advert_detail'),
    path('adverts/create/', views.create_advert, name='create_advert'),
    path('adverts/<int:advert_id>/submit_proposal/', views.submit_proposal, name='submit_proposal'),
    path('proposals/', views.proposal_list, name='proposal_list'),
    path('artisans/', views.artisans_list, name='artisans_list'),
    path('professionals/', views.professionals_list, name='professionals_list'),
    path('project_donations/', views.project_donations_list, name='project_donations_list'),
    path('project_donations/<int:donation_id>/upload_proof/', views.upload_donation_proof, name='upload_donation_proof'),
    path('executives/past/', views.past_executives, name='past_executives'),
    path('executives/present/', views.present_executives, name='present_executives'),
]