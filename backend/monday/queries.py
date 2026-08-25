"""Monday.com GraphQL queries."""

BOARD_METADATA_QUERY = """
query ($boardId: ID!) {
    boards(ids: [$boardId]) {
        id
        name
        description
        columns {
            id
            title
            type
            settings_str
        }
    }
}
"""

BOARD_ITEMS_QUERY = """
query ($boardId: ID!, $limit: Int!, $cursor: String) {
    boards(ids: [$boardId]) {
        id
        name
        items_page(limit: $limit, cursor: $cursor) {
            cursor
            items {
                id
                name
                column_values {
                    id
                    text
                    value
                    type
                }
            }
        }
    }
}
"""

SIMPLE_BOARD_QUERY = """
query ($boardId: ID!) {
    boards(ids: [$boardId]) {
        id
        name
        items_page(limit: 500) {
            cursor
            items {
                id
                name
                column_values {
                    id
                    text
                    value
                    type
                }
            }
        }
    }
}
"""
