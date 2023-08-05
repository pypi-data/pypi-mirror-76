import os
import sys
import urllib.request
from tqdm import tqdm
import zipfile
import json
import logging

logger = logging.getLogger("azureml_ngc.ngc_content")


def downloadurltofile(url, filename, orig_filename):
    if not os.path.exists(filename):
        logger.info(f"    --> [DOWNLOAD] Downloading {orig_filename} to {filename}<--")
        with open(filename, "wb") as file:
            with urllib.request.urlopen(url) as resp:
                length = int(resp.getheader("content-length"))
                blocksize = max(4096, length // 100)
                with tqdm(total=length, file=sys.stdout) as pbar:
                    while True:
                        buff = resp.read(blocksize)
                        if not buff:
                            break
                        file.write(buff)
                        pbar.update(len(buff))
        logger.info(f"    -->> [DOWNLOAD] File {orig_filename} downloaded... <<--")
    else:
        logger.info(
            f"    -->> [DOWNLOAD] {orig_filename} file already exists locally <<--"
        )


def download(url, targetfolder, targetfile):
    path = os.getcwd()
    data_dir = os.path.abspath(os.path.join(path, targetfolder))

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    targetfile_fullpath = os.path.join(data_dir, targetfile)
    downloadurltofile(url, targetfile_fullpath, targetfile)
    return data_dir, targetfile


def unzipFile(filename, srcfolder, destfolder):
    path = os.getcwd()
    data_dir = os.path.abspath(os.path.join(path, srcfolder))
    filepath = os.path.abspath(os.path.join(data_dir, filename))
    destfolder = os.path.join(data_dir, destfolder)

    if not os.path.exists(destfolder):
        logger.info(f"    -->> [EXTRACT] Extracting {filename} to {destfolder}... <<--")
        with zipfile.ZipFile(filepath, "r") as zip_ref:
            zip_ref.extractall(destfolder)
    else:
        logger.info(
            f"    -->> [EXTRACT] {filename} already extracted to {destfolder}... <<--"
        )


def upload_data(workspace, datastore, src_dir, tgt_path, overwrite=False):
    print(src_dir, tgt_path)
    datastore.upload(
        src_dir=src_dir, target_path=tgt_path, show_progress=True, overwrite=overwrite
    )
    logger.info(
        f"    -->> [UPLOAD] Completed uploading folder {src_dir} to {tgt_path} in {datastore.name}... <<--"
    )


def get_config(configfile):
    jsonfile = open(configfile)
    configdata = json.load(jsonfile)
    return configdata
