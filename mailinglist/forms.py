from django import forms
from .models import *
from django.contrib.auth import get_user_model


class SubscriberForm(forms.ModelForm):
    mailing_list = forms.ModelChoiceField(queryset=MailingList.objects.all(), widget=forms.HiddenInput, disabled=True)

    class Meta:
        model = Subscriber
        fields = ['mailing_list', 'email']


class MessageForm(forms.ModelForm):
    mailing_list = forms.ModelChoiceField(queryset=MailingList.objects.all(), widget=forms.HiddenInput, disabled=True)

    class Meta:
        model = Message
        fields = ['mailing_list', 'subject', 'body']


class MailingListForm(forms.ModelForm):
    owner = forms.ModelChoiceField(queryset=get_user_model().objects.all(), widget=forms.HiddenInput, disabled=True)

    class Meta:
        model = MailingList
        fields = ['owner', 'name']
