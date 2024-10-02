from fastapi import APIRouter

from src.storage.urls.products import router as products_router
from src.storage.urls.orders import router as orders_router


router = APIRouter()

router.include_router(
    router=products_router,
    prefix="/products",
    tags=["products"],
)
router.include_router(
    router=orders_router,
    prefix="/orders",
    tags=["orders"],
)
