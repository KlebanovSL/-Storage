"""empty message

Revision ID: 6553a3ebbbe2
Revises: db76b0ac3e57
Create Date: 2024-10-01 12:02:02.770436

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6553a3ebbbe2"
down_revision: Union[str, None] = "db76b0ac3e57"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "orders",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.Enum("in_progress", "sent", "delivered", name="orderstatus"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_orders_id"), "orders", ["id"], unique=False)
    op.create_table(
        "orderitems",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("order_id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.CheckConstraint(
            "quantity > 0", name="quantity should be greater than 0"
        ),
        sa.ForeignKeyConstraint(
            ["order_id"], ["orders.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["products.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_orderitems_id"), "orderitems", ["id"], unique=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_orderitems_id"), table_name="orderitems")
    op.drop_table("orderitems")
    op.drop_index(op.f("ix_orders_id"), table_name="orders")
    op.drop_table("orders")
    # ### end Alembic commands ###
