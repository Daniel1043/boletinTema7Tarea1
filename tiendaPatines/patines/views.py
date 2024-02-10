from django.db.models import Count, Q, Sum
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from rest_framework import permissions
from .models import  Patinete, Alquiler,Usuario
from .serializers import  PatineteSerializer, AlquilerSerializer,UsuarioSerializer
from django.db import transaction


class PatineteViewSet(viewsets.ModelViewSet):
    queryset = Patinete.objects.all()
    serializer_class = PatineteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    @action(detail=False, methods=['get'])
    def patinetes_libres(self, request):
        patinetes_libres = Patinete.objects.exclude(Q(alquiler__isnull=False) & Q(alquiler__fecha_desbloqueo__isnull=True))
        serializer = PatineteSerializer(patinetes_libres, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def patinetes_no_libres(self, request):
        patinetes_ocupados = Patinete.objects.filter(Q(alquiler__isnull=False) & Q(alquiler__fecha_desbloqueo__isnull=True))
        serializer = PatineteSerializer(patinetes_ocupados, many=True, context={'request': request})
        return Response(serializer.data)

    
    @action(detail=False, methods=['get'])
    def ten_patinetes_alquilados(self, request):
        patinetes_mas = Patinete.objects.annotate(num_alquileres=Count('alquiler')).order_by('-num_alquileres')[:10]
        serializer = PatineteSerializer(patinetes_mas, many=True, context={'request': request})
        return Response(serializer.data)
    
    
class usuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    @action(detail=False, methods=['get'])
    def usuario_debitos(self, request):
        user_debt = Usuario.objects.annotate(nsum_debito=Sum('debito')).order_by('-nsum_debito')
        serializer = UsuarioSerializer(user_debt, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def top_tres(self, request):
        user_debt = Usuario.objects.annotate(alquilere_num=Count('alquiler_id')).order_by('-alquilere_num')[:3]
        serializer = UsuarioSerializer(user_debt, many=True, context={'request': request})
        return Response(serializer.data)
 
    
class AlquilerViewSet(viewsets.ModelViewSet):
    queryset = Alquiler.objects.all()
    serializer_class = AlquilerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


    @action(detail=False, methods=['post'])
    def alquilar(self, request):
        usuario = request.user
        patinete_id = request.data.get('patinete_id')
        try:
            patinete = Patinete.objects.get(id=patinete_id)
        except Patinete.DoesNotExist:
            return Response({'error': 'Patinete no encontrado'}, status=400)

        # Verificar si el patinete está disponible
        if patinete.alquiler_set.filter(fecha_entrega=None).exists():
            return Response({'error': 'Patinete ya está en alquiler'}, status=400)


        fecha_desbloqueo = timezone.now()

        Alquiler.objects.create(usuario=usuario, patinete=patinete, fecha_desbloqueo=fecha_desbloqueo)

        return Response({'success': 'Alquiler iniciado correctamente'})


    @action(detail=False, methods=['post'])
    @transaction.atomic
    def liberar(self, request):
        usuario = request.user
        patinete_id = request.data.get('patinete_id')
        
        try:
            patinete = Alquiler.objects.get(id=patinete_id)
        except Patinete.DoesNotExist:
            return Response({'error': 'Patinete no encontrado'}, status=400)

        if patinete.fecha_entrega is not None:
         return Response({'error': 'Patinete ya está en alquiler'}, status=400)


        patinetes=Patinete.objects.get(id=patinete_id)
        fecha_entreg = timezone.now()
        patinete.fecha_entrega = fecha_entreg
        coste_fin= patinete.fecha_desbloqueo-fecha_entreg
        coste_fin2= (coste_fin.total_seconds()/60)*patinetes.precio_minuto+patinetes.precio_desbloqueo
        patinete.coste_final=coste_fin2
        patinete.save()
        
        usur = Usuario.objects.get(user=usuario)
        usur.debito -=coste_fin2
        usur.save()
        
        return Response({'success': 'Alquiler liberado correctamente'})

    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def alquileres_admin(self, request):
        alquileres = Alquiler.objects.all()
        serializer = AlquilerSerializer(alquileres, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def alquileres_usuario(self, request):
        usuario = request.user
        alquileres = Alquiler.objects.filter(usuario=usuario)
        serializer = AlquilerSerializer(alquileres, many=True, context={'request': request})
        return Response(serializer.data)
