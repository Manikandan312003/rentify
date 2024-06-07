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

class NearbyTypeCharFilter(Filter):
    def filter(self, qs, value):
        if not value:
            return qs
        combined_condition = Q()
        conditions = value.split(',')
        lookup = f"{self.field_name}__type__icontains"
        for condition in conditions:
            combined_condition |= Q(**{lookup:condition})
        query = qs.filter(combined_condition)
        return query


class PropertyFilter(django_filters.FilterSet):
    profile = django_filters.CharFilter(lookup_expr="exact")
    place = django_filters.CharFilter(lookup_expr="icontains")
    area = django_filters.CharFilter(lookup_expr="icontains")
    min_no_of_bedrooms = django_filters.CharFilter(field_name="no_of_bedrooms", lookup_expr="gte")
    equal_no_of_bedrooms = django_filters.CharFilter(field_name="no_of_bedrooms", lookup_expr="exact")
    max_no_of_bedrooms = django_filters.CharFilter(field_name="no_of_bedrooms", lookup_expr="lte")
    
    min_no_of_bathrooms = django_filters.CharFilter(field_name="no_of_bathrooms", lookup_expr="gte")
    equal_no_of_bathrooms = django_filters.CharFilter(field_name="no_of_bathrooms", lookup_expr="exact")
    max_no_of_bathrooms = django_filters.CharFilter(field_name="no_of_bathrooms", lookup_expr="lte")
    
    min_no_of_floor = django_filters.CharFilter(field_name="no_of_floor", lookup_expr="gte")
    equal_no_of_floor = django_filters.CharFilter(field_name="no_of_floor", lookup_expr="exact")
    max_no_of_floor = django_filters.CharFilter(field_name="no_of_floor", lookup_expr="lte")
    
    min_no_of_likes = django_filters.CharFilter(lookup_expr="gte", field_name="no_of_likes")
    equal_no_of_likes = django_filters.CharFilter(lookup_expr="exact", field_name="no_of_likes")
    max_no_of_likes = django_filters.CharFilter(lookup_expr="lte", field_name="no_of_likes")

    nearby_name = NearbyNameCharFilter(field_name='nearby')
    nearby_type = NearbyTypeCharFilter(field_name='nearby')

    class Meta:
        model = Property
        exclude = ["image"]
