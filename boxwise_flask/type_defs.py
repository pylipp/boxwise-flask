"""GraphQL type definitions"""
from ariadne import gql

type_defs = gql(
    """
    type Query {
        hello: String!
        allBases: [Base]
        base(id: String!): Base
        allUsers: [User]
        user(email: String): User
        box(qr_code: String): Box
        qr(code: String): QR
        product(id: Int): Product
    }
    type Mutation {
        createBox(input:CreateBoxInput):Box
    }
    type Base {
        id: Int
        name: String
        currencyname: String
        organisation_id: Int
    }
    type User {
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

    type QR {
        id: Int!
        code: String!
    }

    type Product {
        id: Int!
        name: String
        gender_id: Int
    }

    type Box {
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
        created_by: String
    }

    input CreateBoxInput {
        box_id: Int!
        product_id: Int! #this is a foreign key
        size_id: Int! #this is a foreign key
        items: Int
        location_id: Int! #this is a foreign key
        comments: String!
        qr_id: String! #this is a foreign key
        created: String
        created_by: String
        box_state_id: String! #this is a foreign key
    }

    scalar Datetime
    scalar Date
"""
)
