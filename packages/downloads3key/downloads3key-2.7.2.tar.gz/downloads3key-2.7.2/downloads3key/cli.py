import boto3
import os
from datetime import datetime
import click
import json
from downloads3key import __version__

def print_info(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(json.dumps({"version": __version__}, indent=2))
    ctx.exit()

@click.command()
@click.option('--bucket', '-b', required=True, help='Bucket name.', type=None)
@click.option('--key', '-k', required=True, help='Key.')
@click.version_option(version=__version__, prog_name="Download s3 key cli")
@click.option("--info", is_flag=True, is_eager=True, callback=print_info, expose_value=False)
def download(bucket, key):
    session = boto3.Session()
    s3_client = session.client('s3')
    bucket_name = bucket;

    path_separator = os.path.sep
    output_folder_path = '.' + path_separator + 'output' + path_separator + str(datetime.now())

    print('BucketName:' + bucket_name)
    print('Key:' + key)

    versions = s3_client.list_object_versions(Bucket=bucket_name, Prefix=key)

    # Create a reusable Paginator
    paginator = s3_client.get_paginator('list_object_versions')

    page_iterator = paginator.paginate(Bucket=bucket_name, Prefix=key)



    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)
    print('Downloading to:' + output_folder_path)

    i = 0
    head, file_name = os.path.split(key)

    for page in page_iterator or []:
        versions = page['Versions'] or []
        for obj in versions:
            i = i + 1
            actual_version_id = obj.get('VersionId')
            version_id = ''
            if actual_version_id != 'null':
                version_id = actual_version_id
            output_file = output_folder_path + path_separator + file_name + '_' + version_id + '_'+str(
                obj.get('LastModified').date().isoformat()) 
            s3_client.download_file(bucket_name, key, output_file, ExtraArgs={"VersionId": actual_version_id})

    print("Total Files: " + str(i))