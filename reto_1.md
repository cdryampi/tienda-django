# Procesa pagos por internet con tarjeta de crédito en más de 135 divisas.
https://stripe.com/es

- Cómo recoger información del usuario.
- Cómo realizar un cargo asociado a un importe.
- Gestión de productos y precios.
- Manejo de errores.


# pendiente

- Hacer que el carro de compras sea persistente y no elimine al recoger los datos del stripe. Cada vez que acepte el pago, solo vamos a crear un nuevo carro de compras y asignarle al usuario. Tenenemos una ForeignKey hacia el usuario en el carro de compras, por lo tanto podemos tener varios carros de compras por usuario.

- Recoger el PDF de la factura y tenerlo en el datail del payment_detail.