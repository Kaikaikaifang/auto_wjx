import logging
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver import ActionChains
import numpy as np
import time

import conf

# 计数器
count = 0


def choose_answer():
    try:
        choose_one(1, [0.15, 0.5, 0.1, 0.15, 0.1])
        choose_one(2, [0.1, 0.2, 0.5, 0.15, 0.05])
        choose_one(3, [0.125, 0.25, 0.625, 0.0])
        choose_one(4, [0.26, 0.48, 0.23, 0.03])
        choose_multiple(5, [0.225, 0.18, 0.16, 0.17, 0.12, 0.135, 0.01], restrict=6)
        choose_multiple(6, [0.16, 0.17, 0.2, 0.2, 0.1, 0.16, 0.01])
        choose_multiple(7, [0.21, 0.23, 0.24, 0.14, 0.18, 0.0])
        choose_one(8, [0.33, 0.25, 0.17, 0.25, 0.0, 0.0])
        choose_multiple(9, [0.175, 0.2, 0.16, 0.2, 0.15, 0.115, 0])
        choose_one(10, [0.3, 0.4, 0.25, 0.05])
        choose_one(11, [0.3, 0.25, 0.4, 0.05])
        choose_one(12, [0.67, 0.3, 0.03, 0.0])
        choose_one(13, [0.46, 0.34, 0.05, 0.15])
        choose_multiple(14, [0.14, 0.17, 0.21, 0.17, 0.14, 0.16, 0.01, 0.0])
        choose_multiple(15, [0.12, 0.16, 0.14, 0.21, 0.11, 0.13, 0.13, 0.0])
        choose_one(16, [0.71, 0.29])
        choose_one(17, [0.48, 0.22, 0.2, 0.1])
        choose_multiple(18, [0.29, 0.28, 0.25, 0.18, 0.0])
        choose_one(19, [0.21, 0.21, 0.17, 0.41, 0.0])
        choose_multiple(20, [0.215, 0.165, 0.23, 0.21, 0.18, 0.0])
        choose_multiple(21, [0.255, 0.31, 0.255, 0.18, 0.0])
        # choose_multiple(5, [0.13, 0.2, 0.06, 0.13, 0.12, 0.11, 0.09, 0.12, 0.04], num=3)  # 指定选择的个数
        # choose_multiple(24)
        # choose_multiple(27, exclude=[5])
        # choose_multiple(50)
        # write_blank()  # 填写无
        # choose_multiple(19, [0.2, 0.1, 0.3, 0, 0.1, 0.2, 0.1], 3)  # 非相同概率时，没必要用 exclude。
        # choose_multiple(20)  # 各项均为相同概率，可省略不写。
    except NoSuchElementException as e:
        logging.error("任务执行失败，请检查配置。")


def probabilities_generator(choices_num, exclude=None):
    if isinstance(exclude, list):
        choices_num -= len(exclude)
    probability = 1 / choices_num
    res = [probability for i in range(choices_num)]
    if exclude:
        for i in exclude:
            res.insert(i, 0)
    return res


def choose_one(question_number, question_probability=None, exclude=None):
    """
    :param question_number: int
    :param question_probability: [] # If you set it None, It will auto generate an averages list.
    :param exclude: [] # A list which question index you want to exclude.
    """
    el_choices = driver.find_elements(By.XPATH, f"//*[@id=\"div{question_number}\"]/div[2]/div")
    choices_num = len(el_choices)
    if not question_probability:
        question_probability = probabilities_generator(choices_num, exclude=exclude)
    chosen_number = np.random.choice(
        a=list(range(1, choices_num + 1)),
        p=question_probability
    )
    el_checked = driver.find_element(By.XPATH, f"//*[@id=\"div{question_number}\"]/div[2]/div[{chosen_number}]")
    el_checked.click()
    # 随机停顿
    # rt = random.randint(10, 100)
    # time.sleep(rt / 100)


def choose_multiple(question_number, question_probability=None, restrict=10000, exclude=None, num=0):
    """
    @param question_number: int
    @param question_probability: [] # If you set it None, It will auto generate an averages list.
    @param restrict: int # The max number of choices you want to choose.
    @param exclude: [] # A list which question index you want to exclude.
    @param num: int # The number of choices you want to choose.
    """
    el_options = driver.find_elements(By.XPATH, f"//*[@id=\"div{question_number}\"]/div[2]/div")
    choices_num = len(el_options)
    not_zero_num = len(el_options)
    if not question_number:
        question_probability = probabilities_generator(choices_num, exclude=exclude)
    size = num if num else random.randint(1, min(restrict, choices_num))
    for i in question_probability:
        if not i:
            not_zero_num -= 1
    size = size if size <= not_zero_num else not_zero_num
    print(question_number, question_probability, size)
    chosen_number = np.random.choice(
        a=list(range(1, choices_num + 1)),
        p=question_probability,
        size=size,
        replace=False
    )
    for i in chosen_number:
        driver.find_element(By.XPATH, f"//*[@id=\"div{question_number}\"]/div[2]/div[{i}]/span/a").click()
    # 随机停顿
    # rt = random.randint(10, 100)
    # time.sleep(rt / 100)


def write_blank():
    """填写内容"""
    driver.find_element(By.XPATH, '//*[@id="q51"]').send_keys('无')
    # 随机停顿
    # rt = random.randint(10, 100)
    # time.sleep(rt / 100)


def slider_move(dest=380):
    """
    :param dest: int # A position where you want to move.
    """
    try:
        el_slider = driver.find_element(By.XPATH, "//*[@id='nc_1_n1z']") if check_element_exists("//*[@id='nc_1_n1z']") else WebDriverWait(driver, 10).until(
            presence_of_element_located(
                (By.XPATH, "//*[@id='nc_1_n1z']"))
        )
        ActionChains(driver).click_and_hold(el_slider).perform()
        ActionChains(driver).move_by_offset(xoffset=dest, yoffset=0).perform()
        ActionChains(driver).release().perform()
    except (TimeoutException, ElementClickInterceptedException):
        pass


def check_element_exists(element: str) -> bool:
    """ 检查元素是否存在，若不存在会抛出异常

    :param element: id
    :return: Boolean
    """
    try:
        driver.find_element(By.XPATH, element)
        return True
    except Exception as e:
        return False


def skip_verify():
    """跳过验证"""
    if check_element_exists('//*[@id="layui-layer1"]/span/a'):
        driver.find_element(By.XPATH, '//*[@id="layui-layer1"]/span/a').click()
    if check_element_exists('//*[@id="rectMask"]'):
        driver.find_element(By.XPATH, '//*[@id="rectMask"]/div[2]').click()


def main():
    global count
    try:
        for i in range(loop_count):
            driver.get(question_url)
            try:
                driver.find_element(By.XPATH, '//*[@id="confirm_box"]/div[2]/div[3]/button[1]').click()  # 取消提示
            except NoSuchElementException:
                pass
            if check_element_exists('//*[@id="layui-layer1"]/div[3]/a[2]'):
                # 检测到重复填写相同问卷：重启浏览器
                logging.error("检测到重复填写相同问卷：重启浏览器")
                driver.close()
                return False
            choose_answer()
            driver.find_element(By.XPATH, '//*[@id="ctlNext"]').click()
            time.sleep(0.5)
            # 跳过智能验证（点击按钮）
            skip_verify()
            try:
                WebDriverWait(driver, 3).until(
                    ec.url_changes(question_url)
                )
            except TimeoutException:
                # 滑动滑条
                slider_move(dest=380)  # 若验证码逃逸失败，请自行调教参数 dest
            count += 1
            if count == loop_count:
                print('任务完成，正在退出任务: 1')
                driver.close()
                return True
    except Exception as e:
        print('error: ', e)
        logging.error("任务执行错误，正在退出任务: ")
        return False
    print('任务完成，正在退出任务: 2')
    return True


if __name__ == '__main__':
    question_url = conf.QUESTION_URL or input("请输入问卷地址：")
    loop_count = conf.LOOP_COUNT or int(input("请输入填写次数："))
    opt = Options()
    opt.add_experimental_option('excludeSwitches', ['enable-automation'])
    opt.add_experimental_option('useAutomationExtension', False)
    service = Service(executable_path='./chromedriver')
    # 首次配置浏览器
    # include the path(./chromedriver) to ChromeDriver when instantiating webdriver.Chrome
    driver = webdriver.Chrome(service=service, options=opt)
    # driver = webdriver.Safari(options=opt)
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',
                           {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'})
    while True:
        #
        if main():
            break
        else:
            # 重新配置浏览器
            # include the path(./chromedriver) to ChromeDriver when instantiating webdriver.Chrome
            driver = webdriver.Chrome(service=service, options=opt)
            # driver = webdriver.Safari(options=opt)
            driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',
                                   {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'})