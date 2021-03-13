"""
Convert any snake case to camel case as JSON will use camel case and our
database uses snake case.
"""
from database import ma


class CamelCaseSchema(ma.SQLAlchemyAutoSchema):
    """
    Schema that uses camel-case for its external representation
    and snake-case for its internal representation.
    """
    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = camelcase(field_obj.data_key or field_name)


def camelcase(s):
    """
    Convert snake case to camel case.
    """
    parts = iter(s.split('_'))
    return next(parts) + ''.join(i.title() for i in parts)
