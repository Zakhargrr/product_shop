from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        db_user = User.objects.filter(email='admin@mail.ru')
        if not db_user:
            user = User.objects.create(
                email='admin@mail.ru',
                first_name='Admin',
                last_name='Admin',
                is_staff=True,
                is_superuser=True
            )

            user.set_password('12345')
            user.save()
