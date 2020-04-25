import gdown
import os
import logging

bag_url = "https://drive.google.com/u/1/uc?id=14tylU87DGjftjtDpZWXw6M40xnbbQXl2&export=download"
bag_name = "demo"
if not os.path.isfile(bag_name):
    gdown.download(bag_url, output=bag_name + '.bag', quiet=False)

print("Finished downloading rosbag.") 