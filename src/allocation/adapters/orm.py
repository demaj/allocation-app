import logging

from sqlalchemy import event
from sqlalchemy.orm import mapper, relationship
from sqlalchemy.sql.schema import (Column, Date, ForeignKey, Integer, MetaData,
                                   String, Table)

from allocation.domain import model

logger = logging.getLogger(__name__)

metadata = MetaData()

order_lines = Table(
    "order_lines",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sku", String(255)),
    Column("qty", Integer, nullable=False),
    Column("order_id", String(255)),
)

products = Table(
    "products",
    metadata,
    Column("sku", String(255), primary_key=True),
    Column("version_number", Integer, nullable=False, server_default="0"),
)

batches = Table(
    "batches",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("reference", String(255)),
    Column("sku", ForeignKey("products.sku")),
    Column("_purchased_quantity", Integer, nullable=False),
    Column("eta", Date, nullable=True),
)

allocations = Table(
    "allocations",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("order_line_id", ForeignKey("order_line.id")),
    Column("batch_id", ForeignKey("batches.id")),
)

allocations_view = Table(
    "allocations_view",
    metadata,
    Column("order_id", String(255)),
    Column("sku", String(255)),
    Column("batch_ref", String(255)),
)


def start_mappers():
    logger.info("Starting mappers")
    lines_mapper = mapper(model.OrderLine, order_lines)
    batches_mapper = mapper(
        model.Batch,
        batches,
        properties={
            "_allocations": relationship(
                lines_mapper,
                secondary=allocations,
                collection_class=set,
            )
        },
    )
    mapper(
        model.Product,
        products,
        properties={"batches": relationship(batches_mapper)},
    )


@event.listens_for(model.Product, "load")
def receive_load(product, _):
    product.events = []
