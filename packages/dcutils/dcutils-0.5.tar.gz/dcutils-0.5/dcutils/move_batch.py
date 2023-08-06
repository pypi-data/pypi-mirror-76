import datetime
from google.cloud import storage
from move import mv_blob

def mv_batch(config, SRC_BUCKET, DEST_BUCKET, DEST_BLOB, PARENT_FOLDER):
    STORAGE_CLIENT = storage.Client.from_service_account_json(config)

    blobs = STORAGE_CLIENT.list_blobs(SRC_BUCKET)
    for blob in blobs:
        folders = blob.name.split('/')
        if folders[0] == 'datasets':
            print('working on {}'.format(blob.name))
            mv_blob(
                STORAGE_CLIENT,
                blob.name, DEST_BLOB + '/' + blob.name,
                SRC_BUCKET,
                DEST_BUCKET
            )