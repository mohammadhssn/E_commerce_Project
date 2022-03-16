from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

from elasticsearch_dsl import Q

from .documents import ProductInventoryDocument
from django.core.paginator import Paginator


class SearchProductInventory(View):
    template_name = 'search/search.html'
    search_document = ProductInventoryDocument

    def get(self, request):
        try:

            query = request.GET.get('q', None)
            # if query:
            #     response = self.search_document.search().query("match", product__name=query)
            # else:
            #     response = ''

            q = Q(
                "multi_match",
                query=query,
                fields=["product.name"],
                fuzziness="auto",
            ) & Q(
                should=[
                    Q("match", is_default=True),
                ],
                minimum_should_match=1,
            )
            search = self.search_document.search().query(q)
            response = search.execute()
            paginator = Paginator(response, 1)  # Show 10 contacts per page.
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            return render(request, self.template_name, {'response': page_obj, 'query': query, 'search':response})
        except Exception as e:
            return HttpResponse(e, status=500)
