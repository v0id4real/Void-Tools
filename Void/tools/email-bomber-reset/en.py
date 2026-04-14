from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
from colorama import init, Fore

init(autoreset=True)
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--no-sandbox")
Email = input(Fore.RED + '[?] Which email address would you like spam? ')

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.amazon.fr/ap/forgotpassword?showRememberMe=true&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&language=fr_FR&pageId=amzn_noticeform_desktop_fr&openid.return_to=https%3A%2F%2Fwww.amazon.fr%2Freport%2Finfringement%2Fretract&prevRID=E3MEXYCQM15PS0Q6JMC6&openid.assoc_handle=amzn_noticeform_desktop_fr&openid.mode=checkid_setup&prepopulatedLoginId=&failedSignInCount=0&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0")
try:
    box = driver.find_element(By.ID, "ap_email")
    box.clear()
    box.send_keys(Email)
    driver.find_element(By.ID, "continue").click()
    try:
        driver.find_element(By.ID, "cvf-input-code")
        print(Fore.GREEN + "{+} Email address registered on Amazon")
    except NoSuchElementException:
        print(Fore.RED + "{-} Email address not registered on Amazon")
except Exception as ex:
    print(Fore.RED + "{-} Email address not registered on Amazon")
time.sleep(2)

driver.get("https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=152&ct=1716121223&rver=7.3.6960.0&wp=MBI_SSL&wreply=https%3a%2f%2fwww.microsoft.com%2frpsauth%2fv1%2faccount%2fSignInCallback%3fstate%3deyJSdSI6Imh0dHBzOi8vd3d3Lm1pY3Jvc29mdC5jb20vZnItZnIvP2xjPTEwMzYiLCJMYyI6IjEwMzYiLCJIb3N0Ijoid3d3Lm1pY3Jvc29mdC5jb20ifQ&lc=1036&id=74335&aadredir=0")
try:
    box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'i0116')))
    box.clear()
    box.send_keys(Email)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "idSIButton9"))).click()
    time.sleep(2)
    try:
        driver.find_element(By.ID, "idTxtBx_OTC_Password")
        print(Fore.GREEN + "{+} Email address registered on Microsoft")
    except NoSuchElementException:
        print(Fore.RED + "{-} Email address not registered on Microsoft")
except Exception as ex:
    print(Fore.RED + "{-} An error occurred while connecting to Microsoft:", ex)

driver.get("https://secure.lemonde.fr/sfuser/password/lost")
try:
    box = driver.find_element(By.ID, 'email')
    box.clear()
    box.send_keys(Email)
    driver.find_element(By.XPATH, '//*[@id="reset-password"]/main/form/input').click()
    time.sleep(2)
    try:
        driver.find_element(By.XPATH, '//*[@id="reset-password"]/main/div/div/p[1]/b')
        print(Fore.GREEN + "{+} Email address registered on LeMonde")
    except NoSuchElementException:
        print(Fore.RED + "{-} Email address not registered on LeMonde")
except Exception as ex:
    print(Fore.RED + "{-} Email address not registered on LeMonde")

driver.get("https://www.netflix.com/fr/LoginHelp")
time.sleep(3)
try:
    box = driver.find_element(By.ID, 'forgot_password_input')
    box.clear()
    box.send_keys(Email)
    driver.find_element(By.XPATH, '//*[@id="appMountPoint"]/div/div[3]/div[1]/div/button').click()
    time.sleep(2)
    try:
        driver.find_element(By.XPATH, '//*[@id="appMountPoint"]/div/div[3]/div[1]/div/h2')
        print(Fore.GREEN + "{+} Email address registered on Netflix")
    except NoSuchElementException:
        print(Fore.RED + "{-} Email address not registered on Netflix")
except Exception as ex:
    print(Fore.RED + "{-} Email address not registered on Netflix")

driver.get("https://www.paypal.com/authflow/password-recovery/?country.x=FR&locale.x=fr_FR&redirectUri=%252Fsignin")
time.sleep(2)
try:
    box = driver.find_element(By.ID, 'pwrStartPageEmail')
    box.clear()
    box.send_keys(Email)
    driver.find_element(By.XPATH, '//*[@id="pwrStartPageSubmit"]/span').click()
    time.sleep(2)
    try:
        driver.find_element(By.XPATH, '//*[@id="challenge-heading"]')
        print(Fore.GREEN + "{+} Email address registered on PayPal")
    except NoSuchElementException:
        print(Fore.RED + "{-} Email address not registered on PayPal")
except Exception as ex:
    print(Fore.RED + "{-} Email address not registered on PayPal")

driver.get("https://fr.pornhub.com/signup")
time.sleep(2)


try:
    box = driver.find_element(By.XPATH, '//*[@id="modalWrapMTubes"]/div/div/button').click()
    time.sleep(1)
    box = driver.find_element(By.XPATH, '//*[@id="cookieBannerWrapper"]/button[2]').click()
    time.sleep(1)
    box = driver.find_element(By.XPATH, '//*[@id="createEmail"]')
    box.send_keys(Email)
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'errors')))
    error_element = driver.find_element(By.ID, 'errors')
    if "E-mail déjà pris." in error_element.text:
        print(Fore.GREEN + "{+} Email address already registered on Pornhub")
    else:
        print(Fore.RED + "{-} Email address not registered on Pornhub")
except NoSuchElementException: 
    print(Fore.RED + "{-} Email address not registered on Pornhub") 
    
finally:
    driver.quit()