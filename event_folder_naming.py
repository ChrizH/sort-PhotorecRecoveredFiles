import os
from datetime import datetime
from os.path import isfile, isdir
import glob
from time import localtime, strptime, mktime
from pathlib import Path
from jpgSorter import getMinimumCreationTime
import heapq
import exifread
import pandas as pd
import matplotlib.pyplot as plt

from recovery import log


def find_files(path):
    """Recursively yield DirEntry objects for given directory."""
    for entry in os.scandir(path):
        if entry.is_dir(follow_symlinks=False):
            yield from find_files(entry.path)
        else:
            yield entry


def grep_img_size(img_path_gen):
    for entry in img_path_gen:
        img_path = entry.path
        if not isfile(img_path) or not img_path.lower().endswith("jpg") \
                or "date-unknown" in img_path:
            continue
        
        size = os.path.getsize(img_path) / 1024. / 1024.
        yield size


def compute_stats(path):
    """
    plot distribution of recovered image file sizes
    :param path:
    :return:
    """
    file_paths = find_files(path)
    sizes_gen = grep_img_size(file_paths)
    sizes = list(sizes_gen)
    df = pd.DataFrame(sizes)
    plt.figure()
    df.plot.hist(bins=30, width=0.5)
    plt.xticks(range(0, 22, 1))
    plt.title("Distribution of ({}) picture sizes".format(len(sizes)))
    plt.xlabel("Size [Mb]")
    plt.ylabel("Amount")
    plt.savefig("Distribution.png")
    plt.close()


def get_event_dir_name(root_path):
    """
    search for earliest and latest captured picture within that event folder.
    - stores all picture capture times within a heap for easy access of first & last image taken.
    
    folder name is created like *earliest-timestamp__to__latest-timestamp*.
        2019-03-02__to__03-04
    :return: time range as string, YYYY-MM-DD__to__MM-DD
    """
    heap = []
    for img_path in glob.glob(root_path + "/*/*.jpg", recursive=True) + glob.glob(root_path + "/*.jpg", recursive=True):
        
        image = open(os.path.join(root_path, img_path), 'rb')
        creationTime = None
        try:
            exifTags = exifread.process_file(image, details=False)
            creationTime = getMinimumCreationTime(exifTags)
        except:
            log("invalid exif tags for " + fileName)
        
        # distinct different time types
        if creationTime is None:
            creationTime = localtime(os.path.getctime(img_path))
        else:
            try:
                creationTime = strptime(str(creationTime), "%Y:%m:%d %H:%M:%S")
            except:
                creationTime = localtime(os.path.getctime(img_path))
        
        # push time_stamp
        heapq.heappush(heap, mktime(creationTime))
    
    # retrieve first and last timestamp within the folder
    min_date = datetime.fromtimestamp(int(heapq.nsmallest(1, heap)[0]))
    max_date = datetime.fromtimestamp(int(heapq.nlargest(1, heap)[0]))
    
    # event spans across multiple days
    if min_date.day != max_date.day:
        return "{}__to__{}".format(min_date.strftime("%Y-%m-%d"),
                                   max_date.strftime("%m-%d"))
    
    # group of images within one day
    return min_date.strftime("%Y-%m-%d")


def rename_dir(path, new_name):
    new_dir = os.path.join(Path(path).parent, new_name)
    os.rename(path, new_dir)


def process_renaming(path):
    sub_folders = sub_folder_lookup(root_path=path)
    for sub_dir in sub_folders:
        log(sub_dir)
        new_dir_name = get_event_dir_name(sub_dir)
        log("rename event to {}\n".format(new_dir_name))
        rename_dir(sub_dir, new_dir_name)


def sub_folder_lookup(root_path):
    all_dirs = list(os.walk(root_path))
    for dirs in all_dirs:
        dir = dirs[0]
        if isdir(dir) and not "date-unknown" in dir:
            # check if contains already files
            subfile = "{}/{}".format(dir, os.listdir(dir)[0])
            if isfile(subfile):
                log("reached subdir {}".format(dir))
                yield dir


if __name__ == "__main__":
    import sys
    
    compute_stats(sys.argv[1])
