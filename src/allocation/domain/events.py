from dataclasses import dataclass


class Event:
    pass


@dataclass
class Allocated(Event):
    order_id: str
    sku: str
    qty: int
    batch_ref: str


@dataclass
class Deallocated(Event):
    order_id: str
    sku: str
    qty: int


@dataclass
class OutOfStock(Event):
    sku: str
