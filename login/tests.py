from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import CadastroForm


class CadastroFormTests(TestCase):
    def test_registered_users_are_not_staff_or_superusers(self):
        form = CadastroForm(data={
            "username": "cliente",
            "email": "cliente@example.com",
            "password1": "Strong-Test-Password-482!",
            "password2": "Strong-Test-Password-482!",
            "is_staff": "on",
            "is_superuser": "on",
        })

        self.assertTrue(form.is_valid(), form.errors)
        user = form.save()

        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)


class DashboardChartsTests(TestCase):
    def test_regular_user_does_not_see_dashboard_charts(self):
        user = User.objects.create_user(username="cliente", password="test-password")
        self.client.force_login(user)

        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'id="graficoPedidosMes"')
        self.assertNotContains(response, "cdn.jsdelivr.net/npm/chart.js")

    def test_staff_user_sees_dashboard_charts(self):
        user = User.objects.create_user(
            username="staff",
            password="test-password",
            is_staff=True,
        )
        self.client.force_login(user)

        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="graficoPedidosMes"')
