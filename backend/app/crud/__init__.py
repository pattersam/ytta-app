from .crud_video import video  # noqa: F401
from .crud_user import user  # noqa: F401
from .crud_label import label  # noqa: F401
from .crud_label_occurance import label_occurance  # noqa: F401

# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from app.models.item import Item
# from app.schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
