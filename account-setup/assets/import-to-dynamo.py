#!/usr/bin/env python

import sys
import csv
import boto3

dynamodb = boto3.resource("dynamodb")

if len(sys.argv) < 3:
    print("usage: {} <csv_filename_to_import> <dynamodb_table_name>".format(sys.argv[0]))
    exit(1)

filename = sys.argv[1]
tableName = sys.argv[2]


def main():
    with open(filename, 'rt', encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=',')
        write_to_dynamo(reader)

    return print("Done")

def write_to_dynamo(rows):
    table = dynamodb.Table(tableName)
    with table.batch_writer() as batch:
        for row in rows:
            item = dict()
            for k,v in row.items():
                keyname, kind = k.split(" | ")
                if kind == "integer":
                    v = int(v)
                item[keyname] = v
            batch.put_item(Item=item)
main()