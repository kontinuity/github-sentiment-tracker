import json

from aws import get_aws_resource

ddb_table = None


def save_item(id_key, final_sentiment, data_block, only_if_absent=False):
    item = {"identifier_key": id_key, "final_sentiment": final_sentiment, "comprehend_data": json.dumps(data_block)}
    ddbt = _get_ddb_table()
    if only_if_absent:
        ddbt.put_item(Item=item, ConditionExpression="attribute_not_exists(identifier_key)")
    else:
        ddbt.put_item(Item=item)


def get_item(id_key):
    ddbt = _get_ddb_table()
    return ddbt.get_item(Key={"identifier_key": id_key}).get("Item")


def _get_ddb_table():
    global ddb_table
    if not ddb_table:
        dynamodb = get_aws_resource("dynamodb")
        ddb_table = dynamodb.Table("your-dynamodb-table-name")
    return ddb_table
