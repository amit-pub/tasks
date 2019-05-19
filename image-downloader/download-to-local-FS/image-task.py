from concurrent.futures import ThreadPoolExecutor
import threading
import os.path
import json
import sys

import requests

import util


# Declaring Macros
IMG_DIR = "/images/"
IMG_READ_BLOCK = 1024
DIVISION_POWER = 16
LOG_LEVEL = "INFO"
ERROR_FILE = "error-report.json"


class ImageManager():
    """
    This class is basically is created for efficiently downloading and storing
     images from web, by using the image URLs, fed to this program by either
     providing input file as argument or through editing config.conf file.

     This class performs following tasks:
        - to read the IMAGE urls from a text file,
        - store them locally in a directory (configurable through macro)
        - generates the hash value using the name of file
        - creates required sub-directories for possibly equaly and uniform hash
            distribution
        - creates output.log, error-report.json files as part of its execution
    """
    def __init__(self, img_fpath):
        self.img_fpath = img_fpath
        self.pre_checks()
        # get the maximum worker thread counts per the hardware of machine
        self.max_threads = int(util.get_worker_threads_count())
        # create a threadpool for max-thread as max workers
        self.t_exec = ThreadPoolExecutor(max_workers=self.max_threads)

    def pre_checks(self):
        # check whether the input file is present or not
        if not os.path.isfile(self.img_fpath):
            raise Exception("Input image file '{}' doesn't exist".format(
                            self.img_fpath))
        # check whether image directory exists, if not create one
        if not os.path.isdir(IMG_DIR):
            try:
                os.mkdir(IMG_DIR)
            except Exception as e:
                raise Exception("Cannot create '{}' directory: {}".format(
                                IMG_DIR, e.message))

    def deduce_storageparams(self, img_name, make_path=False):
        # get the name-prefix, based on which hash calculation is performed
        img_pre = img_name.split(".")[0][:4]
        hash_value = abs(hash(img_pre))
        # DIVISION_POWER macro is used so that the end-output should be of
        # same length, can be changed, if the number of images are too HIGH
        hash_part = hash_value / (10 ** DIVISION_POWER)
        img_dir = "{}{}/".format(IMG_DIR, hash_part)
        path = img_dir + img_name
        # check whether the images' required directory is present already
        # if not, create the directory.
        if make_path and not os.path.isdir(img_dir):
            try:
                os.mkdir(img_dir)
            except Exception as e:
                raise Exception("Cannot create '{}' directory: {}".format(
                                IMG_DIR, e.message))
        if make_path and os.path.isfile(path):
            print("File '{}' already present".format(path))

        return path

    def store_image(self, imgurl):
        # Get the image nam by parsing the image url
        img_name = imgurl.split("/")[-1].strip()

        # get the current thread-id, so that can be used to debug/identify
        # workers for img-urls
        tid = threading.current_thread().ident

        # call method to deduce the path where images should be stored
        img_path = self.deduce_storageparams(img_name, make_path=True)

        print(">>> Thread({}) - Downloading '{}' ....".format(tid, img_name))

        if os.path.exists(img_path):
            return

        # open the image file as write-binary mode and start writing content
        # block-by-block
        with open(img_path, mode="wb") as image:
            try:
                response = requests.get(imgurl, stream=True)
                if not response.ok:
                    raise Exception("Exception while fetching file from URL "
                                    "'{}': {}".format(imgurl, response.reason))

                for block in response.iter_content(IMG_READ_BLOCK):
                    if not block:
                        break
                    image.write(block)
            except Exception as e:
                raise e
        print("    <<< Thread({}) - Download completed '{}'".format(tid,
                                                                    img_name))

    def download_from_imgfile(self):
        futures_objs = {}  # this maintains the future objets from pool
        succ_count = 0  # count of success downloads
        fail_count = 0  # count of failed downloads
        total_errors = []  # to cache total errors while processing outputs

        with open(self.img_fpath, mode="r") as ifile:
            for line in ifile.readlines():
                try:
                    # read one line at a time, get its url and schedule thread
                    # by submitting it to thread-pool
                    img_url = line.strip()
                    fobj = self.t_exec.submit(self.store_image, img_url)
                    futures_objs[fobj] = img_url
                except Exception as e:
                    total_errors.append({
                        "url": img_url,
                        "error": e.message
                    })
                    fail_count += 1

        # whilst the threadpool executes each requested and scheduled thread
        # this part would fetch the outputs/exception of each and combines
        # them to create the summary
        for fobj, url in futures_objs.items():
            if fobj.exception() is not None:
                fail_count += 1

                total_errors.append({
                    "url": url,
                    "error": fobj.exception().message
                })
            else:
                succ_count += 1

        util.print_line("Report Summary")
        # this is just a short of summary of download success/failure
        print({"success": succ_count, "failure": fail_count})

        util.print_line("Logging errors to error-file")

        # Write errors to error-file
        # JSON data is dumped to error-file, so that- it can be consumed
        # to propagate behavior as information.
        err_file = open(ERROR_FILE, mode="w")
        try:
            json.dump(total_errors, err_file, indent=4)
        except Exception as e:
            print("Unable to write error to {} file, "
                  "Reason:\n{}".format(ERROR_FILE, e.message))
            err_file.close()
            err_file = open(ERROR_FILE, mode="w")
            json.dump([], err_file)
        err_file.close()

    def lookup_file(self, img_name):
        # this method gets the image-name as input, deduces where it should
        # be present and checks for its presence
        file_path = self.deduce_storageparams(img_name)
        if os.path.exists(file_path):
            print("lookup: file '{}' Found!".format(file_path))
        else:
            print("lookup: file '{}' Not found!".format(file_path))


if __name__ == "__main__":
    # read the conf file, if present
    config = util.read_conf_file()

    # check the input arguments, if necessary read from it.
    if len(sys.argv) < 2:
        if config is None:
            raise Exception("Please pass input image file (absolute-path)")

    print("Please wait....")

    # as logger isn't used here considering the motive of the task
    # is small, used the hacky way to generate log-output
    log = open("output.log", "w")
    sys.stdout = log

    # use the config file to read off essential attributes from it.
    # currently support is only imagefie.
    # loglevel is added as an example of how this can be tuned
    if config.get("level"):
        LOG_LEVEL = config["level"]

    file_path = config["imagefile"] if config.get("imagefile") else sys.argv[1]

    # create the ImageManager object and call methods, as to demonstrate
    # downloading & storing images AND
    # searching image files
    img_mgr = ImageManager(file_path)
    util.print_line("Downloading & Storing Images")
    img_mgr.download_from_imgfile()

    util.print_line("Look up checks")

    search_imgs = [
        "barbara.png",
        "airplane.png",
        "boat.png",
        "boat2.png"
    ]
    for img in search_imgs:
        img_mgr.lookup_file(img)
