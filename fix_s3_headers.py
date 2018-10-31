import boto3

s3 = boto3.client('s3')

bucket_name = 'mybucketwebsitetest'

def is_bad_header(bucket, key):
    try:
        response = s3.head_object(Bucket=bucket, Key=key)
        if 'ContentEncoding' in response:
            modified_meta = {}
            for meta in ['CacheControl', 'ContentDisposition', 'ContentLanguage', 'ContentType', 'WebsiteRedirectLocation']:
                if response.get(meta):
                    modified_meta[meta] = response.get(meta)
            return modified_meta 
        else:
            return False
    except Exception as e:
        print(e)


if __name__ == "__main__":
    response = s3.list_objects_v2(
        Bucket=bucket_name,
        MaxKeys=1000,
    )

    count = 0
    while True:
        NextContinuationToken = response.get('NextContinuationToken')
        objects = response['Contents']
        for obj in objects:
            key = obj['Key']

            modified_meta = is_bad_header(bucket_name, key)
            if modified_meta:
                resp = s3.copy_object(
                    Bucket=bucket_name,
                    CopySource={'Bucket': bucket_name, 'Key': key},
                    Key=key,
                    MetadataDirective='REPLACE',
                    **modified_meta
                )
                print('processing {}/{}'.format(bucket_name, key))
                count += 1

        if NextContinuationToken:
            response = s3.list_objects_v2(
                Bucket=bucket_name,
                MaxKeys=1000,
                ContinuationToken=NextContinuationToken
            )
        else: 
            break
    
    print("cleared {} keys".format(count))
