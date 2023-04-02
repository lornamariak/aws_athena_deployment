""" Athena deployment script"""
import boto3

# create an Athena client
client = boto3.client("athena")

CREATE_TABLE_QUERY = """
CREATE EXTERNAL TABLE IF NOT EXISTS acidity_data (
    index BIGINT,
    year INT,
    county STRING,
    violent STRING,
    drug_off STRING,
    population STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LOCATION "s3://bucket_name/testdata.csv"
"""

response = client.start_query_execution(
    QueryString=CREATE_TABLE_QUERY,
    ResultConfiguration={"OutputLocation": "s3://bucket_name/test_query/"},
)

QueryExecutionId = response["QueryExecutionId"]
QUERYSTATUS = "RUNNING"
while QUERYSTATUS == "RUNNING":
    query_execution = client.get_query_execution(QueryExecutionId=QueryExecutionId)
    query_status = query_execution["QueryExecution"]["Status"]["State"]
    print(f"Query execution status: {QUERYSTATUS}")
AGGREGATEQUERY = """
SELECT *
FROM "test_database"."data" limit 50;
"""

response = client.start_query_execution(
    QueryString=AGGREGATEQUERY,
    ResultConfiguration={"OutputLocation": "s3://bucket_name/test_database/"},
)

query_execution_id = response["QueryExecutionId"]
QUERYSTATUS = "RUNNING"
while QUERYSTATUS == "RUNNING":
    query_execution = client.get_query_execution(QueryExecutionId=query_execution_id)
    query_status = query_execution["QueryExecution"]["Status"]["State"]
    print(f"Query execution status: {QUERYSTATUS}")

RESULTBUCKET = "bucket_name"
result_key = query_execution_id + ".csv"
s3 = boto3.resource("s3")
s3.Object(RESULTBUCKET, result_key).download_file(f"/tmp/{result_key}")

with open(f"/tmp/{result_key}", "r", encoding="utf-8") as f:
    print(f.read())
