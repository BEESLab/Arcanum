# -*- coding: utf-8 -*-
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
import os
import platform
from pyvirtualdisplay import Display

driver_path = '/mnt/hgfs/xqg/chromium/c108real/init/opt/chromium.org/chromium-unstable/chromedriver'
chrome_path = '/home/xqg/debug/opt/chromium.org/chromium-unstable/chrome'
user_data_path = '/home/xqg/arti/'
extension_path = '/mnt/hgfs/xqg/ext/arti/geo'
log_path = '/home/xqg/chromium.log'
os.environ["CHROME_LOG_FILE"] = log_path

if platform.release() == '5.4.0-173-generic':

    log_path = '/mnt/chromium/code/chromium.log'
    os.environ["CHROME_LOG_FILE"] = log_path
    extension_path = '/mnt/chromium/code/geo/'
    user_data_path = '/mnt/chromium/code/arti/'
    chrome_path = '/mnt/chromium/chromium/src/out/Default/chrome'
    driver_path = '/mnt/chromium/code/chromedriver'
    os.system('pkill Xvfb')
    display = Display(visible=0, size=(1920, 1080))
    display.start()

def launch_driver():
    service = Service(executable_path=driver_path)
    options = webdriver.ChromeOptions()
    options.binary_location = chrome_path
    options.add_argument('--user-data-dir=%s' % user_data_path)
    options.add_argument("--enable-logging")
    options.add_argument("--v=0")
    options.add_argument('--verbose')
    options.add_argument('--log-path="%s"'%log_path)
    options.add_argument('--net-log-capture-mode=IncludeCookiesAndCredentials')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors=yes')
    # options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--load-extension={}'.format(extension_path))
    options.add_argument('--custom-script-idle-timeout-ms=30000000')
    # options.add_extension(extension_path)
    prefs = {"profile.default_content_setting_values.notifications": 2}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def TestGeolocation():
    os.environ["CHROME_LOG_FILE"] = '/home/xqg/chromium.log'
    os.system('echo $CHROME_LOG_FILE')
    driver = launch_driver()
    driver.execute_cdp_cmd("Emulation.setGeolocationOverride",
                           {
                               "latitude": 33.772163578,
                               "longitude": -84.390165106,
                               "accuracy": 100,
                           }, )
    time.sleep(2)
    driver.get("https://www.google.com")
    time.sleep(1000000)

if __name__ == '__main__':
    os.system('pkill chrome')
    os.system('pkill chromedriver')

    driver = launch_driver()
    driver.execute_cdp_cmd("Emulation.setGeolocationOverride",
    {
        "latitude": 33.772163578,
        "longitude": -84.390165106,
        "accuracy": 100,
    },)
    time.sleep(2)
    driver.get("https://www.google.com")
    time.sleep(1000000)


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

in_debug = True
test_path = "/root/"
debug_executable_path = "/mnt/run/chromium/src/out/Default/chrome"
arcanum_executable_path = test_path + 'arcanum/opt/chromium.org/chromium-unstable/chromium-browser-unstable'
if in_debug:
    arcanum_executable_path = debug_executable_path
chromedriver_path = test_path + 'chromedriver/chromedriver'
user_data_path = '/root/userdata/'
log_path = test_path+'logs/'
os.environ["CHROME_LOG_FILE"] = log_path
wpr_path = '/root/go/pkg/mod/github.com/catapult-project/catapult/web_page_replay_go@v0.0.0-20230901234838-f16ca3c78e46/'

mount_custom_extension_dir = '/mnt/run/Arcanum/Sample_Extensions/Custom/'
custom_extension_dir = '/root/extensions/custom/'
recording_dir = '/root/recordings/'
annotation_dir = '/root/annotations/'
v8_log_path = '/ram/analysis/v8logs/'

url_mp = {
    'fb_post':'https://www.facebook.com/profile.php?id=100084859195049',
    'amazon_address':'https://www.amazon.com/a/addresses',
    'outlook_email':'https://outlook.live.com/mail/0/',
    'ins_profile':'https://www.instagram.com/xqgtiti/',
    'gmail_email': 'https://mail.google.com/mail/u/0/#inbox',
    'paypal_card': 'https://www.paypal.com/myaccount/money/cards/CC-DNGXYXA3SUS8Q',
    'linkedin_profile':'https://www.linkedin.com/in/amy-lee-gt/'
}

rules_map = {
    'amazon_address': "MAP *.amazon.com:80 127.0.0.1:8080,MAP *.amazon.com:443 127.0.0.1:8081,MAP *.media-amazon.com:80 127.0.0.1:8080,MAP *.media-amazon.com:443 127.0.0.1:8081,MAP *.amazon-adsystem.com:80 127.0.0.1:8080,MAP *.amazon-adsystem.com:443 127.0.0.1:8081,MAP *.ssl-images-amazon.com:80 127.0.0.1:8080,MAP *.ssl-images-amazon.com:443 127.0.0.1:8081,MAP *.cloudfront.net:80 127.0.0.1:8080,MAP *.cloudfront.net:443 127.0.0.1:8081,EXCLUDE localhost"
}

def deinit():
    print('==========================================================\n')
    os.system('pkill Xvfb')
    os.system('pkill chrome')
    os.system('pkill chromedriver')
    os.system('pkill wpr')

def init():
    if os.path.exists(custom_extension_dir) == False:
        os.system('mkdir -p %s'%custom_extension_dir)
    if os.path.exists(recording_dir) == False:
        os.system('mkdir -p %s'%recording_dir)
    if os.path.exists(annotation_dir) == False:
        os.system('mkdir -p %s'%annotation_dir)

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

    print('Start running Arcanum ... ')

def launch_driver(load_extension, extension_name, recording_name = None, rules = None):
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
    if recording_name != None:
        os.chdir(wpr_path)
        os.system('nohup go run src/wpr.go replay --http_port=8080 --https_port=8081 %s > %swprgo.log 2>&1 &'%(recording_dir+recording_name,log_path))
        options.add_argument('--host-resolver-rules=%s' % rules)
    # options.add_argument('--custom-script-idle-timeout-ms=30000000')
    prefs = {"profile.default_content_setting_values.notifications": 2}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def extract_raw_string(s):
    if "<String[1]:" in s: return s[14:-1]
    # To Extract the raw string ("/search") from cases like <String[7]: e"/search"> or <String[38]: "https://....">
    return s[s.find('"')+1:-2]


def source_document_location():
    print('\n==========================================================\nYou are testing taint source [DOM location]: ')
    print('Test extension name = Source_DOM_location, Test URL = https://www.google.com/search?q=Gatech')
    init()
    test_extension_name = 'Source_DOM_location'
    test_URL = 'https://www.google.com/search?q=Gatech'
    print('Start running Arcanum ... ')
    driver = launch_driver(True, test_extension_name)
    driver.get(test_URL)
    time.sleep(1)
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

    if success: print("Get expected taint sources in source logs: " +Back.GREEN+"Success"+Back.RESET+".")
    else: print("Get expected taint source logs: " +Fore.RED+"Fail"+Fore.RESET+".")

    deinit()

def source_document_property():
    print('\n==========================================================\nYou are testing taint source [Dom property]: ')
    print('Test extension name = Source_DOM_property, Test URL = https://www.google.com/search?q=Gatech')
    init()
    test_extension_name = 'Source_DOM_property'
    test_URL = 'https://www.google.com/search?q=Gatech'
    print('Start running Arcanum ... ')
    driver = launch_driver(True, test_extension_name)
    driver.get(test_URL)
    time.sleep(1)
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
    expect_sources = ['https://www.google.com/search?q=Gatech', 'www.google.com',
                      'Gatech - Google Search', 'username=Qinge Xie;']
    success = True
    for i in range(len(taint_sources)):
        if i == len(taint_sources)-1:
            if expect_sources[i] in extract_raw_string(taint_sources[i][1]): continue
        elif extract_raw_string(taint_sources[i][1]) == expect_sources[i]: continue
        success = False
        break

    if success:
        print("Get expected taint sources in source logs: " + Back.GREEN + "Success" + Back.RESET + ".")
    else:
        print("Get expected taint source logs: " + Fore.RED + "Fail" + Fore.RESET + ".")

    print('==========================================================\n')
    deinit()

def source_chrome_history():
    print('\n==========================================================\nYou are testing taint source [chrome.history]: ')
    test_extension_name = 'Source_Chrome_history'
    test_URL1 = 'https://www.google.com/search?q=Gatech'
    test_URL2 = 'https://scp.cc.gatech.edu/'
    print('Test extension name = %s, Test URLs = %s, %s'%(test_extension_name, test_URL1, test_URL2))
    init()
    # Generate history records
    driver = launch_driver(False, "")
    driver.get(test_URL1)
    driver.get(test_URL2)
    time.sleep(1)
    driver.quit()
    # Test the extension
    driver = launch_driver(True, test_extension_name)
    driver.get(test_URL1)
    time.sleep(1)
    driver.quit()

    print('End running Arcanum and start checking "/ram/analysis/v8logs/taint_sources.log":')
    # Check Taint Source Logs
    taint_sources = []
    lines = read_taint_source_log()
    for i in range(0, len(lines)):
        line = lines[i]
        if 'api_request_handler:history.getVisits' in line or 'api_request_handler:history.search' in line or \
                'event_emitter:history.onVisited' in line:
            next_line = lines[i + 1]
            object_address = next_line[:14]
            object_info = next_line[14:-1]
            taint_sources.append((object_address, object_info))
            print("[" + str(
                        len(taint_sources)) + '] Object Address: ' + object_address + '; Object Information: ' + object_info)
            continue

    # See the test extension source code for why we should get those expected sources.
    expect_sources = ['https://www.google.com/search?q=Gatech', 'https://scp.cc.gatech.edu/',
                       'School of Cybersecurity and Privacy', 'Gatech - Google Search',
                      'https://www.google.com/search?q=Gatech']
    success = True
    for i in range(len(taint_sources)):
        if extract_raw_string(taint_sources[i][1]) == expect_sources[i]:
            continue
        success = False
        break

    if success:
        print("Get expected taint sources in source logs: " + Back.GREEN + "Success" + Back.RESET + ".")
    else:
        print("Get expected taint source logs: " + Fore.RED + "Fail" + Fore.RESET + ".")
    print('==========================================================\n')
    deinit()

def source_chrome_cookies():
    test_extension_name = 'Source_Chrome_cookies'
    test_URL1 = 'https://www.cookiesget_example.com/'
    test_URL2 = 'https://www.cookiesgetall_example.com/'
    print('\n==========================================================\nYou are testing taint source [chrome.cookies]: ')
    print('Test extension name = %s, Test URL = %s, %s'%(test_extension_name, test_URL1, test_URL2))
    init()
    print('Start running Arcanum ... ')
    driver = launch_driver(True, test_extension_name)
    time.sleep(1)
    driver.quit()

    taint_sources = []
    lines = read_taint_source_log()
    for i in range(0, len(lines)):
        line = lines[i]
        if 'from api_request_handler:cookies.get' in line:
            next_line = lines[i+1]
            object_address = next_line[:14]
            object_info = next_line[14:-1]
            taint_sources.append((object_address, object_info))
            print("["+str(len(taint_sources)) + '] Object Address: ' + object_address + '; Object Information: '+ object_info)
            continue

    # See the test extension source code for why we should get those expected sources.
    expect_sources = ['www.cookiesget_example.com', 'foo', '/', 'foo_val',
                      'www.cookiesgetall_example.com', 'bar', '/', 'bar_val']
    success = True
    for i in range(len(taint_sources)):
        if extract_raw_string(taint_sources[i][1]) == expect_sources[i]: continue
        success = False
        break

    if success: print("Get expected taint sources in source logs: " + Back.GREEN + "Success" + Back.RESET + ".")
    else: print("Get expected taint source logs: " + Fore.RED + "Fail" + Fore.RESET + ".")

    deinit()


def source_chrome_webNavigation():
    test_extension_name = 'Source_Chrome_webNavigation'
    test_URL1 = 'https://www.google.com/'
    test_URL2 = 'https://www.gatech.edu/'
    print('\n==========================================================\nYou are testing taint source [chrome.webNavigation]: ')
    print('Test extension name = %s, Test URL = %s, %s' % (test_extension_name, test_URL1, test_URL2))
    init()
    print('Start running Arcanum ... ')
    driver = launch_driver(True, test_extension_name)
    driver.get(test_URL1)
    time.sleep(1)
    driver.get(test_URL2)
    time.sleep(1)
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

    if success: print("Get expected taint sources in source logs: " + Back.GREEN + "Success" + Back.RESET + ".")
    else: print("Get expected taint source logs: " + Fore.RED + "Fail" + Fore.RESET + ".")

    deinit()

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


def source_chrome_tabs():
    test_extension_name = 'Source_Chrome_tabs'
    init()
    driver = launch_driver(True, test_extension_name)
    driver.switch_to.new_window('tab')
    time.sleep(2)
    driver.close()
    deinit()

def source_chrome_webRequest():
    test_extension_name = 'Source_Chrome_webRequest'
    test_URL1 = 'https://yuanbin.xyz/test/'
    test_URL2 = 'https://gatech.edu'
    recording_name = 'custom.wprgo'
    rules = "MAP *.gatech.edu:80 127.0.0.1:8080,MAP *.gatech.edu:443 127.0.0.1:8081,MAP yuanbin.xyz:80 127.0.0.1:8080,MAP yuanbin.xyz:443 127.0.0.1:8081,EXCLUDE localhost"
    print('\n==========================================================\nYou are testing taint source [chrome.webNavigation]: ')
    print('Test extension name = %s, Test URL = %s, %s' % (test_extension_name, test_URL1, test_URL2))

    init()
    print('Start running Arcanum ... ')
    driver = launch_driver(True, test_extension_name, recording_name, rules)
    driver.get(test_URL1)  # Test "set-cookie" value in responseHeaders
    driver.get(test_URL1)  # Test "cookie" value in requestHeaders then
    driver.get(test_URL2)  # Test  url, ip, and initiator of chrome.webRequest.onCompleted
    time.sleep(1)
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

    if success: print("Get expected taint sources in source logs: " + Back.GREEN + "Success" + Back.RESET + ".")
    else: print("Get expected taint source logs: " + Fore.RED + "Fail" + Fore.RESET + ".")

    deinit()

def source_web_userAgent():
    test_extension_name = 'Source_Web_userAgent'
    print('\n==========================================================\nYou are testing taint source [chrome.webNavigation]: ')
    print('Test extension name = %s' % (test_extension_name))

    init()
    print('Start running Arcanum ... ')
    driver = launch_driver(True, test_extension_name)
    time.sleep(1)
    driver.quit()
    deinit()

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

def source_document_password():

    test_URL = "https://yuanbin.xyz/test/"
    test_extension_name = 'Source_DOM_password'
    recording_name = 'custom.wprgo'
    print('\n==========================================================\nYou are testing taint source [Dom Input Element <input type=“password”> ]: ')
    # print('Test extension name = %s, Test URL = %s'%(test_extension_name, test_URL))
    init()

    if in_debug:
        os.system('rm -rf %s%s'%(custom_extension_dir,test_extension_name))
        os.system('cp -r %s%s %s'%(mount_custom_extension_dir, test_extension_name, custom_extension_dir))

    check_file_exist(test_extension_name,  recording_name, None)

    rules = "MAP yuanbin.xyz:80 127.0.0.1:8080,MAP yuanbin.xyz:443 127.0.0.1:8081,EXCLUDE localhost"
    driver = launch_driver(True, test_extension_name, recording_name, rules)
    driver.get(test_URL)
    time.sleep(1)
    driver.quit()

    source_blocks = parse_taint_source_log()
    success = False

    for i in range(len(source_blocks)):
        if '<String[8]: e"mypasswd">' in source_blocks[i][0]:
            success = True
            break
        print(source_blocks[i][0])

    if success: print("Get expected taint sources in source logs: " + Back.GREEN + "Success" + Back.RESET + ".")
    else: print("Get expected taint source logs: " + Fore.RED + "Fail" + Fore.RESET + ".")

    deinit()

def Amazon_Extension_MV2_Test():
    target_page = 'amazon_address'
    test_URL = url_mp[target_page]
    extension_name = '%s_mv2.crx'%target_page
    recording_name = '%s.wprgo'%target_page
    anotation_name = '%s.js'%target_page
    rules = rules_map[target_page]

    check_file_exist(extension_name = extension_name, recording_name = recording_name, annotation_name = anotation_name)

    init()

    driver = launch_driver(load_extension = True, extension_name = extension_name, recording_name = recording_name, rules = rules)
    time.sleep(1)
    driver.get(test_URL)
    time.sleep(1)
    # driver.save_screenshot('my.png')
    driver.quit()

    deinit()



if __name__ == '__main__':
    Amazon_Extension_MV2_Test()
    #source_document_password()
    # source_web_userAgent()
    # source_chrome_webRequest()
    # source_chrome_tabs()
    # source_chrome_webNavigation()
    # source_chrome_cookies()
    # source_chrome_history()
    # source_document_location()
    # source_document_property()
