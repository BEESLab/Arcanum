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

EXECUTION_TIME = 60
test_path = "/root/"
linkedin_specific_arcanum_executable_path = '/root/LinkedIn_installer/opt/chromium.org/chromium-unstable/chromium-browser-unstable'
arcanum_executable_path = test_path + 'Arcanum/opt/chromium.org/chromium-unstable/chromium-browser-unstable'

chromedriver_path = test_path + 'chromedriver/chromedriver'
user_data_path = '/root/userdata/'
log_path = test_path+'logs/'
os.environ["CHROME_LOG_FILE"] = log_path+'chromium.log'
wpr_path = '/root/go/pkg/mod/github.com/catapult-project/catapult/web_page_replay_go@v0.0.0-20230901234838-f16ca3c78e46/'

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
                  idle_timeout_ms = None, delay_animation_ms = None, linkedin_specific = False):

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
        if os.path.exists(arcanum_executable_path) == False:
            print(
                Fore.RED + "Error: Given Arcanum executable path [%s] does not exist. " % arcanum_executable_path + Fore.RESET)
            exit(0)
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

def read_taint_source_log():
    f = open(v8_log_path + 'taint_sources.log', 'r')
    lines = []
    while True:
        r = f.readline()
        if not r: break
        lines.append(r)
    f.close()
    return lines


def parse_taint_source_log():
    f = open(v8_log_path + 'taint_sources.log', 'r')
    source_blocks = []
    lines = []
    while True:
        r = f.readline()
        if not r: break
        lines.append(r[:-1])
    f.close()

    block_num = 0
    i = 0
    while i < len(lines):
        if '>>> Taint source: ' in lines[i]:
            source_blocks.append([lines[i+1]])
            function_str = ""
            for j in range(i+2, len(lines)):
                if '>>> END Taint source' in lines[j]:
                    i = j
                    break
                else: function_str = function_str + lines[j]
            source_blocks[block_num].append(function_str)
            block_num = block_num + 1
        i = i + 1
    return source_blocks

def extract_raw_string(s):
    if "<String[1]:" in s: return s[14:-1]
    # To Extract the raw string ("/search") from cases like <String[7]: e"/search"> or <String[38]: "https://....">
    return s[s.find('"')+1:-2]

def source_document_password():

    test_URL = "https://yuanbin.xyz/test/"
    test_extension_name = 'Source_DOM_password'
    recording_name = 'custom.wprgo'
    success_output = 'Custom Extension %s: ' % test_extension_name + Back.GREEN + "Success" + Back.RESET + "."
    fail_output = 'Custom Extension %s: ' % test_extension_name + Fore.RED + "Fail" + Fore.RESET + "."
    init(test_extension_name)

    check_file_exist(test_extension_name,  recording_name, None)

    rules = "MAP yuanbin.xyz:80 127.0.0.1:8080,MAP yuanbin.xyz:443 127.0.0.1:8081,EXCLUDE localhost"
    driver = launch_driver(True, test_extension_name, recording_name, rules)
    driver.get(test_URL)
    time.sleep(5)
    driver.quit()

    source_blocks = parse_taint_source_log()
    success = False

    for i in range(len(source_blocks)):
        if '<String[8]: e"mypasswd">' in source_blocks[i][0]:
            success = True
            break
        print(source_blocks[i][0])

    if success: print(success_output)
    else: print(fail_output)

    deinit(test_extension_name)

def source_document_location():

    test_extension_name = 'Source_DOM_location'
    test_URL = 'https://www.google.com/search?q=Gatech'
    success_output = 'Custom Extension %s: ' % test_extension_name + Back.GREEN + "Success" + Back.RESET + "."
    fail_output = 'Custom Extension %s: ' % test_extension_name + Fore.RED + "Fail" + Fore.RESET + "."

    init(test_extension_name)

    driver = launch_driver(True, test_extension_name)
    driver.get(test_URL)
    time.sleep(5)
    driver.quit()

    print('End running Arcanum and start checking "/ram/analysis/v8logs/taint_sources.log":')
    # Check Taint Source Logs
    taint_sources = []
    lines = read_taint_source_log()
    for i in range(0, len(lines)):
        line = lines[i]
        if '>>> Taint source: (invoked from blink)' in line:
            next_line = lines[i+1]
            object_address = next_line[:14]
            object_info = next_line[14:-1]
            taint_sources.append((object_address, object_info))
            print("["+str(len(taint_sources)) + '] Object Address: ' + object_address + '; Object Information: '+ object_info)
            continue

    # See the test extension source code for why we should get those expected sources.
    expect_sources = ['https://www.google.com/search?q=Gatech', 'https:',
                      'www.google.com', 'www.google.com', '/search', '?q=Gatech',
                      'https://www.google.com', 'https://www.google.com/search?q=Gatech']
    success = True
    for i in range(len(taint_sources)):
        if extract_raw_string(taint_sources[i][1]) == expect_sources[i]: continue
        success = False
        break

    if success: print(success_output)
    else: print(fail_output)

    deinit(test_extension_name)

def source_chrome_webRequest():
    test_extension_name = 'Source_Chrome_webRequest'
    test_URL1 = 'https://yuanbin.xyz/test/'
    test_URL2 = 'https://gatech.edu'
    recording_name = 'custom.wprgo'
    rules = "MAP *.gatech.edu:80 127.0.0.1:8080,MAP *.gatech.edu:443 127.0.0.1:8081,MAP yuanbin.xyz:80 127.0.0.1:8080,MAP yuanbin.xyz:443 127.0.0.1:8081,EXCLUDE localhost"
    success_output = 'Custom Extension %s: ' % test_extension_name + Back.GREEN + "Success" + Back.RESET + "."
    fail_output = 'Custom Extension %s: ' % test_extension_name + Fore.RED + "Fail" + Fore.RESET + "."

    init(test_extension_name)
    driver = launch_driver(True, test_extension_name, recording_name, rules)
    driver.get(test_URL1)  # Test "set-cookie" value in responseHeaders
    driver.get(test_URL1)  # Test "cookie" value in requestHeaders then
    driver.get(test_URL2)  # Test  url, ip, and initiator of chrome.webRequest.onCompleted
    time.sleep(5)
    driver.quit()
    print('End running Arcanum and start checking "/ram/analysis/v8logs/taint_sources.log":')

    source_blocks = parse_taint_source_log()
    success_ip = False
    success_url = False
    success_initiator = False
    success_cookie_request = False
    success_cookie_response = False
    for i in range(len(source_blocks)):
        if '<String[9]: "127.0.0.1">' in source_blocks[i][0]: success_ip = True
        if '<String[54]: "https://www.gatech.edu/sites/default/files/favicon.ico">' in source_blocks[i][0]: success_url = True
        if '<String[22]: "https://www.gatech.edu">' in source_blocks[i][0]: success_initiator = True
        if '<String[13]: "user=QingeXie">' in source_blocks[i][0]:
            if 'details.responseHeaders.length' in source_blocks[i][1]: success_cookie_response = True
        if '<String[13]: "user=QingeXie">' in source_blocks[i][0]:
            if 'details.requestHeaders.length' in source_blocks[i][1]: success_cookie_request = True

    success = False
    if success_ip and success_url and success_initiator and success_cookie_request and success_cookie_response:
        success = True

    if success: print(success_output)
    else: print(fail_output)

    deinit(test_extension_name)

def source_chrome_webNavigation():
    test_extension_name = 'Source_Chrome_webNavigation'
    test_URL1 = 'https://www.google.com/'
    test_URL2 = 'https://www.gatech.edu/'

    success_output = 'Custom Extension %s: ' % test_extension_name + Back.GREEN + "Success" + Back.RESET + "."
    fail_output = 'Custom Extension %s: ' % test_extension_name + Fore.RED + "Fail" + Fore.RESET + "."

    init(test_extension_name)

    driver = launch_driver(True, test_extension_name)
    driver.get(test_URL1)
    time.sleep(1)
    driver.get(test_URL2)
    time.sleep(5)
    driver.quit()

    taint_sources_map = {}
    taint_sources_map['webNavigation.onCompleted'] = []
    taint_sources_map['webNavigation.getFrame'] = []
    taint_sources_map['webNavigation.getAllFrames'] = []

    taint_sources = []
    lines = read_taint_source_log()
    for i in range(0, len(lines)):
        line = lines[i]
        if 'event_emitter:webNavigation.onCompleted' in line:
            taint_sources_map['webNavigation.onCompleted'].append(extract_raw_string(lines[i + 1][14:-1]))
        elif 'api_request_handler:webNavigation.getFrame' in line:
            taint_sources_map['webNavigation.getFrame'].append(extract_raw_string(lines[i + 1][14:-1]))
        elif 'api_request_handler:webNavigation.getAllFrames' in line:
            taint_sources_map['webNavigation.getAllFrames'].append(extract_raw_string(lines[i + 1][14:-1]))
        if '>>> Taint source: ' in line:
            next_line = lines[i + 1]
            object_address = next_line[:14]
            object_info = next_line[14:-1]
            taint_sources.append((object_address, object_info))
            # raw_taint_sources.append(extract_raw_string(object_info))
            print("[" + str(
                len(taint_sources)) + '] Object Address: ' + object_address + '; Object Information: ' + object_info)
            continue

    # See the test extension source code for why we should get those expected sources.
    expect_sources = [test_URL1, test_URL2]

    success = True
    for key in taint_sources_map:
        if expect_sources[0] in taint_sources_map[key] and expect_sources[1] in taint_sources_map[key]: continue
        success = False

    if success: print(success_output)
    else: print(fail_output)

    deinit(test_extension_name)

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
                print('Inject annotation success: There are %d tainted DOM elements on the page. (Expected to > 50)'%tainted_element_num)
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
                print('Inject annotation success: There are %d tainted DOM elements on the page. (Expected to > 50)'%tainted_element_num)
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
        if ('Douglasville, Georgia, United States' in source_content and 'amy-lee-gt' in source_content) \
              and ('Douglasville, Georgia, United States' in fetch_content):
            print(success_output)
        else:
            print(fail_output + " Expected content not in the taint logs")
    else:
        print(fail_output + " Expected taint log file not found. ")

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

    """ 
    Each function is one test case. Uncomment any one to start testing.
    """
    Amazon_Extension_MV2_Test()    #Source [Amazon DOM elements] -> Propagation [chrome.runtime.connect, postMessage, String Concat, TextEncode] -> Sink [storage, XMLHTTPRequest]
    Amazon_Extension_MV3_Test()    #Source [Amazon DOM elements] -> Propagation [JSON.stringify] -> Sink [Fetch]

    Facebook_Extension_MV2_Test()  #Source [Facebook DOM elements] -> Propagation [chrome.runtime.connect, postMessage, String Concat, TextEncode] -> Sink [storage, XMLHTTPRequest]
    Facebook_Extension_MV3_Test()  #Source [Facebook DOM elements] -> Propagation [JSON.stringify] -> Sink [Fetch]

    Ins_Extension_MV2_Test()       #Source [Facebook DOM elements] -> Propagation [chrome.runtime.connect, postMessage, String Concat, TextEncode] -> Sink [storage, XMLHTTPRequest]
    Ins_Extension_MV3_Test()       #Source [Facebook DOM elements] -> Propagation [JSON.stringify] -> Sink [Fetch]

    Paypal_Extension_MV2_Test()    # Source [Paypal DOM elements] -> Propagation [chrome.runtime.connect, postMessage, String Concat, TextEncode] -> Sink [storage, XMLHTTPRequest]
    Paypal_Extension_MV3_Test()    # Source [Paypal DOM elements] -> Propagation [JSON.stringify] -> Sink [Fetch]

    Gmail_Extension_MV2_Test()     # Source [Gmail DOM elements] -> Propagation [chrome.runtime.connect, postMessage, String Concat, TextEncode] -> Sink [storage, XMLHTTPRequest]#
    Gmail_Extension_MV3_Test()     # Source [Gmail DOM elements] -> Propagation [JSON.stringify] -> Sink [Fetch]

    Outlook_Extension_MV2_Test()   # Source [Outlook DOM elements] -> Propagation [chrome.runtime.connect, postMessage, String Concat, TextEncode] -> Sink [storage, XMLHTTPRequest]
    Outlook_Extension_MV3_Test()   # Source [Outlook DOM elements] -> Propagation [JSON.stringify] -> Sink [Fetch]


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
    
    """

    LinkedIn_Extension_MV2_Test()  # Source [LinkedIn DOM elements] -> Propagation [chrome.runtime.connect, postMessage, String Concat, TextEncode] -> Sink [storage, XMLHTTPRequest]#
    LinkedIn_Extension_MV3_Test()  # Source [LinkedIn DOM elements] -> Propagation [JSON.stringify] -> Sink [Fetch]


    """
    Other specific test cases for the instructions on using Arcanum: 
    """
    source_document_password()
    source_document_location()
    source_chrome_webRequest()
    source_chrome_webNavigation()



