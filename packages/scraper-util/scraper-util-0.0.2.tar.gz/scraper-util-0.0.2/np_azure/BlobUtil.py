# -*- coding: utf-8 -*-
"""""
Created on Mon Aug 10 13:27:36 2020

@author: mengmeng
"""""

import os
import logging
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError


class BlobUtil:
    @staticmethod
    def upload_data_to_blob(data, container_name, blob_name):
        """
        write data to azure storage blob
        :param data: data content to be written
        :param container_name: container on azure
        :param blob_name: blob name of this file
        """
        try:
            logging.info(f"Trying to write to container, blob: {container_name}, {blob_name}")
            connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
            # Create the BlobServiceClient object which will be used to create a container client
            blob_service_client = BlobServiceClient.from_connection_string(connect_str)

            # Create container if not exists
            try:
                blob_service_client.create_container(container_name)
            except ResourceExistsError:
                blob_service_client.get_container_client(container_name)

            blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
            blob_client.upload_blob(data)
            logging.info(f"Successfully wrote to container, blob: {container_name}, {blob_name}")

        except Exception as ex:
            logging.error(f'Write to blob failed: container {container_name}, blob name {blob_name}')
            logging.error(ex)


if __name__ == "__main__":
    print('start')
    BlobUtil.upload_data_to_blob("test", "edf", "test.txt")