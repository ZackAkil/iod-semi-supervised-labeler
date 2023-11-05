# python -m pytest 

import cloud_storage_to_automl_labels

def test_location_just_bucket():

    location = 'bucket'
    bucket_name, folder = cloud_storage_to_automl_labels.get_bucket_folder(location)

    assert bucket_name == 'bucket'
    assert folder == ''

def test_location_bucket_and_folder_slash():

    location = 'bucket/foo/'
    bucket_name, folder = cloud_storage_to_automl_labels.get_bucket_folder(location)

    assert bucket_name == 'bucket'
    assert folder == 'foo/'

def test_location_bucket_and_folder():

    location = 'bucket/foo'
    bucket_name, folder = cloud_storage_to_automl_labels.get_bucket_folder(location)

    assert bucket_name == 'bucket'
    assert folder == 'foo'

def test_location_bucket_and_deep_folder():

    location = 'bucket/foo/bar/hello/'
    bucket_name, folder = cloud_storage_to_automl_labels.get_bucket_folder(location)

    assert bucket_name == 'bucket'
    assert folder == 'foo/bar/hello/'

