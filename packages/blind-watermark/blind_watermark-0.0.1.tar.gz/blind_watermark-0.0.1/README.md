# blind-watermark
基于傅里叶变换的数字盲水印  

## 如何使用

嵌入水印
```python
from blind_watermark import WaterMark

bwm1 = WaterMark(password_wm=1, password_img=1)

# 读取原图
bwm1.read_ori_img('pic/原图.jpg')

# 读取水印
bwm1.read_wm('pic/水印.png')

# 打上盲水印
bwm1.embed('output/打上水印的图.png')
```


提取水印
```python
from blind_watermark import WaterMark

bwm1 = WaterMark(4399, 2333, 36, 20, wm_shape=(128, 128))
# 注意需要设定水印的长宽wm_shape
bwm1.extract('output/打上水印的图.png', 'output/解出的水印.png')
```

## 效果展示

|原图|水印|
|--|--|
|<img src="https://img1.github.io/blind_watermark/原图.jpg" width = "400" >|![水印](https://img1.github.io/blind_watermark/水印.png)|

|嵌入后的图|提取的水印|
|--|--|
|<img src="https://img1.github.io/blind_watermark/打上水印的图.png" width = "400" >|![提取的水印](https://img1.github.io/blind_watermark/%E8%A7%A3%E5%87%BA%E7%9A%84%E6%B0%B4%E5%8D%B0.png)|


### 各种攻击后的效果

|攻击方式|攻击后的图片|提取的水印|
|--|--|--|
|多遮挡<br>[多遮挡攻击.py](examples/多遮挡攻击.py)| <img src="https://github.com/img1/img1.github.io/blob/master/blind_watermark/%E5%A4%9A%E9%81%AE%E6%8C%A1%E6%94%BB%E5%87%BB.png?raw=true" width = "400" > |![多遮挡_提取水印](https://img1.github.io/blind_watermark/%E5%A4%9A%E9%81%AE%E6%8C%A1%E6%94%BB%E5%87%BB_%E6%8F%90%E5%8F%96%E6%B0%B4%E5%8D%B0.png?raw=true)|
|横向裁剪50%<br>[横向裁剪攻击.py](examples/横向裁剪攻击.py)|<img src="https://github.com/img1/img1.github.io/blob/master/blind_watermark/%E6%A8%AA%E5%90%91%E8%A3%81%E5%89%AA%E6%94%BB%E5%87%BB.png?raw=true" width = "200" >|![](https://img1.github.io/blind_watermark/%E6%A8%AA%E5%90%91%E8%A3%81%E5%89%AA%E6%94%BB%E5%87%BB_%E6%8F%90%E5%8F%96%E6%B0%B4%E5%8D%B0.png?raw=true)|
|纵向裁剪10%<br>[纵向裁剪攻击.py](examples/纵向裁剪攻击.py)|<img src="https://img1.github.io/blind_watermark/%E7%BA%B5%E5%90%91%E8%A3%81%E5%89%AA%E6%89%93%E5%87%BB_%E5%A1%AB%E8%A1%A5.png?raw=true" width = "400" >|![纵向裁剪](https://img1.github.io/blind_watermark/%E7%BA%B5%E5%90%91%E8%A3%81%E5%89%AA%E6%89%93%E5%87%BB_%E6%8F%90%E5%8F%96%E6%B0%B4%E5%8D%B0.png?raw=true)|
|缩放攻击（1200X1920->600X800）<br>[缩放攻击.py](examples/缩放攻击.py)|<img src="https://img1.github.io/blind_watermark/%E7%BC%A9%E6%94%BE%E6%94%BB%E5%87%BB.png?raw=true" width = "300" >![]()|![](https://img1.github.io/blind_watermark/%E7%BC%A9%E6%94%BE%E6%94%BB%E5%87%BB_%E6%8F%90%E5%8F%96%E6%B0%B4%E5%8D%B0.png?raw=true)|
|椒盐攻击<br>[椒盐击.py](examples/椒盐.py)|<img src="https://img1.github.io/blind_watermark/%E6%A4%92%E7%9B%90%E6%94%BB%E5%87%BB.png?raw=true" width = "400" >|![](https://img1.github.io/blind_watermark/%E6%A4%92%E7%9B%90%E6%94%BB%E5%87%BB_%E6%8F%90%E5%8F%96%E6%B0%B4%E5%8D%B0.png?raw=true)|
|亮度提高10%<br>[亮度调高攻击.py](examples/亮度调高攻击.py)|<img src="https://img1.github.io/blind_watermark/%E4%BA%AE%E5%BA%A6%E8%B0%83%E9%AB%98%E6%94%BB%E5%87%BB.png?raw=true" width = "400" >|![](https://img1.github.io/blind_watermark/%E4%BA%AE%E5%BA%A6%E8%B0%83%E9%AB%98%E6%94%BB%E5%87%BB_%E6%8F%90%E5%8F%96%E6%B0%B4%E5%8D%B0.png?raw=true)|
|亮度调低10%<br>[亮度调暗攻击.py](examples/亮度调暗攻击.py)|<img src="https://img1.github.io/blind_watermark/%E4%BA%AE%E5%BA%A6%E8%B0%83%E4%BD%8E%E6%94%BB%E5%87%BB.png?raw=true" width = "400" >|![](https://img1.github.io/blind_watermark/%E4%BA%AE%E5%BA%A6%E8%B0%83%E4%BD%8E%E6%94%BB%E5%87%BB_%E6%8F%90%E5%8F%96%E6%B0%B4%E5%8D%B0.png?raw=true)|
|旋转攻击45度<br>[旋转攻击.py](examples/旋转攻击.py)|<img src="https://github.com/img1/img1.github.io/blob/master/blind_watermark/%E6%97%8B%E8%BD%AC%E6%94%BB%E5%87%BB.png?raw=true" width = "400" >|![](https://github.com/img1/img1.github.io/blob/master/blind_watermark/%E6%97%8B%E8%BD%AC%E6%94%BB%E5%87%BB_%E6%8F%90%E5%8F%96%E6%B0%B4%E5%8D%B0.png?raw=true)|


### 隐水印还可以是二进制数据

作为 demo， 如果要嵌入是如下长度为6的二进制数据
```python
wm = [True, False, True, True, True, False]
```

嵌入水印

```python
# 除了嵌入图片，也可以嵌入比特类数据
from blind_watermark import WaterMark

bwm1 = WaterMark(password_img=1, password_wm=1)
bwm1.read_ori_img('pic/原图.jpg')
bwm1.read_wm([True, False, True, True, True, False], mode='bit')
bwm1.embed('output/打上水印的图.png')
```

解水印：（注意设定水印形状 `wm_shape`）
```python
bwm1 = WaterMark(password_img=1, password_wm=1, wm_shape=6)
wm_extract = bwm1.extract('output/打上水印的图.png', mode='bit')
print(wm_extract)
```

解出的水印是一个0～1之间的实数，方便用户自行卡阈值。如果水印信息量远小于图片可容纳量，偏差极小。

-------------

几种隐写术比较：

|方法|示例|埋入信息量|是否有损|鲁棒性|隐蔽性|
|--|--|--|--|--|--|
|隐写在频域上||少|有损|很强，抗各种攻击。|很强
|隐写在空域上||中|无损|弱|强|
|图种|`copy /b xx.jpg+xx.rar xx.jpg`|理论上无上限|无损|弱|几乎无，像素和文件大小不匹配、扫描内容都可以发现|
