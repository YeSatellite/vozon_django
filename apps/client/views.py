# coding=utf-8
from rest_framework import mixins, status
from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from apps.client import filters
from apps.client.models import Order, Transport, Offer, Route
from apps.client.serializers import OrderSerializer, TransportSerializer, OfferSerializer, RouteSerializer
from apps.client.utils import send_notification
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

    def get_object(self):
        pk = self.kwargs.get('pk')

        if pk == "current":
            return self.request.user

        return super().get_object()


class CourierViewSet(ReadOnlyModelViewSet, mixins.UpdateModelMixin, ):
    serializer_class = UserSerializer
    queryset = User.objects.filter(type=TYPE[1][1])
    permission_classes = (IsItOrReadOnly,)

    def get_object(self):
        pk = self.kwargs.get('pk')

        if pk == 'current':
            return self.request.user

        return super().get_object()


class ClientOrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all().order_by("-created")
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly, IsClient]

    def get_queryset(self):
        queryset = super().get_queryset()
        status_ = self.request.query_params.get('status', 'posted')
        queryset = queryset.filter(offer__isnull=(status_ == 'posted'))
        queryset = queryset.filter(owner=self.request.user)
        return queryset

    @detail_route(methods=['get', 'post', 'delete'], permission_classes=permission_classes)
    def offers(self, request, pk=None):
        if self.request.method == 'GET':
            queryset = Offer.objects.filter(order=pk)
            serializer = OfferSerializer(queryset, many=True, context={"request": request})
            return Response(data=serializer.data)
        elif self.request.method == 'POST':
            offer = Offer.objects.get(pk=self.request.data['offer'])
            order = Order.objects.get(pk=pk)

            send_notification("Клиент принял ваше предложение", order.title, 'accept_offer',
                              user=offer.transport.owner)

            order.to_active(offer)
            return Response(data={'status': 'OK'})
        elif self.request.method == 'DELETE':
            Offer.objects.get(pk=self.request.data['offer']).delete()
            return Response(data={'status:': 'deleted'})

    @detail_route(methods=['post'], permission_classes=permission_classes)
    def done(self, request, pk=None):
        order = Order.objects.get(pk=pk)

        send_notification(order.owner.name, "Оценил вашу услугу", 'done',
                          user=order.offer.transport.owner)

        order.to_done(int(self.request.data['rating']))

        return Response(data={'status': 'OK'})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        instance = serializer.instance

        send_notification("Клиент оформил заказ", instance.title, 'new_order',
                          user__type='courier', user__city=instance.start_point)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CourierOrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all().order_by("-created")
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly, IsCourier]
    filter_backends = (filters.RouteFilterBackend,)


class CourierOfferViewSet(ModelViewSet):
    serializer_class = OfferSerializer
    queryset = Offer.objects.all().order_by("-created")
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly, IsCourier]
    filter_fields = ('order',)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        instance = serializer.instance

        send_notification("Курьер откликнулся на заявку", instance.order.title, 'response_order',
                          user=instance.order.owner)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(order=self.kwargs['order'])
        return queryset

    def perform_create(self, serializer):
        serializer.save(order=Order.objects.get(pk=self.kwargs['order']))

    def list(self, request, *args, **kwargs):
        offer = self.get_queryset().get(order_id=self.kwargs['order'], transport__owner=request.user)
        serializer = self.get_serializer(offer)
        return Response(serializer.data)


class ClientRouteViewSet(ReadOnlyModelViewSet):
    serializer_class = RouteSerializer
    queryset = Route.objects.all().order_by("-created")
    permission_classes = [IsAuthenticated, IsClient]
    filter_backends = (filters.RouteFilterBackend,)


class CourierRouteViewSet(ModelViewSet):
    serializer_class = RouteSerializer
    queryset = Route.objects.all().order_by("-created")
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly, IsCourier]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(owner=self.request.user)
        return queryset
