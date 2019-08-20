from flask import Flask, url_for ,make_response
from utils import sql_helper
import json

app = Flask(__name__)

@app.route('/<pod_name>/')
def queryPodInfo(pod_name) :
	pod = sql_helper.query_tbl_with_name(pod_name)
	if pod == None :
		return makeResponse(200, '成功!')
	return makeResponse(200, '成功!', pod = pod)
	
@app.route('/<pod_name>/search_cnt/')
def queryPodSearchCount(pod_name) :
	search_cnt = sql_helper.query_search_cnt(pod_name)
	if search_cnt == None :
		search_cnt = 0
	return makeResponse(200, '成功!', pod_name = pod_name,search_cnt = search_cnt)
	
@app.route('/<pod_name>/download_cnt/')
def queryPodDownloadCount(pod_name) :
	download_cnt = sql_helper.query_download_cnt(pod_name)
	if download_cnt == None :
		download_cnt = 0
	return makeResponse(200, '成功!', pod_name = pod_name,download_cnt = download_cnt)

@app.route('/<pod_name>/search/')
def podSearched(pod_name) :
	pod_id = queryPodID(pod_name)
	search_cnt = sql_helper.query_search_cnt(pod_name) + 1
	sql_helper.update_search_cnt(pod_id,search_cnt)
	return makeResponse(200, '成功!', pod_name = pod_name,search_cnt = search_cnt)
	
@app.route('/<pod_name>/download/')
def podDownloaded(pod_name) :
	pod_id = queryPodID(pod_name)
	download_cnt = sql_helper.query_download_cnt(pod_name) + 1
	sql_helper.update_download_cnt(pod_id,download_cnt)
	return makeResponse(200, '成功!', pod_name = pod_name,download_cnt = download_cnt)
	
@app.errorhandler(404)
def pageNotFound(error) :
	return makeResponse(404, '无法访问!')

	
def makeResponse(code,msg,**keyValues) :
	res = {}
	res['ec'] = code
	res['em'] = msg
	data = {}
	if len(keyValues) :
		for key,value in keyValues.items() :
			data[key] = value
	res['data'] = data
	return json.dumps(res, separators=(',', ':'), ensure_ascii=False)
	
def queryPodID(pod_name) :
	pod_id = sql_helper.query_id(pod_name)
	if pod_id == None :
		sql_helper.insert_tbl(name = pod_name,search_cnt = 0,download_cnt = 0)
		pod_id = sql_helper.query_id(pod_name)
	return pod_id