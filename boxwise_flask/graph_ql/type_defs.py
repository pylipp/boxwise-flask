"""GraphQL type definitions"""
from ariadne import gql

# type Base {
#     id: Int
#     name: String
#     currencyname: String
#     organisation_id: Int
# }

type_defs = gql(
    """
    type Box {
        id: Int!
        boxLabelNumber: Int!
        location: Location!
        items: Int!
        product: Product!
        gender: ProductGender
        size: String!
        state:  State!
        qrCode: QRCode!
        lastModifiedBy: String!
        lastModifiedOn: Int!
        lastAction: String!
        comment: String
    }

    type QRCode {
        id: Int!
        code: String!
        createdOn: Int
        createdBy: String!
        lastModifiedOn: Int
        box: Box
    }

    type Product {
        id: Int!
        name: String!
        category: ProductCategory!
        sizeRange: SizeRange!
        sizes: [String!]!
        base: Base!
        price: Float
        gender: ProductGender
    }

    type ProductCategory {
        id: Int!
        categoryName: String!
        products: [Product]
        sizeRanges: [SizeRange]
        hasGender: Boolean
    }

    enum ProductGender {
        Men
        Women
        UnisexAdult
        UnisexChild
        UnisexBaby
        TeenGirl
        TeenBoy
        Girl
        Boy
    }

    enum BoxState {
        InStock
        Lost
        Ordered
        Picked
        Donated
        Scrap
    }

    type SizeRange {
        id: Int!
        label: String!
        sizes: [String!]!
        productCategory: [ProductCategory!]
    }

    type Location {
        id: Int!
        base: Base!
        name: String
        isShop: Boolean!
        isDeleted: Boolean!
        boxes: [Box!]
        hasBoxState: BoxState
    }

    type Base {
        id: Int!
        name: String!
        parentOrg: Organisation
        location: [Location]
        currencyName: String
    }

    type Organisation {
        id: Int!
        name: String!
        bases: [Base!]
    }

    type Order {
        id: Int!
        fromLocation: String!
        toLocation: String!
        fromOrg: Int
        toOrg: Int
        boxes: Box!
        isActive: Boolean!
        createdBy: String!
        createdOn: Int!
        lastModifiedBy: String
        lastModifiedOn: Int
        currencyName: String
        organisationId: Int
    }

    type User {
        id: Int!
        organisation_id: Int
        name: String
        email: String!
        usergroup_id: Int
        valid_firstday: Date
        valid_lastday: Date
        base_id: [Int]
        lastlogin: Datetime
        lastaction: Datetime
    }
 
    input CreateBoxInput {
        box_id: String #this is an output, but not an input
        product_id: Int! #this is a foreign key
        size_id: Int #this is a foreign key
        items: Int
        location_id: Int! #this is a foreign key
        comments: String!
        #this will get looked up to turn into qr_id, which is a foreign key
        qr_barcode: String!
        created: Datetime #this is an output, but not an input
        created_by: String #this is null in the table consistently
        box_state_id: Int  #this is an output, but not an input
    }

    scalar Datetime
    scalar Date
    """
)
