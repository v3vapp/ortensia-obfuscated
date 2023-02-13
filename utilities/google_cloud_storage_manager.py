import sys, pathlib, logging, time, os
outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent 
working_dir = pathlib.Path(__file__).resolve().parent.parent 
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append(str(working_dir))
sys.path.append(f"{str(working_dir)}/config")
sys.path.append(f"{str(working_dir)}/strategy")
from google.cloud import storage
import pathlib
import report

logging.basicConfig(level=logging.INFO,format="%(asctime_data)s : %(message)s")

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = f"{working_dir}/config/googleCloud_project.json"

def download():
    bucket_name = 'project_bucket'
    prefix = 'PRODUCTION/'
    dl_dir = f'{current_dir}/{bucket_name}/'

    os.makedirs(dl_dir, exist_ok=True)

    storage_client = storage.Client()
    blobs_in_bucket = storage_client.list_blobs(bucket_name, prefix=prefix)

    for blob in blobs_in_bucket:
        local_filename = (pathlib.Path(dl_dir) / blob.name.split("/")[-1]).resolve()
        blob.download_to_filename(filename=str(local_filename))
        logging.info(f"{local_filename}")


def upload(bucket_name, local_path, googleCloudStorage_path):

    # os.makedirs(f"static/{googleCloudStorage_path}{file_name}", exist_ok=True)

    client_storage = storage.Client()
    bucket         = client_storage.get_bucket(bucket_name)

    blob_data = bucket.blob(googleCloudStorage_path)
    blob_data.upload_from_filename(local_path) 




if __name__ == "__main__":
    # test upload
    # googleCloudStorage_path = f'ACCOUNT/wallet.csv'
    os.makedirs(f"static/ACCOUNT", exist_ok=True)

    googleCloudStorage_path = 'ACCOUNT/position.csv'
    local_path = f'{working_dir}/static/{googleCloudStorage_path}'

    bucket_name    = "project_bucket"

    upload(bucket_name, local_path, googleCloudStorage_path)