from azure.storage.blob import BlobClient, ContentSettings

class Logger():
    def __init__(self, connection_string, container, blob):
        self.container = container
        self.blob = blob
        self.connection_string = connection_string
        self.my_content_settings = ContentSettings(content_type='text/plain')

    def log(self, message:str):
        blob = BlobClient.from_connection_string(
                            conn_str=self.connection_string, 
                            container_name=self.container,
                            blob_name=self.blob)

        try:
            blob.append_block(message + '\n')

            print(f'Succesfully logged message')

        except Exception as e:
            blob.create_append_blob(content_settings=self.my_content_settings)
            blob.append_block(message + '\n')

            print(f'---Blob {self.blob} has been created, did not exist---')
            print(e)
            print(f'Succesfully logged message')
