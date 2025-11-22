from django.db import models
from django.utils import timezone


class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField()
    message = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=512, blank=True)
    processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} <{self.email}> ({self.created_at:%Y-%m-%d %H:%M})"


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    # simple pipe-separated specs shown in the template (e.g. "۳۰۰ شانه|تراکم ۹۶۰|پلی پروپیلین")
    specs = models.CharField(max_length=512, blank=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    featured = models.BooleanField(default=False)
    visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

    @property
    def specs_list(self):
        """Return specs as a list split on pipe character for templates to iterate."""
        if not self.specs:
            return []
        return [s.strip() for s in self.specs.split('|') if s.strip()]
