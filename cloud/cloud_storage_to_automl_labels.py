import argparse
import json

from google.cloud import storage


def get_bucket_folder(location):

    parts = location.split('/', 1)
    bucket_name = parts[0]

    if len(parts) > 1:
        folder = parts[1]
    else:
        folder = ''
    return bucket_name, folder


def extract_label_metadata(raw_metadata):
    labels_metadata = raw_metadata.get('labels')
    return json.loads(labels_metadata)


def create_automl_label_json(file_location, bboxes):

    print('boxes =', bboxes)

    boundingBoxAnnotations = []

    for box in bboxes:
        print('box', box)
        label_object = {'displayName': box['label_name'],
                        'yMin': box['ymin'],
                        'xMin': box['xmin'],
                        'yMax': box['ymax'],
                        'xMax': box['xmax']}
        boundingBoxAnnotations.append(label_object)

    label_record = {'imageGcsUri': file_location,
                    'boundingBoxAnnotations': boundingBoxAnnotations}

    return label_record


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Turn assisted labeled images in Google Storage into a labeled dataset for AutoML.')
    parser.add_argument('gs_location', metavar='gsl', type=str,
                        help='Location of Google Cloud Storage folder.')

    args = parser.parse_args()
    gs_location = args.gs_location

    print(args.gs_location)

    location = gs_location.replace('gs://', '')
    print(f'location: {location}')

    bucket_name, folder = get_bucket_folder(location)

    print(f'bucket: {bucket_name}, folder: {folder}')

    # bucket_name = "your-bucket-name"

    storage_client = storage.Client()

    # # Note: Client.list_blobs requires at least package version 1.17.0.
    blobs = storage_client.list_blobs(bucket_name, prefix=folder)

    # # Note: The call returns a response only when the iterator is consumed.
    label_records_list = []

    for blob in blobs:
        print(blob.name)
        print(blob.metadata)
        labels_metadata = extract_label_metadata(blob.metadata)
        full_file_name = f'gs://{bucket_name}/{blob.name}'
        label_record = create_automl_label_json(
            full_file_name, labels_metadata)
        label_records_list.append(label_record)

    with open('labels.jsonl', 'w') as f:

        for record in label_records_list:
            record_line = json.dumps(record)
            f.write(record_line + "\n")
