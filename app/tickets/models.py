from pydantic import BaseModel

class Ticket(BaseModel):
    event_id: int
    user_id: int
    seat_number: str
