from .quant.futu import FutuContext

futu = FutuContext(
    host=FUTU_HOST,
    port=FUTU_PORT
)

futu.start()
