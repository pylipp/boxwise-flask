"""GraphQL resolver functionality"""
from ariadne import (
    MutationType,
    ObjectType,
    ScalarType,
    make_executable_schema,
    snake_case_fallback_resolvers,
)

from .auth_helper import authorization_test
from .models import (
    QR,
    Box_State,
    Camps,
    Cms_Users,
    Genders,
    Locations,
    Products,
    Sizes,
    Stock,
)
from .type_defs import type_defs

query = ObjectType("Query")
mutation = MutationType()

datetime_scalar = ScalarType("Datetime")
date_scalar = ScalarType("Date")


@datetime_scalar.serializer
def serialize_datetime(value):
    return value.isoformat()


@date_scalar.serializer
def serialize_date(value):
    return value.isoformat()


# registers this fn as a resolver for the "allBases" field, can use it as the
# resolver for more than one thing by just adding more decorators
@query.field("allBases")
def resolve_all_camps(_, info):
    # discard the first input because it belongs to a root type (Query, Mutation,
    # Subscription). Otherwise it would be a value returned by a parent resolver.
    response = Camps.get_all_camps()
    return list(response.dicts())


@query.field("base")
def resolve_camp(_, info, id):
    authorization_test("bases", base_id=id)
    response = Camps.get_camp(id)
    return response


@query.field("allUsers")
def resolve_all_users(_, info):
    response = Cms_Users.get_all_users()
    return list(response.dicts())


@query.field("user")
def resolve_user(_, info, email):
    response = Cms_Users.get_user(email)
    return response


@query.field("qr")
def resolve_qr(_, info, code):
    response = QR.get_qr(code)
    return response


@query.field("product")
def resolve_product(_, info, id):
    response = Products.get_name(id)
    return response


@query.field("gender")
def resolve_gender(_, info, id):
    response = Genders.get_label(id)
    return response


@query.field("size")
def resolve_size(_, info, id):
    response = Sizes.get_label(id)
    return response


@query.field("box_state")
def resolve_box_state(_, info, id):
    response = Box_State.get_label(id)
    return response


@query.field("location")
def resolve_location(_, info, id):
    response = Locations.get_label(id)
    return response


@query.field("box")
def resolve_box(_, info, qr_code):
    response = Stock.get_box(qr_code)
    return response


@mutation.field("createBox")
def create_box(_, info, input):
    response = Stock.create_box(input)
    return response


schema = make_executable_schema(
    type_defs, [query, mutation], snake_case_fallback_resolvers
)
