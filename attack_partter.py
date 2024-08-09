import requests
import json
import sys

def search_stix_core_objects(api_key, search_term, output_file):
    url = "http://192.168.168.143:8080/graphql"

    headers = {
        "Host": "192.168.168.143:8080",
        "Accept": "*/*",
        "Accept-Language": "en-US",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, như Gecko) Chrome/126.0.6478.127 Safari/537.36",
        "Content-Type": "application/json",
        "Origin": "http://192.168.168.143:8080",
        "Referer": f"http://192.168.168.143:8080/dashboard/search/knowledge/v-asm?filters=%7B%22mode%22%3A%22and%22%2C%22filters%22%3A%5B%7B%22id%22%3A%22669b4d8a-fc93-4ad4-9357-667dbe8cda97%22%2C%22key%22%3A%22entity_type%22%2C%22values%22%3A%5B%5D%2C%22operator%22%3A%22eq%22%2C%22mode%22%3A%22or%22%7D%5D%2C%22filterGroups%22%3A%5B%5D%7D&sortBy=_score&orderAsc=false",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Authorization": f"Bearer {api_key}"  # Thêm API key vào headers
    }

    # Loại bỏ ký tự Unicode khỏi headers
    for key, value in headers.items():
        headers[key] = value.encode('ascii', 'ignore').decode('ascii')

    payload = {
        "id": "SearchStixCoreObjectsLinesPaginationQuery",
        "query": """query SearchStixCoreObjectsLinesPaginationQuery(
  $types: [String]
  $search: String
  $count: Int!
  $cursor: ID
  $orderBy: StixCoreObjectsOrdering
  $orderMode: OrderingMode
  $filters: FilterGroup
) {
  ...SearchStixCoreObjectsLines_data_4GmerJ
}

fragment SearchStixCoreObjectLine_node on StixCoreObject {
  __isStixCoreObject: __typename
  id
  parent_types
  entity_type
  created_at
  ... on StixObject {
    __isStixObject: __typename
    representative {
      main
      secondary
    }
  }
  createdBy {
    __typename
    __isIdentity: __typename
    name
    id
  }
  objectMarking {
    id
    definition_type
    definition
    x_opencti_order
    x_opencti_color
  }
  objectLabel {
    id
    value
    color
  }
  creators {
    id
    name
  }
  containersNumber {
    total
  }
}

fragment SearchStixCoreObjectsLines_data_4GmerJ on Query {
  globalSearch(types: $types, search: $search, first: $count, after: $cursor, orderBy: $orderBy, orderMode: $orderMode, filters: $filters) {
    edges {
      node {
        __typename
        id
        entity_type
        created_at
        createdBy {
          __typename
          __isIdentity: __typename
          name
          id
        }
        creators {
          id
          name
        }
        objectMarking {
          id
          definition_type
          definition
          x_opencti_order
          x_opencti_color
        }
        ...SearchStixCoreObjectLine_node
      }
      cursor
    }
    pageInfo {
      endCursor
      hasNextPage
      globalCount
    }
  }
}""",
        "variables": {
            "count": 25,
            "orderMode": "desc",
            "orderBy": "_score",
            "filters": {
                "mode": "and",
                "filters": [
                    {
                        "key": "entity_type",
                        "values": ["Stix-Core-Object"],
                        "operator": "eq",
                        "mode": "or"
                    }
                ],
                "filterGroups": []
            },
            "search": search_term
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    # In ra toàn bộ nội dung response với định dạng JSON dễ đọc và ghi vào tệp
    formatted_response = {
        "Status Code": response.status_code,
        "Response Headers": dict(response.headers),
        "Response Content": response.json()
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(formatted_response, f, ensure_ascii=False, indent=4)

    print(f"Kết quả đã được ghi vào tệp: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python search_query.py <api_key> <search_term> <output_file>")
        sys.exit(1)

    api_key = "b4e69d3d-8e36-4633-ab10-ca542671f821"
    search_term = sys.argv[1]
    output_file = sys.argv[2]
    search_stix_core_objects(api_key, search_term, output_file)
