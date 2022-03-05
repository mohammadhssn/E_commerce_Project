import pytest
from pytest_django.asserts import assertTemplateUsed

from django.urls import reverse


class TestViews:

    def test_basket_basket_summary_view(self, db, client):
        """
            test access to page basket view
        """

        url = reverse('basket:basket_summary')
        response = client.get(url)

        assert response.status_code == 200
        assertTemplateUsed(response, 'basket/basket_summary.html')

    def test_basket_basket_summary_view_method_get_invalid(self, db, client):
        """
            test can't access to page add basket view with method GET
        """

        url = reverse('basket:basket_add')
        response = client.get(url)

        assert response.status_code == 405

    @pytest.mark.skip
    def test_basket_basket_add_view_method_post(self, db, user, client):
        """
            test access to page add basket view with method POST
        """

        pass

    def test_basket_basket_delete_view_method_get_invalid(self, db, client):
        """
            test can't access to page delete basket view with method GET
        """

        url = reverse('basket:basket_delete')
        response = client.get(url)

        assert response.status_code == 405

    @pytest.mark.skip
    def test_basket_basket_delete_view_method_post(self, db, client):
        """
            test access to page delete basket view with method POST
        """

        pass

    def test_basket_basket_update_view_method_get_invalid(self, db, client):
        """
            test can't access to page update basket view with method GET
        """

        url = reverse('basket:basket_update')
        response = client.get(url)

        assert response.status_code == 405

    @pytest.mark.skip
    def test_basket_basket_update_view_method_post(self, db, client):
        """
            test access to page update basket view with method POST
        """

        pass
