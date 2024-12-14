import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import random

try:
    from config import *
except ImportError:
    print("请先复制 config.example.py 为 config.py 并进行配置")
    exit(1)

def random_delay():
    """随机延迟函数"""
    time.sleep(random.uniform(MIN_DELAY, MAX_DELAY))

def get_weather_gradient(weather):
    """根据天气状况返回对应的背景渐变色"""
    for weather_type, gradient in WEATHER_GRADIENTS.items():
        if weather_type in weather:
            return gradient
            
    return DEFAULT_GRADIENT

def get_weather():
    """获取景德镇天气信息"""
    try:
        service = Service(CHROME_DRIVER_PATH)

        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--ignore-ssl-errors')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-logging')
        chrome_options.add_argument('--disable-usb-discovery')
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')

        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        url = "https://weathernew.pae.baidu.com/weathernew/pc?query=江西景德镇天气&srcid=4982"
        driver.get(url)
        
        time.sleep(5)
        
        weather_json = driver.execute_script("return window.tplData.weather")
        
        weather_data = {
            "temperature": f"{weather_json['temperature']}°",
            "weather": weather_json.get('weather', '暂无数据'),
            "wind": f"{weather_json['wind_direction']} {weather_json['wind_power']}",
            "humidity": f"{weather_json['humidity']}%",
            "air_quality": weather_json.get('air_quality', '暂无数据'),
            "updated_time": weather_json['update_time'].split()[1]  # 只取时间部分
        }
        
        driver.quit()
        return weather_data
        
    except Exception as e:
        print(f"获取天气信息失败: {e}")
        if 'driver' in locals():
            try:
                driver.quit()
            except:
                pass
        return None

def get_today_schedule(background_gradient=None):
    """获取今日课程表"""
    try:
        service = Service(CHROME_DRIVER_PATH)

        chrome_options = Options()
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--ignore-ssl-errors')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-logging')
        chrome_options.add_argument('--disable-usb-discovery')
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument("--start-maximized")

        driver = webdriver.Chrome(service=service, options=chrome_options)

        # 打开登录页面
        login_url = "http://171.35.197.121/eams/loginExt.action"
        driver.get(login_url)
        random_delay()

        # 查找用户名和密码输入框并输入凭据
        username_field = driver.find_element(By.NAME, 'username')
        password_field = driver.find_element(By.NAME, 'password')

        username = USERNAME
        password = PASSWORD

        # 模拟鼠标操作输入用户名和密码
        actions = ActionChains(driver)
        actions.move_to_element(username_field).perform()
        random_delay()
        username_field.send_keys(username)
        actions.move_to_element(password_field).perform()
        random_delay()
        password_field.send_keys(password)

        # 点击登录按钮
        login_button = driver.find_element(By.NAME, 'submitBtn')
        actions.move_to_element(login_button).perform()
        random_delay()
        login_button.click()

        # 等待页面加载完成
        random_delay(5, 10)

        # 提取当前登录的 Cookies
        cookies = driver.get_cookies()

        # 关闭浏览器
        driver.quit()

        # 转换 Selenium Cookies 为 requests 的 Cookies 格式
        session_cookies = {cookie['name']: cookie['value'] for cookie in cookies}

        # 构造 fetch 请求的 URL 和 Headers
        url = "http://171.35.197.121/eams/homeExt!main.action"
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "upgrade-insecure-requests": "1",
            "referrer": "http://171.35.197.121/eams/homeExt.action",
        }

        # 使用 requests 模拟登录后进行请求
        response = requests.get(url, headers=headers, cookies=session_cookies)

        if response.status_code == 200:
            page_content = response.text
            soup = BeautifulSoup(page_content, 'html.parser')

            today_courses = soup.select("div.jrkc-box table tbody tr")
            table_rows = ""

            for course in today_courses:
                time_cell = course.find("td", class_="date")
                course_time = " ".join(time_cell.get_text(strip=True).split())
                time_span = time_cell.find("span", class_="time")
                actual_time = time_span.get_text(strip=True) if time_span else ""
                
                course_name = course.find("h5").get_text(strip=True)
                location = course.find("span", class_="zt").get_text(strip=True).replace("上课地点: ", "")

                formatted_time = actual_time if actual_time else course_time

                table_rows += f"""
                <tr style="background: rgba(255, 255, 255, 0.1);">
                    <td style="padding: 12px; text-align: center; border: 1px solid rgba(255, 255, 255, 0.2);">{formatted_time}</td>
                    <td style="padding: 12px; border: 1px solid rgba(255, 255, 255, 0.2);">{course_name}</td>
                    <td style="padding: 12px; text-align: center; border: 1px solid rgba(255, 255, 255, 0.2);">{location}</td>
                </tr>
                """

            current_date = datetime.now().strftime("%Y年%m月%d日")

            if table_rows:
                return f"""
                <div style="padding: 20px 20px 0 20px; background: {background_gradient}; border-radius: 15px 15px 0 0; font-family: Arial, sans-serif; color: white;">
                    <h3 style="margin: 0 0 15px 0; text-align: center; font-size: 24px;">📅 {current_date} 课程表</h3>
                    <table style="width: 100%; border-collapse: collapse; margin-top: 10px;">
                        <thead>
                            <tr style="background: rgba(255, 255, 255, 0.2);">
                                <th style="padding: 12px; text-align: center; border: 1px solid rgba(255, 255, 255, 0.2); width: 30%;">时间</th>
                                <th style="padding: 12px; text-align: center; border: 1px solid rgba(255, 255, 255, 0.2);">课程</th>
                                <th style="padding: 12px; text-align: center; border: 1px solid rgba(255, 255, 255, 0.2); width: 25%;">���点</th>
                            </tr>
                        </thead>
                        <tbody>
                            {table_rows}
                        </tbody>
                    </table>
                </div>
                """
            else:
                return f"""
                <div style="padding: 20px 20px 0 20px; background: {background_gradient}; border-radius: 15px 15px 0 0; font-family: Arial, sans-serif; color: white;">
                    <h3 style="margin: 0 0 15px 0; text-align: center; font-size: 24px;">📅 {current_date}</h3>
                    <p style="text-align: center; padding: 20px; background: rgba(255, 255, 255, 0.1); border-radius: 10px;">今天没有课程安排 🎉</p>
                </div>
                """
    except Exception as e:
        print(f"获取课表失败: {e}")
        return f"""
        <div style="padding: 20px 20px 0 20px; background: {background_gradient}; border-radius: 15px 15px 0 0; font-family: Arial, sans-serif; color: white;">
            <p style="text-align: center;">课表信息获取失败</p>
        </div>
        """

def format_weather_html(weather_data, background_gradient):
    """将天气数据格式化为HTML"""
    if not weather_data:
        return f"""
        <div style="padding: 20px; background: {background_gradient}; border-radius: 0 0 15px 15px; font-family: Arial, sans-serif; color: white; border-top: 1px solid rgba(255, 255, 255, 0.1);">
            <p style="text-align: center;">天气信息获取失败</p>
        </div>
        """
    
    html = f"""
    <div style="padding: 20px; background: {background_gradient}; border-radius: 0 0 15px 15px; font-family: Arial, sans-serif; color: white; border-top: 1px solid rgba(255, 255, 255, 0.1);">
        <div style="text-align: center; margin-bottom: 20px;">
            <h2 style="margin: 0; font-size: 48px; font-weight: bold;">{weather_data['temperature']}</h2>
            <p style="margin: 10px 0; font-size: 18px;">{weather_data['weather']}</p>
            <p style="margin: 5px 0; font-size: 14px; opacity: 0.8;">景德镇</p>
        </div>
        
        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin-top: 20px;">
            <div style="background: rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 10px; text-align: center;">
                <div style="font-size: 20px;">💨</div>
                <div style="font-size: 14px; margin-top: 5px;">风况</div>
                <div style="font-size: 16px; margin-top: 5px;">{weather_data['wind']}</div>
            </div>
            <div style="background: rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 10px; text-align: center;">
                <div style="font-size: 20px;">💧</div>
                <div style="font-size: 14px; margin-top: 5px;">湿度</div>
                <div style="font-size: 16px; margin-top: 5px;">{weather_data['humidity']}</div>
            </div>
            <div style="background: rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 10px; text-align: center;">
                <div style="font-size: 20px;">🌬️</div>
                <div style="font-size: 14px; margin-top: 5px;">空气质量</div>
                <div style="font-size: 16px; margin-top: 5px;">{weather_data['air_quality']}</div>
            </div>
            <div style="background: rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 10px; text-align: center;">
                <div style="font-size: 20px;">🕒</div>
                <div style="font-size: 14px; margin-top: 5px;">更新时间</div>
                <div style="font-size: 16px; margin-top: 5px;">{weather_data['updated_time']}</div>
            </div>
        </div>
    </div>
    """
    return html

def send_daily_info():
    """发送每日天气和课表信息"""
    # 先获取天气数据以确定背景颜色
    weather_data = get_weather()
    background_gradient = get_weather_gradient(weather_data['weather']) if weather_data else "linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)"
    
    # 获取课表和天气的HTML
    schedule_html = get_today_schedule(background_gradient)
    weather_html = format_weather_html(weather_data, background_gradient)
    
    # 组合HTML内容，课表在上面
    content = f"""
    <div style="max-width: 500px; margin: 0 auto; font-family: Arial, sans-serif;">
        <div style="background: {background_gradient}; border-radius: 15px; overflow: hidden;">
            {schedule_html}
            {weather_html}
        </div>
    </div>
    """
    
    # 发送消息
    url = "https://wxpusher.zjiecode.com/api/send/message"
    data = {
        "appToken": WXPUSHER_TOKEN,
        "content": content,
        "contentType": 2,  # 2表示HTML
        "topicIds": [TOPIC_ID],  # 使用主题ID发送
        "summary": "每日天气与课表",
        "url": ""
    }
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200 and response.json()["code"] == 1000:
            print("消息推送成功！")
        else:
            print(f"消息推送失败: {response.json()}")
    except Exception as e:
        print(f"消息推送出错: {e}")

if __name__ == "__main__":
    try:
        # 配置 Chrome 选项来禁用日志
        chrome_options = Options()
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        # 发送一次推送
        send_daily_info()
        print("推送完成！")
    except KeyboardInterrupt:
        print("\n程序已停止运行")
    except Exception as e:
        print(f"程序运行出错: {e}")
    finally:
        exit(0) 