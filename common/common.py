# encoding=utf-8
import os
import readConfig as readConfig
from xlrd import open_workbook
from xml.etree import ElementTree as ElementTree

proDir = readConfig.proDir


# ****************************** read casedata xls ********************************
def get_xls(xls_name, sheet_name):
    cls = []
    # 获取xls文件的路径
    xlsPath = os.path.join(proDir, "testFile", "casedata", xls_name)
    # 打开xls文件
    data = open_workbook(xlsPath)
    # 根据名称获取对应的sheet
    sheet = data.sheet_by_name(sheet_name)
    # 获取一个sheet的行数
    nrows = sheet.nrows
    for i in range(nrows):
        if sheet.row_values(i)[0] != u'case_name':
            cls.append(sheet.row_values(i))
    return cls

# ****************************** read element xml ********************************
activity = {}


def set_xml():
    if len(activity) == 0:
        xml_path = os.path.join(proDir, "testFile", "elements.xml")
        per = ElementTree.parse(xml_path)
        all_element = per.findall("page")

        for firstElement in all_element:
            activity_name = firstElement.get("pagename")
            element = {}
            for secondElement in firstElement.getchildren():
                element_name = secondElement.get("name")
                element_child = {}
                for thirdElement in secondElement.getchildren():
                    element_child[thirdElement.tag] = thirdElement.text
                element[element_name] = element_child
            activity[activity_name] = element


def get_xml_dict(page_name, element_name):
    set_xml()
    element_dict = activity.get(page_name).get(element_name)
    return element_dict
