#!/usr/bin/env python
from boto.dynamodb2.fields import HashKey
from boto.dynamodb2.table import Table
import boto.dynamodb2 as ddb
##################################################################
# Update job information in dynamodb
##################################################################
def dynamodb_update(table, data):
    #print "Updating db with : {0}".format(data)
    return table.put_item(data=data, overwrite=True)


##################################################################
# Get job information from dynamodb
##################################################################
def get_job(request, job_id):
    dyntable = request.app.config['dyno.conn']
    try:
        item = dyntable.get_item(job_id=job_id)
    except ItemNotFound:
        return "The requested job_id was not found in the jobs database"
        raise
    return item

##################################################################
# Update job information in dynamodb
##################################################################
def dynamodb_get(table, job_id):
        return table.get_item(job_id=job_id)

##################################################################
# Update job information in dynamodb
##################################################################

def connect_to_db(app, table_name, hashkey):
    dyno = Table(table_name,
                 schema=[HashKey(hashkey)],
                 connection=ddb.connect_to_region(app.config['dynamodb.region'],
                                                  aws_access_key_id=app.config['keys.key_id'],
                                                  aws_secret_access_key=app.config['keys.key_secret'],
                                                  security_token=app.config['keys.key_token']))
    return dyno



def test():
    import config_manager as cm
    import time
    import uuid
    app = cm.load_configs("production.conf")
    uid = str(uuid.uuid1())

    data = {"job_id"           : uid,
            "username"         : "yadu",
            "jobtype"          : "doc2vec",
            "inputs"           : [{"src": "https://s3.amazonaws.com/klab-jobs/inputs/test.txt", "dest": "test.txt" }],
            "outputs"          : [{"src": "doc_mat.pkl",  "dest": "klab-jobs/outputs/{0}/doc_mat.pkl".format(uid)},
                                  {"src": "word_mat.pkl", "dest": "klab-jobs/outputs/{0}/word_mat.pkl".format(uid)},
                                  {"src": "mdl.pkl",      "dest": "klab-jobs/outputs/{0}/mdl.pkl".format(uid)}],
            "submit_time"      : int(time.time()),
            "status"           : "pending"
    }
    uid = "27013a48-9164-11e5-a61b-0edd34be4cf3"
    #dynamodb_update(app.config["dyno.conn"], data)
    dynamodb_get(app.config["dyno.conn"], uid)

#test()