import pytest
import requests
import os
import logging
from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# 定义测试参数，包括单个文件和文件夹路径
class TestCreateUser:
    memories_list = None
    def test_input_value(self, create_user):  # 直接通过参数获取fixture中的driver
        try:
            # 访问应用首页（无需手动创建driver，fixture已处理）
            driver = create_user["driver"]
            test_data = create_user["test_data"]
             # 验证 Name 输入框
            new_name_box = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, 
            "//input[contains(@placeholder, 'no spaces allowed')]"))
        )
            assert new_name_box.get_attribute("value") == test_data["name"], "Name 值验证失败"

            # 验证 Description 文本域
            new_description_box = driver.find_element(By.XPATH, 
            "//textarea[contains(@placeholder, 'data-driven')]"
        )
            assert new_description_box.get_attribute("value") == test_data["description"], "Description 值验证失败"

            # 验证 Email 输入框
            new_email_box = driver.find_element(By.XPATH, 
            "//input[contains(@placeholder, 'your.name@example.com')]"
        )
            assert new_email_box.get_attribute("value") == test_data["email"], "Email 值验证失败"

            logging.info("所有输入值验证通过！")

        except AssertionError as e:
            logging.info(f"断言失败: {e}")
            raise  # 抛出让pytest捕获失败
        except Exception as e:
            logging.info(f"执行错误: {e}")
            raise


    def test_upload_memories_txt(self,create_user):
        driver = create_user["driver"]

        next_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, 
    "//button[contains(@class, 'bg-blue-500') and contains(@class, 'rounded-lg') and normalize-space(.)='Next: Upload Memories']"))
)       
        before_url = driver.current_url

        next_button.click()
        logging.info("已点击 Next: Upload Memories 按钮")

        # 验证 URL 跳转
        # 等待新页面加载
        WebDriverWait(driver, 10).until(
            EC.url_changes(before_url)
        )
        current_url = driver.current_url
        assert "/dashboard/train/memories" in current_url, f"URL 验证失败：当前 URL 为 {current_url}"
        logging.info("成功跳转到上传记忆页面！")
        test_description = """《星砂海湾的秘密》
潮湿的海风卷着咸涩气息扑在脸上时，林夏的指尖终于触到了那片冰凉
的砂砾。月光下，细沙泛着珍珠母贝般的虹彩，她记得奶奶临终前说过：
“当退潮时星砂铺满海湾，人鱼的歌声会带你找到藏在珊瑚礁里的愿望
瓶。” 海浪退去的沙滩上，无数细小颗粒在掌心流转，像碎掉的星光。
林夏蹲在礁石旁，忽然听见礁石缝隙里传来细碎的敲击声。她屏住呼吸，
用贝壳撬开一块覆盖着海藻的岩石——一个嵌着贝壳花纹的玻璃瓶赫
然躺在凹陷处，瓶口用蜡封着泛黄的纸条。 “小心海雾。”纸条上的字
迹被海水洇得模糊，林夏抬头望向海平面，不知何时起，乳白色的雾正
从深海方向蔓延而来，如同巨大的帷幕笼罩海湾。她攥紧瓶子往回跑，
凉鞋陷进星砂里，身后却传来越来越清晰的脚步声，不是浪花，是某种
有节奏的、类似于鱼尾拍击礁石的声响。 跑到灯塔下时，雾已经浓得
看不清五指。林夏撞开生锈的铁门，灯塔内部积着厚厚的海盐，螺旋楼
梯尽头的玻璃罩里，一盏老旧煤油灯忽明忽暗。她划亮火柴点燃灯芯，
光晕中突然浮现出一个人影——那是个穿着旧式航海服的少年，皮肤苍
白如珍珠，发间沾着水草，右眼戴着一枚黄铜色的单片眼镜。 “你打开
了愿望瓶。”少年的声音像浸在冰水里的玻璃珠，“三百年了，终于有人
敢回应我的召唤。” 林夏后退半步，瓶中的星砂突然发出微光，在两人
之间织成一道银河般的光带。少年抬手触碰光带，单片眼镜下的右眼闪
过幽蓝的光——那分明是一枚鱼鳞状的瞳孔。“我是被诅咒的守灯人，” 少年说，“每任灯塔主人都会在雾夜消失，而我必须诱惑迷途者成为新
的替身。但你不一样......”他盯着林夏颈间晃动的银鱼吊坠，“这是人鱼
族的信物，你奶奶是不是叫‘海月’？” 林夏猛地攥紧吊坠，奶奶临终前
正是握着这块刻着潮汐纹路的银鱼，让她来星砂海湾寻找真相。海雾在
窗外翻涌，传来越来越近的歌声，那是一种介于鲸鸣和竖琴之间的旋律，
让人浑身发麻却无法抗拒。 “快把瓶子摔碎！”少年突然抓住她的手腕，
“当年海月为了救我，用自己的声音和人鱼族做了交易。现在她们来索
债了，那些雾里的影子，都是被歌声夺走灵魂的水手！” 玻璃瓶在石墙
上撞碎的瞬间，星砂如烟花般炸开，化作蓝色火焰燃尽了整片雾气。晨
光穿透灯塔的窗棂，少年的身体逐渐透明，他摘下单片眼镜，露出完好
无损的右眼，眼底倒映着远处正在退去的海浪。 “告诉海月，她藏在珊
瑚礁里的愿望，我终于帮她实现了。”少年微笑着消失在光束中，只剩
一枚银色的鱼鳞落在林夏掌心，渐渐化作一粒星砂。 当第一缕阳光铺
满海湾时，林夏发现沙滩上的星砂已全部退去，只有灯塔下的礁石缝里，
静静躺着一枚新的玻璃瓶，瓶中装着半颗闪烁的人鱼眼泪。"""
        text_box = driver.find_element(By.XPATH, 
            "//textarea[contains(@placeholder, 'Enter your text here...')]"
        )
        text_box.clear()
        text_box.send_keys(test_description)
        save_button = driver.find_element(By.XPATH, 
    "//button[contains(@class, 'ant-btn-primary') and contains(@class, 'ant-btn-lg') and .//span[text()='Save Text']]")

        save_button.click()
        logging.info("已点击 Save Text 按钮")

        details_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, 
    "//button[text()='Details']"))
)
        details_button.click()
        logging.info("已点击 details 按钮")

        text_body = WebDriverWait(driver, 10).until(
EC.visibility_of_element_located((By.CSS_SELECTOR, ".ant-modal-body .markdown-body p"))
)
        text_text = text_body.text
        expected_text = test_description.replace('\n',' ').strip()
        actual_text = text_text.replace('\n',' ').strip()
        try:
            
            assert expected_text == actual_text,"内容验证失败"
            logging.info ("内容验证成功！模态框文本与输入一致")
        except AssertionError as e:
            logging.info(f"断言失败: {e}")
            raise  # 抛出让pytest捕获失败
        except Exception as e:
            logging.info(f"执行错误: {e}")
            raise



    @pytest.mark.parametrize(
    "test_path, is_folder, expected_files_count",
    [
        (os.path.join(os.path.dirname(__file__), "星砂海湾的秘密.pdf"), False, 1),
        (os.path.join(os.path.dirname(__file__), "test_upload_file/allowed"), True, 3),  
    ]
)
    def test_upload_memories_file(self,create_user,test_path, is_folder, expected_files_count):

        api_url = "http://localhost:3000/api/memories/file"
        succesful_count = 0

        try:
            if is_folder:
                folder_path = Path(test_path)
                if not folder_path.is_dir:
                    pytest.fail(f"测试路径不是文件夹: {test_path}")
                for file_path in folder_path.glob('*'):
                    if file_path.is_file():
                        with open(file_path,'rb') as f:
                            files = {
                                'file': (file_path.name,f,'application/octet-stream')
                            }
                            response = requests.post(api_url, files=files)
                            response.raise_for_status()
                        
                            response_data = response.json()
                            assert "message" in response_data, f"上传文件失败: {file_path.name}"
                            assert response_data["message"] == "Upload successful", f"上传文件失败: {file_path.name}"
                            succesful_count += 1
                            logging.info(f"文件上传成功：{file_path.name}")
            else:
                # 处理单个文件上传
                if not os.path.isfile(test_path):
                    pytest.fail(f"测试文件不存在: {test_path}")
                
                with open(test_path, 'rb') as f:
                    files = {
                    'file': (os.path.basename(test_path), f, 'application/pdf')
                        }
                    response = requests.post(api_url, files=files)
                    response.raise_for_status()
                
                    response_data = response.json()
                    assert "message" in response_data, f"上传文件失败: {os.path.basename(test_path)}"
                    assert response_data["message"] == "Upload successful", f"上传文件失败: {os.path.basename(test_path)}"
                
                    succesful_count += 1
                    logging.info(f"文件上传成功：{os.path.basename(test_path)}")
        
                # 验证成功上传的文件数量是否符合预期
            assert succesful_count == expected_files_count, f"成功上传的文件数量不符合预期: {succesful_count} != {expected_files_count}"
        
        except AssertionError as e:
            logging.info(f"断言失败: {e}")
            raise  # 抛出让pytest捕获失败
        except Exception as e:
            logging.info(f"执行错误: {e}")
            raise


    @pytest.mark.dependency(name='test_get_memories_list')
    def test_get_memories_list(self,create_user,test_session_state):
        try:
            url = 'http://localhost:3000/api/documents/list'
            response = requests.get(url)
            response.raise_for_status()
            response_body = response.json()

            assert response_body['code'] == 0,"获取记忆列表失败"
            TestCreateUser.memories_list = response_body['data']
            logging.info(f"成功获取{len(TestCreateUser.memories_list)}条记忆数据")
            # 添加断言确保列表不为空
            assert len(TestCreateUser.memories_list) > 0, "获取的记忆列表为空"

            # 更新会话状态：记忆已上传
            test_session_state["memories_uploaded_state"] = True
            test_session_state["uploaded_memories_idList"] = [mem["id"] for mem in TestCreateUser.memories_list]
            print(f"create_user fixture ID: {id(test_session_state)}")


        except AssertionError as e:
            logging.info(f"断言失败: {e}")
            raise  # 抛出让pytest捕获失败
        except Exception as e:
            logging.info(f"执行错误: {e}")
            raise


    @pytest.mark.dependency(depends=["test_get_memories_list"])
    def test_memory_delete(self,create_user):
        if TestCreateUser.memories_list:
            try:
                id = TestCreateUser.memories_list[0]['id']
                url = f'http://localhost:3000/api/memories/file/id/{id}'
                response = requests.delete(url)
                response.raise_for_status()
                response_body = response.json()

                assert response_body['code'] == 0,f"删除记忆{id}失败"
            except AssertionError as e:
                logging.info(f"断言失败: {e}")
                raise  # 抛出让pytest捕获失败
            except Exception as e:
                logging.info(f"执行错误: {e}")
                raise

        else:
            pytest.skip("记忆数据未获取")

