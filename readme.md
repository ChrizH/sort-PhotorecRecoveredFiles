# Sort files recoverd by Photorec

Photorec does a great job when recovering deleted files. But the result is a huge, unsorted, unnamed amount of files. Especially for external hard drives serving as backup of all the personal data, sorting them is an endless job.

This program sPRF helps you sorting your files. First of all, the **files are copied to own folders for each file type**. Second, **jpgs are distinguished by the year, and optionally by month as well** when they have been taken **and by the event**. We thereby define an event as a time span during them photos are taken. It has a delta of 4 days without a photo to another event. If no date from the past can be detected, these jpgs are put into one folder to be sorted manually.


## Installation

First install the package [exifread](https://pypi.python.org/pypi/ExifRead):

```pip install exifread```

## Run the sorter

Then run the sorter:

```python recovery.py <path to files recovered by Photorec> <destination>```

This copies the recovered file to their file type folder in the destination directory. The recovered files are not modified. If a file already exists in the destination directory, it is skipped. Hence you can interrupt the process with Ctrl+C and continue afterwards.

The first output of the programm is the number of files to copy. To count them might take some minutes depending on the amount of recovered files. Afterwareds you get some feedback on the processed files.

### Parameters

For an overview of all arguments, run with the `-h` option: ```python recovery.py -h```.

#### Max numbers of files per folder

All directories contain maximum 500 files. If one contains more, numbered subdirectories are created. If you want another file-limit, e.g. 1000, just put that number as third parameter to the execution of the programm:

```python recovery.py <path to files recovered by Photorec> <destination> -n1000```

#### Folder for each month

sPRF usually sorts your photos by year:

```
destination
|- 2015
    |- 1.jpg
    |- 2.jpg
    |- ...
|- 2016
    |- ...
```

Sometimes you might want to sort each year by month:

```python recovery.py <path to files recovered by Photorec> <destination> -m```

Now you get:

```
destination
|- 2015
    |- 1    # January
      |- 1.jpg
      |- 2.jpg
    |- 2    # February
      |- 3.jpg
      |- 4.jpg
    |- ...
|- 2016
    |- ...
```

#### Event based image grouping
Images that have been taken within close proximity to each other should be stored together. 

Let's say you have only images from two weekend trips within a month, then it makes sense to group those images accordingly.  

```
destination
|- 2015
    |- 1    # January
        |-2015-01-10__to__01_13
        |-2015-01-23__to__01_24

````

##### Adjust event distance

For the case you want to reduce or increase the timespan between events, simply use the parameter -d. The default is 4:
```python recovery.py <path to files recovered by Photorec> <destination> -d10```


#### Keep original filenames

Use the -k parameter to keep the original filenames:

```python recovery.py <path to files recovered by Photorec> <destination> -k```
