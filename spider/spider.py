import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


class Spider():
    def __init__(self):
        self.option = webdriver.ChromeOptions()  # 加载启动项配置
        # self.option.add_argument('headless')  # 浏览器后台模式
        self.option.add_argument('--blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
        self.driver = webdriver.Chrome(options=self.option)

    def is_element_present(self, by, value):
        """
        用来判断元素标签是否存在，
        :param driver: 浏览器驱动
        :param by: 元素选择器
        :param value: 元素值
        :return:
        """
        try:
            self.driver.find_element(by=by, value=value)
        except NoSuchElementException as e:
            return False  # 未找到该元素
        else:
            return True  # 找到该元素

    def get_website(self):
        """
        加载网页
        :return:
        """
        login_url = "https://www.spotify.com/us/account/overview/"

        try:
            self.driver.get(login_url)  # 进入登录网址
            self.driver.implicitly_wait(10)  # 隐式等待
        except Exception as e:
            print(e)
            print("浏览器驱动加载失败或打不开Spotify官网")
            return "0"
        else:
            return "1"

    def login(self, username, password):
        """
        模拟登录
        :param driver: 浏览器驱动
        :param username: 用户名
        :param password: 密码
        :return:
        """
        # username_input = driver.find_element_by_name("username")  # 找到属性为username的元素（是一个输入框）
        # password_input = driver.find_element_by_name("password")  # 找到属性为password的元素（是一个输入框）

        '''
        一下账号是买家的账号
        '''
        try:
            self.driver.find_element_by_name("username").send_keys(username)  # 账号
            self.driver.find_element_by_name("password").send_keys(password)  # 密码
            self.driver.find_element_by_id("login-button").click()  # 点击登录
        except NoSuchElementException as e:
            print(e)
            print("服务器网页无法访问")
            return "111"


        '''
        判断一下密码是否正确
        '''
        self.driver.implicitly_wait(10)  # 隐式等待
        if self.is_element_present(By.XPATH, '//*[@id="app"]/body/div[1]/div[2]/div/div[2]/div/p/span'):
            print("用户名或密码错误")
            return "100"
        else:
            print("登录成功")
            return "1"

    def check_country(self):
        """
        检查国家
        :param driver:
        :return:
        """
        country = self.driver.find_element(By.XPATH, '//p[@data-qa="Profile Field: Country"]')

        if country.text == "US":
            print("国家对了")
            return "1"
        else:
            try:
                self.driver.find_element(By.PARTIAL_LINK_TEXT, 'Edit profile').click()  # 点击编辑
                self.driver.implicitly_wait(10)  # 隐式等待
                self.driver.find_element(By.XPATH, '//*[@id="profile_country"]').click()  # 点击选择栏
                self.driver.find_element(By.XPATH, '//*[@id="profile_country"]/option[@value="US"]').click()  # 选择美国
                self.driver.find_element(By.XPATH, '//*[@id="profile_save_profile"]').click()  # 确定
                print("国家换成US成功了")
                return "1"
            except Exception as e:
                print(e)
                print("国家更换失败")
                return "101"

    def open_other_link(self, link):
        """
        打开链接
        :param driver: 浏览器驱动
        :param link: 家庭链接
        :return:
        """
        self.driver.get(link)
        self.driver.implicitly_wait(10)  # 隐式等待

        if self.is_element_present(By.XPATH, '//*[@id="plan-already-full-error-page"]/div/section/h1') or \
                self.is_element_present(By.XPATH, '//*[@id="invitation-expired-error-page"]/div/section/h1'):
            print("链接满了")
            return "11"
        else:
            # try:
            #     self.driver.find_element(
            #         By.XPATH,
            #         '//*[@id="duo-home-root"]/main/div/div[1]/section/article/header/div/div[3]/div/button').click()
            # except Exception as e:
            #     print("已经是会员了")
            #     return "110"
            try:
                # You’re invited to Premium Family.
                self.driver.find_element(By.XPATH, '//*[@id="duo-home-root"]/main/div/div[1]/section/article/header/div/div[3]/div/button/span').click()
                time.sleep(2)  # 这里有一个二次跳转，强制等待3秒

                # Continue with this account?
                self.driver.find_element(By.XPATH, '//*[@id="duo-home-root"]/main/div/div/a[1]').click()
                time.sleep(2)  # 这里有一个二次跳转，强制等待3秒

                # Let’s confirm your home address
                self.driver.find_element(By.XPATH, '//*[@id="duo-home-root"]/main/div/div/button[2]').click()
                self.driver.implicitly_wait(10)  # 隐式等待

                # Enter your home address
                self.driver.find_element(
                    By.XPATH, '//*[@id="address"]').send_keys("Calle 25 De Julio, Guanica, Guánica 00653, Puerto Rico")
                self.driver.find_element(By.XPATH, '//*[@id="duo-home-root"]/form/main/div/div/button/span').click()
                self.driver.implicitly_wait(5)  # 隐式等待

                # Confirm address
                self.driver.find_element(By.XPATH, '//*[@id="confirm-address-dialog"]/footer/button[2]/span').click()
                self.driver.implicitly_wait(10)  # 隐式等待
                print("充值成功了")
                return "1"
            except Exception as e:
                print(e)
                print("找不到对应按钮")
                return "110"

    def close(self):
        self.driver.delete_all_cookies()
        self.driver.quit()
        print("关闭成功了")


if __name__ == '__main__':
    username = "111"
    password = "123456"
    link = "https://www.spotify.com/us/family/join/invite/CbaABy24B7c1ZB6/"  # 这个链接满了
