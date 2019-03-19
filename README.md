# GTA_SA_Map_Writer
A python tool for adding your dots and lines on the GTA San Andreas map.
### Examples:
![Example with HD-map](https://i.imgur.com/aqutH51.png)
![Example with SD-map](https://i.imgur.com/AG1doD5.png)

### Usage:
At first you need to add your dots and lines coordinates to their files `dots.csv` and `lines.csv`. **Use game coordinates, not image coords.**
After it you can run `main.py` with python3 by type `python3 main.py` or `python main.py`.
As result yoy will get four files:
* `Edited_HD.png` - Full size satelite map with dots and lines.
* `Edited_SD.png` - Full size standart game map with dots and lines.
* `Thumb_Edited_HD.png` - 250x250px sized copy of `Edited_HD.png`.
* `Thumb_Edited_SD.png` - 250x250px sized copy of `Edited_SD.png`.

#### Depechements:
This script are using:
* *pandas* for parse *.csv* files.
* *PIL* (pillow fork) for editing images.