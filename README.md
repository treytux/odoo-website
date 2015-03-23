```payment_direct_order ```
====
Método de pago para crear un pedido directamente al odoo

```website_cookies_policy ```
====
Añade una alerta sobre el uso de cookies en el sitio que se oculta al aceptarlo.

```website_crm_privacy_policy ```
====
Añade un checkbox al formulario de contacto para aceptar la política de privacidad.

```website_feature_product_template ```
====
Este módulo añade características a la plantilla de productos y permite
búsquedas y agrupaciones desde el sitio web.

```website_improvements ```
====
Módulo de mejoras para Website.
    - Añade nombre publicos de productos en el website (similar a public
    category)
    - Permite configurar los productos por página en el listado de categorias

```website_ratings ```
====
Modulo para añadir al website valoraciones sobre objeto odoo

En cualquier parte de tu template website añadir, por ejemplo:

```
<t t-call="website_ratings.widget">
    <t t-set="object_model">product.product</t>
    <t t-set="object_id" t-value="product.id"/>
    <t t-set="input_name">rating_product</t>
</t>
```

Donde:
- object_model: es el nombre del modelo odoo sobre el cual hacer las valoraciones
- object_id: es el id del objecto del tipo object_model sobre el cual valorar
- input_name: es el nombre del input que se generará para hacer las valoraciones

```website_sale_cart_add_comments ```
====
Añade un campo de comentarios para añadirlos al pedido

```website_sale_disk_images ```
====


```website_sale_product_gallery ```
====
Galería de imágenes para productos en la tienda online.

Nombres de las imágenes para templates:
    slug(plantilla)[-#].jpg

Nombres de las imágenes para variantes:
    slug(plantilla)-variante-valor-#.jpg

```website_sale_product_in_stock ```
====
Permite conocer en la tienda online si un producto está en stock.

```website_sale_products_nav ```
====
Permite ordenar los listados de productos de la tienda online por secuencia [defecto], precio y nombre.

```website_sale_wishlist_products ```
====
Permite a un usuario identificado mantener una lista con sus productos favoritos en una lista de deseos o "wishlist".

```website_social_share ```
====
Permite compartir en las redes sociales el contenido de la página que se está mostrando (Twitter, Facebook, Google+, Pinterest y Tumblr).

```website_sale_custom_lists ```
====
Permite crear listas personalizadas y relacionarlas con las plantillas de producto.

