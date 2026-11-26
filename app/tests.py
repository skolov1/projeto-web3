from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Servico


class ServicosListingVisibilityTests(TestCase):
    def setUp(self):
        self.servico = Servico.objects.create(
            nome="Aula de violão",
            descricao="Aulas para iniciantes",
            preco="75.00",
        )
        self.customer = User.objects.create_user(
            username="cliente",
            password="test-password",
        )
        self.staff = User.objects.create_user(
            username="staff",
            password="test-password",
            is_staff=True,
        )

    def test_customer_sees_service_cards_without_management_table(self):
        self.client.force_login(self.customer)

        response = self.client.get(reverse("servicos"))

        self.assertContains(response, "services-card")
        self.assertContains(response, "Aula de violão")
        self.assertNotContains(response, "services-table")

    def test_staff_sees_management_table_instead_of_service_cards(self):
        self.client.force_login(self.staff)

        response = self.client.get(reverse("servicos"))

        self.assertContains(response, "services-table")
        self.assertContains(response, "Editar")
        self.assertNotContains(response, "services-card")
