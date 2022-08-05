from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from urllib.parse import unquote
from selenium.webdriver.common.keys import Keys
from time import sleep
import re
import requests 
import chromedriver_binary

class BackupController:
    def __init__(self,org_link,login_url="https://login.salesforce.com/",is_headless=1,implicit_wait=30):
        self.login_url = login_url
        self.org_link=org_link
        
        options = webdriver.ChromeOptions()
        if is_headless:
            options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(implicit_wait)
    
    def login(self):
        login_url = self.login_url
        self.driver.get(login_url)
        username = self.driver.find_element(By.ID, 'username')
        username.send_keys('ユーザ名')
        password = self.driver.find_element(By.ID, 'password')
        password.send_keys('パスワード')
        password.send_keys(Keys.ENTER)
        sleep(5)
    
    def detect_lightning(self,timeout):
        try:
            WebDriverWait(self.driver, timeout).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//div[contains(@class,'iframe-parent')]/iframe")))
            print('Lightning Detected')
            return 1
        except TimeoutException:
            print("Classic Detected")
            return 0
    
    def extract_file_info(self,link):
        print("ファイル解析開始：")
        if self.is_lightning:
            link=unquote(link)
            extract_link = re.search(r'srcUp\(\'(.*?)\'\)',link)
            link= extract_link.group(1)
        
        extract_file_name = re.search(r'fileName=(.*?)&id',link)
        file_name= extract_file_name.group(1)
        return link,file_name

    def download_file(self,url,cookies,file_name,download_location):

        with requests.get(url, stream=True, cookies=cookies) as r:
            r.raise_for_status()
            with open(download_location+file_name, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): 
                    # If you have chunk encoded response uncomment if
                    # and set chunk_size parameter to None.
                    #if chunk: 
                    f.write(chunk)

    def download_backups(self,download_location,backup_url,cookies=None):
        
        if cookies is None:
            print('Logging in')
            self.login()
            print('Logged in')
        else:
            raise ValueError("Username and Password Argument is Missing")
        print('Navigate to Backup URL')
        self.driver.get(backup_url)
        sleep(5) ## wait 5 seconds
        timeout=5 
        self.is_lightning=self.detect_lightning(timeout) ##check lightning experience

        soup=BeautifulSoup(self.driver.page_source, 'lxml') ##prepare the source

        #BeautifulSoup4の設定修正テキストをダウンロードに指定する
        if cookies is None:
            cookies = {'oid': self.driver.get_cookie("oid")["value"], 'sid':self.driver.get_cookie("sid")["value"]}
            print('Reading file links')
        for link in soup.find_all('a', href=True, string='ダウンロード'):
            file_path,file_name = self.extract_file_info(link.get('href'))
            file_url= self.org_link+file_path
            print('Downloading file '+file_url)
            self.download_file(file_url,cookies,file_name,download_location)
        self.driver.quit()