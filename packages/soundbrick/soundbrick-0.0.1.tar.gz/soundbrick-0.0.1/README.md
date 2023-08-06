# Soundbrick

**Soundbrick** is simple sound files viwer.

## Usage
### Example.1
```python
from soundbrick import Soundbrick
sb = Soundbrick()
sb.add(['/your/sound/directory/sound_0100.wav',
        '/your/sound/directory/sound_0101.wav',
        '/your/sound/directory/sound_0102.wav',
        '/your/sound/directory/sound_0103.wav',
        '/your/sound/directory/sound_0104.wav',
        '/your/sound/directory/sound_0105.wav',
        '/your/sound/directory/sound_0106.wav',
        '/your/sound/directory/sound_0107.wav',
        '/your/sound/directory/sound_0108.wav',
        '/your/sound/directory/sound_0109.wav',])
sb.show('./tile1.jpg')
sb.close()
```
![demo1](https://raw.githubusercontent.com/cygkichi/wavetile/master/examples/img/tile1.jpg)

### Example.2
```python
import glob
from soundbrick import Soundbrick

sb = Soundbrick(background_color="#b55233",
                line_color="#982222",
                helical_edge_color="#ffffff",
                vartical_edge_color="#ffffff",
                xsize_per_second=1.0,
                aspect=0.5)
file_list = sorted(glob.glob('/your/sound/directory/suond_*.wav'))
sb.add(file_list)
sb.show('./tile2.jpg')
sb.close()
```
![demo2](https://raw.githubusercontent.com/cygkichi/wavetile/master/examples/img/tile2.jpg)


## Args

```python
Soundbrick(
    is_showlabel = True,     #
    label_size = 15,         #
    label_color = "#ff5470", #
    label_alpha = 1.0,       #
    helical_edge_color = "#232323",  #
    vartical_edge_color = "#ff5470", #
    background_color = "#f5f5dc",    #
    line_color = "#078080",          #
    yrange = [-1,1],                 #
    dpi = 100,
    xsize_per_second = 1.0,
    ysize            = 1.0,
    aspect           = 1.0,
)

Soundbrick().add(
    file_list # list of input-sound-filepath
    )

Soundbrick().show(
    file # output-image-filepath
)

```

## Installation

```bash
pip install soundbrick # xxxxx
```


## Developer Memo

```bash
python3 -m venv ./venv
source ./venv/bin/activate

# Install modules
pip install --upgrade pip
pip install numpy
pip install matplotlib
pip install soundfile
pip install opencv-python
pip install wheel
pip install twine

# test
xxx

# update to pypi
python3 setup.py sdist bdist_wheel
python3 -m twine upload --repository testpypi dist/*
```
