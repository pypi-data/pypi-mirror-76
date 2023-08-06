__version__ = '0.1.1'

import io
import re
import time
from typing import Dict
import uuid

import boto3


class Athena:

    def __init__(self,
                 database: str = 'rdb_currentdata',
                 tmp_bucket: str = 'aws-athena-query-results-815622608052-us-east-1',
                 tmp_folder: str = None,
                 region: str = 'us-east-1',
                 print_info: bool = True):

        self.database: str = database
        self.tmp_bucket: str = tmp_bucket
        if tmp_folder is None:
            self.tmp_folder: str = f'tmp-{uuid.uuid4()}'
        else:
            self.tmp_folder: str = tmp_folder
        self.tmp_folder: str = tmp_folder
        self.region: str = region
        self.print_info = print_info

        self.session = boto3.Session()
        self.client = boto3.client('s3')


    def query(self, query_string, number_of_times_to_poll: int = 5) -> (bool, str):
        client = self.session.client('athena', region_name = self.region)

        start_execution_response = client.start_query_execution(
            QueryString = query_string,
            QueryExecutionContext = {
                'Database': self.database
            },
            ResultConfiguration={
                'OutputLocation': f"s3://{self.tmp_bucket}/{self.tmp_folder}"
            }
        )

        query_execution_id = start_execution_response['QueryExecutionId']

        if self.print_info: print('staring query', end = '')
        state = 'RUNNING'
        poll_attempt = 0
        while (number_of_times_to_poll > poll_attempt and state in ['RUNNING', 'QUEUED']):
            get_execution_response = client.get_query_execution(QueryExecutionId = query_execution_id)
            if 'QueryExecution' in get_execution_response and \
                'Status' in get_execution_response['QueryExecution'] and \
                'State' in get_execution_response['QueryExecution']['Status']:
                state = get_execution_response['QueryExecution']['Status']['State']
                if state == 'FAILED':
                    return False, get_execution_response
                elif state == 'SUCCEEDED':
                    s3_path = get_execution_response['QueryExecution']['ResultConfiguration']['OutputLocation']
                    filename = re.findall('.*\/(.*)', s3_path)[0]
                    return True, filename
            
            if self.print_info: print('.', end = '')
            poll_attempt += 1
            time.sleep(1)
        
        return False, ''
    
    def get_query_results(self, object_name: str) -> io.BytesIO:
        obj = self.client.get_object(Bucket = self.tmp_bucket, Key = f'{self.tmp_folder}/{object_name}')
        return io.BytesIO(obj['Body'].read())
