import django_tables2 as tables
from django.contrib.auth.models import User


class UserTable(tables.Table):
    role = tables.Column(
        accessor='get_role_name',
        verbose_name='Роль',
        orderable=False,
    )


    class Meta:
        model = User
        template_name = "django_tables2/bootstrap.html"
        fields = ("id", 'username', 'last_login', 'role')
