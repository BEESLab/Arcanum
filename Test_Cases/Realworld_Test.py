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

in_debug = False
EXECUTION_TIME = 60
test_path = "/root/"
arcanum_executable_path = test_path + 'arcanum/opt/chromium.org/chromium-unstable/chromium-browser-unstable'

linkedin_specific_arcanum_executable_path = test_path + 'LinkedIn_installer/opt/chromium.org/chromium-unstable/chromium-browser-unstable'
chromedriver_path = test_path + 'chromedriver/chromedriver'
wpr_path = '/root/go/pkg/mod/github.com/catapult-project/catapult/web_page_replay_go@v0.0.0-20230901234838-f16ca3c78e46/'

log_path = test_path+'logs/'
os.environ["CHROME_LOG_FILE"] = log_path+'chromium.log'
user_data_path = '/root/userdata/'
realworld_extension_dir = '/root/extensions/realworld/'
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

def init(extension_id):
    if os.path.exists(realworld_extension_dir) == False:
        os.system('mkdir -p %s'%realworld_extension_dir)
    if os.path.exists(recording_dir) == False:
        os.system('mkdir -p %s'%recording_dir)
    if os.path.exists(annotation_dir) == False:
        os.system('mkdir -p %s'%annotation_dir)

    print('=============== Start Testing the Real-world Extension: [%s] ==============='%extension_id)
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


def deinit(extension_id):
    print('=============== Finish Test ===============\n')
    os.system('pkill Xvfb')
    os.system('pkill chrome')
    os.system('pkill chromedriver')
    os.system('pkill wpr')


@func_set_timeout(20)
def launch_driver(load_extension, extension_name, recording_name = None, rules = None, annotation_name = None,
                  idle_timeout_ms = None, delay_animation_ms = None, linkedin_specific = False):

    if os.path.exists(arcanum_executable_path) == False:
        print(Fore.RED + "Error: Given Arcanum executable path [%s] does not exist. "%arcanum_executable_path + Fore.RESET)
        exit(0)

    if os.path.exists(chromedriver_path) == False:
        print(Fore.RED + "Error: Given chromedriver path [%s] does not exist. "%chromedriver_path + Fore.RESET)
        exit(0)

    service = Service(executable_path=chromedriver_path)
    options = webdriver.ChromeOptions()
    if linkedin_specific:
        if os.path.exists(linkedin_specific_arcanum_executable_path) == False:
            print(Fore.RED + "Error: Given Arcanum specific executable path for LinkedIn page [%s] does not exist. Please download it first." % linkedin_specific_arcanum_executable_path + Fore.RESET)
            exit(0)
        options.binary_location = linkedin_specific_arcanum_executable_path
    else:
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
        extension_path = realworld_extension_dir + extension_name
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
    if extension_name != None and os.path.exists(realworld_extension_dir + extension_name) == False:
        print(Fore.RED+"Error: Test extension [%s] does not exist. Download it from the GitHub repo first."%extension_name + Fore.RESET)
        exit(0)

    if recording_name != None and os.path.exists(recording_dir + recording_name) == False:
        print(Fore.RED+"Error: The required recording file [%s] does not exist. Download it from our GitHub repo first." % recording_name + Fore.RESET )
        exit(0)

    if annotation_name != None and os.path.exists(annotation_dir + annotation_name) == False:
        print(Fore.RED + "Error: The required annotation file [%s] does not exist. Download it from our GitHub repo first." % annotation_name + Fore.RESET)
        exit(0)

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

def aamfmnhcipnbjjnbfmaoooiohikifefk():
    """
    This extension extracts user and  profile information from LinkedIn, Facebook, and Instagram and sends the information
    over XMLHttpRequest requests. See Section 4.10 in our paper.
    Here we use the Instagram page as the test case.
    We release our experimental taint logs (and screenshots) of all these sites in /Taint_Logs/aamfmnhcipnbjjnbfmaoooiohikifefk/.
    """
    extension_id = 'aamfmnhcipnbjjnbfmaoooiohikifefk'
    extension_name = extension_id + '.crx'
    target_page = 'ins_profile'
    test_URL = url_mp[target_page]
    recording_name = '%s.wprgo'%target_page
    annotation_name = '%s.js'%target_page
    rules = rules_map[target_page]
    success_output = 'Realworld Extension [%s]: ' % extension_id + Back.GREEN + "Success" + Back.RESET + "."
    fail_output = 'Realworld Extension [%s]: ' % extension_id + Fore.RED + "Fail" + Fore.RESET + "."

    check_file_exist(extension_name=extension_name, recording_name=recording_name, annotation_name=annotation_name)

    init(extension_id)

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
    if os.path.exists(v8_log_path + 'taint_sources.log') \
            and os.path.exists(user_data_path + 'taint_xhr.log'):
        source_content = input_source_logs()
        xhr_content = input_sink_logs('xhr')
        # Profile keywords. See the screenshot in /Taint_Logs/aamfmnhcipnbjjnbfmaoooiohikifefk/ins_profile/ to locate
        # where the sensitive information appears on the page.
        if '<String[14]: e"This is me!!!!">' in source_content and \
                ('This is me!!!!' in xhr_content): # Profile key word
            print(success_output)
        else:
            print(fail_output + " Expected content not in the taint logs")
    else:
        print(fail_output + " Expected taint log file not found. ")

    deinit(extension_name)


def jdianbbpnakhcmfkcckaboohfgnngfcc():
    """
    This extension collects profile and identity information on Facebook,
    and URL information on all pages tested, storing all data within the extension’s local storage.
    See Section 4.10 in our paper.
    Here we use the Facebook page as the test case.
    We release our experimental taint logs (and screenshots) of Facebook in /Taint_Logs/jdianbbpnakhcmfkcckaboohfgnngfcc/.
    """
    extension_id = 'jdianbbpnakhcmfkcckaboohfgnngfcc'
    extension_name = extension_id + '.crx'
    target_page = 'fb_post'
    test_URL = url_mp[target_page]
    recording_name = '%s.wprgo' % target_page
    annotation_name = '%s.js' % target_page
    rules = rules_map[target_page]
    success_output = 'Realworld Extension [%s]: ' % extension_id + Back.GREEN + "Success" + Back.RESET + "."
    fail_output = 'Realworld Extension [%s]: ' % extension_id + Fore.RED + "Fail" + Fore.RESET + "."

    check_file_exist(extension_name=extension_name, recording_name=recording_name, annotation_name=annotation_name)

    init(extension_id)

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

    if os.path.exists(v8_log_path + 'taint_sources.log') \
            and os.path.exists(v8_log_path + 'taint_storage.log'):
        source_content = input_source_logs()
        storage_content = input_sink_logs('storage')
        # Profile keywords. See the screenshot in /Taint_Logs/jdianbbpnakhcmfkcckaboohfgnngfcc/fb_post/ to locate
        # where the sensitive information appears on the page.
        if 'MyComputerCareer' in source_content and 'Atlanta-Georgia-' in source_content \
                and 'MyComputerCareer' in storage_content and 'Atlanta-Georgia-' in storage_content:
            print(success_output)
        else:
            print(fail_output + " Expected content not in the taint logs")
    else:
        print(fail_output + " Expected taint log file not found. ")

    deinit(extension_id)

def oadkgbgppkhoaaoepjbcnjejmkknaobg():
    """
    This extension scrapes and exfiltrates all tainted user data across all target websites
    over Fetch network requests.
    See Section 4.10 in our paper.
    Here we use the Amazon page as the test case.
    We release our experimental taint logs (and screenshots) of these pages in /Taint_Logs/oadkgbgppkhoaaoepjbcnjejmkknaobg/.
    """

    extension_id = 'oadkgbgppkhoaaoepjbcnjejmkknaobg'
    extension_name = extension_id + '.crx'
    target_page = 'amazon_address'
    test_URL = url_mp[target_page]
    recording_name = '%s.wprgo' % target_page
    annotation_name = '%s.js' % target_page
    rules = rules_map[target_page]
    success_output = 'Realworld Extension [%s]: ' % extension_id + Back.GREEN + "Success" + Back.RESET + "."
    fail_output = 'Realworld Extension [%s]: ' % extension_id + Fore.RED + "Fail" + Fore.RESET + "."

    check_file_exist(extension_name=extension_name, recording_name=recording_name, annotation_name=annotation_name)

    init(extension_id)

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
            os.path.exists(user_data_path + 'taint_fetch.log'):
        source_content = input_source_logs()
        fetch_content = input_sink_logs('fetch')
        # Page sensitive information keywords. See the screenshot in /Taint_Logs/oadkgbgppkhoaaoepjbcnjejmkknaobg/amazon_address/ to locate
        # where the sensitive information appears on the page.
        if ('Your Addresses' in source_content and 'Amy Lee1762 CLIFTON RD NEATLANTA, GA 30322-4001United States' in source_content)  \
             and  ('A ST SWJACKSONVILLE, AL' in fetch_content and '+1 470 253 1212' in fetch_content and 'Erin Lee' in fetch_content):
            print(success_output)
        else:
            print(fail_output + " Expected content not in the taint logs")
    else:
        print(fail_output + " Expected taint log file not found. ")

    deinit(extension_id)

def blcdkmjcpgjojjffbdkckaiondfpoglh():
    """
    This extension automatically exfiltrating all sensitive information across all seven pages to an API endpoint at
    a university.
    See Section 4.10 in our paper.
    Here we use the Paypal page as the test case.
    We release our experimental taint logs (and screenshots) of these pages in /Taint_Logs/blcdkmjcpgjojjffbdkckaiondfpoglh/.
    """
    extension_id = 'blcdkmjcpgjojjffbdkckaiondfpoglh'
    extension_name = extension_id + '.crx'
    target_page = 'paypal_card'
    test_URL = url_mp[target_page]
    recording_name = '%s.wprgo' % target_page
    annotation_name = '%s.js' % target_page
    rules = rules_map[target_page]
    success_output = 'Realworld Extension [%s]: ' % extension_id + Back.GREEN + "Success" + Back.RESET + "."
    fail_output = 'Realworld Extension [%s]: ' % extension_id + Fore.RED + "Fail" + Fore.RESET + "."

    check_file_exist(extension_name=extension_name, recording_name=recording_name, annotation_name=annotation_name)

    init(extension_id)

    try:
        driver = launch_driver(load_extension=True, extension_name=extension_name,
                               recording_name=recording_name, rules=rules, annotation_name=annotation_name,
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
                print(
                    'Inject annotation success: There are %d tainted DOM elements on the page. (Expected to be 14)' % tainted_element_num)
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
            and os.path.exists(user_data_path + 'taint_xhr.log'):
        source_content = input_source_logs()
        xhr_content = input_sink_logs('xhr')
        # Page sensitive information keywords. See the screenshot in /Taint_Logs/blcdkmjcpgjojjffbdkckaiondfpoglh/paypal_card/ to locate
        # where the sensitive information appears on the page.
        if "Visa" in source_content and '2143' in source_content and 'This card is about to expire.' in source_content \
              and  ('This card is about to expire.' in xhr_content and 'From September 11, 2023, updated Payment Receiving' in xhr_content):
            print(success_output)
        else:
            print(fail_output + " Expected content not in the taint logs")
    else:
        print(fail_output + " Expected taint log file not found. ")

    deinit(extension_name)

def kecadfolelkekbfmmfoifpfalfedeljo():
    """
    This extension collects location information
    See Table 7 (Section 4.5) in our paper.
    Here we use the Paypal page as the test case.
    We release our experimental taint logs (and screenshots) of these pages in /Taint_Logs/blcdkmjcpgjojjffbdkckaiondfpoglh/.
       """
    extension_id = 'blcdkmjcpgjojjffbdkckaiondfpoglh'
    extension_name = extension_id + '.crx'
    target_page = 'paypal_card'
    test_URL = url_mp[target_page]
    recording_name = '%s.wprgo' % target_page
    annotation_name = '%s.js' % target_page
    rules = rules_map[target_page]
    success_output = 'Realworld Extension [%s]: ' % extension_id + Back.GREEN + "Success" + Back.RESET + "."
    fail_output = 'Realworld Extension [%s]: ' % extension_id + Fore.RED + "Fail" + Fore.RESET + "."

    check_file_exist(extension_name=extension_name, recording_name=recording_name, annotation_name=annotation_name)

    init(extension_id)

def nkecaphdplhfmmbkcfnknejeonfnifbn():
    """
    This extension collects friend information from the page and propagate the info to a sink.
    See Table 7 (Section 4.5) in our paper.
    Here we use the Instagram page as the test case.
    We release our experimental taint logs (and screenshots) of these pages in /Taint_Logs/nkecaphdplhfmmbkcfnknejeonfnifbn/.
    """

    extension_id = 'nkecaphdplhfmmbkcfnknejeonfnifbn'
    extension_name = extension_id + '.crx'
    target_page = 'ins_profile'
    test_URL = url_mp[target_page]
    recording_name = '%s.wprgo' % target_page
    annotation_name = '%s.js' % target_page
    rules = rules_map[target_page]
    success_output = 'Realworld Extension [%s]: ' % extension_id + Back.GREEN + "Success" + Back.RESET + "."
    fail_output = 'Realworld Extension [%s]: ' % extension_id + Fore.RED + "Fail" + Fore.RESET + "."

    check_file_exist(extension_name=extension_name, recording_name=recording_name, annotation_name=annotation_name)

    init(extension_id)

    try:
        driver = launch_driver(load_extension=True, extension_name=extension_name,
                               recording_name=recording_name, rules=rules, annotation_name=annotation_name,
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
                print(
                    'Inject annotation success: There are %d tainted DOM elements on the page. (Expected to be 3)' % tainted_element_num)
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
        #  See the screenshot in /Taint_Logs/nkecaphdplhfmmbkcfnknejeonfnifbn/ins_profile/ to locate
        #  where the sensitive information appears on the page.
        if 'Erin (@xqgtiti)' in source_content and \
                ('relationship_status' in fetch_content and 'age' in fetch_content):
            print(success_output)
        else:
            print(fail_output + " Expected content not in the taint logs")
    else:
        print(fail_output + " Expected taint log file not found. ")

    deinit(extension_id)

def bahcihkpdjlbndandplnfmejnalndgjo():
    """
    This extension collects post information from the page and propagate the info to a sink.
    See Table 7 (Section 4.5) in our paper.
    Here we use the Facebook page as the test case.
    We release our experimental taint logs (and screenshots) of these pages in /Taint_Logs/bahcihkpdjlbndandplnfmejnalndgjo/.
    """
    extension_id = 'bahcihkpdjlbndandplnfmejnalndgjo'
    extension_name = extension_id + '.crx'
    target_page = 'fb_post'
    test_URL = url_mp[target_page]
    recording_name = '%s.wprgo' % target_page
    annotation_name = '%s.js' % target_page
    rules = rules_map[target_page]
    success_output = 'Realworld Extension [%s]: ' % extension_id + Back.GREEN + "Success" + Back.RESET + "."
    fail_output = 'Realworld Extension [%s]: ' % extension_id + Fore.RED + "Fail" + Fore.RESET + "."

    check_file_exist(extension_name=extension_name, recording_name=recording_name, annotation_name=annotation_name)

    init(extension_id)

    try:
        driver = launch_driver(load_extension=True, extension_name=extension_name,
                               recording_name=recording_name, rules=rules, annotation_name=annotation_name,
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
                print(
                    'Inject annotation success: There are %d tainted DOM elements on the page. (Expected to be 11)' % tainted_element_num)
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
        # Page post content keywords. See the screenshot in /Taint_Logs/bahcihkpdjlbndandplnfmejnalndgjo/fb_post/ to locate
        # where the sensitive information appears on the page.
        if 'feeling happy in' in source_content and 'This is a rainy day!' in source_content \
               and ('2 friends' in fetch_content and 'This is a rainy day!' in fetch_content and 'Thank you! ' in fetch_content):
            print(success_output)
        else:
            print(fail_output + " Expected content not in the taint logs")
    else:
        print(fail_output + " Expected taint log file not found. ")

    deinit(extension_id)

def pjmfidajplecneclhdghcgdefnmhhlca():
    """
    This extension collects the Whole HTML from the page and propagate the info to a sink.
    See Table 7 (Section 4.5) in our paper.
    Here we use the Amazon page as the test case.
    We release our experimental taint logs (and screenshots) of these pages in /Taint_Logs/pjmfidajplecneclhdghcgdefnmhhlca/.
    """
    extension_id = 'pjmfidajplecneclhdghcgdefnmhhlca'
    extension_name = extension_id + '.crx'
    target_page = 'amazon_address'
    test_URL = url_mp[target_page]
    recording_name = '%s.wprgo' % target_page
    annotation_name = '%s.js' % target_page
    rules = rules_map[target_page]
    success_output = 'Realworld Extension [%s]: ' % extension_id + Back.GREEN + "Success" + Back.RESET + "."
    fail_output = 'Realworld Extension [%s]: ' % extension_id + Fore.RED + "Fail" + Fore.RESET + "."

    check_file_exist(extension_name=extension_name, recording_name=recording_name, annotation_name=annotation_name)

    init(extension_id)

    try:
        driver = launch_driver(load_extension=True, extension_name=extension_name,
                               recording_name=recording_name, rules=rules, annotation_name=annotation_name,
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
                print(
                    'Inject annotation success: There are %d tainted DOM elements on the page. (Expected to be 6)' % tainted_element_num)
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
            os.path.exists(user_data_path + 'taint_fetch.log'):
        source_content = input_source_logs()
        fetch_content = input_sink_logs('fetch')
        # Page whole HTML keywords. See the screenshot in /Taint_Logs/pjmfidajplecneclhdghcgdefnmhhlca/amazon_address/ to locate
        # where the sensitive information appears on the page.
        if ('...<truncated>>' in source_content) \
               and ('Deliver to Amy' in fetch_content and 'Atlanta 30322' in fetch_content and '1762 CLIFTON RD NE' in fetch_content):
            print(success_output)
        else:
            print(fail_output + " Expected content not in the taint logs")
    else:
        print(fail_output + " Expected taint log file not found. ")

    deinit(extension_name)

def mdfgkcdjgpgoeclhefnjgmollcckpedk():
    """
    the Sentry JS library used by this extension exfiltrates the image element attribute from the Instagram page to an endpoint.
    See Table 7 (Section 4.5) in our paper.
    Here we use the Instagram page as the test case.
    We release our experimental taint logs (and screenshot) of the Instagram page in /Taint_Logs/mdfgkcdjgpgoeclhefnjgmollcckpedk/.
    """

    extension_id = 'mdfgkcdjgpgoeclhefnjgmollcckpedk'
    extension_name = extension_id + '.crx'
    target_page = 'ins_profile'
    test_URL = url_mp[target_page]
    recording_name = '%s.wprgo' % target_page
    annotation_name = '%s.js' % target_page
    rules = rules_map[target_page]
    success_output = 'Realworld Extension [%s]: ' % extension_id + Back.GREEN + "Success" + Back.RESET + "."
    fail_output = 'Realworld Extension [%s]: ' % extension_id + Fore.RED + "Fail" + Fore.RESET + "."

    check_file_exist(extension_name=extension_name, recording_name=recording_name, annotation_name=annotation_name)

    init(extension_id)

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
            and os.path.exists(user_data_path + 'taint_fetch.log'):
        source_content = input_source_logs()
        fetch_content = input_sink_logs('fetch')
        # Page image element attribute keywords. See the screenshot in /Taint_Logs/mdfgkcdjgpgoeclhefnjgmollcckpedk/ins_profile/ to locate
        # where the sensitive information appears on the page.
        if 'Erin' in source_content and \
                ('Photo by Erin in The Collective Food Hall at Coda with @cristiano' in fetch_content and 'May be an image of money and text that say' in fetch_content):
            print(success_output)
        else:
            print(fail_output + " Expected content not in the taint logs")
            print(Back.LIGHTGREEN_EX +
                  'In this test case, since the exfiltration is triggered by the Sentry library and depends on dynamic values, API keys, and library versions, the exfiltration does not happen every time. \n' +
                  'Thus, if you see a ' + Fore.RED + 'failure ' + Fore.RESET + Back.LIGHTGREEN_EX + 'here, please directly check our original experimental taint log in "/Taint_Logs/mdfgkcdjgpgoeclhefnjgmollcckpedk/ins_profile/taint_fetch.log" in the GitHub repository, '
                                                                                                    'which shows the extensions sends the sensitive image attribute to https://o4505330217517056.ingest.sentry.io' +
                  Back.RESET)

    else:
        print(fail_output + " Expected taint log file not found. ")
        print(Back.LIGHTGREEN_EX +
            'In this test case, since the exfiltration is triggered by the Sentry library and depends on dynamic values, API keys, and library versions, the exfiltration does not happen every time. \n' +
            'Thus, if you see a '+ Fore.RED + 'failure ' +Fore.RESET+ Back.LIGHTGREEN_EX+'here, please directly check our original experimental taint log in "/Taint_Logs/mdfgkcdjgpgoeclhefnjgmollcckpedk/ins_profile/taint_fetch.log" in the GitHub repository, '
            'which shows the extensions sends the sensitive image attribute to https://o4505330217517056.ingest.sentry.io' +
              Back.RESET)

    deinit(extension_id)


def haphbbhhknaonfloinidkcmadhfjoghc():

    extension_id = 'haphbbhhknaonfloinidkcmadhfjoghc'
    extension_name = extension_id + '.crx'
    target_page = 'linkedin_profile'
    test_URL = url_mp[target_page]
    recording_name = '%s.wprgo' % target_page
    annotation_name = '%s.js' % target_page
    rules = rules_map[target_page]
    success_output = 'Realworld Extension [%s]: ' % extension_id + Back.GREEN + "Success" + Back.RESET + "."
    fail_output = 'Realworld Extension [%s]: ' % extension_id + Fore.RED + "Fail" + Fore.RESET + "."


    check_file_exist(extension_name=extension_name, recording_name=recording_name, annotation_name=annotation_name)

    init(extension_id)

    try:
        driver = launch_driver(load_extension=True, extension_name=extension_name,
                               recording_name=recording_name, rules=rules, annotation_name=annotation_name,
                               idle_timeout_ms = None, delay_animation_ms = None, linkedin_specific=True)
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
                print(
                    'Inject annotation success: There are %d tainted DOM elements on the page. (Expected to > 50)' % tainted_element_num)
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

        if "Microsoft" in source_content and 'Full-time' in source_content \
               and ('Amy Lee' in fetch_content and 'Marketing Intern' in fetch_content) and 'She/Her' in fetch_content:
            print(success_output)
        else:
            print(fail_output + " Expected content not in the taint logs")
    else:
        print(fail_output + " Expected taint log file not found. ")

    deinit(extension_id)

def kecadfolelkekbfmmfoifpfalfedeljo():

    extension_id = 'kecadfolelkekbfmmfoifpfalfedeljo'
    extension_name = extension_id + '.crx'
    target_page = 'linkedin_profile'
    test_URL = url_mp[target_page]
    recording_name = '%s.wprgo' % target_page
    annotation_name = '%s.js' % target_page
    rules = rules_map[target_page]
    success_output = 'Realworld Extension [%s]: ' % extension_id + Back.GREEN + "Success" + Back.RESET + "."
    fail_output = 'Realworld Extension [%s]: ' % extension_id + Fore.RED + "Fail" + Fore.RESET + "."


    check_file_exist(extension_name=extension_name, recording_name=recording_name, annotation_name=annotation_name)

    init(extension_name)

    try:
        driver = launch_driver(load_extension=True, extension_name=extension_name,
                               recording_name=recording_name, rules=rules, annotation_name=annotation_name,
                               idle_timeout_ms = None, delay_animation_ms = None, linkedin_specific=True)
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
                print(
                    'Inject annotation success: There are %d tainted DOM elements on the page. (Expected to > 50)' % tainted_element_num)
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
        # Location
        if "Marketing Intern at Microsoft" in source_content and 'Douglasville, Georgia, United States' in source_content \
               and '"loc":"Douglasville, Georgia, United States"' in fetch_content:
            print(success_output)
        else:
            print(fail_output + " Expected content not in the taint logs")
    else:
        print(fail_output + " Expected taint log file not found. ")

    deinit(extension_id)

if __name__ == '__main__':


    aamfmnhcipnbjjnbfmaoooiohikifefk()     # Case Study (Sec 4.10), Table 7 (Sec 4.5)
    # jdianbbpnakhcmfkcckaboohfgnngfcc()     # Case Study (Sec 4.10), Table 7 (Sec 4.5)
    # oadkgbgppkhoaaoepjbcnjejmkknaobg()     # Case Study (Sec 4.10), Table 7 (Sec 4.5)
    # blcdkmjcpgjojjffbdkckaiondfpoglh()     # Case Study (Sec 4.10)
    # nkecaphdplhfmmbkcfnknejeonfnifbn()     # Table 7 (Sec 4.5)
    # bahcihkpdjlbndandplnfmejnalndgjo()     # Table 7 (Sec 4.5)
    # pjmfidajplecneclhdghcgdefnmhhlca()     # Table 7 (Sec 4.5)

    """
    LinkedIn Cases Below:

    The LinkedIn page has many resources, inline scripts, and animations to load before we can detect the specific DOM elements we want to taint. 
    It can take a few minutes when we replay the page. 
    Thus, we built another version of Arcanum with a specific delay for content scripts injection for testing extensions on the LinkedIn page. 
    Please download the installer from "https://drive.google.com/file/d/13hPgLHP5TedcsCS5HF8g9_8R6jPwfyWW/view?usp=sharing" 
    and place it in /root/LinkedIn_installer/, then decompress it: 
    "ar x linkedin_profile.deb"
    "tar -vxf control.tar && tar -vxf data.tar"

    Then we have a specific_arcanum_executable in: 
    linkedin_specific_arcanum_executable_path = '/root/LinkedIn_installer/opt/chromium.org/chromium-unstable/chromium-browser-unstable'
    We use this specific executable to run the test case of the two extensions below (and our experiments for LinkedIn page described in the paper).

    You can also directly check our original experimental taint logs in 
    /Taint_Logs/haphbbhhknaonfloinidkcmadhfjoghc/linkedin_profile/taint_fetch.log" and 
    /Taint_Logs/kecadfolelkekbfmmfoifpfalfedeljo/linkedin_profile/taint_fetch.log" in the GitHub repository.
    The logs show that: 
    1) [haphbbhhknaonfloinidkcmadhfjoghc] automatically collects and exfiltrates profile and identification information from LinkedIn via Fetch.
    2) [kecadfolelkekbfmmfoifpfalfedeljo] automatically collects and exfiltrates location, profile and identification information from LinkedIn via Fetch.

    """

    # haphbbhhknaonfloinidkcmadhfjoghc()     # Case Study (Sec 4.10), Table 7 (Sec 4.5)

    # kecadfolelkekbfmmfoifpfalfedeljo()  # Table 7 (Sec 4.5)


    """
    In the test case below, since the exfiltration is triggered by the Sentry library and depends on dynamic values/API keys/online library versions etc., 
    the exfiltration does not happen every time.
    
    Thus, if you see a failure of this test case, please directly check our original experimental taint log in 
    "/Taint_Logs/mdfgkcdjgpgoeclhefnjgmollcckpedk/ins_profile/taint_fetch.log" in the GitHub repository,
    which shows the extensions sends the sensitive image attribute to "https://o4505330217517056.ingest.sentry.io/..." 
    """

    # mdfgkcdjgpgoeclhefnjgmollcckpedk()     # Table 7 (Sec 4.5)

