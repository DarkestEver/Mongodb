# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 05:19:00 2018

@author: keshav
"""
import psycopg2


db_account_const = []
url_table = ""
instant_id = 0
account_group = ''

def postgres_conn():
    conn = psycopg2.connect(database="postgres",user="postgres",password='root',host='173.249.21.142')
    return conn

def set_url_table(_url_table):
    global url_table
    url_table = _url_table

def set_instant_id (_instant_id):
    global instant_id
    instant_id = _instant_id
    

def set_db_account_const(row):
    global db_account_const
    db_account_const = row

def get_db_account_const():
    global db_account_const
    return db_account_const
    
def insertFromDict(table, dict):
    """Take dictionary object dict and produce sql for 
    inserting it into the named table"""
    sql = 'INSERT INTO ' + table
    sql += ' ('
    sql += ', '.join(dict)
    sql += ') VALUES ('
    sql += ', '.join("'{!s}'".format(removesinglequote(val)) for (key,val) in dict.items())
    sql += ');'
    return sql

def removesinglequote(val):
    if type(val) == str:
        val = val.replace("'","''")
    return val

def insert_prospect(dic):
    conn =postgres_conn()
    cursor = conn.cursor()
    """unique_profile_id = ""
    if ui_type==1:
        unique_profile_id = (dic['url'])[39:78]
    elif ui_type==2:
        unique_profile_id = (dic['url'])[38:77]
    conn =postgres_conn()
    cursor = conn.cursor()
    cursor.execute("select count(1) from  prospects where  url like  '%"+unique_profile_id+"%'" )
    row = cursor.fetchone()
    chk = False
    if row[0] == 0:
        cursor.execute(insertFromDict('prospects', dic))
        chk = True
    """
    cursor.execute(insertFromDict('prospects', dic))
    conn.commit()
    cursor.close()
    conn.close()  
    return True
    
def update_url(id):
    global url_table
    conn =postgres_conn()
    print('update_url')
    cursor = conn.cursor()
    cursor.execute("UPDATE %s SET status=1 WHERE id = %d" % (url_table,id))
    conn.commit()
    cursor.close()
    conn.close()

def read_url():
    global url_table,id
    conn = postgres_conn()
    print('read_url')
    cursor = conn.cursor()
    cursor.execute("select * from  %s where  status=%d limit 1" % (url_table,instant_id))
    row = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    return row

def num_of_url():
    global url_table,id
    conn = postgres_conn()
    print('num_of_url')
    cursor = conn.cursor()
    cursor.execute("select count(1) from  %s where  status= %d" % (url_table,instant_id))
    row = cursor.fetchone()
    conn.commit()
    cursor.close()
    print('num_of_url',row[0])
    conn.close()
    return row[0]    


def get_account_details():
    global db_account_const
    global account_group
    conn = postgres_conn()
    print('get account')
    cursor = conn.cursor()
    cursor.execute("select * from  linkedin_sales_account where  is_blocked = 0 and is_over_limit = 0 and is_subscriped = 1 and is_running = 0 and group = %s " % (account_group))
    db_account_const = cursor.fetchone()
    if type(None) != type(db_account_const):
        cursor.execute("UPDATE linkedin_sales_account SET is_running =1 WHERE id = %d" % (db_account_const[0]))
    conn.commit()
    cursor.close()
    conn.close()
    return db_account_const


def set_account_notrunning():
    print('not runingset')
    global db_account_const
    print(len(db_account_const))
    if len(db_account_const) > 1:
        idd = db_account_const[0]
        print(db_account_const[0])
        conn = postgres_conn()
        cursor = conn.cursor()
        cursor.execute("UPDATE linkedin_sales_account SET is_running =0 WHERE id = %d" % (idd))
        conn.commit()
        cursor.close()
        conn.close()

def set_account_block():
    global db_account_const
    if len(db_account_const) > 0:
        print('not runingset')
        idd = db_account_const[0]
        conn = postgres_conn()
        print('update account block')
        cursor = conn.cursor()
        cursor.execute("UPDATE linkedin_sales_account SET is_blocked = 1, is_running =0 WHERE id = %d" % (idd))
        conn.commit()
        cursor.close()
        conn.close()
        
def set_account_urlcount():
    global db_account_const
    if len(db_account_const) > 0:
        idd = db_account_const[0]
        conn = postgres_conn()
        print('update account block')
        cursor = conn.cursor()
        cursor.execute("UPDATE linkedin_sales_account SET url_done =url_done + 1 WHERE id = %d" % (idd))
        conn.commit()
        cursor.close()
        conn.close()        

def set_account_overlimit():
    global db_account_const
    if len(db_account_const) > 0:
        idd = db_account_const[0]    
        conn = postgres_conn()
        print('update account over limit')
        cursor = conn.cursor()
        cursor.execute("UPDATE linkedin_sales_account SET is_over_limit =1 , is_running =0 WHERE id = %d" % (idd))
        conn.commit()
        cursor.close()
        conn.close()


def read_dom_url():
    global url_table,id
    conn = postgres_conn()
    print('read_url')
    cursor = conn.cursor()
    cursor.execute("select id, company_code from  %s where  status=%d limit 1" % (url_table,instant_id))
    row = cursor.fetchone()
    did = row[0]
    cursor.execute("UPDATE %s  SET status = 1  WHERE id = %d" % (url_table,did))
    conn.commit()
    cursor.close()
    conn.close()
    return row

def update_dom_url(idd,status):
    global url_table
    conn =postgres_conn()
    print('update_url')
    cursor = conn.cursor()
    cursor.execute("UPDATE %s SET status= %s WHERE id = %d" % (url_table,status,idd))
    conn.commit()
    cursor.close()
    conn.close()

    
def updateDomFromDict( dict, company_code):
    global url_table
    sql = 'update  ' + url_table +  ' set '
    for n in dict:
        sql = sql + " " + n + " = '" + removesinglequote( dict[n] ) + "' ,"
    sql = sql + ' status = 2 '
    sql = sql + " where company_code = '" + company_code + "'"    
    conn =postgres_conn()
    print('update_url')
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
