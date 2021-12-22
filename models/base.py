"""
Base model and schema.
"""
from database import ma
from common.response import fail


class BaseSchema(ma.SQLAlchemyAutoSchema):
    """
    Schema that uses camel-case for its external representation
    and snake-case for its internal representation.
    """

    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = camelcase(field_obj.data_key or field_name)

    def validate_or_400(self, form):
        errors = self.validate(form)
        if errors:
            message = {"form": errors}
            fail(400, data=message)
        return form


def camelcase(s):
    """
    Convert snake case to camel case.
    """
    parts = iter(s.split("_"))
    return next(parts) + "".join(i.title() for i in parts)
