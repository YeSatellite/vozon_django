from rest_framework import mixins
from rest_framework.decorators import detail_route, list_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from apps.client.models import Order, Transport, Offer
from apps.client.serializers import OrderSerializer, TransportSerializer, OfferSerializer
from apps.core.permission import IsItOrReadOnly, IsOwnerOrReadOnly, IsCourier, IsClient
from apps.user.manager import TYPE
from apps.user.models import User
from apps.user.serializers import UserSerializer


class TransportViewSet(ModelViewSet):
    serializer_class = TransportSerializer
    queryset = Transport.objects.all().order_by("-created")
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly, IsCourier]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(owner=self.request.user)
        return queryset


class ClientViewSet(ReadOnlyModelViewSet, mixins.UpdateModelMixin, ):
    serializer_class = UserSerializer
    queryset = User.objects.filter(type=TYPE[0][0])
    permission_classes = (IsItOrReadOnly,)


class CourierViewSet(ReadOnlyModelViewSet, mixins.UpdateModelMixin, ):
    serializer_class = UserSerializer
    queryset = User.objects.filter(type=TYPE[1][1])
    permission_classes = (IsItOrReadOnly,)


class ClientOrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all().order_by("-created")
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly, IsClient]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = super().get_queryset()
        status_ = self.request.query_params.get('status', 'posted')
        queryset = queryset.filter(transport__isnull=(status_ == 'posted'))
        queryset = queryset.filter(owner=self.request.user)
        return queryset

    @detail_route(methods=['get', 'post', 'delete'], permission_classes=permission_classes)
    def offers(self, request, pk=None):
        if self.request.method == 'GET':
            queryset = Offer.objects.filter(order=pk)
            serializer = OfferSerializer(queryset, many=True)
            return Response(data=serializer.data)
        elif self.request.method == 'POST':
            offer = Offer.objects.get(pk=self.request.data['offer'])
            Order.objects.get(pk=pk).to_active(offer)
            return Response(data={'status': 'OK'})
        elif self.request.method == 'DELETE':
            Offer.objects.get(pk=self.request.data['offer']).delete()
            return Response(data={'status:': 'deleted'})


class CourierOrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all().order_by("-created")
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly, IsCourier]

    def get_queryset(self):
        queryset = super().get_queryset()
        status_ = self.request.query_params.get('status', 'posted')
        offers_orders = Offer.objects.all() \
            .filter(transport__owner=self.request.user) \
            .values_list('order', flat=True)
        print(offers_orders)
        if status_ == 'posted':
            queryset = queryset.filter(start_point=self.request.user.city)
            queryset = queryset.filter(transport=None)
            queryset = queryset.exclude(pk__in=offers_orders)
        elif status_ == 'active':
            transports = Transport.objects.filter(owner=self.request.user)
            queryset = queryset.filter(transport__in=transports)
        else:
            queryset = queryset.filter(pk__in=offers_orders)
        return queryset


class CourierOfferViewSet(ModelViewSet):
    serializer_class = OfferSerializer
    queryset = Offer.objects.all().order_by("-created")
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly, IsCourier]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(order=self.kwargs['order'])

        return queryset

    def perform_create(self, serializer):
        serializer.save(order=Order.objects.get(pk=self.kwargs['order']))
