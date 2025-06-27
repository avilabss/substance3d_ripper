COLLECTION_QUERY = """query Collection($id: String!, $search: String, $page: Int, $limit: Int = 20, $sort: AssetSort = sameAsIds, $sortDir: SortDir = asc, $filters: AssetFilters) {
collection(id: $id) {
    id
    title
    imageUrl
    assets(
      sort: $sort
      sortDir: $sortDir
      page: $page
      limit: $limit
      filters: $filters
      search: $search
    ) {
      total
      hasMore
      items {
        ...AssetAttachmentsFragment
        __typename
      }
      __typename
    }
    __typename
  }
}

fragment AssetAttachmentsFragment on Asset {
  ...AssetFragment
  attachments {
    id
    tags
    label
    ... on PreviewAttachment {
      kind
      url
      __typename
    }
    ... on DownloadAttachment {
      url
      __typename
    }
    __typename
  }
  __typename
}

fragment AssetFragment on Asset {
  id
  title
  tags
  status
  categories
  cost
  new
  free
  licenses
  downloadsRecentlyUpdated
  thumbnail {
    id
    url
    tags
    __typename
  }
  createdAt
  __typename
}"""
