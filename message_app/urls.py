from django.urls import path
from . import views
from message_app.views import ClientListView, ClientCreateView, home_page, MessageListView, MailingListView, \
    ClientDetailView, ClientUpdateView, ClientDeleteView, MessageCreateView, MessageDetailView, MessageUpdateView, \
    MessageDeleteView, MailingCreateView, MailingUpdateView, MailingDeleteView, MailingDetailView

app_name = 'message_app'


urlpatterns = [
    path('', home_page),

    path('client_list/', ClientListView.as_view(), name='client_list'),
    path('client_list/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('client_update/<int:pk>', ClientUpdateView.as_view(), name='client_update'),
    path('client_delete/<int:pk>', ClientDeleteView.as_view(), name='client_delete'),
    path('client_crate/', ClientCreateView.as_view(), name='client_create'),

    path('message_crate/', MessageCreateView.as_view(), name='message_create'),
    path('message_list/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('message_update/<int:pk>', MessageUpdateView.as_view(), name='message_update'),
    path('message_delete/<int:pk>', MessageDeleteView.as_view(), name='message_delete'),
    path('message_list/', MessageListView.as_view(), name='message_list'),

    path('mailing_create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing_update/<int:pk>', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing_delete/<int:pk>', MailingDeleteView.as_view(), name='mailing_delete'),
    path('mailing_list/<int:pk>', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailing_list/', MailingListView.as_view(), name='mailing_list'),

    path('mailings/add_clients/<int:pk>', views.mailing_add_clients, name='mailing_add_clients'),
    path('mailings/<int:pk>/add_client/<int:client_id>',views.mailing_add_client, name='mailing_add_client'),
    path('mailings/<int:pk>/del_client/<int:client_id>', views.mailing_del_client, name='mailing_del_client'),


]