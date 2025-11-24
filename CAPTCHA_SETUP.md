# CAPTCHA Setup Guide for Contact Form

## Overview

A simple math-based CAPTCHA has been successfully integrated into your contact form (`contact-form`). This provides protection against bots and automated form submissions without requiring external API keys.

## Implementation Details

### How It Works

1. **Math Problem Generation**: When users visit the contact form, a simple math problem (e.g., "5 + 3") is generated
2. **Session Storage**: The correct answer is stored in the user's session
3. **User Input**: Users must solve the math problem and enter the answer
4. **Validation**: The form validates that the entered answer matches the stored answer
5. **Security**: The CAPTCHA regenerates on failed attempts

### What Was Changed

#### 1. **Views.py** (`PersianCarpet/views.py`)

- Added `SimpleCaptchaField` custom form field class
- Added `captcha_answer` field to `ContactForm`
- Updated `ContactView.get()` to generate and store CAPTCHA questions
- Updated `ContactView.post()` to validate CAPTCHA before accepting submissions
- CAPTCHA regenerates on validation failure

#### 2. **Template** (`PersianCarpet/templates/contact-us/m_index.html`)

- Added CAPTCHA input field displaying the math problem
- Form now has `id="contact-form"` for reference
- RTL-compatible layout with Persian labels

#### 3. **CSS Styling** (`PersianCarpet/static/contact-us/m_styles.css`)

- Added `.captcha-field` styles for the CAPTCHA container
- Light gray background to distinguish from other form fields
- Centered number input for clean appearance
- RTL-compatible label positioning

#### 4. **Settings** (`PersianCarpet/settings.py`)

- No external packages required (uses Django built-in features)
- Sessions middleware handles CAPTCHA storage

## Features

✅ **No External Dependencies**: Uses only Django built-in functionality
✅ **Session-Based**: Stores answers securely in user sessions
✅ **RTL Support**: Full support for Persian (RTL) layout
✅ **Simple & Effective**: Math-based approach is lightweight and user-friendly
✅ **Regenerates on Failure**: New CAPTCHA generated if answer is wrong
✅ **Error Messages**: Clear Persian error messages for incorrect answers

## How It Looks

Users will see:

```
5 + 3 = ؟
[Input field for answer]
```

## Security Features

1. **Server-Side Validation**: Answers validated on the server, not client-side
2. **Session Security**: Answers stored in secure session data
3. **Rate Limiting Ready**: Can be extended with rate limiting if needed
4. **No External API**: No dependency on third-party services

## Testing the Form

1. Navigate to the contact page
2. Fill in name, phone, email, and message
3. Solve the math CAPTCHA (e.g., if it shows "7 + 2 = ؟", enter "9")
4. Click submit
5. If CAPTCHA is correct → form submits successfully
6. If CAPTCHA is wrong → error message displayed and new CAPTCHA generated

## Form Validation Flow

1. **CAPTCHA Validation**: Check if user's answer matches stored answer
2. **CAPTCHA Failure**: Display error, regenerate new CAPTCHA
3. **Form Validation**: Check other form fields (name, email, message)
4. **Message Validation**: Additional checks for malicious content (existing)
5. **Success**: If all validations pass, form displays success message

## Customization

### Change CAPTCHA Difficulty

Edit `PersianCarpet/views.py` in the `ContactView.get()` method:

```python
# Current: 1-10 range
num1 = random.randint(1, 10)
num2 = random.randint(1, 10)

# Harder: 1-20 range
num1 = random.randint(1, 20)
num2 = random.randint(1, 20)

# Easier: 1-5 range
num1 = random.randint(1, 5)
num2 = random.randint(1, 5)
```

### Add Subtraction or Multiplication

In `ContactView.get()` and `ContactView.post()`, you can add more operations:

```python
import operator
operation = random.choice([operator.add, operator.sub, operator.mul])
captcha_answer = operation(num1, num2)
```

### Customize CAPTCHA Labels

Change the Persian text in `PersianCarpet/templates/contact-us/m_index.html`:

```html
<!-- Current -->
<label for="captcha_answer">{{ captcha_question }} = ؟</label>

<!-- Custom -->
<label for="captcha_answer">لطفا این سوال ریاضی را حل کنید: {{ captcha_question }} = ؟</label>
```

## Troubleshooting

### CAPTCHA Field Not Showing

- Check that `'django.contrib.sessions'` is in `INSTALLED_APPS` (it should be)
- Verify middleware includes `'django.contrib.sessions.middleware.SessionMiddleware'`
- Clear browser cache and try again

### "CAPTCHA Answer is Incorrect" Error When Correct

- Browser may have cached old session
- Clear cookies for the domain
- Try in an incognito/private browser window

### Math Problem Not Generating

- Ensure `random` module is imported in `views.py`
- Check that `get()` method is being called (visit form without POST)

## Production Considerations

1. **Session Backend**: Ensure sessions are properly configured (default is database)
2. **Session Security**: Verify `SESSION_COOKIE_SECURE = True` in production
3. **CSRF Protection**: CSRF token already included in form (keep it)
4. **Logging**: Form submissions are logged with IP addresses

## Performance

- **No Network Requests**: Completely server-side, no API calls
- **Minimal Database Impact**: Only uses Django's existing session storage
- **Fast Response Time**: Math problems load instantly

## Future Enhancements

If you later want to upgrade to Google reCAPTCHA v2:

1. Install: `pip install django-recaptcha`
2. Replace `SimpleCaptchaField` with `ReCaptchaField`
3. Add API keys to `.env`
4. Update template to render reCAPTCHA widget

The current implementation provides solid protection without external dependencies!

---

For more information about Django sessions and forms:

- [Django Sessions Documentation](https://docs.djangoproject.com/en/3.1/topics/http/sessions/)
- [Django Forms Documentation](https://docs.djangoproject.com/en/3.1/topics/forms/)
