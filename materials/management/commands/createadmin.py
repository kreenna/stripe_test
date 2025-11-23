from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Создаем админа автоматически, если его еще нет."

    def handle(self, *args, **kwargs):
        username = "admin"
        email = "admin@example.com"
        if not User.objects.filter(username=username).exists() and not User.objects.filter(is_superuser=True).exists():
            password = "123qwe456rty"
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f"Админ '{username}' создан с паролем: {password}"))
        else:
            self.stdout.write("Админ уже существует.")
