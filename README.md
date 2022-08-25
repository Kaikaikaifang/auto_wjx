## 自动刷问卷星

来自项目：[huzige433/auto_wjx](https://github.com/huzige433/auto_wjx)

### 使用

**安装依赖**

```bash
pip install -r requirements.txt # 安装依赖，python版本为3.10.0
```

**Mac下载chromedriver**

1. 首先查看chrome版本号：打开chrome，在设置 -> 关于Chrome中
2. 下载对应版本的[chromedriver](https://sites.google.com/chromium.org/driver/)（大版本相同即可）
3. 配置环境：将下载的`chromedriver`移动到`/usr/local/bin`
4. 查看`chromedriver`版本：`chromedriver --version`（输出内容则代表配置成功）

**代码配置**

1. 修改 `conf.py` 中的配置项

```python
# conf.py

# 以配置项执行
QUESTION_URL = ""  # 问卷地址
LOOP_COUNT = 1  # 执行次数

# ------或者-------

# 以命令行交互
QUESTION_URL = None
LOOP_COUNT = None
```

2. 修改 `wjx.py` 中的 `choose_answer()` 方法

```python
# wjx.py

choose_one(题号, [概率1, 概率2, ...])
choose_multiple(题号, [概率1, 概率2, ...], 最多选项限制（可选参数）)
```

### 一些问题

**问卷星智能验证**

使用`selenium`会给`window.navigator`添加`webdriver`属性，问卷星网页通过检测`window.navigator`对象是否包含`webdriver`这个属性来进行判断，设置一段代码将此属性设置为`undefined`：

```python
# 将属性设置为undefined
driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',
                           {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'})
```

**每刷几十次都会出现右滑验证码**

每刷几十次，问卷星会根据ip设置右滑验证码。解决办法可以通过ip池，或者每个几十次换一次VPN节点。

同时当前项目代码中实现了右滑验证码逃逸（默认窗口大小应该能够逃逸，有问题请自行调教参数 dest）。
