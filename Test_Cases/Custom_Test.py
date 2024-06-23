# -*- coding: utf-8 -*-
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
import os
import platform
from colorama import Fore, Back, Style
from func_timeout import func_set_timeout
import func_timeout
from pyvirtualdisplay import Display
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

in_debug = True
EXECUTION_TIME = 60
test_path = "/root/"
arcanum_executable_path = test_path + 'arcanum/opt/chromium.org/chromium-unstable/chromium-browser-unstable'
if in_debug:
    # arcanum_executable_path = "/mnt/run/chromium/src/out/Default/chrome"
    # arcanum_executable_path = '/root/Outlook/opt/chromium.org/chromium-unstable/chromium-browser-unstable'
    arcanum_executable_path = '/root/real/opt/chromium.org/chromium-unstable/chromium-browser-unstable'

chromedriver_path = test_path + 'chromedriver/chromedriver'
user_data_path = '/root/userdata/'
log_path = test_path+'logs/'
os.environ["CHROME_LOG_FILE"] = log_path+'chromium.log'
wpr_path = '/root/go/pkg/mod/github.com/catapult-project/catapult/web_page_replay_go@v0.0.0-20230901234838-f16ca3c78e46/'

mount_custom_extension_dir = '/mnt/run/Arcanum/Sample_Extensions/Custom/'
custom_extension_dir = '/root/extensions/custom/'
recording_dir = '/root/recordings/'
annotation_dir = '/root/annotations/'
v8_log_path = '/ram/analysis/v8logs/'

url_mp = {
    'amazon_address': 'https://www.amazon.com/a/addresses',
    'fb_post':'https://www.facebook.com/profile.php?id=100084859195049',
    'gmail_inbox': 'https://mail.google.com/mail/u/0/#inbox',
    'ins_profile':'https://www.instagram.com/xqgtiti/',
    'linkedin_profile':'https://www.linkedin.com/in/amy-lee-gt/',
    'outlook_inbox': 'https://outlook.live.com/mail/0/',
    'paypal_card': 'https://www.paypal.com/myaccount/money/cards/CC-DNGXYXA3SUS8Q',
}

rules_map = {
    'amazon_address': "MAP *.amazon.com:80 127.0.0.1:8080,MAP *.amazon.com:443 127.0.0.1:8081,MAP *.media-amazon.com:80 127.0.0.1:8080,MAP *.media-amazon.com:443 127.0.0.1:8081,MAP *.amazon-adsystem.com:80 127.0.0.1:8080,MAP *.amazon-adsystem.com:443 127.0.0.1:8081,MAP *.ssl-images-amazon.com:80 127.0.0.1:8080,MAP *.ssl-images-amazon.com:443 127.0.0.1:8081,MAP *.cloudfront.net:80 127.0.0.1:8080,MAP *.cloudfront.net:443 127.0.0.1:8081,EXCLUDE localhost",
    'fb_post': "MAP *.facebook.com:80 127.0.0.1:8080,MAP *.facebook.com:443 127.0.0.1:8081,MAP *.fbcdn.net:80 127.0.0.1:8080,MAP *.fbcdn.net:443 127.0.0.1:8081,MAP *.fb.com:80 127.0.0.1:8080,MAP *.fb.com:443 127.0.0.1:8081,EXCLUDE localhost",
    'gmail_inbox': "MAP *.google.com:80 127.0.0.1:8080,MAP *.google.com:443 127.0.0.1:8081,MAP *.gstatic.com:80 127.0.0.1:8080,MAP *.gstatic.com:443 127.0.0.1:8081,MAP *.googleusercontent.com:80 127.0.0.1:8080,MAP *.googleusercontent.com:443 127.0.0.1:8081,EXCLUDE localhost",
    'ins_profile': "MAP *.instagram.com:80 127.0.0.1:8080,MAP *.instagram.com:443 127.0.0.1:8081,MAP *.cdninstagram.com:80 127.0.0.1:8080,MAP *.cdninstagram.com:443 127.0.0.1:8081,MAP *.fbcdn.net:80 127.0.0.1:8080,MAP *.fbcdn.net:443 127.0.0.1:8081,MAP *.facebook.com:80 127.0.0.1:8080,MAP *.facebook.com:443 127.0.0.1:8081,EXCLUDE localhost",
    'linkedin_profile': "MAP *.linkedin.com:80 127.0.0.1:8080,MAP *.linkedin.com:443 127.0.0.1:8081,MAP *.licdn.com:80 127.0.0.1:8080,MAP *.licdn.com:443 127.0.0.1:8081,EXCLUDE localhost",
    'outlook_inbox': "MAP *.office.com:80 127.0.0.1:8080,MAP *.office.com:443 127.0.0.1:8081,MAP *.office.net:80 127.0.0.1:8080,MAP *.office.net:443 127.0.0.1:8081,MAP *.live.com:80 127.0.0.1:8080,MAP *.live.com:443 127.0.0.1:8081,EXCLUDE localhost",
    'paypal_card':"MAP *.paypal.com:80 127.0.0.1:8080,MAP *.paypal.com:443 127.0.0.1:8081,MAP *.paypalobjects.com:80 127.0.0.1:8080,MAP *.paypalobjects.com:443 127.0.0.1:8081,MAP *.recaptcha.net:80 127.0.0.1:8080,MAP *.recaptcha.net:443 127.0.0.1:8081,MAP *.qualtrics.com:80 127.0.0.1:8080,MAP *.qualtrics.com:443 127.0.0.1:8081,MAP *.gstatic.com:80 127.0.0.1:8080,MAP *.gstatic.com:443 127.0.0.1:8081,EXCLUDE localhost"
}

def input_sink_logs(category):
    file_path = ''
    if (category == 'storage'):
        file_path = v8_log_path + 'taint_storage.log'
    else:
        file_path = user_data_path + 'taint_%s.log'%category
    f = open(file_path,'r',encoding='utf-8', errors='ignore')
    r = f.read()
    f.close()
    return r

def input_source_logs():
    f = open(v8_log_path + 'taint_sources.log', 'r',encoding='utf-8', errors='ignore')
    r = f.read()
    f.close()
    return r

def deinit(extension_name):
    print('=============== Finish Test ===============\n')
    os.system('pkill Xvfb')
    os.system('pkill chrome')
    os.system('pkill chromedriver')
    os.system('pkill wpr')

    # Recover transformers.go
    # Although still use transformers_for_gmail_inbox.go is fine.
    if 'gmail_' in extension_name:
        os.chdir(wpr_path + "src/webpagereplay/")
        os.system('cp transformers.go_backup transformers.go')

def init(extension_name):
    if os.path.exists(custom_extension_dir) == False:
        os.system('mkdir -p %s'%custom_extension_dir)
    if os.path.exists(recording_dir) == False:
        os.system('mkdir -p %s'%recording_dir)
    if os.path.exists(annotation_dir) == False:
        os.system('mkdir -p %s'%annotation_dir)

    print('=============== Start Testing the Custom Extension: %s ==============='%extension_name)
    os.system('pkill Xvfb')
    os.system('pkill chrome')
    os.system('pkill chromedriver')
    os.system('pkill wpr')

    # Delete old user data dir
    os.system('rm -rf %s'%user_data_path)
    # Clean old logs
    os.system('rm -rf %s/*'%v8_log_path)

    display = Display(visible=0, size=(1920, 1080))
    display.start()

    # Add nonce in the recording, replace transformers.go with our modified version
    if 'gmail_' in extension_name:
        os.chdir(wpr_path+"src/webpagereplay/")
        os.system('cp transformers_for_gmail_inbox.go transformers.go')


@func_set_timeout(20)
def launch_driver(load_extension, extension_name, recording_name = None, rules = None, annotation_name = None,
                  idle_timeout_ms = None, delay_animation_ms = None):

    if os.path.exists(arcanum_executable_path) == False:
        print(Fore.RED + "Error: Given Arcanum executable path [%s] does not exist. "%arcanum_executable_path + Fore.RESET)
        exit(0)

    if os.path.exists(chromedriver_path) == False:
        print(Fore.RED + "Error: Given chromedriver path [%s] does not exist. "%chromedriver_path + Fore.RESET)
        exit(0)

    service = Service(executable_path=chromedriver_path)
    options = webdriver.ChromeOptions()
    options.binary_location = arcanum_executable_path
    options.add_argument('--user-data-dir=%s' % user_data_path)
    options.add_argument("--enable-logging")
    options.add_argument("--v=0")
    options.add_argument('--verbose')
    options.add_argument('--log-path="%s"'%log_path)
    options.add_argument('--net-log-capture-mode=IncludeCookiesAndCredentials')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')

    if load_extension:
        extension_path = custom_extension_dir + extension_name
        if extension_name.endswith('.crx'): # Crx file
            options.add_extension(extension_path)
        else: # Unpack Extension
            options.add_argument('--load-extension={}'.format(extension_path))

    if idle_timeout_ms != None:
        options.add_argument('--custom-script-idle-timeout-ms=%d' % idle_timeout_ms)
    if delay_animation_ms != None:
        options.add_argument('--custom-delay-for-animation-ms=%d' % idle_timeout_ms)

    if recording_name != None:
        os.chdir(wpr_path)
        options.add_argument('--host-resolver-rules=%s' % rules)
        run_wprgo = ''
        if annotation_name != None:
            run_wprgo = 'nohup /usr/local/go/bin/go run src/wpr.go replay --http_port=8080 --https_port=8081 --inject_scripts=deterministic.js,%s %s > %swprgo.log 2>&1 &'%(annotation_dir+annotation_name,recording_dir+recording_name,log_path)
        else:
            run_wprgo = 'nohup /usr/local/go/bin/go run src/wpr.go replay --http_port=8080 --https_port=8081 %s > %swprgo.log 2>&1 &'%(recording_dir+recording_name,log_path)
        os.system(run_wprgo)

    prefs = {"profile.default_content_setting_values.notifications": 2}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(600)

    return driver

def check_file_exist(extension_name, recording_name, annotation_name):
    if extension_name != None and os.path.exists(custom_extension_dir + extension_name) == False:
        print(Fore.RED+"Error: Test extension [%s] does not exist. Download it from the GitHub repo first."%extension_name + Fore.RESET)
        exit(0)

    if recording_name != None and os.path.exists(recording_dir + recording_name) == False:
        print(Fore.RED+"Error: The required recording file [%s] does not exist. Download it from our GitHub repo first." % recording_name + Fore.RESET )
        exit(0)

    if annotation_name != None and os.path.exists(annotation_dir + annotation_name) == False:
        print(Fore.RED + "Error: The required annotation file [%s] does not exist. Download it from our GitHub repo first." % annotation_name + Fore.RESET)
        exit(0)

def Amazon_Extension_MV2_Test():

    target_page = 'amazon_address'
    test_URL = url_mp[target_page]
    extension_name = '%s_mv2.crx'%target_page
    recording_name = '%s.wprgo'%target_page
    annotation_name = '%s.js'%target_page
    rules = rules_map[target_page]
    success_output = 'Custom Extension %s: '%extension_name + Back.GREEN + "Success" + Back.RESET + "."
    fail_output = 'Custom Extension %s: '%extension_name + Fore.RED + "Fail" + Fore.RESET + "."

    check_file_exist(extension_name = extension_name, recording_name = recording_name, annotation_name = annotation_name)

    init(extension_name)

    try:
        driver = launch_driver(load_extension = True, extension_name = extension_name,
                               recording_name = recording_name, rules = rules, annotation_name = annotation_name,
                               idle_timeout_ms=2000)
        print('Launch Arcanum success. Arcanum starts running.')
        time.sleep(1)
        driver.get(test_URL)
        ui = ''
        try:
            time.sleep(2)
            ui = driver.find_element(By.ID, "a-page")
        finally:
            innerhtml = ui.get_attribute('innerHTML')
            tainted_element_num = innerhtml.count('data-taint')
            if (tainted_element_num):
                print('Inject annotation success: There are %d tainted DOM elements on the page. (Expected to be 6)'%tainted_element_num)
        print('Execute the extension for 60s after the web page has completely loaded, waiting now...')
        time.sleep(EXECUTION_TIME)
        driver.quit()
    except Exception as e:
        print(e)
        print(fail_output)
        return

    print('End running Arcanum. Start checking taint logs. ')
    # Check the extension source to see why we should get the storage sink and XMLHttpRequest sink.
    if os.path.exists(v8_log_path + 'taint_sources.log') and \
            os.path.exists(v8_log_path + 'taint_storage.log') and \
            os.path.exists(user_data_path + 'taint_xhr.log'):
        source_content = input_source_logs()
        storage_content = input_sink_logs('storage')
        xhr_content = input_sink_logs('xhr')
        # You can check the content detail in taint logs, here for test we just check some key values of each log.
        if ('startErin Lee' in source_content and 'delivery instructions_end' in source_content)  \
                and 'startErin Lee' in storage_content and \
                ('xml-send-body-ArrayBuffer' in xhr_content and '<ArrayBuffer map' in xhr_content):
            print(success_output)
        else:
            print(fail_output + " Expected content not in the taint logs")
    else:
        print(fail_output + " Expected taint log file not found. ")

    deinit(extension_name)

def Amazon_Extension_MV3_Test():

    target_page = 'amazon_address'
    test_URL = url_mp[target_page]
    extension_name = '%s_mv3.crx'%target_page
    recording_name = '%s.wprgo'%target_page
    annotation_name = '%s.js'%target_page
    rules = rules_map[target_page]
    success_output = 'Custom Extension %s: '%extension_name + Back.GREEN + "Success" + Back.RESET + "."
    fail_output = 'Custom Extension %s: '%extension_name + Fore.RED + "Fail" + Fore.RESET + "."

    check_file_exist(extension_name = extension_name, recording_name = recording_name, annotation_name = annotation_name)

    init(extension_name)

    try:
        driver = launch_driver(load_extension = True, extension_name = extension_name,
                               recording_name = recording_name, rules = rules, annotation_name = annotation_name,
                               idle_timeout_ms=2000)
        print('Launch Arcanum success. Arcanum starts running.')
        time.sleep(1)
        driver.get(test_URL)
        ui = ''
        try:
            time.sleep(2)
            ui = driver.find_element(By.ID, "a-page")
        finally:
            innerhtml = ui.get_attribute('innerHTML')
            tainted_element_num = innerhtml.count('data-taint')
            if (tainted_element_num):
                print('Inject annotation success: There are %d tainted DOM elements on the page. (Expected to be 6)'%tainted_element_num)
        print('Execute the extension for 60s after the web page has completely loaded, waiting now...')
        time.sleep(EXECUTION_TIME)
        driver.quit()
    except Exception as e:
        print(e)
        print(fail_output)
        return

    print('End running Arcanum. Start checking taint logs. ')
    # Check the extension source to see why we should get the fetch sink.
    if os.path.exists(v8_log_path + 'taint_sources.log') \
            and os.path.exists(user_data_path + 'taint_fetch.log'):
        source_content = input_source_logs()
        fetch_content = input_sink_logs('fetch')
        # You can check the content detail in taint logs, here for test we just check some key values of each log.
        if ('JACKSONVILLE, AL 36265-2402' in source_content and 'United States' in source_content) \
                and ('Erin Lee' in fetch_content and 'JACKSONVILLE, AL' in fetch_content):
            print(success_output)
        else:
            print(fail_output + " Expected content not in the taint logs")
    else:
        print(fail_output + " Expected taint log file not found. ")

    deinit(extension_name)

def Facebook_Extension_MV2_Test():

    target_page = 'fb_post'
    test_URL = url_mp[target_page]
    extension_name = '%s_mv2.crx'%target_page
    recording_name = '%s.wprgo'%target_page
    annotation_name = '%s.js'%target_page
    rules = rules_map[target_page]
    success_output = 'Custom Extension %s: '%extension_name + Back.GREEN + "Success" + Back.RESET + "."
    fail_output = 'Custom Extension %s: '%extension_name + Fore.RED + "Fail" + Fore.RESET + "."

    check_file_exist(extension_name = extension_name, recording_name = recording_name, annotation_name = annotation_name)

    init(extension_name)

    try:
        driver = launch_driver(load_extension = True, extension_name = extension_name,
                               recording_name = recording_name, rules = rules, annotation_name = annotation_name,
                               idle_timeout_ms=12000)
        print('Launch Arcanum success. Arcanum starts running.')
        time.sleep(1)
        driver.get(test_URL)
        ui = ''
        try:
            ui = WebDriverWait(driver, 40).until(
                EC.visibility_of_element_located((By.ID, "mount_0_0_LC")))
        finally:
            innerhtml = ui.get_attribute('innerHTML')
            tainted_element_num = innerhtml.count('data-taint')
            if (tainted_element_num):
                print('Inject annotation success: There are %d tainted DOM elements on the page. (Expected to be 11)'%tainted_element_num)
        print('Execute the extension for 60s after the web page has completely loaded, waiting now...')
        time.sleep(EXECUTION_TIME)
        driver.quit()
    except Exception as e:
        print(e)
        print(fail_output)
        return

    print('End running Arcanum. Start checking taint logs. ')
    # Check the extension source to see why we should get the storage sink and XMLHttpRequest sink.
    if os.path.exists(v8_log_path + 'taint_sources.log') \
            and os.path.exists(v8_log_path + 'taint_storage.log') \
            and os.path.exists(user_data_path + 'taint_xhr.log'):
        source_content = input_source_logs()
        storage_content = input_sink_logs('storage')
        xhr_content = input_sink_logs('xhr')
        # You can check the content detail in taint logs, here for test we just check some key values of each log.
        if 'High School Reunion' in source_content and \
                'startHigh School Reunion_end' in storage_content and \
                ('xml-send-body-ArrayBuffer' in xhr_content and '<ArrayBuffer map' in xhr_content):
            print(success_output)
        else:
            print(fail_output + " Expected content not in the taint logs")
    else:
        print(fail_output + " Expected taint log file not found. ")

    deinit(extension_name)

def Facebook_Extension_MV3_Test():

    target_page = 'fb_post'
    test_URL = url_mp[target_page]
    extension_name = '%s_mv3.crx'%target_page
    recording_name = '%s.wprgo'%target_page
    annotation_name = '%s.js'%target_page
    rules = rules_map[target_page]
    success_output = 'Custom Extension %s: '%extension_name + Back.GREEN + "Success" + Back.RESET + "."
    fail_output = 'Custom Extension %s: '%extension_name + Fore.RED + "Fail" + Fore.RESET + "."

    check_file_exist(extension_name = extension_name, recording_name = recording_name, annotation_name = annotation_name)

    init(extension_name)

    try:
        driver = launch_driver(load_extension = True, extension_name = extension_name,
                               recording_name = recording_name, rules = rules, annotation_name = annotation_name,
                               idle_timeout_ms=12000)
        print('Launch Arcanum success. Arcanum starts running.')
        time.sleep(1)
        driver.get(test_URL)
        ui = ''
        try:
            ui = WebDriverWait(driver, 40).until(
                EC.visibility_of_element_located((By.ID, "mount_0_0_LC")))
        finally:
            innerhtml = ui.get_attribute('innerHTML')
            tainted_element_num = innerhtml.count('data-taint')
            if (tainted_element_num):
                print('Inject annotation success: There are %d tainted DOM elements on the page. (Expected to be 11)'%tainted_element_num)
        print('Execute the extension for 60s after the web page has completely loaded, waiting now...')
        time.sleep(EXECUTION_TIME)
        driver.quit()
    except Exception as e:
        print(e)
        print(fail_output)
        return

    print('End running Arcanum. Start checking taint logs. ')
    # Check the extension source to see why we should get the storage sink and XMLHttpRequest sink.
    if os.path.exists(v8_log_path + 'taint_sources.log') \
            and os.path.exists(user_data_path + 'taint_fetch.log'):
        source_content = input_source_logs()
        fetch_content = input_sink_logs('fetch')
        # You can check the content detail in taint logs, here for test we just check some key values of each log.
        if 'Amy Lee' in source_content and \
                '2 friends' in fetch_content:
            print(success_output)
        else:
            print(fail_output + " Expected content not in the taint logs")
    else:
        print(fail_output + " Expected taint log file not found. ")

    deinit(extension_name)

def Gmail_Extension_MV2_Test():

    target_page = 'gmail_inbox'
    test_URL = url_mp[target_page]
    extension_name = '%s_mv2.crx'%target_page
    recording_name = '%s.wprgo'%target_page
    annotation_name = '%s.js'%target_page
    rules = rules_map[target_page]
    success_output = 'Custom Extension %s: '%extension_name + Back.GREEN + "Success" + Back.RESET + "."
    fail_output = 'Custom Extension %s: '%extension_name + Fore.RED + "Fail" + Fore.RESET + "."

    check_file_exist(extension_name = extension_name, recording_name = recording_name, annotation_name = annotation_name)

    init(extension_name)

    try:
        driver = launch_driver(load_extension = True, extension_name = extension_name,
                               recording_name = recording_name, rules = rules, annotation_name = annotation_name,
                               idle_timeout_ms=25000)
        print('Launch Arcanum success. Arcanum starts running.')
        time.sleep(1)
        driver.get(test_URL)
        ui = ''
        try:
            ui = WebDriverWait(driver, 40).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "nH")))
        finally:
            innerhtml = ui.get_attribute('innerHTML')
            tainted_element_num = innerhtml.count('data-taint')
            if (tainted_element_num):
                print('Inject annotation success: There are %d tainted DOM elements on the page. (Expected to be 3-5, mutate case)'%tainted_element_num)
        print('Execute the extension for 60s after the web page has completely loaded, waiting now...')
        time.sleep(EXECUTION_TIME)

        driver.quit()
    except Exception as e:
        print(e)
        print(fail_output)
        return

    print('End running Arcanum. Start checking taint logs. ')
    # Check the extension source to see why we should get the storage sink and XMLHttpRequest sink.
    if os.path.exists(v8_log_path + 'taint_sources.log') \
            and os.path.exists(v8_log_path + 'taint_storage.log') \
            and os.path.exists(user_data_path + 'taint_xhr.log'):
        source_content = input_source_logs()
        storage_content = input_sink_logs('storage')
        xhr_content = input_sink_logs('xhr')
        # You can check the content detail in taint logs, here for test we just check some key values of each log.
        if 'Payment declined: Update your information so we can ship your order' in source_content and \
                'Hello Amy, We are having trouble authorizing your payment' in storage_content and \
                ('xml-send-body-ArrayBuffer' in xhr_content and 'Please verify or update your payment method' in xhr_content):
            print(success_output)
        else:
            print(fail_output + " Expected content not in the taint logs")
    else:
        print(fail_output + " Expected taint log file not found. ")

    deinit(extension_name)

def Gmail_Extension_MV3_Test():

    target_page = 'gmail_inbox'
    test_URL = url_mp[target_page]
    extension_name = '%s_mv3.crx'%target_page
    recording_name = '%s.wprgo'%target_page
    annotation_name = '%s.js'%target_page
    rules = rules_map[target_page]
    success_output = 'Custom Extension %s: '%extension_name + Back.GREEN + "Success" + Back.RESET + "."
    fail_output = 'Custom Extension %s: '%extension_name + Fore.RED + "Fail" + Fore.RESET + "."

    check_file_exist(extension_name = extension_name, recording_name = recording_name, annotation_name = annotation_name)

    init(extension_name)

    try:
        driver = launch_driver(load_extension = True, extension_name = extension_name,
                               recording_name = recording_name, rules = rules, annotation_name = annotation_name,
                               idle_timeout_ms=25000)
        print('Launch Arcanum success. Arcanum starts running.')
        time.sleep(1)
        driver.get(test_URL)
        ui = ''
        try:
            ui = WebDriverWait(driver, 40).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "nH")))
        finally:
            innerhtml = ui.get_attribute('innerHTML')
            tainted_element_num = innerhtml.count('data-taint')
            if (tainted_element_num):
                print('Inject annotation success: There are %d tainted DOM elements on the page. (Expected to be 3-5, mutate case)'%tainted_element_num)
        print('Execute the extension for 60s after the web page has completely loaded, waiting now...')
        time.sleep(EXECUTION_TIME)
        driver.quit()
    except Exception as e:
        print(e)
        print(fail_output)
        return

    print('End running Arcanum. Start checking taint logs. ')
    # Check the extension source to see why we should get the fetch sink.
    if os.path.exists(v8_log_path + 'taint_sources.log') \
            and os.path.exists(user_data_path + 'taint_fetch.log'):
        source_content = input_source_logs()
        fetch_content = input_sink_logs('fetch')
        # You can check the content detail in taint logs, here for test we just check some key values of each log.
        if ('Jack Ma' in source_content and 'One off event' in source_content) \
              and ('"str1":"U.S. Department of Educati.' in fetch_content):
            print(success_output)
        else:
            print(fail_output + " Expected content not in the taint logs")
    else:
        print(fail_output + " Expected taint log file not found. ")

    deinit(extension_name)

def Ins_Extension_MV2_Test():

    target_page = 'ins_profile'
    test_URL = url_mp[target_page]
    extension_name = '%s_mv2.crx'%target_page
    recording_name = '%s.wprgo'%target_page
    annotation_name = '%s.js'%target_page
    rules = rules_map[target_page]
    success_output = 'Custom Extension %s: '%extension_name + Back.GREEN + "Success" + Back.RESET + "."
    fail_output = 'Custom Extension %s: '%extension_name + Fore.RED + "Fail" + Fore.RESET + "."

    check_file_exist(extension_name = extension_name, recording_name = recording_name, annotation_name = annotation_name)

    init(extension_name)

    try:
        driver = launch_driver(load_extension = True, extension_name = extension_name,
                               recording_name = recording_name, rules = rules, annotation_name = annotation_name,
                               idle_timeout_ms=20000, delay_animation_ms=20000)
        print('Launch Arcanum success. Arcanum starts running.')
        time.sleep(1)
        driver.get(test_URL)
        ui = ''
        try:
            # wait after the animation
            time.sleep(10)
            ui = WebDriverWait(driver, 40).until(
                EC.visibility_of_element_located((By.ID, "mount_0_0_tc")))
        finally:
            innerhtml = ui.get_attribute('innerHTML')
            tainted_element_num = innerhtml.count('data-taint')
            if (tainted_element_num):
                print('Inject annotation success: There are %d tainted DOM elements on the page. (Expected to be 3)'%tainted_element_num)
        print('Execute the extension for 60s after the web page has completely loaded, waiting now...')
        time.sleep(EXECUTION_TIME)
        driver.quit()
    except Exception as e:
        print(e)
        print(fail_output)
        return

    print('End running Arcanum. Start checking taint logs. ')
    # Check the extension source to see why we should get the storage sink and XMLHttpRequest sink.
    if os.path.exists(v8_log_path + 'taint_sources.log') \
            and os.path.exists(v8_log_path + 'taint_storage.log') \
            and os.path.exists(user_data_path + 'taint_xhr.log'):
        source_content = input_source_logs()
        storage_content = input_sink_logs('storage')
        xhr_content = input_sink_logs('xhr')
        # You can check the content detail in taint logs, here for test we just check some key values of each log.
        if 'This is me!!!!' in source_content and \
                'Photo by Erin in The Collective Food Hall at Coda with @cristiano' in storage_content and \
                ('xml-send-body-ArrayBuffer' in xhr_content and '<ArrayBuffer map' in xhr_content):
            print(success_output)
        else:
            print(fail_output + " Expected content not in the taint logs")
    else:
        print(fail_output + " Expected taint log file not found. ")

    deinit(extension_name)

def Ins_Extension_MV3_Test():

    target_page = 'ins_profile'
    test_URL = url_mp[target_page]
    extension_name = '%s_mv3.crx'%target_page
    recording_name = '%s.wprgo'%target_page
    annotation_name = '%s.js'%target_page
    rules = rules_map[target_page]
    success_output = 'Custom Extension %s: '%extension_name + Back.GREEN + "Success" + Back.RESET + "."
    fail_output = 'Custom Extension %s: '%extension_name + Fore.RED + "Fail" + Fore.RESET + "."

    check_file_exist(extension_name = extension_name, recording_name = recording_name, annotation_name = annotation_name)

    init(extension_name)

    try:
        driver = launch_driver(load_extension = True, extension_name = extension_name,
                               recording_name = recording_name, rules = rules, annotation_name = annotation_name,
                               idle_timeout_ms=20000, delay_animation_ms=20000)
        print('Launch Arcanum success. Arcanum starts running.')
        time.sleep(1)
        driver.get(test_URL)
        ui = ''
        try:
            # wait after the animation
            time.sleep(10)
            ui = WebDriverWait(driver, 40).until(
                EC.visibility_of_element_located((By.ID, "mount_0_0_tc")))
        finally:
            innerhtml = ui.get_attribute('innerHTML')
            tainted_element_num = innerhtml.count('data-taint')
            if (tainted_element_num):
                print('Inject annotation success: There are %d tainted DOM elements on the page. (Expected to be 3)'%tainted_element_num)
        print('Execute the extension for 60s after the web page has completely loaded, waiting now...')
        time.sleep(EXECUTION_TIME)
        driver.quit()
    except Exception as e:
        print(e)
        print(fail_output)
        return

    print('End running Arcanum. Start checking taint logs. ')
    # Check the extension source to see why we should get the storage sink and XMLHttpRequest sink.
    if os.path.exists(v8_log_path + 'taint_sources.log') \
            and os.path.exists(user_data_path + 'taint_fetch.log'):
        source_content = input_source_logs()
        fetch_content = input_sink_logs('fetch')
        # You can check the content detail in taint logs, here for test we just check some key values of each log.
        if 'Erin' in source_content and \
                'Jul 1, 2023 678 KOREAN BBQ Food' in fetch_content:
            print(success_output)
        else:
            print(fail_output + " Expected content not in the taint logs")
    else:
        print(fail_output + " Expected taint log file not found. ")

    deinit(extension_name)

def Outlook_Extension_MV2_Test():

    target_page = 'outlook_inbox'
    test_URL = url_mp[target_page]
    extension_name = '%s_mv2.crx'%target_page
    recording_name = '%s.wprgo'%target_page
    annotation_name = '%s.js'%target_page
    rules = rules_map[target_page]
    success_output = 'Custom Extension %s: '%extension_name + Back.GREEN + "Success" + Back.RESET + "."
    fail_output = 'Custom Extension %s: '%extension_name + Fore.RED + "Fail" + Fore.RESET + "."

    check_file_exist(extension_name = extension_name, recording_name = recording_name, annotation_name = annotation_name)

    init(extension_name)

    try:
        driver = launch_driver(load_extension = True, extension_name = extension_name,
                               recording_name = recording_name, rules = rules, annotation_name = annotation_name,
                               idle_timeout_ms=20000)
        print('Launch Arcanum success. Arcanum starts running.')
        time.sleep(1)
        driver.get(test_URL)
        ui = ''
        try:
            ui = WebDriverWait(driver, 40).until(
                EC.visibility_of_element_located((By.ID, "MainModule")))
        finally:
            driver.save_screenshot('/mnt/run/Arcanum/Test_Cases/my.png')
            innerhtml = ui.get_attribute('innerHTML')
            tainted_element_num = innerhtml.count('data-taint')
            if (tainted_element_num):
                print('Inject annotation success: There are %d tainted DOM elements on the page. (Expected to be 1)'%tainted_element_num)
        print('Execute the extension for 60s after the web page has completely loaded, waiting now...')
        time.sleep(30)
        driver.quit()
    except Exception as e:
        print(e)
        print(fail_output)
        return

    print('End running Arcanum. Start checking taint logs. ')
    # Check the extension source to see why we should get the storage sink and XMLHttpRequest sink.
    if os.path.exists(v8_log_path + 'taint_sources.log') \
            and os.path.exists(v8_log_path + 'taint_storage.log') \
            and os.path.exists(user_data_path + 'taint_xhr.log'):
        source_content = input_source_logs()
        storage_content = input_sink_logs('storage')
        xhr_content = input_sink_logs('xhr')
        # You can check the content detail in taint logs, here for test we just check some key values of each log.
        if "Lease Approved For 1016 West Avenue" in source_content and \
                'The executed agreement is attached to this email.' in storage_content and \
                ('xml-send-body-ArrayBuffer' in xhr_content and 'Fidelity Investments' in xhr_content):
            print(success_output)
        else:
            print(fail_output + " Expected content not in the taint logs")
    else:
        print(fail_output + " Expected taint log file not found. ")

    deinit(extension_name)

def Outlook_Extension_MV3_Test():

    target_page = 'outlook_inbox'
    test_URL = url_mp[target_page]
    extension_name = '%s_mv3.crx'%target_page
    recording_name = '%s.wprgo'%target_page
    annotation_name = '%s.js'%target_page
    rules = rules_map[target_page]
    success_output = 'Custom Extension %s: '%extension_name + Back.GREEN + "Success" + Back.RESET + "."
    fail_output = 'Custom Extension %s: '%extension_name + Fore.RED + "Fail" + Fore.RESET + "."

    check_file_exist(extension_name = extension_name, recording_name = recording_name, annotation_name = annotation_name)

    init(extension_name)

    try:
        driver = launch_driver(load_extension = True, extension_name = extension_name,
                               recording_name = recording_name, rules = rules, annotation_name = annotation_name,
                               idle_timeout_ms=20000)
        print('Launch Arcanum success. Arcanum starts running.')
        time.sleep(1)
        driver.get(test_URL)
        ui = ''
        try:
            ui = WebDriverWait(driver, 40).until(
                EC.visibility_of_element_located((By.ID, "MainModule")))
        finally:
            innerhtml = ui.get_attribute('innerHTML')
            tainted_element_num = innerhtml.count('data-taint')
            if (tainted_element_num):
                print('Inject annotation success: There are %d tainted DOM elements on the page. (Expected to be 1)'%tainted_element_num)
        print('Execute the extension for 60s after the web page has completely loaded, waiting now...')
        time.sleep(EXECUTION_TIME)
        driver.quit()
    except Exception as e:
        print(e)
        print(fail_output)
        return

    print('End running Arcanum. Start checking taint logs. ')
    # Check the extension source to see why we should get the fetch sink.
    if os.path.exists(v8_log_path + 'taint_sources.log') \
            and os.path.exists(user_data_path + 'taint_fetch.log'):
        source_content = input_source_logs()
        fetch_content = input_sink_logs('fetch')
        # You can check the content detail in taint logs, here for test we just check some key values of each log.
        if ('Amazon Orders' in source_content) \
              and ("Hello Amy, We're writing to let you know that your order has been successfully canceled." in fetch_content):
            print(success_output)
        else:
            print(fail_output + " Expected content not in the taint logs")
    else:
        print(fail_output + " Expected taint log file not found. ")

    deinit(extension_name)

def LinkedIn_Extension_MV2_Test():

    target_page = 'linkedin_profile'
    test_URL = url_mp[target_page]
    extension_name = '%s_mv2.crx'%target_page
    recording_name = '%s.wprgo'%target_page
    annotation_name = '%s.js'%target_page
    rules = rules_map[target_page]
    success_output = 'Custom Extension %s: '%extension_name + Back.GREEN + "Success" + Back.RESET + "."
    fail_output = 'Custom Extension %s: '%extension_name + Fore.RED + "Fail" + Fore.RESET + "."

    check_file_exist(extension_name = extension_name, recording_name = recording_name, annotation_name = annotation_name)

    init(extension_name)

    try:
        driver = launch_driver(load_extension = True, extension_name = extension_name,
                               recording_name = recording_name, rules = rules, annotation_name = annotation_name,
                               idle_timeout_ms=240000)
        print('Launch Arcanum success. Arcanum starts running.')
        print('Note: driver.get() can take longer than with other target sites '
              'because the LinkedIn page has many resources and animations.')
        time.sleep(1)
        driver.get(test_URL)
        ui = ''
        try:
            ui = WebDriverWait(driver, 40).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "application-outlet")))
        finally:
            innerhtml = ui.get_attribute('innerHTML')
            tainted_element_num = innerhtml.count('data-taint')
            if (tainted_element_num):
                print('Inject annotation success: There are %d tainted DOM elements on the page. (Expected to be 58)'%tainted_element_num)
        print('Execute the extension for 60s after the web page has completely loaded, waiting now...')
        time.sleep(EXECUTION_TIME)
        driver.quit()
    except Exception as e:
        print(e)
        print(fail_output)
        return

    print('End running Arcanum. Start checking taint logs. ')
    # Check the extension source to see why we should get the storage sink and XMLHttpRequest sink.
    if os.path.exists(v8_log_path + 'taint_sources.log') \
            and os.path.exists(v8_log_path + 'taint_storage.log') \
            and os.path.exists(user_data_path + 'taint_xhr.log'):
        source_content = input_source_logs()
        storage_content = input_sink_logs('storage')
        xhr_content = input_sink_logs('xhr')
        # You can check the content detail in taint logs, here for test we just check some key values of each log.
        if "Amy Lee is skilled in leadership" in source_content and \
                "startLinkedIn Offer See who's hiring_end" in storage_content and \
                ('xml-send-body-ArrayBuffer' in xhr_content and '<ArrayBuffer map' in xhr_content):
            print(success_output)
        else:
            print(fail_output + " Expected content not in the taint logs")
    else:
        print(fail_output + " Expected taint log file not found. ")

    deinit(extension_name)

def LinkedIn_Extension_MV3_Test():

    target_page = 'linkedin_profile'
    test_URL = url_mp[target_page]
    extension_name = '%s_mv3.crx'%target_page
    recording_name = '%s.wprgo'%target_page
    annotation_name = '%s.js'%target_page
    rules = rules_map[target_page]
    success_output = 'Custom Extension %s: '%extension_name + Back.GREEN + "Success" + Back.RESET + "."
    fail_output = 'Custom Extension %s: '%extension_name + Fore.RED + "Fail" + Fore.RESET + "."

    check_file_exist(extension_name = extension_name, recording_name = recording_name, annotation_name = annotation_name)

    init(extension_name)

    try:
        driver = launch_driver(load_extension = True, extension_name = extension_name,
                               recording_name = recording_name, rules = rules, annotation_name = annotation_name,
                               idle_timeout_ms=240000)
        print('Launch Arcanum success. Arcanum starts running.')
        print('Note: driver.get() can take longer than with other target sites '
              'because the LinkedIn page has many resources and animations.')
        time.sleep(1)
        driver.get(test_URL)
        ui = ''
        try:
            ui = WebDriverWait(driver, 40).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "application-outlet")))
        finally:
            innerhtml = ui.get_attribute('innerHTML')
            tainted_element_num = innerhtml.count('data-taint')
            if (tainted_element_num):
                print('Inject annotation success: There are %d tainted DOM elements on the page. (Expected to be 58)'%tainted_element_num)
        print('Execute the extension for 60s after the web page has completely loaded, waiting now...')
        time.sleep(EXECUTION_TIME)
        driver.quit()
    except Exception as e:
        print(e)
        print(fail_output)
        return

    # print('End running Arcanum. Start checking taint logs. ')
    # # Check the extension source to see why we should get the fetch sink.
    # if os.path.exists(v8_log_path + 'taint_sources.log') \
    #         and os.path.exists(user_data_path + 'taint_fetch.log'):
    #     source_content = input_source_logs()
    #     fetch_content = input_sink_logs('fetch')
    #     # You can check the content detail in taint logs, here for test we just check some key values of each log.
    #     if ('Jack Ma' in source_content and 'One off event' in source_content) \
    #           and ('"str1":"U.S. Department of Educati.' in fetch_content):
    #         print(success_output)
    #     else:
    #         print(fail_output + " Expected content not in the taint logs")
    # else:
    #     print(fail_output + " Expected taint log file not found. ")

    deinit(extension_name)

def Paypal_Extension_MV2_Test():

    target_page = 'paypal_card'
    test_URL = url_mp[target_page]
    extension_name = '%s_mv2.crx'%target_page
    recording_name = '%s.wprgo'%target_page
    annotation_name = '%s.js'%target_page
    rules = rules_map[target_page]
    success_output = 'Custom Extension %s: '%extension_name + Back.GREEN + "Success" + Back.RESET + "."
    fail_output = 'Custom Extension %s: '%extension_name + Fore.RED + "Fail" + Fore.RESET + "."

    check_file_exist(extension_name = extension_name, recording_name = recording_name, annotation_name = annotation_name)

    init(extension_name)

    try:
        driver = launch_driver(load_extension = True, extension_name = extension_name,
                               recording_name = recording_name, rules = rules, annotation_name = annotation_name,
                               idle_timeout_ms=5000)
        print('Launch Arcanum success. Arcanum starts running.')
        time.sleep(1)
        driver.get(test_URL)
        ui = ''
        try:
            ui = WebDriverWait(driver, 40).until(
                EC.visibility_of_element_located((By.ID, "contents")))
        finally:
            innerhtml = ui.get_attribute('innerHTML')
            tainted_element_num = innerhtml.count('data-taint')
            if (tainted_element_num):
                print('Inject annotation success: There are %d tainted DOM elements on the page. (Expected to be 14)'%tainted_element_num)
        print('Execute the extension for 60s after the web page has completely loaded, waiting now...')
        time.sleep(EXECUTION_TIME)
        driver.quit()
    except Exception as e:
        print(e)
        print(fail_output)
        return

    print('End running Arcanum. Start checking taint logs. ')
    # Check the extension source to see why we should get the storage sink and XMLHttpRequest sink.
    if os.path.exists(v8_log_path + 'taint_sources.log') \
            and os.path.exists(v8_log_path + 'taint_storage.log') \
            and os.path.exists(user_data_path + 'taint_xhr.log'):
        source_content = input_source_logs()
        storage_content = input_sink_logs('storage')
        xhr_content = input_sink_logs('xhr')
        # You can check the content detail in taint logs, here for test we just check some key values of each log.
        if "\\x8d8a\\x57ce\\x533a\\x76db\\x4e16\\x540d" in source_content and \
                '0120_end' in storage_content and \
                ('xml-send-body-ArrayBuffer' in xhr_content and '<ArrayBuffer map' in xhr_content):
            print(success_output)
        else:
            print(fail_output + " Expected content not in the taint logs")
    else:
        print(fail_output + " Expected taint log file not found. ")

    deinit(extension_name)

def Paypal_Extension_MV3_Test():

    target_page = 'paypal_card'
    test_URL = url_mp[target_page]
    extension_name = '%s_mv3.crx'%target_page
    recording_name = '%s.wprgo'%target_page
    annotation_name = '%s.js'%target_page
    rules = rules_map[target_page]
    success_output = 'Custom Extension %s: '%extension_name + Back.GREEN + "Success" + Back.RESET + "."
    fail_output = 'Custom Extension %s: '%extension_name + Fore.RED + "Fail" + Fore.RESET + "."

    check_file_exist(extension_name = extension_name, recording_name = recording_name, annotation_name = annotation_name)

    init(extension_name)

    try:
        driver = launch_driver(load_extension = True, extension_name = extension_name,
                               recording_name = recording_name, rules = rules, annotation_name = annotation_name,
                               idle_timeout_ms=5000)
        print('Launch Arcanum success. Arcanum starts running.')
        time.sleep(1)
        driver.get(test_URL)
        ui = ''
        try:
            ui = WebDriverWait(driver, 40).until(
                EC.visibility_of_element_located((By.ID, "contents")))
        finally:
            innerhtml = ui.get_attribute('innerHTML')
            tainted_element_num = innerhtml.count('data-taint')
            if (tainted_element_num):
                print('Inject annotation success: There are %d tainted DOM elements on the page. (Expected to be 14)'%tainted_element_num)
        print('Execute the extension for 60s after the web page has completely loaded, waiting now...')
        time.sleep(EXECUTION_TIME)
        driver.quit()
    except Exception as e:
        print(e)
        print(fail_output)
        return

    print('End running Arcanum. Start checking taint logs. ')
    # Check the extension source to see why we should get the storage sink and XMLHttpRequest sink.
    if os.path.exists(v8_log_path + 'taint_sources.log') \
            and os.path.exists(user_data_path + 'taint_fetch.log'):
        source_content = input_source_logs()
        fetch_content = input_sink_logs('fetch')
        # You can check the content detail in taint logs, here for test we just check some key values of each log.
        if ('Visa Credit' in source_content and "2143" in source_content) \
              and ('PayPal balance' in fetch_content and '$0.00' in fetch_content):
            print(success_output)
        else:
            print(fail_output + " Expected content not in the taint logs")
    else:
        print(fail_output + " Expected taint log file not found. ")

    deinit(extension_name)

if __name__ == '__main__':

    # Amazon_Extension_MV2_Test()    #Source [Amazon DOM elements] -> Propagation [chrome.runtime.connect, postMessage, String Concat, TextEncode] -> Sink [storage, XMLHTTPRequest]
    # Amazon_Extension_MV3_Test()    #Source [Amazon DOM elements] -> Propagation [JSON.stringify] -> Sink [Fetch]

    # Facebook_Extension_MV2_Test()  #Source [Facebook DOM elements] -> Propagation [chrome.runtime.connect, postMessage, String Concat, TextEncode] -> Sink [storage, XMLHTTPRequest]
    # Facebook_Extension_MV3_Test()  #Source [Facebook DOM elements] -> Propagation [JSON.stringify] -> Sink [Fetch]

    # Ins_Extension_MV2_Test()       #Source [Facebook DOM elements] -> Propagation [chrome.runtime.connect, postMessage, String Concat, TextEncode] -> Sink [storage, XMLHTTPRequest]
    # Ins_Extension_MV3_Test()       #Source [Facebook DOM elements] -> Propagation [JSON.stringify] -> Sink [Fetch]

    # Paypal_Extension_MV2_Test()    # Source [Paypal DOM elements] -> Propagation [chrome.runtime.connect, postMessage, String Concat, TextEncode] -> Sink [storage, XMLHTTPRequest]
    # Paypal_Extension_MV3_Test()    # Source [Paypal DOM elements] -> Propagation [JSON.stringify] -> Sink [Fetch]

    # Gmail_Extension_MV2_Test()     # Source [Gmail DOM elements] -> Propagation [chrome.runtime.connect, postMessage, String Concat, TextEncode] -> Sink [storage, XMLHTTPRequest]#
    # Gmail_Extension_MV3_Test()     # Source [Gmail DOM elements] -> Propagation [JSON.stringify] -> Sink [Fetch]

    # Outlook_Extension_MV2_Test()   # Source [Outlook DOM elements] -> Propagation [chrome.runtime.connect, postMessage, String Concat, TextEncode] -> Sink [storage, XMLHTTPRequest]
    # Outlook_Extension_MV3_Test()   # Source [Outlook DOM elements] -> Propagation [JSON.stringify] -> Sink [Fetch]

    # LinkedIn_Extension_MV2_Test()  # Source [LinkedIn DOM elements] -> Propagation [chrome.runtime.connect, postMessage, String Concat, TextEncode] -> Sink [storage, XMLHTTPRequest]#
    LinkedIn_Extension_MV3_Test()  # Source [LinkedIn DOM elements] -> Propagation [JSON.stringify] -> Sink [Fetch]




