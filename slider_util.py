import random
import time

import ddddocr
import requests
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


def get_img_and_move(img_bg_url: str, img_slider_url: str, driver: WebDriver, slider: WebElement):
    """
    获取图片并移动滑块
    :param img_bg_url: 背景图片元素
    :param img_slider_url: 滑块图片元素
    :param driver: selenium浏览器对象
    :param slider: 滑块元素
    :return:
    """
    # 下载图片
    background_bytes = requests.get(img_bg_url).content
    target_bytes = requests.get(img_slider_url).content
    det = ddddocr.DdddOcr(det=False, ocr=False)
    res = det.slide_match(target_bytes, background_bytes)

    # 拖动滑块
    time.sleep(0.5)
    # 计算出来的距离与实际拖动距离可能存在偏差
    move_to_gap(driver, slider, res.get('target'))


def move_to_gap(driver: WebDriver, slider: WebElement, distance: int):
    """
    移动滑块到对应的位置，计算出来的距离与实际拖动距离可能存在偏差
    :param driver: selenium浏览器对象
    :param slider: 要移动的滑块
    :param distance: 滑动距离
    :return:
    """
    tracks = __get_slide_track(distance)
    ActionChains(driver).click_and_hold(slider).perform()
    for x, y in tracks:
        ActionChains(driver).move_by_offset(xoffset=x, yoffset=y).perform()
    time.sleep(0.1)
    ActionChains(driver).release().perform()


def __ease_out_expo(sep):
    """
    缓动函数 easeOutExpo
    参考：https://easings.net/zh-cn#easeOutExpo
    """
    if sep == 1:
        return 1
    else:
        return 1 - pow(2, -10 * sep)


def __get_slide_track(distance):
    """
    根据滑动距离生成滑动轨迹
    :param distance: 需要滑动的距离
    :return: 滑动轨迹<type 'list'>: [[x,y], ...]
        x: 滑动的横向距离
        y: 滑动的纵向距离
    """

    if not isinstance(distance, int) or distance < 0:
        raise ValueError(f"distance类型必须是大于等于0的整数: distance: {distance}, type: {type(distance)}")
    # 初始化轨迹列表
    slide_track = []
    # 共记录count次滑块位置信息
    count = random.randint(10, 20)
    # 初始化滑动时间
    t = random.randint(50, 100)
    # 记录上一次滑动的距离
    _x = 0
    _y = 0
    for i in range(count):
        # 已滑动的横向距离
        x = round(__ease_out_expo(i / count) * distance)
        # 滑动过程消耗的时间
        t += random.randint(10, 20)
        if x == _x:
            continue
        # slide_track.append([x, _y, t])
        slide_track.append([x - _x, random.randint(-2, 2)])
        _x = x
    slide_track.append(slide_track[-1])
    return slide_track
