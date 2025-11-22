from django.core.management.base import BaseCommand
from django.utils.text import slugify
from PersianCarpet.models import Product


class Command(BaseCommand):
    help = 'Add sample products to the database'

    def handle(self, *args, **options):
        sample_products = [
            {
                'title': 'فرش آذین',
                'description': 'فرشی با طراحی مدرن و رنگ‌های زیبا',
                'specs': '۳۰۰ شانه|تراکم ۹۶۰|پلی پروپیلین',
                'visible': True,
                'featured': True,
                'order': 1,
            },
            {
                'title': 'فرش نیما',
                'description': 'فرش با کیفیت بالا و دوام طولانی',
                'specs': '۵۰۰ شانه|تراکم ۱۲۰۰|ابریشم',
                'visible': True,
                'featured': True,
                'order': 2,
            },
            {
                'title': 'فرش مهناز',
                'description': 'فرشی سنتی با نقش‌های اصیل',
                'specs': '۴۰۰ شانه|تراکم ۱۰۸۰|پنبه و پلی استر',
                'visible': True,
                'featured': False,
                'order': 3,
            },
            {
                'title': 'فرش زیبا',
                'description': 'فرش دستباف با کیفیت فاخر',
                'specs': '۶۰۰ شانه|تراکم ۱۴۴۰|ابریشم و پنبه',
                'visible': True,
                'featured': False,
                'order': 4,
            },
            {
                'title': 'فرش مریم',
                'description': 'فرش مقرون به صرفه و پائدار',
                'specs': '۲۰۰ شانه|تراکم ۷۲۰|پلی پروپیلین',
                'visible': True,
                'featured': False,
                'order': 5,
            },
            {
                'title': 'فرش رستگار',
                'description': 'فرش برای اتاق‌های بزرگ',
                'specs': '۴۵۰ شانه|تراکم ۱۲۰۰|ابریشم',
                'visible': True,
                'featured': False,
                'order': 6,
            },
        ]

        created_count = 0
        for product_data in sample_products:
            slug = slugify(product_data['title'], allow_unicode=True)
            # Check if product already exists
            if Product.objects.filter(slug=slug).exists():
                self.stdout.write(
                    self.style.WARNING(f'Product "{product_data["title"]}" already exists, skipping.')
                )
                continue

            Product.objects.create(
                title=product_data['title'],
                slug=slug,
                description=product_data['description'],
                specs=product_data['specs'],
                visible=product_data['visible'],
                featured=product_data['featured'],
                order=product_data['order'],
            )
            created_count += 1
            self.stdout.write(
                self.style.SUCCESS(f'✓ Added product: {product_data["title"]}')
            )

        self.stdout.write(
            self.style.SUCCESS(f'\n✓ Successfully created {created_count} sample product(s).')
        )
