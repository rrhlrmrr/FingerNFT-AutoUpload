import tkinter
import subprocess
from tkinter import *
from tkinter import filedialog
import os
import sys
import pickle
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as ExpectedConditions
from selenium.webdriver.support.ui import Select


############################################ Env Setup #############################################

root = Tk()
root.geometry('350x300')
root.title("NFTs Bulk Upload to eedea")
input_save_list = ["NFTs folder :", 0, 0, 0, 0, 0, 0, 0, 0]
main_directory = os.path.join(sys.path[0]) ## Current space

# Pyinstaller


def open_chrome_profile():
    subprocess.Popen(
        [
            "start",
            "chrome",
            "--remote-debugging-port=8989",
            "--user-data-dir=C:/eedea/datadir"
        ],
        shell=True,
    )

def save_file_path():
    return 'C:/eedea/' + "Save_file.cloud"

# ask for directory on clicking button, changes button name.
def upload_folder_input():
    global upload_path
    upload_path = filedialog.askdirectory()
    Name_change_img_folder_button(upload_path)

def Name_change_img_folder_button(upload_folder_input):
    upload_folder_input_button["text"] = upload_folder_input

class InputField:
    def __init__(self, label, row_io, column_io, pos, master=root):
        self.master = master
        self.input_field = Entry(self.master)
        self.input_field.label = Label(master, text=label)
        self.input_field.label.grid(row=row_io, column=column_io)
        self.input_field.grid(row=row_io, column=column_io + 1)
        try:
            with open(save_file_path(), "rb") as infile:
                new_dict = pickle.load(infile)
                self.insert_text(new_dict[pos])
        except FileNotFoundError:
            pass

    def insert_text(self, text):
        self.input_field.delete(0, "end")
        self.input_field.insert(0, text)

    def save_inputs(self, pos):
        input_save_list.insert(pos, self.input_field.get())
        with open(save_file_path(), "wb") as outfile:
            pickle.dump(input_save_list, outfile)

###input objects###
pname_input = InputField("이름:", 2, 0, 1)
desc_input = InputField("설명(선택):", 3, 0, 2)
noc_input = InputField("수량:", 4, 0, 3)
royalties_input = InputField("인세:", 5, 0, 4)
start_num_input = InputField("시작 숫자:", 6, 0, 5)
end_num_input = InputField("끝 숫자:", 7, 0, 6)

############################################ Env Setup #############################################


############################################ Save Input #############################################
def save():
    input_save_list.insert(0, upload_path) ## User Setting
    pname_input.save_inputs(1)
    desc_input.save_inputs(2)
    noc_input.save_inputs(3)
    royalties_input.save_inputs(4)
    start_num_input.save_inputs(5)
    end_num_input.save_inputs(6)



# _____MAIN_CODE_____
def main_program_loop():
    # Main code
    project_path = main_directory
    file_path = upload_path
    pname = pname_input.input_field.get()
    pdesc = desc_input.input_field.get()
    pnoc = noc_input.input_field.get()
    roy = royalties_input.input_field.get()
    start_num = int(start_num_input.input_field.get())
    end_num = int(end_num_input.input_field.get())

    ##chromeoptions
    opt = Options()
    opt.add_experimental_option("debuggerAddress", "127.0.0.1:8989")
    opt.add_argument('--no-sandbox')
    opt.add_argument("--disable-setuid-sandbox")
    opt.add_argument("--disable-dev-shm-usage")
    if getattr(sys, 'frozen', False):
        chromedriver_path = os.path.join(sys._MEIPASS, "C:/eedea/chromedriver.exe")
        driver = webdriver.Chrome(chromedriver_path,
        options=opt
        )
    else:
        pass
    wait = WebDriverWait(driver, 60)

    ### deff
    def wait_xpath(code):
        wait.until(ExpectedConditions.presence_of_element_located((By.XPATH, code)))

    while end_num >= start_num:
        print("Start creating NFT " + str(start_num).zfill(5))
        driver.switch_to.window(driver.window_handles[0])
        driver.get('https://www.eedea.io/create/erc1155')
        time.sleep(3)

        # Upload Function
        wait_xpath('//*[@id="app"]/div/div[2]/div/div[2]/div[1]/div/div/div/div[1]/form/div[1]/div/div[2]/div[1]/input')
        imageupload = driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[2]/div[1]/div/div/div/div[1]/form/div[1]/div/div[2]/div[1]/input')
        imagepath = os.path.abspath(file_path + "\\" + "file.mp4")
        imageupload.send_keys(imagepath)
        time.sleep(2)

        # Thumnail Upload
        thumupload = driver.find_element_by_css_selector('#app > div > div:nth-child(2) > div > div.widClass > div.collection-wrapper > div > div > div > div.collection-left > form > div:nth-child(2) > div > div.upload-pic > div.el-upload.el-upload--text > input')
        thumpath = os.path.abspath(file_path + "\\" + "cover.gif")
        thumupload.send_keys(thumpath)
        time.sleep(1)

        # Put on sale Disable
        pos = driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[2]/div[1]/div/div/div/div[1]/form/div[3]/div/div[1]/div/span')
        pos.click()
        time.sleep(1)

        # change the Token
        Token = driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[2]/div[1]/div/div/div/div[1]/form/div[4]/div/div[2]/div[3]/div/div[1]/div/img')
        Token.click()
        time.sleep(1)

        # Name
        name = driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[2]/div[1]/div/div/div/div[1]/form/div[5]/div/div[2]/input')
        name.send_keys(pname + str(start_num).zfill(5))  # Expression like 00001
        time.sleep(1)

        # Description(Optional)
        desc = driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[2]/div[1]/div/div/div/div[1]/form/div[6]/div/div[2]/textarea')
        desc.send_keys(pdesc)
        time.sleep(1)


        # Number of copies
        noc = driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[2]/div[1]/div/div/div/div[1]/form/div[7]/div/div[2]/input')
        noc.send_keys(pnoc)
        time.sleep(1)

        # Royalties
        royalties = driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[2]/div[1]/div/div/div/div[1]/form/div[9]/div/div[2]/input')
        royalties.clear()
        royalties.send_keys(roy)
        time.sleep(1)

        # Creatite Item
        create = driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[2]/div[1]/div/div/div/div[1]/form/div[11]/button')
        create.click()
        time.sleep(1)

        #Mint Button
        fmint = driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[2]/div[2]/button')
        fmint.click()
        time.sleep(2)

        #Metamask Confirm button
        driver.execute_script("window.open('');") ## Open New Tab Function
        driver.switch_to.window(driver.window_handles[1]) ## move other tab
        driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/notification.html')
        time.sleep(3)
        mconfirm = driver.find_element_by_xpath('//*[@id="app-content"]/div/div[2]/div/div[5]/div[3]/footer/button[2]')
        mconfirm.click()
        driver.close() #나중에 테스트
        time.sleep(9)

        start_num = start_num + 1
        print("등록성공")
############################################ Button Zone #############################################

open_browser = tkinter.Button(root, width=20,  text="Open Chrome Browser", command=open_chrome_profile)
open_browser.grid(row=22, column=1)
button_save = tkinter.Button(root, width=20, text="Save Form", command=save)
button_save.grid(row=23, column=1)
button_start = tkinter.Button(root, width=20, bg="green", fg="white", text="Start", command=main_program_loop)
button_start.grid(row=25, column=1)
upload_folder_input_button = tkinter.Button(root, width=20, text="Add NFTs Upload Folder", command=upload_folder_input)
upload_folder_input_button.grid(row=21, column=1)
try:
    with open(save_file_path(), "rb") as infile:
        new_dict = pickle.load(infile)
        global upload_path
        Name_change_img_folder_button(new_dict[0])
        upload_path = new_dict[0]
except FileNotFoundError:
    pass

############################################ Button Zone #############################################
root.mainloop()

