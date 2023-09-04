# 自动刷问卷星

fork自项目：[swpfY/auto_wjx](https://github.com/swpfY/auto_wjx)

## 使用

#### 安装依赖

```bash
pip install -r requirements.txt # 安装依赖，python版本为3.10.0
```

##### 下载 chromedriver

1. 首先查看chrome版本号：打开chrome，在设置 -> 关于Chrome中
2. 若为 144... 则不需下载
3. 否则与下载对应版本的[chromedriver](https://sites.google.com/chromium.org/driver/)（大版本相同即可）
4. 替换项目中的 `chromedriver.exe` 文件

#### 代码配置

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

## 多线程运行

> 单线程运行时速度较慢，可以借助多线程提高速度

### 借助 `pycharm` 实现多实例运行

1. 修改 `pycharm` 运行配置
2. `Run` -> `Edit Configurations...` -> `Allow multiple instances` 勾选 -> `Apply` -> `OK`
3. 运行 `wjx.py`，多点几次运行按钮，点一次开一个实例

## 一些问题

### 问卷星智能验证

使用`selenium`会给`window.navigator`添加`webdriver`属性，问卷星网页通过检测`window.navigator`对象是否包含`webdriver`这个属性来进行判断，设置一段代码将此属性设置为`undefined`：

```python
# 将属性设置为undefined
driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',
                           {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'})
```

#### 每刷几十次都会出现右滑验证码

每刷几十次，问卷星会根据ip设置右滑验证码。解决办法可以通过ip池，或者每个几十次换一次VPN节点。

同时当前项目代码中实现了右滑验证码逃逸。

#### windows and wsl

在 win 系统下使用 pycharm 运行程序时，需指定 python 解释器，应指定位于 win 系统下的 python 解释器，切记不可选择 wsl 下的解释器，因为我们的 chrome 浏览器以及 chromedriver 都是安装在 win 系统下的，使用 wsl 下的解释器会出现找不到 chromedriver PATH 的错误。

#### 被检测到重复提交问卷

两个方案：

1. 使用网上免费的 ip 池中的 ip 作为代理发送请求，实际测了一下，网上免费的 ip 大多数是用不了的，除非用付费的，不然速度贼慢。

2. 借助 clash 的节点切换实现请求 ip 的切换，需要注意的一点是 `wjx.cn` 位于国内，`Rule` 模式下默认是不经过代理的，需要添加相关配置：

    + Clash for windows ——> Profiles ————> 右键当前配置文件 ————> Edit

    + 文件最下方找到 rules 配置项

    + 添加 - DOMAIN-SUFFIX,wjx.cn,Proxy

    > 需要注意的是，根据科学上网提供商的策略设置不同，`clash.py` 代码可能会需要微调。
