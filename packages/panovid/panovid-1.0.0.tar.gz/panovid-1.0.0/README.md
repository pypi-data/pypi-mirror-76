# Panovid
Turn panoramic photos into scrolling videos! This project can be used as a standalone script, or can be used in another python project.

# Standalone
To setup use as a standalone application, run the following commands:

```bash
git clone https://github.com/kylelrichards11/panovid.git
cd panovid
pip install --user -r requirements.txt
```

To use, simpy call `python panovid.py <filename> [options]`, where filename is the file name of the panorama photo. The options are specified below and can also be seen by running `python panovid.py --help`.

Note that the python version must be Python 3.6 or greater.

## Options
| Option | Description |
| -- | -- |
| --fps | Frames per second of video (default=60) |
| --framejump | Pixels to move between frames (default=4) |
| --landscape | Save a video in landscape mode |
| --portrait | Save a video in portrait mode (default) |

# In python project
```bash
pip install panovid
```

```python
from panovid import convert_to_vid
convert_to_vid("my_photo.jpg")
```

The optional arguments are the same as for the standalone version (without dashes).

```