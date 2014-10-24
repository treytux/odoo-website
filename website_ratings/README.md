website_ratings
===============

Modulo para añadir al website valoraciones sobre objeto odoo

Funcionamiento
==============

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