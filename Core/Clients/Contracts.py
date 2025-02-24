GET_BOOKING_ID = {
    "type": "object",
    "properties": {
        "firstname": "string",
        "lastname": "string",
        "totalprice": "number",
        "depositpaid": "bool",
        "bookingdates": {
            "checkin": "string",
            "checkout": "string"
        },
        "additionalneeds": "string"
    },
    "required": ["firstname", "lastname", "totalprice", "depositpaid", "checkin", "checkout", "additionalneeds"]
}
