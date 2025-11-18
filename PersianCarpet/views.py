from django import forms
from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
from django.utils.html import escape
import re
import logging

logger = logging.getLogger(__name__)


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    phone = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, max_length=5000)

    def clean_message(self):
        m = self.cleaned_data.get('message', '').strip()
        # Disallow dangerous tags
        if re.search(r'<\s*(script|iframe|object|embed|img)\b', m, re.I):
            logger.warning('Contact message rejected: disallowed HTML tag')
            raise forms.ValidationError('پیام حاوی تگ‌های نامعتبر است.')
        # Disallow common code patterns
        if re.search(r'(\<?php\b|\beval\s*\(|base64_decode\(|document\.cookie|window\.location|onerror\s*=|onload\s*=|javascript:)', m, re.I):
            logger.warning('Contact message rejected: code-like patterns')
            raise forms.ValidationError('پیام حاوی الگوهای کد یا مخرب است.')
        # Block ANY URLs or links
        urls = re.findall(r'https?://[^\s]+|www\.[^\s]+|ftp://[^\s]+', m, re.I)
        if urls:
            logger.warning('Contact message rejected: contains URLs %s', urls)
            raise forms.ValidationError('پیام نباید شامل لینک یا آدرس وب باشد.')
        # Detect long base64-like strings
        if re.search(r'([A-Za-z0-9+/]{100,}=*)', m):
            logger.warning('Contact message rejected: long base64-like string')
            raise forms.ValidationError('پیام حاوی محتوای رمزگذاری‌شده طولانی است.')
        # Detect possible sensitive financial data
        if re.search(r'\b(account|password|card number|iban|bank|رمز|کارت)\b', m, re.I) and re.search(r'\d{6,}', m):
            logger.warning('Contact message rejected: possible sensitive data')
            raise forms.ValidationError('پیام حاوی اطلاعات حساس است؛ لطفا اطلاعات خصوصی را وارد نکنید.')

        # Best-effort escape before returning
        return escape(m)


class ContactView(View):
    template_name = 'contact-us/m_index.html'

    def get(self, request):
        form = ContactForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ContactForm(request.POST)
        client_ip = request.META.get('REMOTE_ADDR')
        if form.is_valid():
            # TODO: send email or persist to DB. For now log the submission (without storing raw message)
            logger.info('Contact form submitted: name=%s email=%s ip=%s',
                        form.cleaned_data.get('name'),
                        form.cleaned_data.get('email'),
                        client_ip)
            # Redirect back with a success flag
            return redirect(reverse('contact') + '?sent=1')
        else:
            # log suspicious attempts at warning level
            logger.warning('Contact form validation failed from ip=%s errors=%s', client_ip, form.errors.as_json())
            return render(request, self.template_name, {'form': form})
