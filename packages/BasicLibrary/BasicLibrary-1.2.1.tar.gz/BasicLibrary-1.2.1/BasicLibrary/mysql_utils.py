import pymysql

def __get_mysql_connection_with_config(config):
    '''
    通过标准配置连接数据库，底层方法
    :param config: 字典类型，形如：{'host': '127.0.0.1', 'port': 3306, 'user': 'test', 'password': 'test', 'database': 'users'}
    :return: Connection类型
    '''
    if config.get('charset') is None:
        config['charset'] = 'utf8'
    connect = pymysql.connect(**config)
    return connect

def __query_one(con,sql):
    cur = con.cursor()
    cur.execute(sql)
    result = cur.fetchone()
    fields_list = []
    for field in cur.description:
        fields_list.append(field[0])
    con.commit()
    result_dict = {}
    if result is None or len(result) == 0:
        return None
    for index in range(len(result)):
        result_dict[fields_list[index]] = result[index]
    cur.close()
    con.close()
    return result_dict

def __query_all(con,sql):
    cur = con.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    fields_list = []
    for field in cur.description:
        fields_list.append(field[0])
    con.commit()
    if result is None or len(result) == 0:
        return None
    result_list = []
    for i in range(len(result)):
        row_dict = {}
        row = result[i]
        for j in range(len(row)):
            row_dict[fields_list[j]] = row[j]
        result_list.append(row_dict)
    cur.close()
    con.close()
    return result_list

def __execute_sql(con,sql):
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    cur.close()
    con.close()

def excute_mysql_sql_with_mysql(config,sql):
    '''
    数据库的删除、修改调用此方法
    :param config: 字典类型，形如：{'host': '127.0.0.1', 'port': 3306, 'user': 'test', 'password': 'test', 'database': 'users'}
    :param sql: sql语句
    :return: 空
    '''
    con = __get_mysql_connection_with_config(config)
    return __execute_sql(con,sql)

def query_one_with_config(config,sql):
    '''
    查询一条数据调用此方法，如果有多条数据，查询出来的是最老的一条
    :param config: 字典类型，形如：{'host': '127.0.0.1', 'port': 3306, 'user': 'test', 'password': 'test', 'database': 'users'}
    :param sql: sql语句
    :return: {'':''} 字典数据格式
    '''
    con = __get_mysql_connection_with_config(config)
    return __query_one(con,sql)

def query_all_with_config(config,sql):
    '''
    查询多条数据调用此方法
    :param config: 字典类型，形如：{'host': '127.0.0.1', 'port': 3306, 'user': 'test', 'password': 'test', 'database': 'users'}
    :param sql: sql语句
    :return:[{'':''},{'':''}] 列表数据格式
    '''
    con = __get_mysql_connection_with_config(config)
    return __query_all(con, sql)

def get_define_data_by_field(config,sql,field):
    '''
    先查询出所有数据，再根据传入的field返回该字段对应的所有值，例如一个表有多条订单，传入订单号字段返回所有订单号的LIST
    :param config: config: 字典类型，形如：{'host': '127.0.0.1', 'port': 3306, 'user': 'test', 'password': 'test', 'database': 'users'}
    :param sql: sql: sql语句
    :param field: 想要获取的字段，例如order_no
    :return: [] 列表数据类型
    '''
    database_data = query_all_with_config(config, sql)
    field_list = []
    try:
        for i in range(len(database_data)):
            if field not in database_data[i].keys():
                print('field【%s】不存在，请检查！' % field)
                break
            else:
                field_list.append(database_data[i].get(field))
        return field_list
    except TypeError as e:
        return field_list
    # except

def get_define_data_by_database(config,sql,rownum=0):
    '''
    先查询所有数据，再根据rownum，查询某一行
    :param config: config: 字典类型，形如：{'host': '127.0.0.1', 'port': 3306, 'user': 'test', 'password': 'test', 'database': 'users'}
    :param sql: sql: sql语句
    :param rownum: 数字格式，想要查询的行，从0开始
    :return: {'':''} 字典数据格式
    '''
    database_data = query_all_with_config(config,sql)
    return database_data[rownum]