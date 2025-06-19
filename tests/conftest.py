import pytest
import json
import tempfile
import requests
import logging
import os
from dotenv import load_dotenv
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC

_TEST_SESSION_STATE = {
    "memories_uploaded_state": False,
    "uploaded_memories_idList": [],
    "local_training_started": False,
    "cloud_training_started": False
}
@pytest.fixture(scope="session")
def global_test_state():
    """会话级全局状态"""
    return _TEST_SESSION_STATE

@pytest.fixture(scope="module")
def test_session_state(global_test_state):
    """模块级状态，但实际共享全局状态"""
    # 返回全局状态引用
    return global_test_state

load_dotenv(dotenv_path="/Users/wangwanyu/actions/tests/.env")
@pytest.fixture(scope="module")
def driver():
    # 配置 Chrome 选项（无头模式、禁用沙盒等）
 
    # 更新ChromeDriver初始化以优化资源管理
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')  # 添加禁用GPU参数 
    options.add_argument('--window-size=1920,1080')
    # 添加页面加载策略
    options.set_capability('pageLoadStrategy', 'eager')


    
    # 创建浏览器实例
    driver = webdriver.Chrome(service=service, options=options)
    
    # 将浏览器实例传递给测试函数
    yield driver
    
    # 测试结束后关闭浏览器
    driver.quit()

@pytest.fixture(scope="module")  # 模块级作用域，整个模块只创建一次用户
def create_user(driver):
        """创建用户的通用方法"""
        # 访问应用首页
        driver.get('http://localhost:3000/')
        logging.info("成功打开首页")

        # 找到创建按钮并点击
        create_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'btn-primary'))
        )
        create_button.click()
        logging.info("已点击创建按钮")

        # 找到继续按钮并点击
        continue_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH,
            "//button[contains(@class, 'bg-gray-900') and contains(@class, 'rounded-lg') and contains(., 'Continue')]"
        )))
        continue_button.click()
        logging.info("已点击继续按钮")

        test_name = "eqe"
        test_description = "eqe"
        test_email = "eqe@e.q"

        # 创建用户
        name_box = driver.find_element(By.ID, 'name')
        name_box.clear()
        name_box.send_keys(test_name)
        
        description_box = driver.find_element(By.ID, 'description')
        description_box.clear()
        description_box.send_keys(test_description)
        
        email_box = driver.find_element(By.ID, 'email')
        email_box.clear()
        email_box.send_keys(test_email)
        
        logging.info("已输入用户信息")

        # 点击创建用户按钮
        create_user_button = driver.find_element(By.XPATH,
            "//button[contains(@class, 'bg-gray-900') and contains(@class, 'rounded-lg') and contains(., 'Create')]"
        )
        create_user_button.click()

        # 等待新页面加载
        WebDriverWait(driver, 10).until(
            EC.url_contains("/dashboard/train/identity")
        )

        # 保存测试数据供后续使用
        return {
        "driver": driver,
        "test_data": {
            "name": test_name,
            "description": test_description,
            "email": test_email
        }
    }
@pytest.fixture(scope="module")
def model_conf():
    print("环境变量列表：", os.environ.keys())
    try:
    
        # 检查单个变量是否存在
        if "PROVIDER_TYPE" not in os.environ:
            raise ValueError("PROVIDER_TYPE 未在环境变量中找到")
        url = "http://localhost:3000/api/user-llm-configs"
        headers = {
   'Content-Type': 'application/json',
   'Accept': '*/*',
   'Connection': 'keep-alive'
}
        payload = json.dumps({
        "provider_type": os.environ["PROVIDER_TYPE"],
        "chat_api_key": os.environ["CHAT_API_KEY"],
        "chat_endpoint": os.environ["CHAT_ENDPOINT"],
        "chat_model_name": os.environ["CHAT_MODEL_NAME"],
        "cloud_service_api_key": os.environ["CLOUD_SERVICE_API_KEY"],
        "embedding_api_key": os.environ["EMBEDDING_API_KEY"],
        "embedding_endpoint": os.environ["EMBEDDING_ENDPOINT"],
        "embedding_model_name": os.environ["EMBEDDING_MODEL_NAME"],
})
        response = requests.request("PUT", url, headers=headers, data=payload)
        
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.info(f"执行错误: {e}")
        raise


# @pytest.fixture(scope="session")
# def test_session_state():
#      """跟踪测试状态，供训练使用"""
#      return {
#           "memories_uploaded_state": False,
#           "uploaded_memories_idList": [],
#           "local_training_started": False,
#           "cloud_training_started": False
#      }

def pytest_collection_modifyitems(session, config, items):
    # 定义测试顺序（支持完整路径匹配，避免同名测试混淆）
    file_order = [
        "test_create_user",
        "test_local_training",
        "test_cloud_training"
    ]
    
    # 创建测试路径到测试项的映射（确保唯一性）
    item_path_map = {}
    for item in items:
        # 获取测试的完整路径（如：tests.test_create_user.test_create_user）
        item_path = ".".join([item.module.__name__, item.name])
        item_path_map[item_path] = item
    
    # 按预期顺序重新排列测试
    ordered_items = []
    for expected_path in file_order:
        # 匹配包含预期路径的测试（支持部分匹配，如 "tests.test_create_user" 匹配所有该文件中的测试）
        matched = [item for path, item in item_path_map.items() if expected_path in path]
        ordered_items.extend(matched)
    
    # 添加未匹配的测试（可选）
    remaining = [item for item in items if item not in ordered_items]
    ordered_items.extend(remaining)
    
    # 更新测试顺序
    items[:] = ordered_items

@pytest.fixture(scope="module")
def test_config():
    return {
        "cloud_api_base": "http://localhost:3000/api/cloud_service",
        "local_api_base": "http://localhost:3000/api/trainprocess",
        "retry_interval": 1,
        "timeout_seconds": 30 * 60
    }

@pytest.fixture(scope="function")
def get_model_list(test_config):
    def _get_model_list():
        try:
            url = f"{test_config['cloud_api_base']}/list_available_models"
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            pytest.fail(f"获取模型列表失败: {str(e)}")
            raise
    return _get_model_list

# 公共工具函数：启动训练任务
@pytest.fixture(scope="function")
def start_training(test_config):
    def _start_training(url, payload):
        headers = {"Content-Type": "application/json"}
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            pytest.fail(f"启动训练失败: {str(e)}")
            raise
    return _start_training

@pytest.fixture(scope="function")
def get_training_progress(test_config):
    def _get_training_progress(url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            pytest.fail(f"获取训练进度失败: {str(e)}")
            raise
    return _get_training_progress
