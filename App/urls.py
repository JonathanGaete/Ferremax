from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import LoginForm, MyPasswordResetForm, MySetPasswordForm, MyPasswordChangeForm

urlpatterns = [
    path('', views.principal, name='principal'),
    path('categoria/<slug:val>/', views.CategoriaView.as_view(), name='categoria'),
    path('productos/', views.productos_view, name='productos'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('logout/', auth_view.LogoutView.as_view(next_page='login'), name='logout'),
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('listar_productos/', views.listar_productos, name='listar_productos'),

    # Registration and authentication
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('accounts/login/', auth_view.LoginView.as_view(template_name='pagina/login.html', authentication_form=LoginForm), name='login'),

    # Password reset
    path('password-reset/', auth_view.PasswordResetView.as_view(template_name='pagina/password_reset.html', form_class=MyPasswordResetForm), name='password_reset'),
    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='pagina/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='pagina/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/', auth_view.PasswordResetCompleteView.as_view(template_name='pagina/password_reset_complete.html'), name='password_reset_complete'),

    path('administracion/', views.listar_administracion, name='listar_administracion'),

    # Password change
    path('passwordchangedone/', auth_view.PasswordChangeDoneView.as_view(template_name='pagina/passwordchangedone.html'), name='passwordchangedone'),
    path('passwordchange/', auth_view.PasswordChangeView.as_view(template_name='pagina/changepassword.html', form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'), name='passwordchange'),

    # Categoria
    path('agregar_categoria/', views.agregar_categoria, name='agregar_categoria'),
    path('eliminar-categoria/<int:pk>/', views.eliminar_categoria, name='eliminar-categoria'),
    path('editar_categoria/<int:pk>/', views.editar_categoria, name='editar_categoria'),
    path('guardar_categoria_editada/<int:pk>/', views.guardar_categoria_editada, name='guardar_categoria_editada'),

    # Producto
    path('confirmar_eliminar/<int:producto_id>/', views.confirmar_eliminar_producto, name='confirmar_eliminar_producto'),
    path('editar_producto/<int:id_producto>/', views.editar_producto, name='editar_producto'),
    path('eliminar_producto/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),
    path('agregar_producto/', views.agregar_producto, name='agregar_producto'),

    path('agregar_destacado/', views.agregar_destacado, name='agregar_destacado'),
    path('editar_destacado/<int:pk>/', views.editar_destacado, name='editar_destacado'),
    path('eliminar_destacado/<int:id>/', views.eliminar_destacado, name='eliminar_destacado'),

    # URLs cambiar tipo Usuario
    path('change_user_type/<int:user_id>/', views.change_user_type, name='change_user_type'),

    path('agregar_al_carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('eliminar/<int:item_id>/', views.borrar_producto_carrito, name='borrar_producto_carrito'),
    path('mostrar_carrito/', views.mostrar_carrito, name='mostrar_carrito'),
    path('procesar_pago_paypal/', views.procesar_pago_paypal, name='procesar_pago_paypal'),
    path('pago_exitoso/', views.pago_exitoso, name='pago_exitoso'),
    path('pago_cancelado/', views.pago_cancelado, name='pago_cancelado'),
    path('historial-compras/', views.historial_compras, name='historial_compras'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
