def identify_columns(
        header_row,
        identifier_name='',
        country_code_name='ga:countryIsoCode',
        value_name=None,  # Value assumed to be last
        **extra_columns
):
    """Optional call: Get index of relevant columns in each GA row.

    Args:
        header_row (list): Column headers for the GA rows
        identifier_name (str): Name of GA dimension for the identifier.
        country_code_name (str): Name of GA dimension for the country.
        value_name (str): Name of GA dimension for the value.

    Returns:
        tuple: indexes of identifier, country and value in each GA row.
    """
    value_index = header_row.index(value_name) if value_name else -1

    return [
        header_row.index(identifier_name),
        header_row.index(country_code_name),
        value_index,
    ] + [header_row.index(column) for column in extra_columns]


def generate_row_data(results, headers=None):
    """Yield headers and data from a Google Analytics report.

    Args:
        results (dict): Google Analytics statistics results.
        headers (dict): GA columns for identifier, country and value.

    Yields:
        list: CSV-style headers and data from the report.
    """
    report = results.get("reports")[0]
    column_header = report.get('columnHeader', {})

    metric_headers = column_header.get(
        'metricHeader', {}
    ).get('metricHeaderEntries', [])

    headers_row = column_header.get('dimensions', []).copy()
    headers_row.extend(header.get("name") for header in metric_headers)

    header_indices = [i for i in range(len(headers_row))]

    if headers:
        header_indices = identify_columns(headers_row, **headers)
        headers_row = [headers_row[i] for i in header_indices]

    yield headers_row

    for row in report.get('data', {}).get('rows', []):
        full_row = row['dimensions'] + row['metrics'][0]['values']
        full_row = [full_row[i] for i in header_indices]
        yield full_row


def build_ga_request(
        view_id,
        start_date,
        end_date,
        metrics,
        dimensions,
        filters=None,
        raw_filters=None,
):
    """Build a request body for querying Google Analytics.

    Args:
        view_id (str): View ID associated with GA account.
        start_date (str): in format YYYY-mm-dd.
        end_date (str): in format YYYY-mm-dd.
        metrics (list): Specific metrics to report.
        dimensions (list): How to break down metrics.
        filters (str): Path to filter dimensions by - only page path filters.
        raw_filters (dict): Complete filters, including filter types.

    Returns:
        dict: Request body used to query Google Analytics.
    """
    request_dict = {
        'viewId': view_id,
        'dateRanges': [{'startDate': start_date, 'endDate': end_date}],
        'metrics': [{'expression': metric} for metric in metrics],
        'dimensions': [{'name': dimension} for dimension in dimensions],
    }

    if filters:
        filter_set = [{'dimension_name': 'ga:pagePath', 'expressions': filters}]
        request_dict.update(dimensionFilterClauses=[{'filters': filter_set}])

    elif raw_filters:
        request_dict.update(dimensionFilterClauses=[{'filters': raw_filters}])

    return {'reportRequests': [request_dict]}


def get_statistics(service, request):
    return service.reports().batchGet(body=request).execute()
