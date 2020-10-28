import threading
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

################################################################
# 必填设置
# 你想报列表里的第几科，从1开始
# 改为None（不加引号，注意大小写）以每次手动选择
SUBJECT_INDEX = 1
# 你想同时开多少个浏览器窗口操作，正整数
THREADS_COUNT = 1
# APID
AP_ID = ''
# 姓的拼音
STUDENT_LAST_NAME = ''
# 身份证号
GOV_ID = ''  # #GOVID
# 姓的拼音
LEGAL_LAST_NAME = ''  # #Legal Last (Family) Name
# 名的拼音
LEGAL_FIRST_NAME = ''  # #Legal First (Given) Name
# 姓的中文
LEGAL_LAST_NAME_CHINESE = ''  # #Legal Last (Family) Name in Chinese
# 名的中文
LEGAL_FIRST_NAME_CHINESE = ''  # #Legal First (Given) Name in Chinese
# 出生日期，格式为‘YYYY/MM/DD’
BIRTH_DATE = ''  # name: mydate
# 性别，'Male' 或者 'Female'
GENDER = ''  # #GENDER > option[value="Male"] (or Female)
# 手机号，不用+86
MOBILE_PHONE = ''  # #M_PHONE
# 地址行1
ADDRESS1 = ''  # #ADDRESS1
# 地址行2（选填）
ADDRESS2 = ''  # #ADDRESS2
################################################################

# 下面的可以不用改
CITY = '北京, 中国'
GOV_ID_COUNTRY = 'China'  # #GOV_ID_COUNTRY
CITY_ = 'Beijing'  # #CITY
COUNTRY = 'CHINA'  # select#COUNTRY > option[value="CHINA"]
GRADE = '11th Grade'  # select#Grade > option[value="11th Grade"]
PREFERRED_LANGUAGE = 'I do not wish to respond'  # select#Preferred Language > option[value="I do not wish to respond"]
PARENT1_EDU_LEVEL = 'I do not wish to respond'  # select#Parent/Guardian 1 Education Level > option[value="I do not wish to respond"]

# 不要改
INDEX_URL = 'https://proscheduler.prometric.com/home'
INFO_BY_ID = [
    {'id': 'GOV_ID', 'content': GOV_ID},
    {'id': 'GOV_ID_COUNTRY', 'content': GOV_ID_COUNTRY},
    {'id': 'Legal Last (Family) Name', 'content': LEGAL_LAST_NAME},
    {'id': 'Legal First (Given) Name', 'content': LEGAL_FIRST_NAME},
    {'id': 'Legal Last (Family) Name in Chinese', 'content': LEGAL_LAST_NAME_CHINESE},
    {'id': 'Legal First (Given) Name in Chinese', 'content': LEGAL_FIRST_NAME_CHINESE},
    {'id': 'M_PHONE', 'content': MOBILE_PHONE},
    {'id': 'ADDRESS1', 'content': ADDRESS1},
    {'id': 'ADDRESS2', 'content': ADDRESS2},
    {'id': 'CITY', 'content': CITY_},
]


def wait_for(browser: webdriver, by: By, element: str):
    try:
        browser.find_element(by, element)
    except NoSuchElementException:
        sleep(1)
        wait_for(browser, by, element)
        return


def wait_for_id(browser: webdriver, element_id: str):
    return wait_for(browser, By.ID, element_id)


def wait_for_class(browser: webdriver, element_class: str):
    return wait_for(browser, By.CLASS_NAME, element_class)


def click_button(browser: webdriver, element_id: str):
    try:
        browser.find_element_by_id(element_id).click()
    except NoSuchElementException:
        sleep(1)
        click_button(browser, element_id)
        return
    except ElementClickInterceptedException:
        sleep(1)
        click_button(browser, element_id)
        return


def next_step(browser: webdriver):
    click_button(browser, 'nextBtn')


def previous_step(browser: webdriver):
    click_button(browser, 'prevBtn')


def fuck_prometric():
    def select(select_id: str, value: str):
        element = browser.find_element_by_id(select_id)
        element.send_keys(Keys.TAB)
        selector = Select(element)
        selector.select_by_value(value)
        # selector = 'select#' + select_id + '>option[value="' + value + '"]'
        # browser.find_element_by_css_selector(selector).click()

    def next_step_():
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        wait_for_class(browser, 'tempSucBtn')
        browser.execute_script("arguments[0].click();", browser.find_element_by_class_name('tempSucBtn'))

    global INDEX_URL, AP_ID, STUDENT_LAST_NAME, CITY, GOV_ID, GOV_ID_COUNTRY, LEGAL_FIRST_NAME, LEGAL_LAST_NAME, \
        LEGAL_FIRST_NAME_CHINESE, LEGAL_LAST_NAME_CHINESE, BIRTH_DATE, GENDER, MOBILE_PHONE, ADDRESS1, ADDRESS2, \
        CITY_, COUNTRY, GRADE, PREFERRED_LANGUAGE, PARENT1_EDU_LEVEL, INFO_BY_ID, SUBJECT_INDEX
    option = webdriver.ChromeOptions()
    option.add_experimental_option('useAutomationExtension', False)
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_experimental_option("detach", True)
    browser = webdriver.Chrome(options=option)
    # browser = webdriver.Firefox()
    browser.get(INDEX_URL)
    # 选中文
    wait_for_class(browser, 'language-picker')
    browser.find_element_by_class_name('language-picker') \
        .find_element_by_css_selector('option[value="Chinese"') \
        .click()
    # 安排
    browser.find_element_by_css_selector('img[src="/dist/assets/images/Schedule.png"]') \
        .click()
    # 选AP考试
    wait_for_id(browser, 'selectClient')
    browser.find_element_by_id('selectClient') \
        .find_element_by_xpath('//option[contains(text(),"College Board - AP Exams")]') \
        .click()
    wait_for_id(browser, 'selectProgram')
    browser.find_element_by_id('selectProgram') \
        .find_elements_by_tag_name('option')[1] \
        .click()
    next_step(browser)
    # 没用的提示
    next_step(browser)
    # 本人确认...  我同意...
    wait_for_class(browser, 'form-check')
    browser.find_element_by_name('chkPolicy').send_keys(Keys.TAB)
    while True:
        try:
            browser.find_element_by_name('chkConsent').find_element_by_xpath('.//..').click()
            browser.find_elements_by_name('chkPolicy')[0].find_element_by_xpath('.//..').click()
        except ElementClickInterceptedException:
            sleep(1)
        else:
            break
    browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    next_step(browser)
    # 资格信息
    wait_for_id(browser, 'ELIGIBILITY_NUMBER')
    browser.find_element_by_id('ELIGIBILITY_NUMBER') \
        .send_keys(AP_ID)
    browser.find_element_by_id('LAST_NAME') \
        .send_keys(STUDENT_LAST_NAME)
    browser.find_element_by_class_name('textSucBtn') \
        .click()
    # 选科目
    wait_for_class(browser, 'exam-detail-block')
    subject_rows = browser.find_elements_by_class_name('exam-detail-block')[1] \
        .find_elements_by_xpath('.//div[@class="row"]')
    subjects = []
    for subject_row in subject_rows:
        subjects.append({
            'name': subject_row.find_element_by_tag_name('h5').text,
            'radio': subject_row.find_element_by_name('selectedExam'),
        })
    if SUBJECT_INDEX is None:
        print('请选择你要报考的科目: ')
        for i in range(len(subjects)):
            print(i + 1, subjects[i]['name'])
        radio = subjects[int(input()) - 1]['radio']
    else:
        radio = subjects[SUBJECT_INDEX - 1]['radio']
    radio.send_keys(Keys.TAB)
    radio.click()
    # 这个页面还有一个隐藏起来的#nextBtn，且优先级比能按的高，所以按类选择
    next_step_()
    new_page = True
    if not new_page:
        # 选城市
        # 于2020 Oct. 29th 00:00失效，改为选国家页面
        # 又在同一天 00:17左右 改了回来
        # 又在00:40左右 改为选择国家
        wait_for(browser, By.CSS_SELECTOR, 'input.form-control[placeholder="地址，城市或邮编/邮政编码"]')
        browser.find_element_by_css_selector('input.form-control[placeholder="地址，城市或邮编/邮政编码"]') \
            .send_keys('北京, 中国')
        wait_for(browser, By.CSS_SELECTOR, 'button.dropdown-item')
        browser.find_element_by_css_selector('button.dropdown-item').click()
        next_step_()
    else:
        # 选国家
        wait_for_id(browser, 'selectCountryList')
        for i in browser.find_element_by_id('selectCountryList').find_elements_by_tag_name('option'):
            if i.text.count(COUNTRY) != 0:
                i.click()
        next_step(browser)
    # 选考场
    sleep(1)
    while True:
        wait_for_class(browser, 'testCenterMonth')
        browser.find_element_by_class_name('testCenterMonth').click()
        sleep(3)
        try:
            warning = browser.find_element_by_css_selector('div.text-left.warning-text')
        except NoSuchElementException:
            break
        else:
            print('没有座位')
            browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            previous_step(browser)
            sleep(2)
            next_step_()
    wait_for(browser, By.CSS_SELECTOR, 'div.card-heading.card-heading-sm.testcenterTimeDate')
    browser.find_element_by_css_selector('div.card-heading.card-heading-sm.testcenterTimeDate').find_element_by_xpath('.//../..').click()
    browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    next_step(browser)
    wait_for_id(browser, 'GOV_ID')

    def fill_by_id(element_id: str, content: str):
        browser.find_element_by_id(element_id).send_keys(content)

    for info in INFO_BY_ID:
        fill_by_id(info['id'], info['content'])
    # browser.find_element_by_name('mydate').send_keys(BIRTH_DATE)
    browser.execute_script('arguments[0].value = "' + BIRTH_DATE + '"', browser.find_element_by_name('mydate'))
    select('GENDER', GENDER)
    select('COUNTRY', COUNTRY)
    select('Grade', GRADE)
    select('Preferred Language', PREFERRED_LANGUAGE)
    select('Parent/Guardian 1 Education Level', PARENT1_EDU_LEVEL)
    browser.execute_script("arguments[0].removeAttribute(arguments[1])",
                           browser.find_element_by_class_name('tempSucBtn'),
                           'disabled')
    next_step_()
    print('自动填充完毕')


if __name__ == '__main__':
    threads = []
    for i in range(THREADS_COUNT):
        threads.append(threading.Thread(target=fuck_prometric))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()