"""
Base model and schema.
"""
from database import ma
from common.response import fail
from common.case import camelcase


class BaseSchema(ma.SQLAlchemyAutoSchema):
    """
    Schema that uses camel-case for its external representation
    and snake-case for its internal representation.

    Data in pre_load and post_dump methods for schemas that inherit from this
    class will have camel-case field names.
    """

    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = camelcase(field_obj.data_key or field_name)

    def validate_or_400(self, form):
        errors = self.validate(form)
        if errors:
            message = {"form": errors}
            fail(400, data=message)
        return form

    def field_names(self):
        return self._declared_fields.keys()
