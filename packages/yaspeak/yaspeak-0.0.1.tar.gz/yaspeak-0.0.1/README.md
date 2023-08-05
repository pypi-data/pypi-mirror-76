<div align="center">
	<h1>YaSpeak</h1>

Python wrapper for Yandex text voiceover

![pypi](https://badge.fury.io/py/YaSpeak.svg)

</div>

## Install
`pip install --upgrade yaspeak`

## Usage
```python
from yaspeak import YaSpeak

ysp = YaSpeak()

ysp.oksana("hello")
ysp.levitan("hello", "out1.mp3")
ysp.yandex("hello", "out2.mp3")
```