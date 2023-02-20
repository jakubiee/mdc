# MDC - Most Dominant Colors 🎨
MDC allows you to create a palette of the most dominant colors in an image or video using the kmeans clustering.
## Installation
```
$ pip install mdcolors
```
## Usage
### Image
![](fish.png)
```
$ mdc image <image> [OPTIONS]
```
-	Arguments 
	-	`<image>` - The path of the image you want to convert.
- Options
	- `-c` - Number of colors in the palette.
	- `-hex` - Shows the hex color code of each color on the palette
	- `-t` - Set a palette title.


### Video
![](MandelbrotSet.png)
```
$ mdc video <video> [OPTIONS]
```
-	Arguments 
	-	`<video>` - The path of the video you want to convert.
- Options
	- `-s` - Convert video from this time. (hh:mm:ss)
	- `-e` - Convert video up to this time. (hh:mm:ss)
	- `-t` - Set a palette title.

## License
This project is distributed under the [MIT](LICENSE) license.