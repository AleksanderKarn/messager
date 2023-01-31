from datetime import datetime
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView

from message_app.models import Client, Mailing, Message, MailingToClient, Attempt

from threading import Timer


def change_status():
    '''Функция для смены статуса
    рассылки с выполненной на запущенную при
    наступлении условия зависящего от периода каждой рассылки
    '''
    mail = Mailing.objects.all().filter(status='ended')
    for mailing in mail:

        if datetime.now().time() > mailing.time_mailing_start:
            continue
        if mailing.period_mailing == 'one_month' and datetime.now().day != 1:
            continue
        if mailing.period_mailing == 'one_month' and datetime.now().day != 1:
            continue

        mailing.status = Mailing.STATUS_RUN
        mailing.save()


def send_mailing(mailing):
    '''
    функция собирает айдишники клиентов указанных в рассылке
    собирает в список их емайлы и производит рассылку на основании полученных данных
    :param mailing:
    :return:
    '''
    client_ids = MailingToClient.objects.all().filter(mailing=mailing.id)
    ids = []
    for i in client_ids:
        ids.append(i.client)

    clients = Client.objects.all().filter(id__in=ids)
    client_email = []
    for client in clients:
        client_email.append(client.email)

    message = Message.objects.get(id=mailing.id_message_id)
    send_mail(
        subject=message.title,
        message=message.content,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=client_email
    )


def send_mails():
    '''
    функция берет все запущенные рассылки
    и проверяет время их завпуска и в случае если наступает период запуска рассылки
    она меняет статус рассылки на исполнена и формируект Attempt(попытку рассылки)
    :return:
    '''
    mailings = Mailing.objects.all().filter(status=Mailing.STATUS_RUN)
    for mailing in mailings:
        if datetime.now().time() > mailing.time_mailing_start:
            try:
                send_mailing(mailing)
                mailing.status = Mailing.STATUS_END
                mailing.save()
                answer = 200
                status_attempt = 'Успех'
            except:
                answer = 500
                status_attempt = 'Фейл'
            Attempt.objects.create(mailing_id=mailing.id, answer=answer, status_attempt=status_attempt)


def castomer_cron_for_windows():
    '''
    функция таймер запускающая скрипты через
     указанные промежутки времени
    :return:
    '''
    change_status()
    send_mails()
    nt = Timer(60, castomer_cron_for_windows)
    nt.start()


castomer_cron_for_windows()


def home_page(request):
    return render(request, 'home_page.html')


def mailing_add_clients(request, pk):
    clients_to_mailing = {}
    for client in MailingToClient.objects.all().filter(mailing=pk):
        clients_to_mailing[client.client] = client.mailing

    clients = []
    for client in Client.objects.all():
        if clients_to_mailing.get(client.id):
            is_add = True
        else:
            is_add = False
        clients.append({'id': client.id, 'name': client.full_name, 'email': client.email, 'is_add': is_add})
    context = {
        'mailing': Mailing.objects.get(id=pk),
        'client_list': clients,
    }
    return render(request, 'message_app/mailing_add_client_list.html', context)


def mailing_add_client(request, pk, client_id):
    if not MailingToClient.objects.all().filter(mailing=pk, client=client_id).exists():
        new_record = MailingToClient(mailing=pk, client=client_id)
        new_record.save()

    return redirect('message_app:mailing_add_clients', pk)


def mailing_del_client(request, pk, client_id):
    MailingToClient.objects.filter(mailing=pk, client=client_id).delete()
    return redirect('message_app:mailing_add_clients', pk)


####################################################################################################

                                ### CRUD для сущности Client
class ClientListView(ListView):
    model = Client


class ClientDetailView(DetailView):
    model = Client


class ClientCreateView(CreateView):
    model = Client
    fields = ['email', 'full_name', 'comment']
    success_url = reverse_lazy('message_app:client_list')


class ClientUpdateView(UpdateView):
    model = Client
    fields = ['email', 'full_name', 'comment']
    success_url = reverse_lazy('message_app:client_list')


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('message_app:client_list')

    ### CRUD для сущности Mailing


class MailingListView(ListView):
    model = Mailing


class MailingDetailView(DetailView):
    model = Mailing


class MailingCreateView(CreateView):
    model = Mailing
    fields = ['time_mailing_start', 'time_mailing_end', 'period_mailing', 'status', 'id_message']
    success_url = reverse_lazy('message_app:mailing_list')


class MailingUpdateView(UpdateView):
    model = Mailing
    fields = ['time_mailing_start', 'time_mailing_end', 'period_mailing', 'status', 'id_message']
    success_url = reverse_lazy('message_app:mailing_list')


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('message_app:mailing_list')

    ### CRUD для сущности Message


class MessageListView(ListView):
    model = Message


class MessageDetailView(DetailView):
    model = Message


class MessageCreateView(CreateView):
    model = Message
    fields = ['title', 'content']
    success_url = reverse_lazy('message_app:message_list')


class MessageUpdateView(UpdateView):
    model = Message
    fields = ['title', 'content']
    success_url = reverse_lazy('message_app:message_list')


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('message_app:message_list')
