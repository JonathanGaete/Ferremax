from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from Productos.models import Producto, Categoria, Destacados
from .forms import *
from django.views import View
from django.db.models import Count
from rest_framework import viewsets
from Productos.serializers import ProductoSerializer
from Productos.permissions import IsBodeguero
from django.conf import settings
import paypalrestsdk
from django.db.models import Q
import requests


paypalrestsdk.configure({
    "mode": "sandbox",  # Cambiar a "live" para entorno de producción
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET,
})


def obtener_tasas_de_cambio():
    response = requests.get('https://mindicador.cl/api')
    data = response.json()
    return {
        'USD': data['dolar']['valor'],
        'EUR': data['euro']['valor'],
        'UF': data['uf']['valor'],
        'CLP': 1  # La tasa de cambio para CLP a CLP es 1
    }


def principal(request):
    banners = Banner.objects.all()
    destacados = Destacados.objects.all()
    data = {
        'banners': banners,
        'destacados': destacados
    }
    return render(request, 'pagina/principal.html', data)

class CategoriaView(View):
    def get(self, request, val):
        categoria = get_object_or_404(Categoria, nombre=val)
        productos = Producto.objects.filter(categoria=categoria)
        titulo = productos.values('nombre').annotate(total=Count('nombre'))
        return render(request, 'pagina/categoria.html', {'categoria': categoria, 'productos': productos, 'titulo': titulo})




def listar_productos(request):
    query = request.GET.get('q')
    if query:
        productos = Producto.objects.filter(
            Q(nombre__icontains=query) | Q(descripcion__icontains=query)
        )
    else:
        productos = Producto.objects.all()

    tasas_de_cambio = obtener_tasas_de_cambio()

    data = {
        'productos': productos,
        'query': query,
        'tasas_de_cambio': tasas_de_cambio
    }
    return render(request, 'pagina/productos.html', data)




def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    tasas_de_cambio = obtener_tasas_de_cambio()  # Obtener las tasas de cambio desde la función definida
    context = {
        'producto': producto,
        'tasas_de_cambio': tasas_de_cambio  # Pasar las tasas de cambio al contexto
    }
    return render(request, 'pagina/detalle_producto.html', context)






class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'pagina/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Registro exitoso!")
            return redirect('principal')  # Redirige a donde desees después del registro exitoso
        else:
            messages.warning(request, "Datos ingresados no válidos")
        return render(request, 'pagina/customerregistration.html', {'form': form})




class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm(instance=request.user)
        return render(request, 'pagina/perfil.html', {'form': form})

    def post(self, request):
        form = CustomerProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Perfil actualizado correctamente!")
        else:
            messages.warning(request, "Datos incorrectos")
        return render(request, 'pagina/perfil.html', {'form': form})

@login_required  # Asegúrate de importar @login_required desde django.contrib.auth.decorators
def address(request):
    addresses = CustomUser.objects.filter(user=request.user)
    return render(request, 'pagina/address.html', {'addresses': addresses})

class UpdateAddress(View):
    def get(self, request, pk):
        address = get_object_or_404(CustomUser, pk=pk)
        form = CustomerProfileForm(instance=address)
        return render(request, 'pagina/updateAddress.html', {'form': form})

    def post(self, request, pk):
        address = get_object_or_404(CustomUser, pk=pk)
        form = CustomerProfileForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Dirección actualizada correctamente!")
            return redirect('address')  # Redirige a donde desees después de la actualización exitosa
        else:
            messages.warning(request, "Datos incorrectos")
        return render(request, 'pagina/updateAddress.html', {'form': form})



@login_required
def borrar_categoria(request, categoria_id):
    if request.user.tipo == 'admin':
        categoria = get_object_or_404(Categoria, pk=categoria_id)
        if request.method == 'POST':
            categoria.delete()
            return redirect('listar_administracion')
        return render(request, 'borrar_categoria.html', {'categoria': categoria})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")




@login_required
def borrar_producto(request, producto_id):
    if request.user.tipo == 'admin':
        producto = get_object_or_404(Producto, pk=producto_id)
        if request.method == 'POST':
            producto.delete()
            return redirect('listar_administracion')
        return render(request, 'borrar_producto.html', {'producto': producto})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")



    

@login_required
def borrar_destacado(request, destacado_id):
    if request.user.tipo == 'admin':
        destacado = get_object_or_404(Destacados, pk=destacado_id)
        if request.method == 'POST':
            destacado.delete()
            return redirect('listar_administracion')
        return render(request, 'borrar_destacado.html', {'destacado': destacado})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
    
@login_required
def listar_administracion(request):
    if request.user.tipo == 'bodeguero':
        categorias = Categoria.objects.all()
        productos = Producto.objects.all()
        destacados = Destacados.objects.all()

        return render(request, 'pagina/administracion.html', {'categorias': categorias, 'productos': productos, 'destacados': destacados})
    else:
        return render(request, 'pagina/error_permisos.html')

User = get_user_model()

@login_required
def change_user_type(request, user_id):
    # Verificar si el usuario actual es administrador
    if not request.user.tipo == 'admin':
        return redirect('some_redirect_url')  # Redirigir a donde sea necesario si no es admin

    user = get_object_or_404(User, pk=user_id)
    
    if request.method == 'POST':
        form = ChangeUserTypeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('success_url')  # Redirigir a la URL de éxito después de cambiar el tipo de usuario
    else:
        form = ChangeUserTypeForm(instance=user)
    
    return render(request, 'pagina/change_user_type.html', {'form': form, 'user': user})


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsBodeguero]  # Aplica el permiso personalizado

def productos_view(request):
    return render(request, 'pagina/productos.html')

# App/views.py




@login_required
def editar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('listar_administracion')  # Redirige a donde desees después de guardar los cambios
    else:
        form = CategoriaForm(instance=categoria)
    
    return render(request, 'pagina/editar_categoria.html', {'form': form, 'categoria': categoria})


@login_required
def eliminar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    
    if request.method == 'POST':
        categoria.delete()
        return redirect('listar_administracion')  # Redirige a donde sea necesario después de eliminar la categoría
    
    return render(request, 'pagina/eliminar_categoria.html', {'categoria': categoria})




@login_required
def agregar_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_administracion')  # Redirige a la lista de administración después de guardar correctamente la categoría
    else:
        form = CategoriaForm()
    return render(request, 'pagina/agregar_categoria.html', {'form': form})



#PRODUCTO
 
def editar_producto(request, id_producto):
    producto = get_object_or_404(Producto, pk=id_producto)
    
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('listar_administracion')  # Redirigir a la página de administración o donde sea necesario
    else:
        form = ProductoForm(instance=producto)
    
    return render(request, 'pagina/editar_producto.html', {'form': form})


@login_required
def eliminar_producto(request, pk):  # Cambio de 'id_producto' a 'pk'
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('listar_administracion')  # Redirigir a la página de administración o donde sea necesario
    return render(request, 'pagina/confirmar_eliminar_producto.html', {'producto': producto})




def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('listar_administracion')  # Cambia 'administracion' por la URL correcta de tu vista de administración
    else:
        form = ProductoForm()
    
    return render(request, 'pagina/agregar_producto.html', {'form': form})


def agregar_destacado(request):
    if request.method == 'POST':
        form = DestacadosForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_administracion')  # Cambia 'principal' por la URL a la que deseas redirigir después de guardar el destacado
    else:
        form = DestacadosForm()
    return render(request, 'pagina/agregar_destacado.html', {'form': form})



@login_required
def guardar_categoria_editada(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('listar_administracion')  # Redirige después de guardar
    else:
        form = CategoriaForm(instance=categoria)
    
    return render(request, 'pagina/guardar_categoria_editada.html', {'form': form, 'categoria': categoria})


@login_required
def editar_destacado(request, pk):
    destacado = get_object_or_404(Destacados, pk=pk)
    
    if request.method == 'POST':
        form = DestacadosForm(request.POST, instance=destacado)
        if form.is_valid():
            form.save()
            return redirect('listar_administracion')  # Redirige a donde desees después de guardar los cambios
    else:
        form = DestacadosForm(instance=destacado)
    
    return render(request, 'pagina/editar_destacado.html', {'form': form, 'destacado': destacado})


def eliminar_destacado(request, id):
    destacado = get_object_or_404(Destacados, id=id)
    destacado.delete()
    return redirect('listar_administracion')




def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    context = {'producto': producto}
    return render(request, 'pagina/detalle_producto.html', context)




def borrar_producto_carrito(request, item_id):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        cart_id = request.session.get('cart_id')
        if cart_id:
            cart = Cart.objects.filter(id=cart_id).first()
        else:
            cart = None

    if cart:
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        cart_item.delete()

    return redirect('mostrar_carrito')


@login_required
def procesar_pago_paypal(request):
    cart = Cart.objects.filter(user=request.user).first()
    if not cart or not cart.items.exists():
        return HttpResponse("No hay artículos en el carrito")

    total = sum(item.get_total_price() for item in cart.items.all())
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": request.build_absolute_uri(reverse('pago_exitoso')),
            "cancel_url": request.build_absolute_uri(reverse('pago_cancelado'))
        },
        "transactions": [{
            "amount": {
                "total": f"{total:.2f}",
                "currency": "USD"
            },
            "description": "Compra en MiTienda"
        }]
    })

    if payment.create():
        for link in payment.links:
            if link.method == "REDIRECT":
                return redirect(link.href)
    else:
        return HttpResponse(f"Error al procesar el pago: {payment.error}")

    return HttpResponse("Error desconocido al procesar el pago.")


@login_required
def pago_exitoso(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    if payment_id and payer_id:
        payment = paypalrestsdk.Payment.find(payment_id)
        if payment.execute({"payer_id": payer_id}):
            cart = Cart.objects.get(user=request.user)
            pedido = Pedido.objects.create(usuario=request.user, total=payment.transactions[0].amount.total)

            # Guardar cada item del carrito como PedidoItem
            for cart_item in cart.items.all():
                PedidoItem.objects.create(
                    pedido=pedido,
                    cart_item=cart_item,
                    cantidad=cart_item.quantity,
                    precio=cart_item.get_total_price()
                )


            # Limpiar el carrito después de procesar el pedido
            cart.delete()

            return render(request, 'pagina/pago_exitoso.html', {'pedido': pedido})
        else:
            return HttpResponse(f"Error al procesar el pago: {payment.error}")

    return HttpResponse("Pago no completado")



@login_required
def pago_cancelado(request):
    return render(request, 'pagina/pago_cancelado.html')



def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    cantidad = int(request.POST.get('cantidad', 1))  # Obtener cantidad del formulario, default a 1 si no se especifica

    # Obtener o crear el carrito
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        cart_id = request.session.get('cart_id')
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = Cart.objects.create()
            request.session['cart_id'] = cart.id
    
    # Verificar si el item ya está en el carrito
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=producto)

    # Si el item ya existe en el carrito, actualizar la cantidad
    if not created:
        cart_item.quantity += cantidad
        cart_item.save()
    else:
        cart_item.quantity = cantidad  # Si es creado, establecer la cantidad inicial
        cart_item.save()
    
    return redirect('mostrar_carrito')



def mostrar_carrito(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        cart_id = request.session.get('cart_id')
        if cart_id:
            cart = Cart.objects.filter(id=cart_id).first()
        else:
            cart = None
    
    if cart:
        cart_items = cart.items.all()  # Obtener todos los items del carrito
        total_pedido = sum(item.get_total_price() for item in cart_items)  # Calcular el total del pedido
    else:
        cart_items = []
        total_pedido = 0  # Si no hay carrito, el total es cero
    
    # Obtener las tasas de cambio
    tasas_de_cambio = obtener_tasas_de_cambio()

    return render(request, 'pagina/mostrar_carrito.html', {'cart': cart, 'cart_items': cart_items, 'total_pedido': total_pedido, 'tasas_de_cambio': tasas_de_cambio})





@login_required
def historial_compras(request):
    # Obtener todos los pedidos del usuario ordenados por fecha descendente
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-fecha')

    # Obtener el token de autenticación del usuario (este es solo un ejemplo, ajusta según tu método de autenticación)
    token = 'tu_token_de_autenticacion_aqui'

    headers = {
        'Authorization': f'Token {token}',
    }

    # Obtener los productos desde la API local
    try:
        response = requests.get('http://127.0.0.1:8000/api/productos/', headers=headers)
        response.raise_for_status()
        productos = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching products: {e}")
        productos = []

    # Crear un diccionario de productos para acceder fácilmente
    productos_dict = {producto['id']: producto for producto in productos}

    return render(request, 'pagina/historial_compras.html', {'pedidos': pedidos, 'productos_dict': productos_dict})





def eliminar_producto_carrito(request, producto_id):
    carrito = Cart.objects.get_or_create(user=request.user)[0]  # Obtener el carrito del usuario
    
    # Obtener el item del carrito por el id del producto
    item = get_object_or_404(CartItem, cart=carrito, product_id=producto_id)
    
    # Eliminar el item del carrito
    item.delete()
    
    # Recalcular el precio total del carrito
    carrito.actualizar_total()
    
    messages.success(request, 'Producto eliminado del carrito.')

    return redirect('nombre_de_la_vista_del_carrito')  # Redirigir a la vista del carrito o a donde desees


def confirmar_eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)

    if request.method == 'POST':
        # Procesar la eliminación del producto
        producto.delete()
        return redirect('pagina:lista_productos')  # Redirigir a la lista de productos o a donde sea necesario después de eliminar

    return render(request, 'pagina/confirmar_eliminar_producto.html', {'producto': producto})