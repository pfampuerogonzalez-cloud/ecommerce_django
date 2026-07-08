# Documentación del Proyecto — Ecommerce Django

## 1. Resumen del Proyecto

Aplicación web de comercio electrónico construida con **Django 6.0.6** que permite:

- **Catálogo de productos** con imágenes, precios y descripciones.
- **Carrito de compras** basado en sesión (agregar, quitar, actualizar cantidades).
- **Flujo de compra** con registro de pedidos y asociación al usuario autenticado.
- **Autenticación** de clientes y administradores.
- **CRUD completo** de productos (solo administradores).
- **Productos Premium** como categoría separada.
- **Panel de administración** de Django para gestión directa de datos.

El frontend utiliza **Bootstrap 5.3.8** (CDN) con estilos personalizados. La base de datos en desarrollo es **SQLite3**.

---

## 2. Requisitos e Instalación

### Requisitos

```
asgiref==3.11.1
Django==6.0.6
psycopg2-binary==2.9.12
sqlparse==0.5.5
```

### Instalación

```bash
# 1. Clonar el repositorio
git clone <repo-url>
cd ecommerce_django

# 2. Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar migraciones
python manage.py migrate

# 5. Crear credenciales de prueba
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
User.objects.create_superuser('admin', 'admin@test.com', 'admin123')
User.objects.create_user('cliente', 'cliente@test.com', 'cliente123')
"

# 6. Iniciar servidor
python manage.py runserver
```

---

## 3. Estructura de Directorios

```
ecommerce_django/
├── manage.py                     # Punto de entrada de Django
├── requirements.txt              # Dependencias
├── db.sqlite3                    # Base de datos (desarrollo)
├── .gitignore                    # Exclusiones Git
├── README.md                     # Descripción breve
│
├── config/                       # Configuración del proyecto
│   ├── __init__.py
│   ├── asgi.py                   # Servidor ASGI
│   ├── settings.py               # Configuración general
│   ├── urls.py                   # Rutas raíz
│   └── wsgi.py                   # Servidor WSGI
│
├── tienda/                       # App principal (tienda)
│   ├── __init__.py
│   ├── admin.py                  # Registro en admin
│   ├── apps.py                   # Configuración de la app
│   ├── context_processors.py     # Context processor del carrito
│   ├── forms.py                  # Formularios
│   ├── models.py                 # Modelos (Producto, Premium, Pedido, ItemPedido)
│   ├── tests.py                  # Tests (pendientes)
│   ├── urls.py                   # Rutas de la tienda
│   ├── views.py                  # Vistas (CRUD, carrito, pedidos)
│   ├── migrations/               # Migraciones de base de datos
│   │   ├── 0001_initial.py       # Crea modelo Prodcuto (typo original)
│   │   ├── 0002_rename_prodcuto_producto.py
│   │   ├── 0003_producto_imagen.py
│   │   ├── 0004_producto_descripcion.py
│   │   ├── 0005_productopremium.py
│   │   └── 0006_pedido_itempedido.py
│   │
│   ├── templates/                # Templates HTML
│   │   ├── base.html             # Layout principal
│   │   ├── index.html            # Página de inicio
│   │   ├── productos.html        # Catálogo de productos
│   │   ├── crear_producto.html   # Formulario de creación
│   │   ├── actualizar_productos.html  # Formulario de edición (sin base.html)
│   │   ├── carrito.html          # Carrito de compras
│   │   ├── confirmar_pedido.html # Resumen previo a comprar
│   │   ├── detalle_pedido.html   # Confirmación de pedido
│   │   ├── detalle_producto.html # Detalle de producto
│   │   ├── mis_pedidos.html      # Listado de pedidos del usuario
│   │   └── registration/
│   │       └── login.html        # Página de inicio de sesión
│   │
│   └── premium/                  # Templates para productos premium
│       ├── formulario_premium.html
│       ├── lista_premium.html
│       └── actualizar_productos_premium.html
│
├── pasarela/                     # App de pasarela de pago (stub)
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py                 # Modelo Producto propio (no usado)
│   ├── tests.py
│   ├── urls.py                   # Ruta /pago/
│   ├── views.py                  # Vista mercadolibre() stub
│   └── migrations/
│       └── 0001_initial.py
│
└── media/                        # Archivos subidos por usuarios
    └── productos/                # Imágenes de productos
        ├── PC.jpg, whey.PNG, ... # 12 imágenes de ejemplo
```

---

## 4. Configuración (`settings.py`)

### Aplicaciones Instaladas

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "tienda",       # App principal
    "pasarela",     # Pasarela de pago (stub)
]
```

### Autenticación

```python
LOGIN_URL = "/accounts/login/"          # Dónde redirigir si no hay sesión
LOGIN_REDIRECT_URL = "/tienda/"         # Dónde ir tras iniciar sesión
LOGOUT_REDIRECT_URL = "/tienda/"        # Dónde ir tras cerrar sesión
```

### Archivos Multimedia

```python
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
```

Los archivos multimedia se sirven en desarrollo mediante:

```python
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### Context Processors

Se agregó el context processor `tienda.context_processors.carrito_cantidad` para disponer de la variable `{{ carrito_cantidad }}` en todos los templates (usada en el nav para el badge del carrito).

---

## 5. Enrutamiento (`urls.py`)

### Raíz (`config/urls.py`)

| Ruta | Destino | Descripción |
|------|---------|-------------|
| `/admin/` | `admin.site.urls` | Panel de administración Django |
| `/accounts/` | `django.contrib.auth.urls` | Login, logout, password reset |
| `/tienda/` | `tienda.urls` | Rutas de la tienda |
| `/pasarela/` | `pasarela.urls` | Rutas de pasarela de pago |
| `/media/<path>` | `static()` | Servir archivos multimedia (solo DEBUG) |

### Tienda (`tienda/urls.py`)

| Ruta | Vista | Nombre | Método | Descripción |
|------|-------|--------|--------|-------------|
| `/tienda/` | `index` | `index` | GET | Página de inicio |
| `/tienda/crear/` | `crear_producto` | `crear_producto` | GET/POST | Crear producto (admin) |
| `/tienda/productos/` | `lista_productos` | `lista_productos` | GET | Catálogo de productos |
| `/tienda/actualizar/<id>/` | `actualizar_producto` | `actualizar_producto` | GET/POST | Editar producto (admin) |
| `/tienda/borrar/<id>/` | `borrar_producto` | `borrar_producto` | GET | Eliminar producto (admin) |
| `/tienda/lista_premium/` | `lista_productos_premium` | `lista_productos_premium` | GET | Listado premium (admin) |
| `/tienda/crear_premium/` | `crear_premium` | `crear_premium` | GET/POST | Crear premium (admin) |
| `/tienda/actualizar_premium/<id>/` | `actualizar_premium` | `actualizar_premium` | GET/POST | Editar premium (admin) |
| `/tienda/borrar_premium/<id>/` | `borrar_premium` | `borrar_producto_premium` | GET | Eliminar premium (admin) |
| `/tienda/producto/<id>/` | `detalle_producto` | `detalle_producto` | GET | Detalle de producto |
| `/tienda/carrito/` | `ver_carrito` | `ver_carrito` | GET | Ver carrito |
| `/tienda/carrito/agregar/<producto_id>/` | `agregar_al_carrito` | `agregar_al_carrito` | GET | Agregar al carrito |
| `/tienda/carrito/quitar/<producto_id>/` | `quitar_del_carrito` | `quitar_del_carrito` | GET | Quitar del carrito |
| `/tienda/carrito/actualizar/<producto_id>/` | `actualizar_cantidad` | `actualizar_cantidad` | POST | Actualizar cantidad |
| `/tienda/carrito/confirmar/` | `confirmar_pedido` | `confirmar_pedido` | GET/POST | Confirmar compra |
| `/tienda/pedido/<pedido_id>/` | `detalle_pedido` | `detalle_pedido` | GET | Detalle de pedido |
| `/tienda/mis-pedidos/` | `mis_pedidos` | `mis_pedidos` | GET | Listado de pedidos del usuario |

### Pasarela (`pasarela/urls.py`)

| Ruta | Vista | Descripción |
|------|-------|-------------|
| `/pasarela/pago/` | `mercadolibre` | Stub de pago (retorna texto plano) |

---

## 6. Modelos

### `Producto` (tienda)

| Campo | Tipo | Detalles |
|-------|------|----------|
| `id` | BigAutoField | Clave primaria (automática) |
| `nombre` | CharField | max_length=30 |
| `precio` | IntegerField | Precio en unidades enteras |
| `imagen` | ImageField | upload_to="productos/", blank=True, null=True |
| `descripcion` | TextField | blank=True, null=True |

`__str__` retorna `self.nombre`.

### `ProductoPremium` (tienda)

Misma estructura que `Producto` pero con `upload_to="premium/"`.

### `Pedido` (tienda)

| Campo | Tipo | Detalles |
|-------|------|----------|
| `id` | BigAutoField | Clave primaria |
| `usuario` | ForeignKey(User) | related_name="pedidos", on_delete=CASCADE |
| `creado` | DateTimeField | auto_now_add=True |
| `actualizado` | DateTimeField | auto_now=True |
| `total` | IntegerField | default=0 |

`Meta`: ordenado por `-creado` (más reciente primero).

`__str__`: `f"Pedido #{self.id} - {self.usuario.username}"`.

### `ItemPedido` (tienda)

| Campo | Tipo | Detalles |
|-------|------|----------|
| `id` | BigAutoField | Clave primaria |
| `pedido` | ForeignKey(Pedido) | related_name="items", on_delete=CASCADE |
| `producto` | ForeignKey(Producto) | on_delete=CASCADE |
| `cantidad` | PositiveIntegerField | default=1 |
| `precio` | IntegerField | Precio al momento de la compra |

**Propiedad**: `subtotal` → `self.precio * self.cantidad`.

`__str__`: `f"{self.cantidad} x {self.producto.nombre}"`.

### `Producto` (pasarela) — *no utilizado actualmente*

| Campo | Tipo |
|-------|------|
| `nombre` | CharField(max_length=30) |
| `precio` | IntegerField |

Modelo separado del de `tienda`, existe como preparación para integración de pagos.

---

## 7. Vistas

### Vistas Públicas (sin autenticación requerida)

| Vista | Ruta | Método | Template | Descripción |
|-------|------|--------|----------|-------------|
| `index` | `/tienda/` | GET | `index.html` | Página de bienvenida centrada |
| `lista_productos` | `/tienda/productos/` | GET | `productos.html` | Grilla de productos con tarjetas |
| `detalle_producto` | `/tienda/producto/<id>/` | GET | `detalle_producto.html` | Detalle con imagen y botón carrito |
| `ver_carrito` | `/tienda/carrito/` | GET | `carrito.html` | Tabla con items, cantidades, total |
| `agregar_al_carrito` | `/tienda/carrito/agregar/<id>/` | GET | — (redirect) | Agrega/Incrementa producto en sesión |
| `quitar_del_carrito` | `/tienda/carrito/quitar/<id>/` | GET | — (redirect) | Elimina producto del carrito |
| `actualizar_cantidad` | `/tienda/carrito/actualizar/<id>/` | POST | — (redirect) | Actualiza cantidad (valida > 0) |

### Vistas Protegidas (`@login_required`)

| Vista | Ruta | Método | Template | Descripción |
|-------|------|--------|----------|-------------|
| `confirmar_pedido` | `/tienda/carrito/confirmar/` | GET/POST | `confirmar_pedido.html` | GET: resumen; POST: crea Pedido + Items |
| `detalle_pedido` | `/tienda/pedido/<id>/` | GET | `detalle_pedido.html` | Confirmación con detalle |
| `mis_pedidos` | `/tienda/mis-pedidos/` | GET | `mis_pedidos.html` | Listado de pedidos del usuario |

### Vistas de Administración (sin decorador, pero enlaces solo visibles para staff)

| Vista | Ruta | Método | Template | Descripción |
|-------|------|--------|----------|-------------|
| `crear_producto` | `/tienda/crear/` | GET/POST | `crear_producto.html` | Formulario de creación |
| `actualizar_producto` | `/tienda/actualizar/<id>/` | GET/POST | `actualizar_productos.html` | Formulario de edición |
| `borrar_producto` | `/tienda/borrar/<id>/` | GET | — (redirect) | Elimina con confirmación |
| `crear_premium` | `/tienda/crear_premium/` | GET/POST | `premium/formulario_premium.html` | Crear producto premium |
| `lista_productos_premium` | `/tienda/lista_premium/` | GET | `premium/lista_premium.html` | Listado premium |
| `actualizar_premium` | `/tienda/actualizar_premium/<id>/` | GET/POST | `premium/actualizar_productos_premium.html` | Editar premium |
| `borrar_premium` | `/tienda/borrar_premium/<id>/` | GET | — (redirect) | Eliminar premium |

### Vista Stub

| Vista | Ruta | Descripción |
|-------|------|-------------|
| `mercadolibre` (pasarela) | `/pasarela/pago/` | Retorna HttpResponse("pago mercado pago") |

---

## 8. Formularios

### `ProductoForms` (hereda de `ModelForm`)

- **Modelo**: `Producto`
- **Campos**: `nombre`, `precio`, `imagen`, `descripcion`
- **Validación**: `clean_precio` — rechaza precio ≤ 0 con mensaje "El precio debe ser mayor a 0."

### `ProductoPremiumForms` (hereda de `ModelForm`)

- **Modelo**: `ProductoPremium`
- **Campos**: `nombre`, `precio`, `imagen`, `descripcion`
- **Validación**: misma que `ProductoForms` (precio > 0)

---

## 9. Context Processor

### `carrito_cantidad` (`tienda/context_processors.py`)

```python
def carrito_cantidad(request):
    cart = request.session.get('cart', {})
    cantidad = sum(cart.values())
    return {'carrito_cantidad': cantidad}
```

Hace disponible `{{ carrito_cantidad }}` en todos los templates. Se usa en `base.html` para mostrar un badge en el enlace del carrito:

```html
<a href="{% url 'ver_carrito' %}">
  Carrito {% if carrito_cantidad > 0 %}({{ carrito_cantidad }}){% endif %}
</a>
```

---

## 10. Templates

### Herencia

Todos los templates (excepto `actualizar_productos.html` y `actualizar_productos_premium.html`) extienden `base.html`.

### `base.html` — Layout Principal

- Bootstrap 5.3.8 CSS/JS (CDN)
- CSS personalizado (header oscuro, footer al fondo, botones, tablas, mensajes)
- **Bloques**: `{% block content %}`
- **Variables disponibles globalmente**: `user`, `messages`, `carrito_cantidad`
- **Navegación condicional**:
  - Usuario anónimo: Inicio, Catálogo, Carrito, Iniciar sesión
  - Usuario autenticado: + Mis pedidos, Cerrar sesión
  - Staff: + Admin: Crear producto, Admin: Premium, Admin: Panel

### Lista completa de templates

| Template | Extiende | Propósito |
|----------|----------|-----------|
| `index.html` | `base.html` | Página de inicio centrada |
| `productos.html` | `base.html` | Grilla de tarjetas de productos |
| `crear_producto.html` | `base.html` | Formulario crear producto |
| `actualizar_productos.html` | *(ninguno)* | Formulario editar (independiente) |
| `carrito.html` | `base.html` | Tabla del carrito con acciones |
| `confirmar_pedido.html` | `base.html` | Resumen previo a comprar |
| `detalle_pedido.html` | `base.html` | Confirmación post-compra |
| `detalle_producto.html` | `base.html` | Detalle del producto |
| `mis_pedidos.html` | `base.html` | Listado de pedidos |
| `registration/login.html` | `base.html` | Inicio de sesión |
| `premium/formulario_premium.html` | `base.html` | Crear premium |
| `premium/lista_premium.html` | `base.html` | Listado premium |
| `premium/actualizar_productos_premium.html` | *(ninguno)* | Editar premium (independiente) |

---

## 11. Autenticación y Roles

### Login / Logout

Se utiliza el sistema de autenticación incorporado de Django (`django.contrib.auth.urls`):

| Ruta | Vista | Template |
|------|-------|----------|
| `/accounts/login/` | `LoginView` | `registration/login.html` |
| `/accounts/logout/` | `LogoutView` | — (redirige a `/tienda/`) |

### Roles

- **Cliente** (`is_staff=False`): puede ver el catálogo, usar el carrito, confirmar compras y ver sus pedidos.
- **Administrador** (`is_staff=True`, `is_superuser=True`): todo lo del cliente + acceso al panel `/admin/`, creación/edición/borrado de productos y productos premium.

### Navegación condicional

En `base.html`, los enlaces de administración se muestran solo si `user.is_staff` es `True`:

```html
{% if user.is_staff %}
    <a href="{% url 'crear_producto' %}">Admin: Crear producto</a>
    <a href="{% url 'lista_productos_premium' %}">Admin: Premium</a>
    <a href="{% url 'admin:index' %}">Admin: Panel</a>
{% endif %}
```

Los botones de Editar/Borrar en el catálogo también están protegidos por `{% if user.is_staff %}`.

---

## 12. Carrito de Compras

### Implementación

El carrito se almacena en la sesión del navegador como un diccionario:

```python
request.session['cart'] = {
    "1": 3,   # producto_id: cantidad
    "5": 1,
}
```

### Operaciones

| Acción | Vista | Comportamiento |
|--------|-------|----------------|
| **Agregar** | `agregar_al_carrito` | Si el producto ya está, incrementa la cantidad en 1; si no, lo agrega con cantidad 1. |
| **Quitar** | `quitar_del_carrito` | Elimina el producto del diccionario. |
| **Actualizar** | `actualizar_cantidad` | Recibe la nueva cantidad por POST. Si es > 0 actualiza; si es ≤ 0 elimina. |
| **Ver** | `ver_carrito` | Itera el diccionario, busca cada `Producto` en BD, calcula subtotales y total. |

### Vista del Carrito

Template `carrito.html`: tabla con columnas Producto, Precio, Cantidad (con input y botón Actualizar), Subtotal, y botón Quitar. Al pie: total general, botones "Confirmar compra" y "Seguir comprando".

Si el carrito está vacío, muestra mensaje y enlace al catálogo.

---

## 13. Flujo de Compra

### Paso a paso

1. **Catálogo** → el usuario ve productos y hace clic en "Agregar al carrito".
2. **Carrito** → revisa items, puede ajustar cantidades o quitar productos.
3. **Confirmar compra** (`/tienda/carrito/confirmar/`):
   - **GET**: muestra resumen con tabla de productos, cantidades, subtotales y total.
   - **POST** (`@login_required`):
     - Crea un `Pedido` con `usuario=request.user`.
     - Por cada item en el carrito, crea un `ItemPedido` con producto, cantidad y precio actual.
     - Calcula y guarda el total del pedido.
     - Vacía el carrito de la sesión.
     - Muestra mensaje de éxito y redirige al detalle del pedido.
4. **Detalle del pedido** (`/tienda/pedido/<id>/`): confirma la compra con todos los detalles.

### Protección

Las vistas `confirmar_pedido`, `detalle_pedido` y `mis_pedidos` tienen el decorador `@login_required`. Si el usuario no ha iniciado sesión, Django redirige automáticamente a `/accounts/login/`.

---

## 14. CRUD de Productos

### Operaciones

| Operación | Ruta | Método | Descripción |
|-----------|------|--------|-------------|
| **Crear** | `/tienda/crear/` | GET/POST | Formulario con nombre, precio, imagen, descripción |
| **Listar** | `/tienda/productos/` | GET | Grilla de tarjetas Bootstrap |
| **Actualizar** | `/tienda/actualizar/<id>/` | GET/POST | Formulario pre-cargado con datos existentes |
| **Borrar** | `/tienda/borrar/<id>/` | GET | Elimina con confirmación JS |

### Mensajes

Cada operación muestra un mensaje de éxito usando `django.contrib.messages`:
- "Producto guardado correctamente."
- "producto actualizado correctamente"
- "borrado correctamente!"

---

## 15. Productos Premium

Modelo separado `ProductoPremium` con los mismos campos que `Producto` pero con `upload_to="premium/"`. Tiene su propio CRUD completo:

- Crear: `/tienda/crear_premium/`
- Listar: `/tienda/lista_premium/`
- Actualizar: `/tienda/actualizar_premium/<id>/`
- Borrar: `/tienda/borrar_premium/<id>/`

Los enlaces a estas secciones solo son visibles para usuarios staff en la barra de navegación.

---

## 16. Panel de Administración

### Modelos registrados

| Modelo | Configuración |
|--------|---------------|
| `Producto` | `ProductoAdmin` (sin personalización adicional) |
| `ProductoPremium` | Default |
| `Pedido` | `PedidoAdmin`: `list_display = ['id', 'usuario', 'total', 'creado']`, `list_filter = ['creado']` |
| `ItemPedido` | Default (inline en Pedido mediante `ItemPedidoInline`) |

### Acceso

`/admin/` — requiere usuario con `is_staff=True` y `is_superuser=True`.

---

## 17. Pasarela de Pago

La app `pasarela` contiene una implementación **stub** (placeholder) para futura integración con Mercado Pago u otro gateway:

- **Modelo**: `Producto` (independiente del de tienda, con nombre y precio).
- **Vista**: `mercadolibre()` → retorna `HttpResponse("pago mercado pago")`.
- **Ruta**: `/pasarela/pago/`.

Actualmente no está integrada con el flujo de compra.

---

## 18. Credenciales de Prueba

| Rol | Usuario | Contraseña |
|-----|---------|-----------|
| **Administrador** | `admin` | `admin123` |
| **Cliente** | `cliente` | `cliente123` |

Para crear usuarios adicionales:

```bash
python manage.py createsuperuser   # Admin
python manage.py createuser        # Cliente (usar shell para is_staff=False)
```

---

## 19. Archivos Multimedia

### Configuración

```python
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
```

### Almacenamiento

- `Producto.imagen` → `media/productos/`
- `ProductoPremium.imagen` → `media/premium/`

### Servido en desarrollo

Se configuró en `config/urls.py`:

```python
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### Imágenes de ejemplo

El directorio `media/productos/` contiene 12 imágenes de ejemplo subidas durante el desarrollo.
