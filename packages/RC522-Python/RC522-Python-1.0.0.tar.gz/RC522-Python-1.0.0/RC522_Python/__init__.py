__version__ = "1.0.0"

try:
    from .rfid import RFID
    from .util import RFIDUtil
except RuntimeError:
    print("Must be used on Raspberry Pi")
