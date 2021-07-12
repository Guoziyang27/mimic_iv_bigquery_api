
from flask import Blueprint, request
import sys
import json
import re
sys.path.append("..")
from module.connect import BigQuery_client
from module.utils import retrive_query_result

icu = Blueprint("icu", __name__)

d_item_header = ['itemid', 'label', 'abbreviation', 'linksto', 'category', 'unitname', 'param_type', 'lownormalvalue', 'highnormalvalue']
chartevents_header = ['subject_id', 'hadm_id', 'stay_id', 'charttime', 'storetime', 'itemid', 'value', 'valuenum', 'valueuom', 'warning']
datetimeevents_header = ['subject_id','hadm_id','stay_id','charttime','storetime','itemid','value','valueuom','warning']
icustays_header = ['subject_id','hadm_id','stay_id','first_careunit','last_careunit','intime','outtime','los']
inputevents_header = ['subject_id','hadm_id','stay_id','starttime','endtime','storetime','itemid','amount','amountuom','rate','rateuom','orderid','linkorderid','ordercategoryname','secondaryordercategoryname','ordercomponenttypedescription','ordercategorydescription','patientweight','totalamount','totalamountuom','isopenbag','continueinnextdept','cancelreason','statusdescription','originalamount','originalrate']
outputevents_header = ['subject_id','hadm_id','stay_id','charttime','storetime','itemid','value','valueuom']
procedureevents_header = ['subject_id','hadm_id','stay_id','starttime','endtime','storetime','itemid','value','valueuom','location','locationcategory','orderid','linkorderid','ordercategoryname','secondaryordercategoryname','ordercategorydescription','patientweight','totalamount','totalamountuom','isopenbag','continueinnextdept','cancelreason','statusdescription','comments_date','ORIGINALAMOUNT','ORIGINALRATE']


@icu.route('/item', methods=['GET'])
def item_get():

    if len(BigQuery_client) == 0:
        return json.dumps({'succeed': False,
                           'info': 'No BigQuery client is established.'})

    item_id_list = request.args.get('itemidlist').strip('][').split(',')
    if not isinstance(item_id_list, list) or any(re.match('^[0-9]*$', item_id) is None for item_id in item_id_list):
        return json.dumps({'succeed': False,
                           'info': 'Item id list is not a list or item id is not an integer.'})

    with_header = True if request.args.get('withheader') == 'true' else False

    name_group_query = """
        SELECT *
        FROM `physionet-data.mimic_icu.d_items`
        WHERE itemid in ({})
    """.format(','.join(item_id_list))

    query_results = BigQuery_client[0].query(name_group_query)

    return json.dumps({'succeed': True,
                       'item': retrive_query_result(query_results, with_header, d_item_header)})

@icu.route('/itemheader', methods=['GET'])
def item_get_header():

    return json.dumps({'succeed': True,
                       'item_header': d_item_header})

@icu.route('/chartevents', methods=["GET"])
def chartevents_get():
    if len(BigQuery_client) == 0:
        return json.dumps({'succeed': False,
                           'info': 'No BigQuery client is established.'})

    item_id_list = request.args.get('itemidlist').strip('][').split(',')
    if not isinstance(item_id_list, list) or any(re.match('^[0-9]*$', item_id) is None for item_id in item_id_list):
        return json.dumps({'succeed': False,
                           'info': 'Item id list is not a list or item id is not an integer.'})

    with_header = True if request.args.get('withheader') == 'true' else False

    name_group_query = """
        SELECT *
        FROM `physionet-data.mimic_icu.chartevents`
        WHERE itemid in ({})
        LIMIT 10000
    """.format(','.join(item_id_list))

    query_results = BigQuery_client[0].query(name_group_query)

    return json.dumps({'succeed': True,
                       'item': retrive_query_result(query_results, with_header, chartevents_header)})


@icu.route('/charteventsheader', methods=['GET'])
def chartevents_get_header():

    return json.dumps({'succeed': True,
                       'item_header': chartevents_header})

@icu.route('/datetimeevents', methods=["GET"])
def datetimeevents_get():
    if len(BigQuery_client) == 0:
        return json.dumps({'succeed': False,
                           'info': 'No BigQuery client is established.'})

    item_id_list = request.args.get('itemidlist').strip('][').split(',')
    if not isinstance(item_id_list, list) or any(re.match('^[0-9]*$', item_id) is None for item_id in item_id_list):
        return json.dumps({'succeed': False,
                           'info': 'Item id list is not a list or item id is not an integer.'})

    with_header = True if request.args.get('withheader') == 'true' else False

    name_group_query = """
        SELECT *
        FROM `physionet-data.mimic_icu.datetimeevents`
        WHERE itemid in ({})
    """.format(','.join(item_id_list))

    query_results = BigQuery_client[0].query(name_group_query)

    return json.dumps({'succeed': True,
                       'item': retrive_query_result(query_results, with_header, datetimeevents_header)})

@icu.route('/datetimeeventsheader', methods=['GET'])
def datetimeevents_get_header():

    return json.dumps({'succeed': True,
                       'item_header': datetimeevents_header})

@icu.route('/icustays', methods=["GET"])
def icustays_get():
    if len(BigQuery_client) == 0:
        return json.dumps({'succeed': False,
                           'info': 'No BigQuery client is established.'})

    stay_id_list = request.args.get('stayidlist').strip('][').split(',')
    if not isinstance(stay_id_list, list) or any(re.match('^[0-9]*$', item_id) is None for item_id in stay_id_list):
        return json.dumps({'succeed': False,
                           'info': 'Stay id list is not a list or item id is not an integer.'})

    with_header = True if request.args.get('withheader') == 'true' else False

    name_group_query = """
        SELECT *
        FROM `physionet-data.mimic_icu.icustays`
        WHERE stay_id in ({})
    """.format(','.join(stay_id_list))

    query_results = BigQuery_client[0].query(name_group_query)

    return json.dumps({'succeed': True,
                       'item': retrive_query_result(query_results, with_header, icustays_header)})

@icu.route('/icustaysheader', methods=['GET'])
def icustays_get_header():

    return json.dumps({'succeed': True,
                       'item_header': icustays_header})

@icu.route('/inputevents', methods=["GET"])
def inputevents_get():
    if len(BigQuery_client) == 0:
        return json.dumps({'succeed': False,
                           'info': 'No BigQuery client is established.'})

    item_id_list = request.args.get('itemidlist').strip('][').split(',')
    if not isinstance(item_id_list, list) or any(re.match('^[0-9]*$', item_id) is None for item_id in item_id_list):
        return json.dumps({'succeed': False,
                           'info': 'Item id list is not a list or item id is not an integer.'})

    with_header = True if request.args.get('withheader') == 'true' else False

    name_group_query = """
        SELECT *
        FROM `physionet-data.mimic_icu.inputevents`
        WHERE itemid in ({})
    """.format(','.join(item_id_list))

    query_results = BigQuery_client[0].query(name_group_query)

    return json.dumps({'succeed': True,
                       'item': retrive_query_result(query_results, with_header, inputevents_header)})

@icu.route('/inputeventsheader', methods=['GET'])
def inputevents_get_header():

    return json.dumps({'succeed': True,
                       'item_header': inputevents_header})

@icu.route('/outputevents', methods=["GET"])
def outputevents_get():
    if len(BigQuery_client) == 0:
        return json.dumps({'succeed': False,
                           'info': 'No BigQuery client is established.'})

    item_id_list = request.args.get('itemidlist').strip('][').split(',')
    if not isinstance(item_id_list, list) or any(re.match('^[0-9]*$', item_id) is None for item_id in item_id_list):
        return json.dumps({'succeed': False,
                           'info': 'Item id list is not a list or item id is not an integer.'})

    with_header = True if request.args.get('withheader') == 'true' else False

    name_group_query = """
        SELECT *
        FROM `physionet-data.mimic_icu.outputevents`
        WHERE itemid in ({})
    """.format(','.join(item_id_list))

    query_results = BigQuery_client[0].query(name_group_query)

    return json.dumps({'succeed': True,
                       'item': retrive_query_result(query_results, with_header, outputevents_header)})

@icu.route('/outputeventsheader', methods=['GET'])
def outputevents_get_header():

    return json.dumps({'succeed': True,
                       'item_header': outputevents_header})

@icu.route('/procedureevents', methods=["GET"])
def procedureevents_get():
    if len(BigQuery_client) == 0:
        return json.dumps({'succeed': False,
                           'info': 'No BigQuery client is established.'})

    item_id_list = request.args.get('itemidlist').strip('][').split(',')
    if not isinstance(item_id_list, list) or any(re.match('^[0-9]*$', item_id) is None for item_id in item_id_list):
        return json.dumps({'succeed': False,
                           'info': 'Item id list is not a list or item id is not an integer.'})

    with_header = True if request.args.get('withheader') == 'true' else False

    name_group_query = """
        SELECT *
        FROM `physionet-data.mimic_icu.procedureevents`
        WHERE itemid in ({})
    """.format(','.join(item_id_list))

    query_results = BigQuery_client[0].query(name_group_query)

    return json.dumps({'succeed': True,
                       'item': retrive_query_result(query_results, with_header, procedureevents_header)})

@icu.route('/procedureeventsheader', methods=['GET'])
def procedureevents_get_header():

    return json.dumps({'succeed': True,
                       'item_header': procedureevents_header})