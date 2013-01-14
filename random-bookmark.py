#!/usr/bin/python

import json
import os.path
import os.environ
import webbrowser
from sys import exit
from random import randint 

# Filepath to JSON file containing names of bookmark folders to use
TARGET_FOLDERS_FILEPATH = "~/.random-bookmark-folders.json"

# Filepath to JSON file Chrome stores Bookmarks in
BOOKMARKS_FILEPATH = ""

# Try to guess filepath to Chrome bookmarks if none specified
if BOOKMARKS_FILEPATH == "" or BOOKMARKS_FILEPATH == None:
    system = platform.system()
    if system == "Linux":
        bookmark_filepath_guess = "~/.config/google-chrome/Default/Bookmarks"
    elif system == "Windows":
        windows_username = os.environ.get("USERNAME")
        bookmark_filepath_guess = "C:\Documents and Settings\" + windows_username + "User Name\Local Settings\Application Data\Chromium\User Data\Default"
    else:
        print("Unable to determine Chrome bookmarks filepath; please specify manually")
        exit()





"""
Given a list of items from the bookmark bar and a set of folder names to search for, add all URL
items under the target folders to the given set
 - items: list of items from bookmark bar
 - target_folders: set of names of folders to pull URLs from
 - target_urls: set to add folder URLs to
"""
def get_target_urls(items, target_folders, target_urls):
    for item in items:
        if "type" not in item or "name" not in item:
            raise KeyError("Item missing 'type' or 'name' field: " + str(item))
        if item["type"] == "folder":
            # If folder is one of the target folders, add the URLs under it to the target URL set
            if item["name"] in target_folders:
                get_folder_urls(item, target_urls)
            # If it isn't, search its children for target folders
            elif "children" in item:
                get_target_urls(item["children"], target_folders, target_urls)

"""
Given a pointer to a dict representing a bookmark folder, recursively add all URL items under 
the folder to the set of URLs being considered for random selection
- folder : dict representing a bookmark folder
- target_urls : set of URLs which bookmark will be chosen from
"""
def get_folder_urls(folder, target_urls):
    if "children" in folder:
        for item in folder["children"]:
            if item["type"] == "url":
                target_urls.add(item["url"])
            elif item["type"] == "folder":
                get_folder_urls(item, target_urls)

# Parse Chrome Bookmarks file into object
BOOKMARKS_FILEPATH = os.path.expanduser(BOOKMARKS_FILEPATH)
bookmarks_fp = open(BOOKMARKS_FILEPATH)
bookmarks = json.load(bookmarks_fp)
bookmarks_bar = bookmarks["roots"]["bookmark_bar"]
bookmarks_fp.close()

# Parse 'target folders' file into object
TARGET_FOLDERS_FILEPATH = os.path.expanduser(TARGET_FOLDERS_FILEPATH)
target_folders_fp = open(TARGET_FOLDERS_FILEPATH)
target_folders = json.load(target_folders_fp)
target_folders_fp.close()

# Do nothing if no bookmarks found
if "children" not in bookmarks_bar:
    exit()

# Generate set of URLs to select from randomly
target_urls = set()
get_target_urls(bookmarks_bar["children"], target_folders, target_urls)
if len(target_urls) == 0:
    print ("No bookmarks selected")
    exit()

# Choose a random element from the target URL set and open in Chrome
random_bookmark_index = randint(1, len(target_urls))
counter = 1
for url in target_urls:
    if counter == random_bookmark_index:
        selected_url = url
        break
    counter += 1
if selected_url == None:
    raise ValueError("Unable to select random bookmark")
webbrowser.open(selected_url)
