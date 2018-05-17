from decimal import Decimal

# when numbers are retreived from the message queue, they sometimes
# end up as large scientific numbers. In order to avoid this and get
# nice, clean integers we needed to use this work around.
def sanitize(num):
    return int(Decimal( num ))
