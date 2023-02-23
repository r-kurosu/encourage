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


def get_entor_list_by_conditions(browser):
    # 条件設定
    elem_target_year = browser.find_element(By.XPATH, '/html/body/div/div[2]/div[2]/div/div[1]/div[2]/div/div[6]/div/div/div/div[2]')
    elem_target_year.click()
    elem_status = browser.find_element(By.XPATH, '/html/body/div/div[2]/div[2]/div/div[1]/div[2]/div/div[6]/div/div/div[2]/ul/li[4]')
    elem_status.click()
    elem_interview_status = browser.find_element(By.XPATH, '/html/body/div/div[2]/div[2]/div/div[1]/div[2]/div/div[8]/div/div/div[1]/div[2]')
    elem_interview_status.click()
    elem_status = browser.find_element(By.XPATH, '/html/body/div/div[2]/div[2]/div/div[1]/div[2]/div/div[8]/div/div/div[2]/ul/li[3]')
    elem_status.click()
    sleep(SLEEP_TIME)

    is_entor_list = True
    entor_count = 0
    mail_list = []
    while is_entor_list:
        entor_count += 1
        try:
            elements_entor_page = browser.find_element(By.XPATH, f'/html/body/div/div[2]/div[2]/div/div[2]/div/table/tbody/tr[{entor_count}]/td[1]/div/a')
        except NoSuchElementException:
            elements_entor_page = browser.find_element(By.XPATH, f'/html/body/div/div[2]/div[2]/div/div[2]/div/table/tbody/tr[{entor_count-1}]/td[1]/div/a')
            
            sleep(SLEEP_TIME*2)
            try:
                elements_entor_page = browser.find_element(By.XPATH, f'/html/body/div/div[2]/div[2]/div/div[2]/div/table/tbody/tr[{entor_count}]/td[1]/div/a')
            except NoSuchElementException:
                is_entor_list = False
                break
        
        elements_entor_page.click()
        sleep(SLEEP_TIME)
        
        elem_entor_mail = browser.find_element(By.XPATH, '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div[1]/div[2]/div[8]')
        entor_mail = elem_entor_mail.text
        print(entor_mail)
        mail_list.append(entor_mail)
        browser.back()
        sleep(SLEEP_TIME)

    print(mail_list)

    sleep(10)
    browser.quit()

    return mail_list


def get_entor_list_by_list(browser, target_list):
    mail_list = []
    
    for target in target_list:
        elem_name_searchbox = browser.find_element(By.ID, 'name')
        elem_name_searchbox.clear()
        elem_name_searchbox.send_keys(target)
        sleep(SLEEP_TIME)
        try:
            elem_entor_page = browser.find_element(By.XPATH, f'/html/body/div/div[2]/div[2]/div/div[2]/div/table/tbody/tr/td[1]/div/a')
            elem_entor_page.click()
            sleep(SLEEP_TIME)
            elem_entor_mail = browser.find_element(By.XPATH, '/html/body/div/div[2]/div[2]/div/div[2]/div[2]/div[1]/div[2]/div[8]')
            entor_mail = elem_entor_mail.text
            mail_list.append([target, entor_mail])
            browser.back()
            sleep(SLEEP_TIME)
        except:
            continue
        
    sleep(10)
    browser.quit()

    return mail_list


def main():
    import get_info_tools.access_ss as access_ss
    no_apply_list = access_ss.get_no_apply_entors()
    
    browser = access_entor_page()
    mail_list = get_entor_list_by_list(browser, no_apply_list)
    print(mail_list)
    
    access_ss.output_mail_list(mail_list)
    
    
    return


if __name__ == '__main__':
    main()
    
    