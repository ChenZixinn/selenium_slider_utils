### selenium通过滑块验证码工具



![image-20231012161749558](./example.png)

#### 一、说明

使用selenium能比较方便的解决滑块验证码，如果不考虑性能的话，这是比较高效的方式。

使用该工具可以方便地进行滑块拖动，成功较高。



#### 二、使用示例

1. ##### 需要判断距离的情况

注意：计算出来的距离与实际要拖动的距离可能有偏差，因为滑块并不一定在图片的最左侧，请调试后进入源码修改

```python
from slider_util import get_img_and_move

# 浏览器对象
driver = webdriver.Chrome(options=chrome_options)
driver.get('xxx.xxxxx.com')

# 获取图片url
img_bg_src = driver.find_element(by=By.XPATH, value='//img[@alt="验证码背景"]').get_attribute('src')
img_slider_src = driver.find_element(by=By.XPATH, value='//img[@alt="验证码滑块"]').get_attribute('src')
# 获取滑块元素
slider = driver.find_element(by=By.XPATH, value='//div[contains(@class,"yidun_slider--hover")]')

# 调用工具(参数：背景图片链接、滑块图片链接、selenium对象、滑块元素)
get_img_and_move(img_bg_src, img_slider_src, driver, slider)
```



2. ##### 已经计算出距离的情况

```python
from slider_util import move_to_gap
# 浏览器对象
driver = webdriver.Chrome(options=chrome_options)
driver.get('xxx.xxxxx.com')

# 计算距离
distance = 50

# 获取滑块元素
slider = driver.find_element(by=By.XPATH, value='//div[contains(@class,"yidun_slider--hover")]')

# 调用工具(参数：selenium对象，滑块对象，距离)
move_to_gap(driver, slider, distance)
```

