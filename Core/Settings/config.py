from enum import Enum
from pyclbr import Class


class Users(Enum):
    USERNAME = 'admin'
    PASSWORD = 'password123'

class Timeouts(Enum):
    TIMEOUT = 5


class BookingId(Enum):
    BOOKING_ID = '1'
