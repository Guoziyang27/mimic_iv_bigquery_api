from flask import Blueprint, request
import sys
import json
import re
sys.path.append("..")
from module.connect import BigQuery_client
from module.utils import retrive_query_result

core = Blueprint("core", __name__)


patients_header = ["subject_id", "gender", "anchor_age", "anchor_year", "anchor_year_group", "dod"]
admissions_header = ['subject_id', 'hadm_id', 'admittime', 'dischtime', 'deathtime', 'admission_type', 'admission_location', 'discharge_location', 'insurance', 'language', 'marital_status', 'ethnicity', 'edregtime', 'edouttime', 'hospital_expire_flag']
transfers_header = ['subject_id', 'hadm_id', 'transfer_id', 'eventtype', 'careunit', 'intime', 'outtime']


@core.route('/patients', methods=['GET'])
def patient_get():

    if len(BigQuery_client) == 0:
        return json.dumps({'succeed': False,
                           'info': 'No BigQuery client is established.'})

    patient_id_list = request.args.get('patientidlist').strip('][').split(',')
    if not isinstance(patient_id_list, list) or any(re.match('^[0-9]*$', patient_id) is None for patient_id in patient_id_list):
        return json.dumps({'succeed': False,
                           'info': 'Patient id list is not a list or patient id is not an integer.'})

    with_header = True if request.args.get('withheader') == 'true' else False

    name_group_query = """
        SELECT *
        FROM `physionet-data.mimic_core.patients`
        WHERE subject_id in ({})
    """.format(','.join(patient_id_list))

    query_results = BigQuery_client[0].query(name_group_query)

    return json.dumps({'succeed': True,
                       'content': retrive_query_result(query_results, with_header, patients_header)})

@core.route('/patientsheader', methods=['GET'])
def patient_get_header():
    return json.dumps({'succeed': True,
                       'header': patients_header})

@core.route('/admissions', methods=['GET'])
def admissions_get():

    if len(BigQuery_client) == 0:
        return json.dumps({'succeed': False,
                           'info': 'No BigQuery client is established.'})

    patient_id_list = request.args.get('patientidlist').strip('][').split(',')
    if not isinstance(patient_id_list, list) or any(re.match('^[0-9]*$', patient_id) is None for patient_id in patient_id_list):
        return json.dumps({'succeed': False,
                           'info': 'Patient id list is not a list or patient id is not an integer.'})

    with_header = True if request.args.get('withheader') == 'true' else False

    name_group_query = """
        SELECT *
        FROM `physionet-data.mimic_core.admissions`
        WHERE subject_id in ({})
    """.format(','.join(patient_id_list))

    query_results = BigQuery_client[0].query(name_group_query)

    return json.dumps({'succeed': True,
                       'content': retrive_query_result(query_results, with_header, admissions_header)})

@core.route('/admissionsheader', methods=['GET'])
def admissions_get_header():
    return json.dumps({'succeed': True,
                       'header': admissions_header})



@core.route('/transfers', methods=['GET'])
def transfers_get():

    if len(BigQuery_client) == 0:
        return json.dumps({'succeed': False,
                           'info': 'No BigQuery client is established.'})

    patient_id_list = request.args.get('patientidlist').strip('][').split(',')
    if not isinstance(patient_id_list, list) or any(re.match('^[0-9]*$', patient_id) is None for patient_id in patient_id_list):
        return json.dumps({'succeed': False,
                           'info': 'Patient id list is not a list or patient id is not an integer.'})

    with_header = True if request.args.get('withheader') == 'true' else False

    name_group_query = """
        SELECT *
        FROM `physionet-data.mimic_core.transfers`
        WHERE subject_id in ({})
    """.format(','.join(patient_id_list))

    query_results = BigQuery_client[0].query(name_group_query)

    return json.dumps({'succeed': True,
                       'content': retrive_query_result(query_results, with_header, transfers_header)})

@core.route('/transfersheader', methods=['GET'])
def transfers_get_header():
    return json.dumps({'succeed': True,
                       'header': transfers_header})


