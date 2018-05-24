from selenium import webdriver
your_name = input("Enter Your Name: ")
crush_name = input("Enter Your Crush's Name: ")
browser = webdriver.Firefox()
browser.get("http://www.ultimatelovecalc.com/")
try:
    fname = browser.find_element_by_id("fname")
    fname.send_keys(your_name)
    cname = browser.find_element_by_id("cname1")
    cname.send_keys(crush_name)
    cname.submit()
except:
    print("Could not find Element(s)")
#submit_button = browser.find_element_by_link_text('Calculate')
#submit_button.click()