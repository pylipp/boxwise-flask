"""GraphQL type definitions"""
from ariadne import gql

type_defs = gql(
    """
    type Query {
        hello: String!
        allBases: [Base]
        allUsers: [User]
        user(email: String): User
        box(id: Int): Box
    }
    type Base {
        id: Int!
        name: String
        organisation_id: Int
    }
    type User{
        id: Int!
        organisation_id: Int
        name: String
        email: String!
        cms_usergroups_id: Int
        valid_firstday: Date
        valid_lastday: Date
        camp_id: [Int]
        lastlogin: Datetime
        lastaction: Datetime
    }
    type Box{
        id: Int!
        box_id: String!
        product_id: Int!
        size_id: Int!
        items: Int!
        location_id: Int!
        qr_id: Int
        comments: String
        box_state_id: Int
        deleted: Datetime
    }

    scalar Datetime
    scalar Date
"""
)
