# Flyr
Flyr is a library for extracting thermal data from FLIR images written fully in Python, without depending on ExifTool.

Other solutions are wrappers around ExifTool to actually do the hard part of extracting the thermal data. Flyr is a reimplementation of the ExifTool's FLIR parser. Practically, this offers the following benefits:

* Faster decoding because no new process needs to be started and in-memory data does not need to be communicated to this other process
* More accurate, because Flyr uses all of the metadata to translate the raw values into Kelvin, while other projects have a certain set hardcoded. The differences are often about 0.1°C, but can be as high as 0.6°C. Furthermore ExifTool rounds some of the values, while Flyr uses unrounded values from the metadata. The only starts mattering around the 6th decimal, so whether it matters is up for debate.
* Easier and robust installation and deployment, because `flyr.py` is not an external executable
* Arguably simpler use: no need to create a superfluous extraction object; simply call `thermal = flyr.unpack(flir_file_path)` and done

## Installation

Flyr is installable from [PyPi](https://pypi.org/project/flyr/): `pip install flyr`.

Alternatively, download flyr.py and include in your source tree.

Flyr depends on three external packages, all installable through pip: `pip install numpy nptyping pillow`. Pillow does the conversion from embedded images to numpy arrays, nptyping allows for high quality array type annotations. Numpy provides the n-dimensional arrays necessary to contain the thermal and optical data.

## Usage
Call `flyr.unpack` on a filepath to receive a numpy array with the thermal data. Alternatively, first open the file in binary mode for reading and and pass the the file handle to `flyr.unpack`.

```python
import flyr

# Thermograms can be read directly from a file, or from a bytes stream, using
# the `unpack()` function.
flir_path = "/path/to/FLIR9121.jpg"
thermogram = flyr.unpack(flir_path)  # Reading directly

with open(flir_path, "rb") as flir_handle:  # In binary mode!
	thermogram = flyr.unpack(flir_handle)  # Reading from file handle

# Temperatures available in Kelvin and in Celsius
thermal = thermogram.celsius
thermal = thermogram.kelvin

# Optical image availabe too
optical = thermogram.optical

# Thermogram can also be rendered using different strategies. The `render`
# function has default value that can be overridden to configure it.
render = thermogram.render(min_v=5.0, max_v=20.0, mode="minmax", palette="grayscale")
render = thermogram.render(min_v=0.4, max_v=0.99, mode="percentiles", palette="jet")

# There is also a convenience function that returns a Pillow `Image` object,
# taking the same arguments as `render()`.
render = thermogram.render_pil()
```

## Status
Currently this library has been tested to work with:

* FLIR E4
* FLIR E5
* FLIR E6
* FLIR E8
* FLIR E8XT
* FLIR E53
* FLIR P60 (PAL)
* FLIR E75
* FLIR T630SC
* FLIR T660

However, the library is still in an early phase and lacks robust handling of inconsistent files. When it encounters such an image it immediately gives up raising a ValueError, while it could also do a best effort attempt to extract anyway. This is planned.

Camera's that sometimes do and don't work:

* FLIR ThermaCAM P640
* FLIR ThermaCAM P660 West (more often doesn't than does)

Camera's found not to work (yet):

* FLIR E60BX
* FLIR ThermoCAM B400
* FLIR ThermaCAM SC640
* FLIR ThermaCam SC660 WES
* FLIR ThermaCAM T-400
* FLIR S60 NTSC
* FLIR SC620 Western
* FLIR T400 (Western)
* FLIR T640
* FLIR P660

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. Most help is currently needed supporting more models and testing against more pictures. Testing and developing for your own camera's images or FLIR Tools' samples is recommended.

## Acknowledgements
This code would not be possible without [ExifTool](https://exiftool.org/)'s efforts to [document](https://exiftool.org/TagNames/FLIR.html) the FLIR format.
[Previous work](https://github.com/Nervengift/read_thermal.py) in Python must
also be acknowledged for creating a workable solution.

## License
Flyr is licensed under The European Union Public License 1.2. The English version is included in the license file. Translations for all EU languages, each fully legally valid, can be found at the [EUPL](https://eupl.eu/) website.
