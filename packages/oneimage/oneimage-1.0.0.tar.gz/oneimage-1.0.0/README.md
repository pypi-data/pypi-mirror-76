# oneimage
A simple python lib to create poster image with define data.

Install oneimage
===============
```
 pip install oneimage
```

Usage
===============
```python
data = {
    'width': 300,
    'height': 300,
    'background': 'white',
    'elements': [
        {'type': 'image', 'url': 'http://www.inruan.com/static/img/logo.png', 'left': 0, 'top': 0, 'width': 100, 'height': 100},
        {'type': 'image', 'url': 'http://www.inruan.com/static/img/logo.png', 'left': 200, 'top': 200, 'width': 100, 'height': 100},
        {'type': 'text', 'text': 'Hello', 'font': 'https://cdn-qn.huaeb.com/ifarm/20200305/WeiRuanYaHei-1.ttf', 'left': 0, 'top': 100, 'width': 300, 'size': 20, 'height': 100, 'align': 'center', 'vertical': 'center', 'color': 'black'}
    ]
}
from oneimage import create_image
img = create_image(data=data)
img.show()
```
