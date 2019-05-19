import os

from pprint import pprint as pp
import google
from google.cloud import storage

BKT_NAME = "images3"
img_dir = "/images/"

class CloudStorage():
        def __init__(self):
                self.client = storage.Client()
                self.bkt_name = BKT_NAME
                try:
                        import pdb; pdb.set_trace()
                        self.bkt_obj = self.client.get_bucket(self.bkt_name)
                #except google.cloud.exceptions.NotFound:
                #       raise Exception("Sorry, that bucket does not exist!")
                except Exception as e:
                        print e.message
                        self.create_bucket()

        def create_bucket(self):
                self.bkt_obj = self.client.create_bucket(self.bkt_name)

        def check_create_bucket(self):
                bucket = self.client.lookup_bucket(BKT_NAME)
                if bucket is None:
                        raise Exception("Sorry, that bucket does not exist!")

        def upload_file(self, src_name, dest_name):
                print("Uploading {} file...".format(src_name))
                blob = self.bkt_obj.blob(dest_name)
                blob.upload_from_filename(src_name)
                print("File {} uploaded to {}".format(
                        src_name, dest_name))
                #import pdb; pdb.set_trace()


cs = CloudStorage()
fname = "temp.txt"
floc = "/temp.txt"

for img in os.listdir(img_dir):
        img_name = img
        img_path = img_dir + img_name
        cs.upload_file(img_path, img_name)

