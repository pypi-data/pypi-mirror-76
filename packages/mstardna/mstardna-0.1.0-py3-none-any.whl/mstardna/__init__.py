__version__ = '0.1.0'

import io
import re
import time

import boto3
import pandas as pd


def query_athena(session, params, max_execution = 5):
    client = session.client('athena', region_name=params["region"])
    start_execution_response = client.start_query_execution(
        QueryString=params["query"],
        QueryExecutionContext={
            'Database': params['database']
        },
        ResultConfiguration={
            'OutputLocation': f"s3://{params['bucket']}/{params['bucket_folder']}"
        }
    )
    query_execution_id = start_execution_response['QueryExecutionId']
    state = 'RUNNING'

    while (max_execution > 0 and state in ['RUNNING', 'QUEUED']):
        max_execution = max_execution - 1
        get_execution_response = client.get_query_execution(QueryExecutionId = query_execution_id)

        if 'QueryExecution' in get_execution_response and \
                'Status' in get_execution_response['QueryExecution'] and \
                'State' in get_execution_response['QueryExecution']['Status']:
            state = get_execution_response['QueryExecution']['Status']['State']
            if state == 'FAILED':
                return get_execution_response
            elif state == 'SUCCEEDED':
                s3_path = get_execution_response['QueryExecution']['ResultConfiguration']['OutputLocation']
                filename = re.findall('.*\/(.*)', s3_path)[0]
                return filename
        time.sleep(1)
    
    return False
