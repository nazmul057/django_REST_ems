from rest_framework.pagination import PageNumberPagination

class SmallResultsSetPagination(PageNumberPagination):
    page_size = 10                 # default page size
    page_size_query_param = "page_size"  # allow client query override (?page_size=50) e.g. "http://.../employees/?page=3&page_size=20"
    max_page_size = 100            # safety cap

