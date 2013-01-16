Overview
---
I often use Chrome's bookmarking feature to store sites that I find interesting or enlightening, but I usually forget to dig through the folder I store the bookmarks in to look at them again.
To encourage myself to go back and visit these sites, I wrote this simple script that takes a set of names of Chrome bookmark folders and randomly chooses one of the bookmarks contained inside to open.
I've set the script to run on my startup, so now every time I log in Chrome loads up one of my favorite sites.

Installation
---
You will need to define a JSON file listing the names of the Chrome bookmark folders you want to choose a bookmark from.
Example:
```json
[
    "FooFolder",
    "BarFolder",
    "ZapFolder"
]
```
<i>Note that <b>folder names are capitalization-sensitive</b>!</i>
The script will attempt to guess the path to your Chrome bookmark file, but you may need to manually specify it in the below section


Troubleshooting
---
If the script is behaving in unexpected ways, ensure that 
