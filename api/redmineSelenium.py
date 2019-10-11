import time
import os
from selenium import webdriver
from selenium.webdriver.support.select import Select
from redminelib import Redmine
from flask import Flask

app = Flask(__name__)
import logging
app.logger.setLevel(logging.INFO)
redmineUrl = os.getenv('REDMINE_URL')

def seleniumRedmine(username, password, name):
    app.logger.info("Redmine username is %s, password is %s, name is %s" %(username,password,name))
    redmine = Redmine(redmineUrl, username=username, password=password)
    id = list(redmine.issue.all(limit=100).filter(project__id=36, assigned_to__name=name, status__name='New').values('id'))
    try:
        if id:
            # print(id)
            issues_id = id[0]['id']
            issue = redmine.issue.get(issues_id)
            app.logger.info("issues_id is %s" %issues_id)
            app.logger.info("issue is %s" %issue)
            selenium_firefox(username, password, issues_id)
            result = "%s:%s 已完成" % (issue, issues_id)
        else:
            # issues_id = 0
            app.logger.warn("no issue in %s" %name)
            # selenium_firefox(username, password, issues_id)
            result = "no issue in" + name
    except Exception as e:
        # print(e.message)
        app.logger.warn(e)
        result = "error:" + e
    return result


def selenium_firefox(username,password,issues_id):
    pwd = os.getcwd()
    pjs_dir = pwd + "/phantomjs"
    driver = webdriver.PhantomJS(pjs_dir)
    driver.maximize_window()
    if issues_id:
        driver.get(redmineUrl + "/issues/" + issues_id)
        driver.find_element_by_id("username").send_keys(username)
        driver.find_element_by_id("password").send_keys(password)
        driver.find_element_by_name("login").click()
        # driver.save_screenshot('static/img/issues_id.jpg')
        app.logger.info("open issues")
        driver.find_element_by_xpath('//*[@id="content"]/div[1]/a[1]').click()
        time.sleep(1)
        selector1 = Select(driver.find_element_by_xpath('//*[@id="issue_status_id"]'))
        selector1.select_by_visible_text("Resolved")
        selector2 = Select(driver.find_element_by_xpath('//*[@id="issue_done_ratio"]'))
        selector2.select_by_value("100")
        time.sleep(1)
        for i in range(15):
            driver.find_element_by_xpath('//*[@id="issue_checklists_attributes_%s_is_done"]' % i).click()
        time.sleep(1)
        app.logger.info("submit issues")
        driver.find_element_by_xpath('//*[@id="issue-form"]/input[6]').click()
        app.logger.info("close chrome")
        time.sleep(3)
        driver.close()
    else:
        # print("no issue")
        app.logger.warn("no issue")
