import os
import mainlib as run
import time
import random as rn


linkedin_username = 'keshavkantsingh.darkest@gmail.com'
linkedin_password = 'k@8090551004'
instant_id = 0
search_limit_url = 100
url_table = 'chunk.linkedin_url_cntry_de'
dir_path = 'C:\\Users\\Administrator\\Desktop\\driver\\'

while True:    
    strt_tm = time.time()
    driver = run.get_driver('C:\\Users\\Administrator\\Desktop\\driver\\chromedriver.exe',
                            browser = 'chrome',
                            _PROXY_HOST= '' ,
                            _PROXY_PORT=23750,
                            _USERNAME='singh4',
                            _PASSWORD='ghh7jr5',
                            _url_table = url_table,
                            _instant_id = instant_id,
                            _search_limit_url = search_limit_url,
                            _dir_path = dir_path,
                            db=False)    
    
    if driver != False:
        run.action_linkedin_login(driver,linkedin_username , linkedin_password)
        run.scarp(driver)
        driver.quit()
    end_tm = time.time()
    diff_tm = int(end_tm - strt_tm)
    if diff_tm < 14400:
        slep_tm = 14400 - diff_tm + rn.randint(3600,7200)
        print('waiting', slep_tm)
        time.sleep(slep_tm)
    else:
        print('waiting normal')
        time.sleep(rn.randint(3600,7200))

