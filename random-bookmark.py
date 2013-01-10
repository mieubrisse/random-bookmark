#!/usr/bin/python

import json
import os.path
import webbrowser
from random import randint 

"""
Given a hierarchy of items from the bookmark bar and a set of folder names to search for, create a set
of all URL items under the desired folders
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
Given a pointer to a dict representing a bookmark folder, recursively add all bookmarks under 
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




TARGET_FOLDERS_FILEPATH = "~/.random-bookmark-folders.json"
BOOKMARKS_FILEPATH = "~/.config/google-chrome/Default/Bookmarks"

# Grab bookmarks from Chrome file
BOOKMARKS_FILEPATH = os.path.expanduser(BOOKMARKS_FILEPATH)
bookmarks_fp = open(BOOKMARKS_FILEPATH)
bookmarks = json.load(bookmarks_fp)
bookmarks_bar = bookmarks["roots"]["bookmark_bar"]
bookmarks_fp.close()

# Get names of folders to pull from
TARGET_FOLDERS_FILEPATH = os.path.expanduser(TARGET_FOLDERS_FILEPATH)
target_folders_fp = open(TARGET_FOLDERS_FILEPATH)
target_folders = json.load(target_folders_fp)
target_folders_fp.close()

# Generate set of URLs to select from randomly
if "children" in bookmarks_bar:
    target_urls = set()
    get_target_urls(bookmarks_bar["children"], target_folders, target_urls)

    if len(target_urls) == 0:
        print ("No bookmarks to choose from")
    else:
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
else:
    print("Could not get random page; bookmark bar is empty")
