'''
@Date: 2020-02-01 14:30:47
@LastEditors  : 赵青岩
@LastEditTime : 2020-02-09 20:37:16
@Description: 
'''

import pymysql
import math
import time
import datetime
import decimal
import getData
import mysql_lib

def get_separator(conn):
    '''
    @description: 
    @param {type} 
    @return: 分隔符，类型：元祖
    '''
    sql = "SELECT other.`内容` from other WHERE other.`类别` = '分隔符';"
    cursor = mysql_lib.Cursor(conn)
    results = cursor.select(sql)
    separator = ()
    for result in results:
        separator += result
    return separator

def get_login(name, password):
    login = getData.Login()
    login.login(name=name, password=password)
    return login

def get_ID_max(conn, table):
    sql = "select ifnull(max(`ID`),0) AS `ID_max` from `{table}`;".format(table=table)
    cursor = mysql_lib.Cursor(conn)
    ID_max = cursor.select(sql)
    return ID_max[0][0]

def get_id_category(subject):
    if '日常差旅费' in subject:
        id_category = '差旅'
    elif '款项支出审批单' in subject:
        id_category = '款项'
    elif '日常外出参会费用报销单' in subject:
        id_category = '会议'
    elif '职工教育经费报销单（专项费用）' in subject:
        id_category = '培训'
    else:
        id_category = '其他费用'
    return id_category

def get_id_list(conn):
    sql = "SELECT 标识 as id from general_table;"
    cursor = mysql_lib.Cursor(conn)
    results = cursor.select(sql)
    id_list = ()
    for result in results:
        id_list += result
    return id_list

def caltime(date1,date2):
    date1=time.strptime(date1,"%Y-%m-%d")
    date2=time.strptime(date2,"%Y-%m-%d")
    date1=datetime.datetime(date1[0],date1[1],date1[2])
    date2=datetime.datetime(date2[0],date2[1],date2[2])
    return (date2-date1).days

def get_person_level(department, person, conn):
    sql = "select `person`.`级别` AS `级别` from `person` where ((`person`.`部门` = '{department}') and (`person`.`姓名` = '{person}'));".format(department=department, person=person)
    cursor = mysql_lib.Cursor(conn)
    result = cursor.select(sql)
    if len(result) == 0:
        return '其他人员'
    return result[0][0]

def get_destination(destinations):
    for destination in destinations:
        if ('北京' in destination) or ('上海' in destination):
            return '北京、上海'
        elif ('杭州' in destination) or ('厦门' in destination) or ('广州' in destination) or ('深圳' in destination):
            return '杭州、厦门、广州、深圳'
        
    return '一般城市'

def get_standard_list(conn):
    sql = "select `standard`.`人员级别` AS `人员级别`,`standard`.`地区类别` AS `地区类别`,`standard`.`标准` AS `标准` from `standard`;"
    cursor = mysql_lib.Cursor(conn)
    results = cursor.select(sql)
    return results

def get_standard(person_level, destination, standard_list):
    for standard_row in standard_list:
        if standard_row[0]==person_level and standard_row[1]==destination:
            return standard_row[2]
    return 0

def run(name_oa, password_oa, host, user, password, db):
    conn = pymysql.connect(host=host, user=user, password=password, port=3306, db=db)
    # 获取分隔符
    separator = get_separator(conn)
    login = get_login(name_oa, password_oa)
    data = login.getData()

    # 初始化统计数据
    success_num = 0
    faild_num = 0
    exist_num = 0
    other_num = 0
    # 判断获取主数据是否成功，成功继续，失败返回统计数据
    if data == 0:
        return success_num, faild_num, exist_num, other_num
    # 主表信息
    table_general_table = 'general_table'
    keys_general_table = ['ID', '标识', '类别', '报销事由', '部门', '报销人', '电话', '报销金额', '发起时间', '审批时间', '费用', '客运增值税', '专票增值税', '状态', '费用大类', '费用分类', '费用名称']
    
    # 客运表信息
    table_passenger_transport = 'passenger_transport'
    keys_passenger_transport = ['ID', '标识', '序号', '开车时间', '开车地点', '到站时间', '到站地点', '交通工具', '票价', '燃油附加', '其他', '税额', '不含税价']
    
    # 住宿表信息
    table_accommodation = 'accommodation'
    keys_accommodation = ['ID', '标识', '序号', '发票类别', '发票号', '无税金额', '税率', '税额', '含税金额']
    
    # 发票表信息
    table_invoice = 'invoice'
    keys_invoice = ['ID', '标识', '序号', '发票类别', '发票号', '无税金额', '税率', '税额', '含税金额']
    
    # 出租车表信息
    table_taxi = 'taxi'
    keys_taxi = ['ID', '标识', '序号', '日期', '车号', '金额']
    
    # 补助表信息
    table_subsidy = 'subsidy'
    keys_subsidy = ['ID', '标识', '序号', '人员', '级别', '开始时间', '结束时间', '出差地', '住宿标准', '住宿天数', '住宿费', '住宿补助', '伙食补助天数', '伙食补助金额', '交通补助天数', '交通补助金额']
    
    standard_list = get_standard_list(conn) # 获取住宿标准
    
    # 获取插入数据sql
    insert_sql = mysql_lib.Cursor(conn)
    sql_general_table = insert_sql.get_insert_sql(table_general_table, keys_general_table)
    sql_passenger_transport = insert_sql.get_insert_sql(table_passenger_transport, keys_passenger_transport)
    sql_accommodation = insert_sql.get_insert_sql(table_accommodation, keys_accommodation)
    sql_taxi = insert_sql.get_insert_sql(table_taxi, keys_taxi)
    sql_subsidy = insert_sql.get_insert_sql(table_subsidy, keys_subsidy)
    sql_invoice = insert_sql.get_insert_sql(table_invoice, keys_invoice)
    
    cursor = conn.cursor()
    # 获取单行数据，后期添加循环

    for i in range(len(data['data'])): 
        # 初始化数据
        values_general_table = []
        values_passenger_transport = []
        values_accommodation = []
        values_invoice = []
        values_taxi = []
        values_subsidy = []
        #获取单行数据
        data_row = data['data'][i]

        # 判断id是否已经存在，如果存在跳过本次循环
        id_list = get_id_list(conn)
        if data_row['id'] in id_list:
            exist_num += 1
            continue

        if data_row['bodyType'] == '20': # 判断是否是协同
            id_category = get_id_category(data_row['subject'])
            if id_category == "差旅": # 差旅费
                data_id = login.getData_id_travel(data_row['id'], separator)
                if data_id == 0:
                    faild_num += 1
                    continue
                # 获取ID最大值
                ID_max_passenger_transport = get_ID_max(conn, table_passenger_transport)
                ID_max_accommodation = get_ID_max(conn, table_accommodation)
                ID_max_invoice = get_ID_max(conn, table_invoice)
                ID_max_taxi = get_ID_max(conn, table_taxi)
                ID_max_subsidy = get_ID_max(conn, table_subsidy)
                ID_max_general_table = get_ID_max(conn, table_general_table)
                # 主表信息
                if len(login.reason) == 0:
                    reason = data_row['subject']
                else:
                    reason = login.reason[0]
                if len(login.tel) == 0:
                    tel = '无'
                else:
                    tel = login.tel[0]
                if len(login.amount_total) == 0:
                    amount_total = '0'
                else:
                    amount_total = login.amount_total[0]
                if len(login.big_category) == 0:
                    big_category = ''
                else:
                    big_category = login.big_category[0]
                if len(login.category) == 0:
                    category = ''
                else:
                    category = login.category[0]
                if len(login.name) == 0:
                    name = ''
                else:
                    name = login.name[0]
                createMemberName = data_row['createMemberName']
                value_general_table = (str(ID_max_general_table+1), data_row['id'], id_category, reason, login.department[0], createMemberName, tel, amount_total, data_row['createDate'].split(' ', 1)[0], data_row['completeTime'].split(' ', 1)[0], amount_total, '0', '0', '待录入', big_category, category, name)
                values_general_table.append(value_general_table)
                # 客运表信息
                # 城市间交通
                start_time = ['2020-01-01']
                end_time = ['2020-01-01']
                destinations = []
                for m in range(math.ceil(len(login.transport)/8)):
                    if m == 0:
                        start_time = []
                        end_time = []
                    value_passenger_transport = (str(ID_max_passenger_transport+m+1), data_row['id'], str(m+1), login.transport[m*8], login.transport[m*8+1], login.transport[m*8+2], login.transport[m*8+3], login.transport[m*8+4], login.transport[m*8+5], '0', '0', login.transport[m*8+6], login.transport[m*8+7])
                    values_passenger_transport.append(value_passenger_transport)
                    start_time.append(login.transport[m*8])
                    end_time.append(login.transport[m*8+2])
                    destinations.append(login.transport[m*8+3])
                # 飞机
                airplane = login.airplane
                if airplane[0][0] != '\xa0':
                    
                    airplane = ["0" if x == [] else x for x in airplane]
                    for m in range(math.ceil(len(airplane)/10)):
                        value_passenger_transport = (str(ID_max_passenger_transport+math.ceil(len(login.transport)/8)+m+1), data_row['id'], str(math.ceil(len(login.transport)/8)+m+1), airplane[m*10][0], airplane[m*10+1][0], airplane[m*10+2][0], airplane[m*10+3][0], '飞机', airplane[m*10+4][0], airplane[m*10+5][0], airplane[m*10+6][0], airplane[m*10+8][0], airplane[m*10+9][0])
                        values_passenger_transport.append(value_passenger_transport)
                        start_time.append(airplane[m*10][0])
                        end_time.append(airplane[m*10+2][0])
                        destinations.append(airplane[m*10+3][0])
                # 住宿
                if len(login.Accommodation_amount)>0:
                    value_accommodation = (str(ID_max_accommodation+1), data_row['id'], '1', '普票', '', login.Accommodation_amount[0], '0', '0', login.Accommodation_amount[0])
                    values_accommodation.append(value_accommodation)
                    accommodation_day = login.Accommodation_day[0]
                    accommodation_amount = login.Accommodation_amount[0]
                else:
                    accommodation_day = '0'
                    accommodation_amount = '0'

                # 出租
                for m in range(math.ceil(len(login.taxi)/6)):
                    value_taxi = (str(ID_max_taxi+m+1), data_row['id'], str(m+1), login.taxi[m*6], '', login.taxi[m*6+5])
                    values_taxi.append(value_taxi)
                # 补助
                persons = login.person
                if len(persons) == 0:
                    persons = [createMemberName]
                accommodation_amount_onePerson = (decimal.Decimal(accommodation_amount)/len(persons)).quantize(decimal.Decimal('0.0000'))
                for m in range(len(persons)):
                    person = persons[m]                
                    department = login.department[0]
                    person_level = get_person_level(department, person, conn)
                    destination = get_destination(destinations)
                    standard = get_standard(person_level, destination, standard_list)
                    accommodation_subsidy = standard * decimal.Decimal(accommodation_day) - accommodation_amount_onePerson
                    if accommodation_subsidy > 0:
                        accommodation_subsidy = accommodation_subsidy/2
                    strat_date = min(start_time)
                    end_date = max(end_time)
                    travel_day = caltime(strat_date, end_date) + 1
                    value_subsidy = (str(ID_max_subsidy+m+1), data_row['id'], str(m+1), person, person_level, strat_date, end_date, destination, standard, accommodation_day, accommodation_amount_onePerson, accommodation_subsidy, travel_day, travel_day*60, travel_day, travel_day*20)
                    values_subsidy.append(value_subsidy)

                # 录入信息
                try:                
                    cursor.executemany(sql_general_table, values_general_table)                
                    cursor.executemany(sql_passenger_transport, values_passenger_transport)
                    cursor.executemany(sql_accommodation, values_accommodation)
                    cursor.executemany(sql_taxi, values_taxi)
                    cursor.executemany(sql_subsidy, values_subsidy)
                    conn.commit()
                    success_num += 1
                except:
                    conn.rollback()
                    faild_num += 1
            elif id_category == "款项":
                other_num += 1
                continue
            else: # 其他费用
                data_id = login.getData_id_other(data_row['id'])
                if data_id == 0:
                    faild_num += 1
                    continue
                # 主表信息
                ID_max_general_table = get_ID_max(conn, table_general_table)
                if len(login.reason) == 0:
                    reason = data_row['subject']
                else:
                    reason = login.reason[0]
                if len(login.tel) == 0:
                    tel = '无'
                else:
                    tel = login.tel[0]
                if len(login.amount_total) == 0:
                    amount_total = '0'
                else:
                    amount_total = login.amount_total[0]
                if len(login.big_category) == 0:
                    big_category = ''
                else:
                    big_category = login.big_category[0]
                if len(login.category) == 0:
                    category = ''
                else:
                    category = login.category[0]
                if len(login.name) == 0:
                    name = ''
                else:
                    name = login.name[0]
                value_general_table = (str(ID_max_general_table+1), data_row['id'], id_category, reason, login.department[0], data_row['createMemberName'], tel, amount_total, data_row['createDate'].split(' ', 1)[0], data_row['completeTime'].split(' ', 1)[0], amount_total, '0', '0', '待录入', big_category, category, name)
                values_general_table.append(value_general_table)
                # 发票信息        
                ID_max_invoice = get_ID_max(conn, table_invoice)
                expense_detail = login.expense_detail
                expense_detail = ["0" if x == [] else x for x in expense_detail]
                for m in range(math.ceil(len(login.expense_detail)/6)):
                    value_invoice = (str(ID_max_invoice+m+1), data_row['id'], login.expense_detail[0][0], '普票', '', login.expense_detail[4][0], '0', '0', login.expense_detail[4][0])
                    values_invoice.append(value_invoice)

                # 录入信息 
            
                try:
                    cursor.executemany(sql_general_table, values_general_table)
                    cursor.executemany(sql_invoice, values_invoice)
                    conn.commit()
                    success_num += 1
                except:
                    conn.rollback()
                    faild_num += 1
        else:
            other_num += 1
    cursor.close()
    conn.close()
    return success_num, faild_num, exist_num, other_num
