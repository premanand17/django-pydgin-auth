''' Test JS in search engine app. '''
from django.test import TestCase
from django.conf import settings
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)
BROWSERS = []
BROWSERS_SIZES = [[1000, 800]]

SELENIUM = getattr(settings, 'SELENIUM', {})
logger.debug(SELENIUM)
HEADLESS = SELENIUM.get('HEADLESS', True)
HOST = SELENIUM.get('HOST', "http://localhost:8000")
HOST = "http://prem-rh1:8000"


def setUpModule():
    ''' Open browsers for testing. '''
    global BROWSER

    if HEADLESS:
        display = Display(visible=0, size=(1000, 800))
        display.start()

    BROWSERS.append(webdriver.Firefox())
    # BROWSERS.append(webdriver.Chrome(SELENIUM.get('CHROME_DRIVER', "")))
    # BROWSERS.append(_get_opera_driver())


def tearDownModule():
    ''' Close web browsers. '''
    for br in BROWSERS:
        br.quit()


def _get_opera_driver():
    ''' Use OperaChromiumDriver for Opera testing.
    L{https://github.com/operasoftware/operachromiumdriver}
    L{https://github.com/operasoftware/operachromiumdriver/blob/master/docs/python-setup-step-by-step.md}
    L{https://github.com/operasoftware/operachromiumdriver/blob/master/docs/desktop.md}
    '''
    webdriver_service = service.Service(SELENIUM.get('OPERA_DRIVER', ""))
    webdriver_service.start()
    desired_caps = DesiredCapabilities.OPERA
    desired_caps['operaOptions'] = {'binary': SELENIUM.get('OPERA_BIN', "/usr/bin/opera")}
    return webdriver.Remote(webdriver_service.service_url, desired_caps)


class AuthorizationTest(TestCase):

    def test_login(self):
        ''' Test auto-suggest '''
        for br in BROWSERS:
            for br_size in BROWSERS_SIZES:
                br.set_window_size(br_size[0], br_size[1])

                br.get(HOST+'/accounts/login/')
                time.sleep(0.2)

                username_ele = br.find_element_by_id("id_username")
                pass_ele = br.find_element_by_id("id_password")
                self.assertTrue(username_ele.is_displayed())
                self.assertTrue(pass_ele.is_displayed())

                username_ele.send_keys("prem_ro")
                pass_ele.send_keys("test123")

                # Locate Login button and click it
                br.find_element_by_xpath('//input[@value="login"]').click()
                html_source = br.page_source
                self.assertTrue("Search" in html_source, "Logout present in html_source")
                self.assertTrue("prem_ro" in html_source, "prem_ro present in html_source")
                self.assertTrue("Logout" in html_source, "Logout present in html_source")
