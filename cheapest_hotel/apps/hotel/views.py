import sys

from rest_framework import viewsets
from hotel.serializers import HotelSerializer, TaxSerializer
from hotel.models import Hotel, Tax
from collections import defaultdict
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

class HotelViewSet(viewsets.ModelViewSet):

    queryset = Hotel.objects.all().order_by('name')
    serializer_class = HotelSerializer


class TaxViewSet(viewsets.ModelViewSet):

    queryset = Tax.objects.all()
    serializer_class = TaxSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        monday = bool(data.get('monday', None))
        tuesday = bool(data.get('tuesday', None))
        wednesday = bool(data.get('wednesday', None))
        thursday = bool(data.get('thursday', None))
        friday = bool(data.get('friday', None))
        saturday = bool(data.get('saturday', None))
        sunday = bool(data.get('sunday', None))
        tax = Tax.objects.filter(Q(monday=monday) | Q(tuesday=tuesday) | Q(wednesday=wednesday) | Q(thursday=thursday) |
                                 Q(friday=friday) | Q(saturday=saturday) | Q(sunday=sunday), user=data.get('user'),
                                 hotel=data.get('hotel').split('/')[-2])
        if tax:
            return Response({"Já existe uma taxa para um desses dias com o mesmo hotel e tipo de usuário!", status.HTTP_400_BAD_REQUEST})
        response = super().create(request)
        return Response(response.data)

class Cheapest(APIView):
    USERS = {
        'Regular': 1,
        'Reward': 2,
    }

    def get(self, request):
        if not request.query_params:
            return Response({'Query string é obrigatória', status.HTTP_400_BAD_REQUEST})
        user, days = self._sanitize_data(request.query_params)
        hotel_prices = defaultdict(lambda: {'price': 0.0})
        for day in days:
            taxes = self._search_taxes(self._find_weekday_in_string(day), user)
            for tax in taxes:
                hotel_prices[tax.hotel.name]['price'] += tax.price
                hotel_prices[tax.hotel.name]['stars'] = tax.hotel.stars

        return Response({'cheapest': self._check_the_cheapest(hotel_prices)})

    def _sanitize_data(self, data):
        data = list(data.keys())[0].split(':')
        user = data[0]
        days = data[1].split(',')
        return user, days

    def _find_weekday_in_string(self, string):
        return string[string.find('(') + 1:string.find(')')]

    def _search_taxes(self, day, user):
        if day == 'mon':
            return Tax.objects.filter(monday=True, user=self.USERS[user])
        elif day == 'tues':
            return Tax.objects.filter(tuesday=True, user=self.USERS[user])
        elif day == 'wed':
            return Tax.objects.filter(wednesday=True, user=self.USERS[user])
        elif day == 'thur':
            return Tax.objects.filter(thursday=True, user=self.USERS[user])
        elif day == 'fri':
            return Tax.objects.filter(friday=True, user=self.USERS[user])
        elif day == 'sat':
            return Tax.objects.filter(saturday=True, user=self.USERS[user])
        elif day == 'sun':
            return Tax.objects.filter(sunday=True, user=self.USERS[user])

    def _check_the_cheapest(self, hotel_prices):
        cheapest_hotel = {
            'price': sys.float_info.max,
            'stars': 0
          }
        cheapest_hotel_name = ''
        for hotel_price in hotel_prices.items():
            if hotel_price[1]['price'] < cheapest_hotel['price']:
                cheapest_hotel = hotel_price[1]
                cheapest_hotel_name = hotel_price[0]
            elif hotel_price[1]['price'] == cheapest_hotel['price']:
                if hotel_price[1]['stars'] > cheapest_hotel['stars']:
                    cheapest_hotel = hotel_price[1]
                    cheapest_hotel_name = hotel_price[0]
        return cheapest_hotel_name

