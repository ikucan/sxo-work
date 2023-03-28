# -*- coding: utf-8 -*-
import os
import shutil
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

#
# # get any expected config fromn env variables
#
def get_config():
    out_path = os.getenv("TOKEN_PATH", "/tmp")
    token_file = os.getenv("TOKEN_FILE", "saxo_token")
    saxo_user = os.getenv("SAXO_USER")
    saxo_pass = os.getenv("SAXO_PASS")
    if saxo_user is None:
        raise Exception("you need to pass SAXO_USER environment var")
    if saxo_pass is None:
        raise Exception("you need to pass SAXO_PASS environment var")
    if not Path(out_path).exists():
        raise Exception(f"ondfigured output path does not exist: {out_path}")
    return saxo_user, saxo_pass, f"{out_path}/{token_file}"

#
# # write a string to file
#
def wrt_str(fnm, str):
    fle = open(fnm, "w+")
    fle.writelines([str])
    fle.close()


display = None

def mk_drvr():
    usr_tmp_dir = f"/tmp/selenium_chomium_profile_dir_{123}"
    p = Path(usr_tmp_dir)
    if p.exists():
        shutil.rmtree(p)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    return webdriver.Chrome(options=chrome_options)


if __name__ == "__main__":
    saxo_user, saxo_pass, token_file = get_config()

    logon_url = "https://www.developer.saxo/accounts/signin"
    driver = mk_drvr()
    driver.get(logon_url)

    login_form = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "loginForm")))

    uid_text_box = login_form.find_element(By.ID, "field_userid")
    pass_text_box = login_form.find_element(By.ID, "field_password")
    login_button = login_form.find_element(By.ID, "button_login")
    uid_text_box.send_keys(saxo_user)
    pass_text_box.send_keys(saxo_pass)
    login_button.click()
    footer = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, "container-hero-title")))

    token_url = "https://www.developer.saxo/openapi/token"
    driver.get(token_url)
    footer = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, "cookie-popup")))
    cookie_accept_button = footer.find_element(By.TAG_NAME, "button")
    cookie_accept_button.click()

    token_form = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, "token-form")))
    token = token_form.find_element(By.CLASS_NAME, "btn--submit")
    token.click()

    token_element = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, "code--flow")))
    token_txt = token_element.text

    print()
    print("----------------------")
    print("--- got 24hr token ---")
    print(token_txt)

    fout = open(token_file, "w")
    fout.write(token_txt)
    fout.close()
    print("----------------------")
    print(f"--- written to file :{token_file}")
    print("----------------------")
    print()
