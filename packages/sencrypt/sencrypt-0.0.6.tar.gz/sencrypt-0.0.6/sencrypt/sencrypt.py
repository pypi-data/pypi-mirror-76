import boto3
import click

session = boto3.session.Session()
s3 = session.resource('s3')

@click.group()
def cli():
    "Webotron lists and encripts S3 AWS buckets "
    pass

@cli.command('list-buckets')
def list_buckets():
    "List all buckets"
    for bucket in s3.buckets.all():
        print(bucket.name)

# @cli.command('list-bucket-objects')
# @click.argument('buckets', nargs=-1)
# def list_bucket_objects(buckets):
#     "Lists bucket objects"
#     allBuckets = s3.buckets.all()
#     for bucket in buckets:
#         print("-Objects from bucket: ", bucket)
#         print("----------------------------------")
#         if(s3.Bucket(bucket) in allBuckets):
#             for obj in s3.Bucket(bucket).objects.all():
#                 print(obj.key, end = " ")
#                 print("encrypted with ", s3.Object(bucket, obj.key).server_side_encryption)
#         else:
#             print("Bucket " + bucket + " does not exist")
#             print("Run 'list-buckets' command to see list of valid buckets")

@cli.command('audit-encryption')
@click.argument('bucket', required=False)
def audit_encription(bucket):
    "Check encription of all buckets OR objects of a bucket"
    s3client = session.client("s3")
    if(bucket is not None):
        allBuckets = s3.buckets.all()
        print("-Objects from bucket: ", bucket)
        print("----------------------------------")
        if (s3.Bucket(bucket) in allBuckets):
            for obj in s3.Bucket(bucket).objects.all():
                print('{:30}'.format(obj.key), end=" ")
                print("encrypted with ", s3.Object(bucket, obj.key).server_side_encryption)
        else:
            print("Bucket " + bucket + " does not exist")
            print("Run 'list-buckets' command to see list of valid buckets")
    else:
        for bucket in s3.buckets.all():
            try:
                default_encryption = s3client.get_bucket_encryption(Bucket = bucket.name)
            except Exception as e:
                if e.response['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFoundError':
                    print('{:50}'.format(bucket.name),": None")
                elif e.response['Error']['Code'] == 'AccessDenied':
                    print( bucket['Name'] + ' access denied while trying to check default encryption')
                else:
                    print( bucket['Name'] + ' error while trying to check default encryption:')
                    print(e)
            else:
                if 'ServerSideEncryptionConfiguration' in default_encryption and 'Rules' in default_encryption['ServerSideEncryptionConfiguration']:
                    print('{:50}'.format(bucket.name), end = " : encryption: ")
                    print( default_encryption['ServerSideEncryptionConfiguration']['Rules'][0]['ApplyServerSideEncryptionByDefault'])

@cli.command('set-encryption')
@click.argument('buckets', nargs=-1)
@click.option('--kms', help='kms key to be used')
@click.option('--existingobjects', help='Encrypt existing objects in bucket: TRUE or FALSE' )
def apply_encription(kms, buckets, existingobjects):
    "Enable encryption for a bucket(s)"
    s3client = session.client("s3")

    if kms is not None:
        target_encryption = {
            'Rules': [
                {
                    'ApplyServerSideEncryptionByDefault': {
                        'SSEAlgorithm': 'aws:kms',
                        'KMSMasterKeyID': kms
                    }
                },
            ]
        }
    else:
        target_encryption = {
            'Rules': [
                {
                    'ApplyServerSideEncryptionByDefault': {
                        'SSEAlgorithm': 'AES256',
                    }
                },
            ]
        }

    for bucket in buckets:
        fix_default_encryption(bucket, target_encryption)
        print(existingobjects)
        if(existingobjects.upper() == 'TRUE'):
            print("encrypting existing obj")
            # Encript existing objects
            for obj in s3.Bucket(bucket).objects.all():
                print(obj.key)
                s3.Bucket(bucket).copy({'Bucket': bucket,'Key': obj.key}, obj.key)


def fix_default_encryption(bucketName, target_encryption):
    s3client = session.client("s3")
    try:
        s3client.put_bucket_encryption(
            Bucket=bucketName,
            ServerSideEncryptionConfiguration=target_encryption
        )
    except Exception as e:
        if e.response['Error']['Code'] == 'AccessDenied':
            print( bucketName + ': access denied while trying to apply default encryption policy')
        else:
            print( bucketName + ': error while while trying to apply default encryption policy')
            print(e)
        return False
    else:
        print( bucketName + ':  default encryption policy ' + target_encryption['Rules'][0]['ApplyServerSideEncryptionByDefault']['SSEAlgorithm'] + ' successfully added.')
        return True

if __name__ == '__main__':
    cli()
