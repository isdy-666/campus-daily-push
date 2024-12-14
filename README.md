# 景艺大课表推送小助手

一个基于 Python 的自动化课表天气信息推送工具,可以定时获取天气信息并通过微信推送给用户。

## 功能特点

- 自动抓取天气数据
- 支持自定义样式的天气信息展示
- 通过 WxPusher 实现微信消息推送
- 支持不同天气状况的动态背景颜色
- 包含随机延迟功能,防止频繁请求

## 必要条件

- Python 3.6+
- Chrome 浏览器
- ChromeDriver

## 依赖库

```bash
pip install requests
pip install beautifulsoup4
pip install selenium
```

## 配置说明

所有配置项都集中在 `config.py` 文件中，首次使用需要复制 `config.example.py` 并重命名为 `config.py`：

```bash
cp config.example.py config.py
```

### 配置项说明

1. WxPusher 配置
```python
WXPUSHER_TOKEN = "your_token_here"  # 你的WxPusher Token
TOPIC_ID = 0  # 你的主题ID
```

2. ChromeDriver 配置
```python
CHROME_DRIVER_PATH = "path/to/chromedriver"  # ChromeDriver路径
```

3. 随机延迟配置
```python
MIN_DELAY = 1  # 最小延迟时间(秒)
MAX_DELAY = 3  # 最大延迟时间(秒)
```

4. 天气背景颜色配置
```python
WEATHER_GRADIENTS = {
    "晴": "linear-gradient(135deg, #FF8C00 0%, #FFD700 100%)",
    "多云": "linear-gradient(135deg, #4B6CB7 0%, #182848 100%)",
    # ... 其他天气状况的颜色配置
}

DEFAULT_GRADIENT = "linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)"
```

5. 定时任务配置
```python
SCHEDULE_TIME = "0 7 * * *"  # crontab 格式的定时配置
```

## 文件结构

- `daily_push.py`: 主程序文件,包含核心功能实现
- `weather.py`: 天气数据获取和处理模块
- `7.2.py`: 消息推送模块

## 使用方法

1. 克隆仓库
```bash
git clone [仓库地址]
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 修改配置文件中的相关参数

4. 运行程序
```bash
python weather.py
```

## 自定义配置

### 天气背景颜色
可以在 `daily_push.py` 中的 `get_weather_gradient` 函数修改不同天气状况对应的背景渐变色：

```python
gradients = {
    "晴": "linear-gradient(135deg, #FF8C00 0%, #FFD700 100%)",
    "多云": "linear-gradient(135deg, #4B6CB7 0%, #182848 100%)",
    # 可以根据需要添加或修改更多天气状况的颜色
}
```

### 随机延迟设置
可以在 `daily_push.py` 中修改随机延迟的时间范围：

```python
def random_delay(min_delay=1, max_delay=3):
    """随机延迟函数"""
    time.sleep(random.uniform(min_delay, max_delay))
```

## 定时任务设置

### Windows
可以使用任务计划程序设置定时运行

### Linux
可以使用 crontab 设置定时运行：
```bash
# 编辑 crontab
crontab -e

# 添加定时任务 (例如每天早上 7 点运行)
0 7 * * * /usr/bin/python3 /path/to/weather.py
```

## 注意事项

1. 请确保 ChromeDriver 版本与 Chrome 浏览器版本匹配
2. 首次使用需要关注 WxPusher 公众号并绑定
3. 建议适当设置随机延迟,避免频繁请求
4. 请遵守相关网站的使用规则和约束

## 常见问题

1. ChromeDriver 启动失败
   - 检查 Chrome 浏览器和 ChromeDriver 版本是否匹配
   - 确认 ChromeDriver 路径是否正确

2. 消息推送失败
   - 检查 WxPusher Token 是否正确
   - 确认是否已关注并绑定 WxPusher 公众号

## 贡献指南

欢迎提交 Issue 和 Pull Request 来帮助改进项目。

## 许可证

本项目采用 MIT 许可证。

## 更新日志

### v1.0.0 (2023-12-14)
- 初始版本发布
- 实现基本的天气数据获取和推送功能
- 支持自定义样式展示

## 联系方式

如有问题或建议,欢迎通过以下方式联系：
- 提交 Issue
- 发送邮件至: ctrdlg666@outlook.com

## 项目预览

### 效果展示
# #### 晴天无课程
  ![晴天无课程效果](assets/sunny-no-class.png)

# #### 阴天有课程
+ ![阴天有课程效果](assets/rainy-with-class.png)

## 项目徽章
[![License](https://img.shields.io/github/license/isdy-666/campus-daily-push)](https://github.com/isdy-666/campus-daily-push/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/)
[![Issues](https://img.shields.io/github/issues/isdy-666/campus-daily-push)](https://github.com/isdy-666/campus-daily-push/issues)
[![Stars](https://img.shields.io/github/stars/isdy-666/campus-daily-push)](https://github.com/isdy-666/campus-daily-push/stargazers)

## 快速开始

```bash
# 克隆项目
git clone https://github.com/isdy-666/campus-daily-push.git

# 进入项目目录
cd campus-daily-push

# 安装依赖
pip install -r requirements.txt

# 修改配置
cp config.example.py config.py
# 编辑 config.py 填入你的配置信息

# 运行项目
python weather.py
```

## 项目结构

```
.
├── README.md
├── requirements.txt
├── LICENSE
├── daily_push.py
├── weather.py
├── 7.2.py
└── config.example.py
```

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=isdy-666/campus-daily-push&type=Date)](https://star-history.com/#isdy-666/campus-daily-push&Date)
