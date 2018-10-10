import os
import mainlib1 as run
import time
import random as rn


linkedin_username = "keshavjain16@outlook.com"
linkedin_password = "P"
instant_id = 0
search_limit_url = 100
url_table1 = 'prod.workondomain'
dir_path = 'C:\\Users\\Administrator\\Desktop\\'
min_time = 3600

while True:    
    strt_tm = time.time()
    driver = run.get_driver(r'C:\Users\ksingh\Desktop\new ui\chromedriver.exe',
                            browser = 'chrome',
                            _PROXY_HOST= '' ,
                            _PROXY_PORT=23750,
                            _USERNAME='singh4',
                            _PASSWORD='ghh7jr5',
                            _url_table = url_table1,
                            _instant_id = instant_id,
                            _search_limit_url = search_limit_url,
                            _dir_path = dir_path,
                            db=False)    
    
    if driver != False:
        run.action_linkedin_login(driver,linkedin_username , linkedin_password)
        run.run_company_extraction(driver)
        driver.quit()
    end_tm = time.time()
    diff_tm = int(end_tm - strt_tm)
    if diff_tm < min_time:
        slep_tm = min_time - diff_tm + rn.randint(3600,7200)
        print('waiting', slep_tm)
        time.sleep(slep_tm)
    else:
        print('waiting normal')
        time.sleep(rn.randint(3600,7200))

