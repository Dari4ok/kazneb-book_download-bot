from selenium import webdrivergit config --system user.email 
from selenium.webdriver.common.by import By
import requests
import os
import time

class ImageDownloader:
    def __init__(self, url, folder, min_width=1100, min_height=1600):
        self.url = url
        self.min_width = min_width
        self.min_height = min_height
        self.folder = folder

        # веб драйвты қосу
        self.driver = webdriver.Chrome()

        # беттерге қалта жасай
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)

    def download_images(self):
        try:
            # сайтты ашу
            self.driver.get(self.url)
            time.sleep(5)  # толық ашылғанша күту

            # барлық беттерді табу
            images = self.driver.find_elements(By.TAG_NAME, 'img')

            # беттерді өлшеу
            for i, img in enumerate(images):
                self.download_image_if_large_enough(img, i)

            self.driver.quit()  # браузерді жабу
        except Exception as e:
            print(f"Ошибка: {e}")
            self.driver.quit()  # қателік болса жабу

    def download_image_if_large_enough(self, img, index):
        # суреттердің өлшемін табу
        width = img.get_attribute('naturalWidth')
        height = img.get_attribute('naturalHeight')

        if width and height:
            width = int(width)
            height = int(height)

            # суреттерді өлшеу
            if width > self.min_width and height > self.min_height:
                img_url = img.get_attribute('src')
                if img_url and img_url.startswith('http'):
                    self.save_image(img_url, index, width, height)

    def save_image(self, img_url, index, width, height):
        # суреттерді сақтау
        img_data = requests.get(img_url).content
        file_path = os.path.join(self.folder, f'image_{index+1}.jpg')
        with open(file_path, 'wb') as f:
            f.write(img_data)


if __name__ == "__main__":
    url = 'https://kazneb.kz/kk/bookView/view?brId=1651358&simple=false'
    downloader = ImageDownloader(url, 'Сөзтүзер')
    downloader.download_images()
