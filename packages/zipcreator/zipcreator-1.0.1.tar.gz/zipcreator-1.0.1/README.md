# zipcreator

A quick tool for creating a zipfile from a list of files and/or directories. 

## Getting Started

### Documentation
Find full documentation of the project here:
https://zipcreator.readthedocs.io

### Installing

```
python setup.py install
```

or

```
pip install zipcreator
```

### Example

```python
from zipcreator import list_zip

files = ['test.txt', 'testdir/']
dest = 'result.zip'

list_zip.create(files, dest)
```

## Versioning

- v1.0.0 - Initial Release - 04/20/2020
- v1.0.1 - Added ability to pass in directory name only - 08/15/2020

## Authors

* **Matt Palazzolo** - [GitHub Profile](https://github.com/mpalazzolo)

## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details


