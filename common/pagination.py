from flask import request
from sqlalchemy import sql
from models.user import UserSchema
from common.case import snakecase
from common.response import fail


def get_pagination_args():
    """
    Pagination for collections will use page and size as query params
    """
    page = int(request.args.get("page", 1))
    size = int(request.args.get("size", 10))
    return page, size


def get_sort_by():
    """
    Return the string for sqlalchemy to use for order_by from query_params.
    """
    sort_by = snakecase(request.args.get("sortby", "id"))
    if sort_by not in UserSchema().field_names():
        fail(400, {"sortby": "Sortby is not a valid field for resource"})

    order = request.args.get("order", "asc").lower()
    if order not in ["asc", "desc"]:
        fail(400, {"order": "Order must be asc or desc"})

    return sql.text(f"{sort_by} {order}")
