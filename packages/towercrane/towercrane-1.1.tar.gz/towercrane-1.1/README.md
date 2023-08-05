# TowerCrane

towercrane is an easy to use commandline tool for keeping your large project files on the cloud.
It simply searches for specific file extensions in your project and let your simply upload and downlaod them between your local and cloud.
It's designed to work with AWS S3, Google Cloud Storage and other storage services in the future.
towercrane is desined for Linux and macOS. Support for windows is in the backlog.

I used to run out of space on my laptop all time. very often it was because of large datasets or other formats of project files, which I didn't want to remove from my local. I wrote towecrane and decided to make it open source for other people to contribute to.

Cheers

## Quick start


you can install towercrane on using pip.
when running config there is a choice for using either AWS S3 or Google Cloud Storage. and you need have their cli tool authnticated. look for the links at the bottom.

```bash

pip3 install towercrane

towercrane config 
  
 ```


## Basic Usage

### towercrane commands

```bash

Start by moving to the root of your project

cd my_project

towercrane scan 
towercrane status

towercrane init 
towercrane upload 
towercrane remove 
towercrane download
  
```

## Status lifecycle of a towercrane project 

local
cloud
local_and_cloud

upload
uploaded

remove
removed

download



