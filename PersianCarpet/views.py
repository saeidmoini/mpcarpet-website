from django import forms
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from .models import ContactMessage, Product
from django.urls import reverse
from django.utils.html import escape
from django.core.exceptions import ValidationError
import re
import logging
import random

logger = logging.getLogger(__name__)


class SimpleCaptchaField(forms.CharField):
    """Simple math-based CAPTCHA field"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = "تائید: حاصل جمع را وارد کنید"
        self.help_text = ""
    
    def clean(self, value):
        value = super().clean(value)
        if not value:
            raise ValidationError("لطفا جواب کپچا را وارد کنید.")
        return value


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label="نام")
    phone = forms.CharField(max_length=30, required=False, label="شماره تلفن")
    email = forms.EmailField(required=True, label="ایمیل")
    message = forms.CharField(widget=forms.Textarea, max_length=5000, label="متن پیام")
    captcha_answer = SimpleCaptchaField(max_length=10, required=True)

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
        # Generate simple math CAPTCHA
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        captcha_answer = num1 + num2
        request.session['captcha_answer'] = captcha_answer
        request.session['captcha_question'] = f"{num1} + {num2}"
        
        return render(request, self.template_name, {
            'form': form,
            'captcha_question': request.session.get('captcha_question', '')
        })

    def post(self, request):
        form = ContactForm(request.POST)
        client_ip = request.META.get('REMOTE_ADDR')
        
        # Validate CAPTCHA
        captcha_answer = request.session.get('captcha_answer')
        user_answer = request.POST.get('captcha_answer', '').strip()
        
        captcha_valid = False
        try:
            if str(captcha_answer) == user_answer:
                captcha_valid = True
        except (ValueError, TypeError):
            pass
        
        if not captcha_valid:
            form.add_error('captcha_answer', 'جواب کپچا نادرست است.')
        
        if form.is_valid() and captcha_valid:
            # Persist submission to DB so it can be managed in admin
            try:
                ContactMessage.objects.create(
                    name=form.cleaned_data.get('name'),
                    phone=form.cleaned_data.get('phone', ''),
                    email=form.cleaned_data.get('email'),
                    message=form.cleaned_data.get('message'),
                    ip_address=client_ip,
                    user_agent=request.META.get('HTTP_USER_AGENT', '')
                )
            except Exception:
                logger.exception('Failed to persist contact message')
            logger.info('Contact form submitted: name=%s email=%s ip=%s',
                        form.cleaned_data.get('name'),
                        form.cleaned_data.get('email'),
                        client_ip)
            # Clear CAPTCHA from session
            request.session.pop('captcha_answer', None)
            request.session.pop('captcha_question', None)
            # Redirect back with a success flag
            return redirect(reverse('contact') + '?sent=1')
        else:
            # Regenerate CAPTCHA for new attempt
            num1 = random.randint(1, 10)
            num2 = random.randint(1, 10)
            new_captcha_answer = num1 + num2
            request.session['captcha_answer'] = new_captcha_answer
            request.session['captcha_question'] = f"{num1} + {num2}"
            
            # log suspicious attempts at warning level
            logger.warning('Contact form validation failed from ip=%s errors=%s', client_ip, form.errors.as_json())
            return render(request, self.template_name, {
                'form': form,
                'captcha_question': request.session.get('captcha_question', '')
            })


class ProductListView(ListView):
    model = Product
    template_name = 'products/m_index.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(visible=True).order_by('order', '-created_at')
