from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import os
from selenium.common.exceptions import NoSuchElementException
import user_info

SLEEP_TIME = 3 #NOTE： エラーが起きる場合、この数字をでかくしてください（その分実行時間は長くなります）


admin_url = 'https://admin-v2.en-courage.com/login'
user_mail = user_info.USER_MAIL
user_pass = user_info.USER_PASS


def access_entor_page():
    browser  = webdriver.Chrome()
    browser.get(admin_url)

    ### 場所とアクションを指定
    elem_usermail = browser.find_element(By.ID,"email")
    elem_usermail.send_keys(user_mail)

    elem_userpass = browser.find_element(By.ID,"password")
    elem_userpass.send_keys(user_pass)

    elem_login_btn = browser.find_elements(By.TAG_NAME, "button")[0]
    elem_login_btn.click()
    sleep(SLEEP_TIME) # NOTE: 数秒待機して、ページ推移の情報変化に耐える

    elements_entor_tab = browser.find_element(By.XPATH, '/html/body/div/div[2]/div[1]/div[2]/a[3]')
    elements_entor_tab.click()
    sleep(SLEEP_TIME)

    return browser


def get_25entors_list(browser, all_entors):
    all_25entors_list = []
    other_entors_list = []
    
    for target in all_entors:
        # elem_target_year = browser.find_element(By.XPATH, '/html/body/div/div[2]/div[2]/div/div[1]/div[2]/div/div[6]/div/div/div/div[2]')
        # elem_target_year.click()
        print(target)
        elem_name_searchbox = browser.find_element(By.ID, 'name')
        elem_name_searchbox.clear()
        elem_name_searchbox.send_keys(target)
        sleep(SLEEP_TIME)
        try:
            elem_entor_page = browser.find_element(By.XPATH, f'/html/body/div/div[2]/div[2]/div/div[2]/div/table/tbody/tr/td[1]/div/a')
            all_25entors_list.append(target)
            browser.back()
        except:
            other_entors_list.append(target)
        
    sleep(10)
    browser.quit()

    return all_25entors_list, other_entors_list


def main():
    import get_info_tools.access_ss as access_ss
    all_entors_list = access_ss.get_all_entors()
    
    browser = access_entor_page()
    all_25entors_list, other_entors_list = get_25entors_list(browser, all_entors_list)
    print(all_25entors_list)
    print(other_entors_list)
    
    access_ss.output_25entors_list(all_25entors_list, '25entors')
    access_ss.output_25entors_list(other_entors_list, 'other_entors')
    
    return


if __name__ == '__main__':
    main()