import django_filters


from seller.models import Property

from django_filters import Filter
from django.db.models import Q


class NearbyNameCharFilter(Filter):
    def filter(self, qs, value):
        if not value:
            return qs

        lookup = f"{self.field_name}__name__icontains"
        return qs.filter(Q(**{lookup: value}))


class PropertyFilter(django_filters.FilterSet):
    profile = django_filters.CharFilter(lookup_expr="exact")
    place = django_filters.CharFilter(lookup_expr="icontains")
    area = django_filters.CharFilter(lookup_expr="exact")
    no_of_bedrooms = django_filters.CharFilter(lookup_expr="gte")
    no_of_bathrooms = django_filters.CharFilter(lookup_expr="gte")
    no_of_floor = django_filters.CharFilter(lookup_expr="gte")
    nearby = NearbyNameCharFilter()
    no_of_likes = django_filters.CharFilter(lookup_expr="gte")

    class Meta:
        model = Property
        exclude = ["image"]
