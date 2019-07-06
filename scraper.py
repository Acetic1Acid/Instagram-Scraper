from selenium import webdriver
from time import sleep
import os
import shutil
import requests
from bs4 import BeautifulSoup
from xlsxwriter import Workbook

class Insta:

    def __init__(self, username='scrap.data.12', password='justforfun', target='scrap.data.12',
                 path='C:\ScrapedImages'):
        self.username = username
        self.password = password
        self.target = target
        self.path = path
        self.error = False
        self.browser = webdriver.Chrome()
        self.main_url = 'https://www.instagram.com/accounts/login/?hl=en'
        self.browser.get(self.main_url)
        sleep(3)
        #Login
        self.Login()
        sleep(3)
        self.close_notifs()
        self.search_Target()
        sleep(1)
        #Scrolling
        self.Scrolling()
        sleep(1)
        #Making Folder
        if self.error is False:
            try:
                if not os.path.exists(path):
                    os.mkdir(path)
                    print('Directory Created.')
                    # Downloading Images
                    self.downloadImage()
                else:
                    self.downloadImage()
                    print("Directory Already Present.")
            except Exception as a:
                self.error = True
                print(a)
                print("Error while making directory.")
        sleep(3)
        self.browser.close()

    def Login(self):
        username_input = self.browser.find_element_by_xpath('//input[@aria-label="Phone number, username, or email"]')
        username_input.send_keys(self.username)
        password_input = self.browser.find_element_by_xpath('//input[@aria-label="Password"]')
        password_input.send_keys(self.password)
        login_button = self.browser.find_element_by_xpath('//button[@type="submit"]')
        login_button.click()

    def close_notifs(self):
        not_now = self.browser.find_element_by_xpath('//button[@class="aOOlW   HoLwm "]')
        not_now.click()

    def search_Target(self):
        search_button = self.browser.find_element_by_xpath('//input[@placeholder="Search"]')
        search_button.send_keys(self.target)
        target_url = 'https://www.instagram.com/' + self.target + '/'
        self.browser.get(target_url)
        sleep(3)

    def Scrolling(self):
        try:
            posts = self.browser.find_element_by_xpath('//span[@class="g47SY "]')
            posts = str(posts.text.replace(',',''))
            posts = int(posts)
            if posts > 36:
                number_scroll = int(abs((posts - 36))/12)
                number_scroll += 2
                try:
                    for value in range(posts):
                        self.browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
                        sleep(2)
                except Exception as e:
                    self.error = True
                    print(e)
                    print("Error occurred while trying to scroll down")
                sleep(10)
            else:
                self.browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        except Exception:
            self.error = True
            print("Could not find number of posts while trying to scroll down")

    def downloadImage(self):
        soup = BeautifulSoup(self.browser.page_source,'lxml')
        all_images = soup.find_all('img')
        print('Length of all images', len(all_images))
        for index,image in enumerate(all_images):
            filename = 'image_' + str(index) + '.jpg'
            image_path = os.path.join(self.path,filename)
            link = image['src']
            print("Downloading Image ", index)
            response = requests.get(link,stream = True)
            try:
                with open(image_path,'wb') as file:
                    shutil.copyfileobj(response.raw,file)
            except Exception as e:
                print(e)
                print("Error occurred while downloading %s "%index)
                print("Link -> ",link)

if __name__ == '__main__':
    user = str(input("Enter target username: "))
    application = Insta(target=user)

