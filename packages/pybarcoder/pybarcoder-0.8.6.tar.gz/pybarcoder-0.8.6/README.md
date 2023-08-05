## BarCodeBuilder

### Introduction
this is a bar tool which base on python-barcode and barcode.

### Usage

##### 1. install
```bash
pip install pybarcoder
```

##### 2. usage
```python
BarCoder().set_options({
    'module_width': 0.2,  # 默认值0.2，每个条码宽度，单位为毫米
    'module_height': 8.0,  # 默认值15.0，条码高度，单位为毫米
    'quiet_zone': 3,  # 默认值6.5，两端空白宽度，单位为毫米
    'font_size': 12,  # 默认值10，文本字体大小，单位为磅
    'format': 'PNG',  # 默认值'PNG'，保存文件格式，默认为PNG，也可以设为JPEG、BMP等，只在使用ImageWriter时有效。
    'dpi': 300,  # 默认值300，图片分辨率，，只在使用ImageWriter时有效。
}).set_msg("S123456789", "左上角信息", "左下角信息", "右上角信息", "右下角信息").base64()
print("生成成功")
```
