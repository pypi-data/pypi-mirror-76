from selenium import webdriver
import time


class Slider:

    def __init__(self , driver , xpathData , noOfImages):
        self.xpathData = xpathData
        self.noOfImages = noOfImages 
        self.driver = driver

    def setup(self ):
        pass
        

    def getXpath(self,xpath , driver):
        element = driver.find_element_by_xpath(xpath)
        if element.is_displayed():
            return element
        else:
            raise "Some error"

    def clickActions(self,xpathData,driver):
        for elemXPath in xpathData:
            ele = self.getXpath(elemXPath,driver)
            ele.click()


    def sliderClick(self,noOfImages, buttonXPath, driver):
        for i in range(noOfImages):
            rightArrow = self.getXpath(buttonXPath,driver)
            rightArrow.click()
            time.sleep(1)
            if i == noOfImages:
                i = 0

    def teardown(self,driver):
        print("All is Well")
        driver.quit()
