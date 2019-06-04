# coding:utf-8
'''
1.利用xml.etree.Element来对xml文件进行操作，然后通过我们自定义的方法，根据传递不同的参数取得不（想）同（要）的值。
2.利用xlrd来操作excel文件用excel文件来管理测试用例的。
'''
import os
from xlrd import open_workbook
from xml.etree import ElementTree as ElementTree
from common.Log import MyLog as Log
from common.configHttp import ConfigHttp as ConfigHttp
import readConfig

localConfigHttp = ConfigHttp()
log = Log.get_log()
logger = log.get_logger()

# 从excle文件中读取测试用例
def get_xls(xls_name,sheet_name):
    cls = []
    # get xls file's path
    xlsPath = os.path.join(readConfig.proDir,"testFile",xls_name)
    # open xls file
    file = open_workbook(xlsPath)
    # get sheet by name
    sheet = file.sheet_by_name(sheet_name)
    # get one sheet's rows
    nrows = sheet.nrows
    for i in range(nrows):
        if sheet.row_values(i)[0] != u"case_name":
            cls.append(sheet.row_values(i))
    return cls

# 从xml文件中读取sql语句
database = {}
def set_xml():
    if len(database) == 0:
        sql_path = os.path.join(readConfig.proDir,"testFile","SQL.xml")
        tree = ElementTree.parse(sql_path)
        for db in tree.findall("database"):
            db_name = db.get("name")
            print(db_name)
            table = []
            for tb in db.getchildren():
                table_name = tb.get("name")
                print(table_name)
                sql = {}
                for data in tb.getchildren():
                    sql_id = data.get("id")
                    print(sql_id)
                    sql[sql_id] = data.text
                table[table_name] = sql
            database[db_name] = table

def get_xml_dict(database_name,table_name):
    set_xml()
    database_dict = database.get(database_name).get(table_name)
    return database_dict

def get_sql(database_name,table_name,sql_id):
    db = get_xml_dict(database_name,table_name)
    sql = db.get(sql_id)
    return sql
