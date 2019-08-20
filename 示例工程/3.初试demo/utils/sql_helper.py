import sqlite3
db = None
db_path = './db/pod.db'
tbl_name = 'PodsCounter'
tbl_f_id = 'id'
tbl_f_name = 'name'
tbl_f_search_cnt = 'search_cnt'
tbl_f_download_cnt = 'download_cnt'


def get_db():
	global db
	if not db :
		db = sqlite3.connect(db_path,check_same_thread=False)
		db.row_factory = dict_factory
		cursor = db.cursor()
		sql = "CREATE TABLE IF NOT EXISTS {0} ({1} INTEGER PRIMARY KEY AUTOINCREMENT,{2} TEXT,{3} int,{4} int)".format(tbl_name,tbl_f_id, tbl_f_name,tbl_f_search_cnt,tbl_f_download_cnt)
		cursor.execute(sql)
		db.commit()
	return db

# 以名字查询id
def query_id(name) :
	ret = query_field('id', tbl_f_name, name)
	for i in ret :
		return i['id']

# 按名字查表
def query_tbl_with_name(name) :
	rets = query_tbl(name = name)
	for ret in rets :
		return ret

# 以名字查询搜索次数	
def query_search_cnt(name) :
	return query_field_cnt(name, tbl_f_search_cnt)
		 
# 以名字查询下载次数
def query_download_cnt(name) :
	return query_field_cnt(name, tbl_f_download_cnt)

# 以名字查询一个次数	
def query_field_cnt(name,field) :
	rets = query_field(field, tbl_f_name, name)
	for ret in rets :
		return ret[field] 

# 以一个条件查询某个字段	
def query_field(field,condition,condition_v) :
	sql = "SELECT {0} FROM {1} WHERE {2} = '{3}'".format(field, tbl_name,condition,condition_v)
	return excute_sql(sql)

# 以指定条件查询表	
def query_tbl(**conditions) :
	sql = "SELECT * FROM {0}".format(tbl_name)
	if len(conditions) > 0 :
		sql = sql + " WHERE"
		for key,value in conditions.items() :
			sql = sql + " {0} = '{1}' AND".format(key, value)
		sql = sql[:-4]
	return excute_sql(sql)

# 插入表	
def insert_tbl(**conditions) :
	if len(conditions) == 0 :
		return 
	sql = "INSERT INTO {0} (".format(tbl_name)
	for key in conditions.keys() :
		sql = sql + " {0},".format(key)
	sql = sql[:-1] + " ) VALUES ("
	for value in conditions.values() :
		sql = sql + " '{0}',".format(value)
	sql = sql[:-1] + " )"
	excute_sql(sql)
	
	
# 以id修改搜索次数
def update_search_cnt(id,cnt) :
	update_field_by_id(id, tbl_f_search_cnt, cnt)

# 以id修改下载次数
def update_download_cnt(id,cnt) :
	update_field_by_id(id, tbl_f_download_cnt, cnt)

# 以id修改指定字段的值
def update_field_by_id(id,field,value) :
	update_field_cnt(field, value, 'id', id)

# 根据指定条件修改指定字段的值
def update_field_cnt(field,value,condition,condition_v) :
	sql = "UPDATE {0} SET {1} = {2} WHERE {3} = '{4}'".format(tbl_name, field, value, condition, condition_v)
	excute_sql(sql)

# 以id修改表中指定项目的指定字段值
def update_tbl(id,**fields) :
	sql = "UPDATE {0} SET".format(tbl_name)
	for key,value in fields.items() :
		sql = sql + " {0} = '{1}' ,".format(key, value)
	sql = sql[:-1] + "WHERE id = {0}".format(id)
	excute_sql(sql)
	
# 执行sql
def excute_sql(sql) :
	print(sql)
	db = get_db()
	cursor = db.cursor()
	ret = cursor.execute(sql)
	db.commit()
	return ret


# python3 官方提供的sqlite3结果转字典方案
def dict_factory(cursor, row):  
	d = {}  
	for idx, col in enumerate(cursor.description):  
		d[col[0]] = row[idx]  
	return d
	