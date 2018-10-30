


from time import sleep
import re
from random import randint
from datetime import datetime
import time
import os
from selenium import webdriver
import chromewithproxy
import connection as connect
from selenium.webdriver.common.keys import Keys

search_limit_url = 100
dir_path = os.path.dirname(os.path.realpath(__file__))
error_log = ''



#df = pd.read_csv(r"D:\linkedin crawling\udc csv\job functon search.csv",encoding='ISO_8859_5')
#df_job_level = pd.read_csv(r"D:\linkedin crawling\udc csv\job level search .csv",encoding='ISO_8859_5')

def get_jcriteria_search(df,jobtitle):
    title = jobtitle.lower()
    for index, row in df.iterrows():
        search_term = row['search'].lower()
        criteria = row['criteria'].lower()
        #print(search_term,criteria )
        if criteria == 'contains' and search_term in title:
            return row['return']
        if criteria == 'begins' and title.startswith(search_term, 0,len(title)) == search_term:
            return row['return']
        if criteria  == 'end' and title[len(title) - len(search_term):] == search_term:
            return row['return']
        
def create_url(profile_country,employee_size,industry_type,total_exp, cur_pos_yr,ui_type=1, trackingInfoJson="", logid= ""):
    url = ""
    if ui_type == 1:
        url = ["https://www.linkedin.com/sales/search?facet=G&facet=I&facet=CS&facet=YP&facet=TE&" ,
        "&facet.G=" , profile_country , "%3A0" ,
        "&facet.I=" , industry_type ,
        "&facet.CS=" , employee_size ,
        "&facet.YP=" , cur_pos_yr ,
        "&facet.SE=8&facet.SE=7&facet.SE=6&facet.SE=5&facet.SE=4"
        "&facet.TE=" , total_exp ,
        "&count=25&start=0&EL=auto&updateHistory=true&trackingInfoJson.contextId=" , trackingInfoJson]
    if ui_type == 2:
        url = ["https://www.linkedin.com/sales/search/people?" ,
        "companySize=" , employee_size ,
        "&geo=" , profile_country , "%3A0" ,
        "&industry=" , industry_type ,
        "&logHistory=true" ,
        "&logId=" , str(logid) ,
        "&page=1" ,
        "&searchSessionId=" , trackingInfoJson ,
        "&seniority=4%2C5%2C6%2C7%2C8",
        "&tenureAtCurrentPosition=" , cur_pos_yr ,
        "&yearsOfExperience=" , total_exp]
    
    return ''.join(str(e) for e in url)

def check_ui_type(driver):
    try:
        driver.find_element_by_css_selector('.collapsible-container')
        return 2
    except:
        return 1 

def get_loginid_tractsess(driver,ui_type=1):
    if ui_type == 1:
        sleep(5)
        log_mesage('old ui')
        log_mesage('excludes-suggestion 1')
        driver.find_element_by_class_name('excludes-suggestion-link').click()
        sleep(randsec())
        log_mesage('excludes-suggestion 2')
        driver.find_element_by_class_name('excludes-suggestion-link').click()
        sleep(randsec())
    elif ui_type == 2:
        log_mesage('new ui')
        log_mesage('keyword 1')
        keyword_input = driver.find_element_by_xpath("//input[@placeholder='Enter keywords …']")
        keyword_input.clear()
        keyword_input.send_keys('dell')
        keyword_input.send_keys(Keys.RETURN)
        sleep(10)
        keyword_input.clear()
        log_mesage('keyword 2')
        keyword_input.send_keys('accenture')
        keyword_input.send_keys(Keys.RETURN)
        sleep(10)
        
def get_param_from_url(url, ui_type=1):
    query_param = url.split('?')[-1]
    params = dict(x.split('=') for x in query_param.split('&'))   
    if ui_type ==1:
        return  params['trackingInfoJson.contextId'],params['searchHistoryId']
    if ui_type ==2: 
        return  params['logId'],params['searchSessionId']


def hideglobalhelp(driver,ui_type=1):   
    if ui_type==1:
        driver.execute_script("document.getElementsByClassName('global-nav-help-section')[0].style.visibility='hidden'; ")
        log_mesage('hidding global buton')
    elif ui_type==2:
        try:
            driver.execute_script("document.getElementsByClassName('global-nav-help-button')[0].style.visibility='hidden'; ")
            log_mesage('new ui - hidding global buton1')
        except:
            driver.execute_script("$('.global-nav-help-button').hide(); ")
            log_mesage('new ui - hidding global buton2')
            pass


def get_searched_count(driver,ui_type=1):
    if ui_type==1:
        return profile_count(getDataByClass(driver,'spotlight-result-count'))
    elif ui_type==2:
        return driver.find_elements_by_css_selector('.artdeco-tab-primary-text')[0].text.replace(",","")

def click_next_pagination(driver,ui_type=1):
    scrap = False
    if ui_type==1:
        try:
            driver.find_element_by_xpath('//*[@id="pagination"]/a[2]').click()
            scrap = True
        except:
            sleep(randsec())
            try:
                driver.find_element_by_xpath("//*[@class='next-pagination page-link']").click()
                scrap = True
            except:
                try:
                    sleep(randsec())
                    driver.find_element_by_xpath("//*[@class='next-pagination page-link']").click()
                    scrap = True
                except:
                    scrap = False
                    print('clicking next pagination - error')
    elif ui_type==2:
         sleep(randsec())
         try:
            print('click next try 1')
            driver.find_element_by_class_name("search-results__pagination-next-button").click()
            scrap = True
         except:
            try:
                sleep(randsec())
                print('click next try 2')
                driver.find_element_by_class_name("search-results__pagination-next-button").click()
                scrap = True
            except:
                scrap = False
                print('clicking next pagination - error')
    return scrap

def fetch_profile_attributes(profile, ui_type=1):
    l_first_name = l_last_name = l_mid_name = address = job_title = rolein = profile_name =profile_link = company_link = company_name = ""
    if ui_type==1:
        profile_name = getDataByClass( profile,'name')
        profile_link = getDataByClass( profile,'.name > a','href')
        company_link = getDataByClass( profile,'.company-name','href')
        company_name = getDataByClass( profile,'company-name')
        job_info = ""
        try:
            job_info =  profile.find_element_by_css_selector('.info').text.strip()
        except:
            job_info = ""
        job_title , rolein , address =jobinfo_split(job_info)        
        if profile_name != '' and  (re.match('^[\s\w-]+$', profile_name) is not None):
            l_first_name , l_mid_name ,l_last_name  = usernames(profile_name)
        return l_first_name , l_last_name , l_mid_name , address ,job_info, job_title , rolein , profile_name , profile_link , company_link , company_name 
    if ui_type==2:
        profile_name = getDataByClass( profile,'result-lockup__name')
        profile_link = getDataByClass( profile,'.result-lockup__name > a','href')
        company_link = getDataByClass( profile,'.result-lockup__position-company > a','href')
        company_name = getDataByClass( profile,'result-lockup__position-company')
        job_info = ""
        try:
            job_title =  profile.find_element_by_css_selector('.result-lockup__highlight-keyword > span').text.strip()
        except:
            job_title = ""
        if profile_name != '' and  (re.match('^[\s\w-]+$', profile_name) is not None):
            l_first_name , l_mid_name ,l_last_name  = usernames(profile_name)
        try:
            address =  profile.find_element_by_css_selector('.result-lockup__misc-item').text.strip()
        except:
            address = ""
        try:
            rolein =  profile.find_element_by_css_selector('div.horizontal-person-entity-lockup-4.result-lockup__entity.ml4 > dl > dd:nth-child(4) > span').text.strip()
        except:
            pass
        return l_first_name , l_last_name , l_mid_name , address ,job_info, job_title , rolein , profile_name , profile_link , company_link , company_name 
    
def create_date_folder(path):
    datetoday =path  + datetime.now().strftime('%Y/%m/%d')
    if not os.path.exists(datetoday):
        os.makedirs(datetoday)
    return datetoday
        
def savehtml(filename, html):
    time = datetime.today().strftime('%Y/%m/%d')
    folder =dir_path + '\\html\\' + time 
    if not os.path.exists(folder):
        os.makedirs(folder)
    file = filename + '.html'
    f = open(folder + file, 'w')
    f.write(html.encode('utf-8'))
    f.close()

def check_more_pagination(driver, ui_type=1):
    if ui_type==1:
        try:
            el3 = driver.find_element_by_xpath("//*[@class='next-pagination page-link disabled']") 
            return False
        except:
            return True
    elif ui_type==2:
        try:
            print('is next enabled')
            el3 = driver.find_elements_by_css_selector(".search-results__pagination-next-button")[0].get_property('disabled')
            if el3 ==  False:
                return True
            else:
                return False
        except:
            print('error false')
            return False
   
def usernames(name):
    zen_first_name = zen_last_name = zen_mid_name = ""
    user_name = name.split(' ')
    if len(user_name) == 1:
        zen_first_name = user_name[0]
        zen_last_name = ''
        zen_mid_name = ''
    elif len(user_name) == 2:
        zen_first_name = user_name[0]
        zen_mid_name = ''
        zen_last_name = user_name[1]
    elif len(user_name) > 2:
        zen_first_name = user_name[0]
        zen_last_name = user_name[-1]
        zen_mid_name = ' '.join(user_name[1:len(user_name)-1]).strip()
    return zen_first_name ,  zen_mid_name, zen_last_name

def jobinfo_split(jobinfo):
    jobtitle = rolein = address = ""
    job = jobinfo.split('\n')
    if len(job) == 1:
        jobtitle = ''
        rolein = ''
        address = ''
    elif len(job) == 2:
        if 'role' in job[1] :
            rolein = job[1]
            jobtitle = job[0]
        if 'role' in job[0] :
            rolein = job[0]
            address = job[1]
    elif len(job) == 3:
        jobtitle = job[0]
        rolein = job[1]
        address = job[2]
    return jobtitle , rolein , address


def getDataByClass(driver_object, classname, _type="text"):
    try:
        if _type == "text":
            return driver_object.find_element_by_class_name(classname).text.strip()
        if _type == "click":
            return driver_object.find_element_by_class_name(classname).click()
        if _type == "href":
            return driver_object.find_element_by_css_selector(classname).get_attribute('href').strip()
        if _type == "sel_text":
            return driver_object.find_element_by_css_selector(classname).text.strip()
    except:
        return ''

def profile_count(count, ui_type=1):
    cal_count = 0
    if count == '':
        cal_count = 0
    elif 'K' in str(count):
       cal_count =  float(count.replace('K',''))*1000
    elif 'M' in str(count):
       cal_count = float(count.replace('M',''))*1000000
    else:
        cal_count =  int(count)
    return int(round(cal_count))

use_database = False
def get_driver(executable_path,_PROXY_HOST='',_PROXY_PORT='',_USERNAME='',_PASSWORD='',  browser = 'firefox' ,
               db = False , _url_table ="", _instant_id=0,_search_limit_url=100,_dir_path='', account_group=''):
    global use_database,url_table,instant_id,search_limit_url, dir_path
    use_database  = db
    PROXY_HOST  = _PROXY_HOST
    PROXY_PORT = _PROXY_PORT
    USERNAME = _USERNAME
    PASSWORD = _PASSWORD
    search_limit_url = _search_limit_url
    connect.set_instant_id(_instant_id)
    if _dir_path != '':
        dir_path = _dir_path
    if use_database == True:
        print('use data base')
        connect.set_account_group(account_group)
        row = connect.get_account_details()
        if type(None) != type(row):
            PROXY_HOST=row[6]
            PROXY_PORT=int(row[7])
            USERNAME=row[8]
            PASSWORD=row[9]
            connect.set_url_table(row[14])
            print(PROXY_HOST)
            #connect.set_db_account_const(row)
        else:
            log_mesage('no available account')
            return False
    else:
        connect.set_db_account_const([])
        connect.set_url_table(_url_table)
        
    if browser == 'chrome':
        if PROXY_HOST != "":
            chrome = chromewithproxy.main_chrome(executable_path,PROXY_HOST,PROXY_PORT,USERNAME,PASSWORD)
            return chrome
        else:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('start-maximized')
            chrome_options.add_argument('allow-running-insecure-content')
            chrome_options.add_argument("test-type")
            chrome_options.add_argument('disable-infobars')
            chrome = webdriver.Chrome(executable_path=executable_path,chrome_options=chrome_options)
            return chrome
    if browser == 'firefox':
        if PROXY_HOST != "":
            print('pp')
            profile = webdriver.FirefoxProfile()
            profile.set_preference("network.proxy.type", 1)
            profile.set_preference("network.proxy.http", PROXY_HOST)
            profile.set_preference("network.proxy.http_port", PROXY_PORT)
            profile.set_preference("network.proxy.socks_username", USERNAME)
            profile.set_preference("network.proxy.socks_password", PASSWORD)
            profile.set_preference("network.proxy.ssl", PROXY_HOST)
            profile.set_preference("network.proxy.ssl_port", PROXY_PORT)
            chrome = webdriver.Firefox(executable_path=executable_path, firefox_profile=profile)
            return chrome
        else:
            chrome = webdriver.Firefox(executable_path=executable_path)
            return chrome

def is_logged_in(driver):
    try:
        driver.find_element_by_id("nav-settings__dropdown-options").text
        return True
    except:
        return False
    
linked_user_name  = ""        
def action_linkedin_login(driver, _username, _password):
    global use_database
    global linked_user_name
    linked_user_name = _username
    username= _username
    password = _password 
    log_mesage('credentials set')
    try:
        if use_database == True:
            db_account = connect.get_db_account_const()
            print(db_account)
            username = db_account[1]
            password = db_account[2]
            print(username )
        log_mesage('loggin')
        time.sleep(randsec())
        driver.get('https://www.linkedin.com/uas/login?fromSignIn=true&trk=uno-reg-join-sign-in')
        sleep(5)
        sleep(randsec())
        driver.find_element_by_name("session_key").send_keys(username)
        sleep(randsec())
        try:
        	password = driver.find_element_by_id("session_password-login").send_keys(password)	
        except Exception as e:
            try:
            	password = driver.find_element_by_id("password").send_keys(password)	
            except Exception as e:
            	pass
        
        sleep(randsec())
        try:
        	sndbutton = driver.find_element_by_id("btn-primary")	
        except Exception as e:
            try:
            	sndbutton = driver.find_element_by_class_name("btn__primary--large")
            except Exception as e:
            	pass
        sndbutton.submit()
        time.sleep(60)
        if is_logged_in(driver):
            log_mesage('logged in')
            send_email(linked_user_name +' ' + datetime.now().strftime('%Y/%m/%d') + ' started','')
        else:
            log_mesage('unable to login- username password missmatch')
            connect.set_account_notrunning()
            driver.quit()
            send_email(linked_user_name +' ' + datetime.now().strftime('%Y/%m/%d') + ' started',log_mesage())
    except Exception as e:
        log_mesage('unable to login' + str(e))
        connect.set_account_notrunning()
        driver.quit()
        send_email(linked_user_name +' ' + datetime.now().strftime('%Y/%m/%d') + ' started',log_mesage())
        
def if_empty_search(driver):
    try:
        txt = driver.find_element_by_id('results-list').text
        if 'no results containing' in txt:
            return False
        else:
            return True
    except:
        return True
    
def if_account_blocked(driver):
    try:
        txt = driver.find_element_by_id('stream-container').text
        if 'we were unable to process your request' in txt :
            print('account blocked')
            return False
        else:
            return True
    except:
        return True    
    
def findcount(driver, url, ui_type=1):
    if ui_type==2:
        return 1
    else:
        #url = "https://www.linkedin.com/sales/search?facet=G&facet.G=in%3A0&count=25&start=0&EL=auto&updateHistory=true&trackingInfoJson.contextId=7FBAD892F75C4515C0FE07F9742B0000"
        url = url.replace('https://www.linkedin.com/sales/search?','https://www.linkedin.com/sales/search/results/people?')
        url = url.replace('&count','&decHits=false&decFacets=false&count')
        js_script= '$.ajax({ type: "GET", url:"' + url +'" , success: function(result) {try{$("#searchcount").val(result.pagination.total);} catch {$("#searchcount").val("error");} }});'
        driver.execute_script(js_script)
        sleep(randsec())
        str_searchcount = driver.find_element_by_id('searchcount').get_attribute('value')
        if str_searchcount != 'error':
            try:
                searchcount = int(str_searchcount)
                print('js search count - ', searchcount)
                if searchcount > 5:
                    return 1
                else:
                    return 0
            except:
                return 2
        else:
            return 2
    
def scarp(driver, diff_quit=14400):
    linkedin_network(driver)
    run_company_extraction(driver)
    sec_then = time.time()
    try:
        global linked_user_name
        log_mesage('navigating sales ')
        driver.get("https://www.linkedin.com/sales/search")
        sleep(randsec())
        ui_type = check_ui_type(driver)
        try:
             a = """ $('#header').append('<input type="hidden" id="searchcount" >');   """ 
             driver.execute_script(a)
        except:
             pass
        get_loginid_tractsess(driver,ui_type)
        log_mesage('current url - set up')
        url = driver.current_url
        cid,searchid = get_param_from_url(url,ui_type)
        """
        trackingInfoJson = params['trackingInfoJson.contextId']
        searchHistoryId = params['searchHistoryId']
        updateHistory = params['updateHistory']
        """
        log_mesage('current url - set up done')
        search_count = 0        
        while connect.num_of_url() != 0: # and search_limit_url > search_count:
            print('search count ' + str(search_count))
            search_count = search_count + 1
            row = connect.read_url()
            rowid = row[0]
            profile_country = row[1]
            employee_size = row[3]
            industry_type = row[5]
            total_exp = row[8]
            current_role_exp = row[10]
            
            
            try:
                a = """ $('#header').append('<input type="hidden" id="searchcount" >');   """ 
                driver.execute_script(a)
            except:
                 pass
            
            url  = create_url(profile_country,employee_size,industry_type,total_exp, current_role_exp,ui_type, searchid, cid)
            
            chk_findcount = findcount(driver, url, ui_type)
            if chk_findcount == 1:
                driver.get(url)
                print('new url ')
                connect.set_account_urlcount()
                hideglobalhelp(driver,ui_type)
                if if_account_blocked(driver) == False:
                    log_mesage('account blocked')
                    connect.set_account_block()
                    return
                if if_empty_search(driver):
                    count_profile = get_searched_count(driver,ui_type)
                    count_next_click = 0
                    scrap = True
                    pagination = 0 
                    while scrap:
                        if if_account_blocked(driver) and if_empty_search(driver):
                            time.sleep(randsec())
                            driver.execute_script( 'window.scrollTo(0,document.body.scrollHeight);')
                            time.sleep(1)
                            driver.execute_script( 'window.scrollTo(0,document.body.scrollHeight);')
                            pagination = pagination + 1
                            count_p = 0
                            result_container = ""
                            if ui_type == 1:
                                result_container = driver.find_elements_by_css_selector('#results-list > li')
                            elif ui_type == 2:
                                result_container = driver.find_elements_by_css_selector('.search-results__result-container')
                                                                                    
                            for profile in result_container:
                                count_p = count_p + 1
                                l_first_name , l_last_name , l_mid_name , address ,job_info, job_title , rolein , profile_name , profile_link , company_link , company_name  = fetch_profile_attributes(profile, ui_type) 
                                profile_info = {
                                'search_url':url,
                                'url':profile_link,
                                'first_name':l_first_name,
                                'last_name':l_last_name,
                                'mid_name':l_mid_name,
                                'user_name':profile_name,
                                'company_name':company_name,
                                'company_link':company_link,
                                'job_title':job_title,
                                'address':address,
                                'country':profile_country,
                                'employee_size':employee_size,
                                'industry':industry_type,
                                'job_info':job_info,
                                'url_pro_count':count_profile,
                                'rolein' :rolein,
                                'linked_user_name':linked_user_name
                                } 
                                
                                
                                if connect.insert_prospect(profile_info):
                                    print('insert into ')
                                else:
                                    print('already exits')
                                
                        else:
                            log_mesage('account blocked')
                            connect.set_account_block()
                            return 
                        """
                        if count_p == 0:
                            scrap = False
                            driver.quit()
                            log_mesage('crossed limit URL')
                            connect.set_account_overlimit()
                            return 'over limit'
                        """
                        if check_more_pagination(driver, ui_type):
                            scrap = click_next_pagination(driver,ui_type)
                            sleep(3)
                            count_next_click = count_next_click + 1
                        else:
                            scrap = False     
                    connect.update_url(rowid)
                    print('url done')
                else:
                    print('empty page')
                    connect.update_url(rowid)
            elif chk_findcount == 0 :
                print('0 count')
                connect.update_url(rowid)
            
            elif chk_findcount == 2:
                connect.set_account_notrunning()
                return 
            sec_now = time.time()
            if int(sec_now - sec_then) > diff_quit :
                try:
                    driver.quit()
                    log_mesage('quiting forcely : time exceed 4 hr') 
                except:
                    pass
        connect.set_account_notrunning()
        #driver.get('https://www.linkedin.com/m/logout/')
        #send_email(linked_user_name +' ' + datetime.now().strftime('%Y/%m/%d') + ' ended',log_mesage())
    except Exception as e:
        connect.set_account_notrunning()
        #driver.get('https://www.linkedin.com/m/logout/')
        log_mesage(str(e))        
        #send_email(linked_user_name +' ' + datetime.now().strftime('%Y/%m/%d') + ' error ',log_mesage())
        return
        
def log_mesage(message=''):
    global error_log
    error_log = error_log + " \n " + message
    print(message)
    return error_log

def linkedin_network(driver):
    driver.get('https://www.linkedin.com/')
    driver.execute_script( 'window.scrollTo(0,document.body.scrollHeight);')
    time.sleep(randsec())
    driver.execute_script( 'window.scrollTo(0,document.body.scrollHeight);')
    sleep(randint(1,5))
    for i in range(1,2):
        driver.get('https://www.linkedin.com/mynetwork/')
        time.sleep(randsec())
        try:
             driver.execute_script("$('.artdeco-scrolling-container > artdeco-tablist > artdeco-tab')[1].click()")
        except:
            pass
            time.sleep(randsec()) 
            try:
                connect_network = " $('button[data-control-name=" + '"invite"]' + "').each(function(index, value) {setTimeout(function() { jQuery(value).trigger('click'); }, index * 1000);});"
                driver.execute_script( connect_network)
            except:
                 pass
        time.sleep(randsec())
    try:
        driver.get('https://www.linkedin.com/me/profile-views/urn:li:wvmp:summary/')
    except:
        pass
    try:
        driver.get('https://www.linkedin.com/messaging/')
    except:
         pass
    time.sleep(randsec())
    driver.get('https://www.linkedin.com/notifications/')
    time.sleep(randsec())
    driver.get('https://www.linkedin.com/')

def linkedin_network_connection(driver):
    global linked_user_name
    #send_email(linked_user_name +' ' + datetime.now().strftime('%Y/%m/%d') + ' normal started','')
    linkedin_network(driver)
    driver.get('https://www.linkedin.com/m/logout/')
    send_email(linked_user_name +' ' + datetime.now().strftime('%Y/%m/%d') + ' normal ended','')
    
def randsec():
    return randint(4,15)

def send_email(subject, body):
    import smtplib
    FROM = 'yogesh@linkedinextract.in'
    user = FROM
    pwd = "k@80905510041" 
    recipient = 'nayalaunch@gmail.com'
    TO = recipient if isinstance(recipient, list) else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.zoho.com", 587)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        server.sendmail(FROM, TO, message)
        server.close()
    except:
        print('mail error')
        
def extract_company(driver):
    global linkedin_user_name
    company_link = driver.current_url
    about_us = getDataByClass(driver, 'org-about-us-organization-description__text')
    company_domain = getDataByClass(driver, 'org-about-company-module__company-page-url')
    head_quater = getDataByClass(driver, 'org-about-company-module__headquarters')
    founded_year = getDataByClass(driver, 'org-about-company-module__founded')
    company_type = getDataByClass(driver, 'org-about-company-module__company-type')
    employee_size = getDataByClass(driver, 'org-about-company-module__company-staff-count-range')
    company_name = getDataByClass(driver,'org-top-card-module__name')
    addressess =  getDataByClass(driver,'org-location-viewer__location-card-list')
    industry = getDataByClass(driver,'company-industries') 
    dic_company_details = {
             'company_link1':company_link,
             'about_us':about_us,
             'company_domain':company_domain,
             'head_quater':head_quater,
             'founded_year':founded_year,
             'company_type':company_type,
             'employee_size':employee_size,
             'company_name1':company_name,
             'addressess': addressess,
             'industry':industry
            }
    return dic_company_details

def run_company_extraction(driver):   
    print('starting company extraction')
    # status 0 - not run , 1- working, 2- done, 3- expection
    urlcount = 0
    limit = randint(5,10)
    global linked_user_name
    while connect.num_of_url_dom() != 0 and urlcount < limit:
            urlcount = urlcount + 1
            print(urlcount)
            row = connect.read_dom_url()
            company_code = row[1]
            url = 'https://www.linkedin.com/company/' + str(company_code)
            idd = row[0]
            try:
                sleep(3)
                driver.get(url)
                sleep(10)
                driver.execute_script( 'window.scrollTo(0,50);')
                sleep(10)
                try:
                    driver.find_element_by_id('org-about-company-module__show-details-btn').click()
                except:
                    pass
                sleep(5)
                driver.execute_script( 'window.scrollTo(0,50);')
                sleep(10)
                dic_company_details = extract_company(driver)
                dic_company_details['linkedin_user_name'] = linked_user_name
                connect.updateDomFromDict(dic_company_details,company_code)
            except Exception as e  :
                print('error', str(e))           
                connect.update_dom_url(company_code,3)
                return
    print('ending company extraction')