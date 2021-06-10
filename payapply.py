"""
Automating cart adding for multi-person to mailing on book website
Setup selenium client package and Chromewebdriver.
Search the Books4school website, inspect to get element names from the html file. 
Get user booking information from Google Sheet by Google doc API.    
Use Python to implement automatically adding books to the shopping cart. 
"""
import time
from selenium import webdriver
from googlesheet import getsheetvalues
def addbookbyISBN(driver,isbn,amount):
    search_box = driver.find_element_by_name('substring')
    search_box.send_keys(isbn)
    search_box.submit()
    time.sleep(1.5) # Let the user actually see something!
    try:
        booklink = driver.find_element_by_class_name('fn.url.next-previous-assigned')
    except:
        print('Out of Stock :', isbn)
        return
    booklink.click()
    time.sleep(1)
    addamount = driver.find_element_by_name('amount')
    addamount.clear()
    addamount.send_keys(amount)
    addbook = driver.find_element_by_class_name('btn.regular-button.regular-main-button.add2cart.submit')
    addbook.click()
    time.sleep(1)  
def driverinit():
    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir=/Users/chenzhang/ChromeProfile")
    options.add_argument("--profile-directory=Profile 1")
    driver = webdriver.Chrome(chrome_options=options)  # Optional argument, if not specified will search path.
    driver.get('https://www.books4school.com')
    return driver
def main():
    values = getsheetvalues() # get book number and amount list from googlesheet
    driver = driverinit() # init Chrome get handle 
    time.sleep(1) # Let the user actually see something!
    for row in values[:-1]:
        if row[0] != None and row[1] != '0':
            addbookbyISBN(driver,row[0],row[1])

if __name__ == '__main__':
    main()