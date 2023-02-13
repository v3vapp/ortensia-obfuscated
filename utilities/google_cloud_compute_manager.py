import sys, pathlib
outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent 
working_dir = pathlib.Path(__file__).resolve().parent.parent 
current_dir = pathlib.Path(__file__).resolve().parent 
sys.path.append(str(working_dir))
sys.path.append(f"{str(working_dir)}/config")
sys.path.append(f"{str(working_dir)}/tools")
import os
from googleapiclient.discovery import build, Resource
from oauth2client.client import GoogleCredentials
import logging, time
# import boto3
import discorder
import config

logging.basicConfig(level=logging.INFO,format="%(asctime_data)s : %(message)s")

#_______________________________________________________________________
# googleCloud #
googleCloud_project  = config.googleCloudProject
googleCloud_zone     = config.googleCloudZone
googleCloud_instance = config.googleCloudInstance
#______________________________________________________________________

# ---------  googleCloud  ----------

def googleCloud_start(project, zone, instance_name):
    credentials: GoogleCredentials = GoogleCredentials.get_application_default()
    compute: Resource = build('compute', 'v1', credentials=credentials)
    instance: dict = compute.instances().get(project=project, zone=zone, instance=instance_name).execute()
    result: dict = compute.instances().start(project=project, zone=zone, instance=instance['name']).execute()
    # Wait Running
    while True:
        instance: dict = compute.instances().get(project=project, zone=zone, instance=instance_name).execute()
        logging.info(instance["status"])
        # TERMINATED -> STAGING -> RUNNING
        if instance["status"] == "RUNNING":
            break
        time.sleep(5)


def googleCloud_stop(platform, project, zone, instance_name):

    if platform == "LOCAL":
        print("This is LOCAL MACHINE. NO INSTANCE TO STOP... good bye.")
    
    else:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = f"{working_dir}/config/googleCloud_september.json"

        try:
            logging.warning(f"\n----- Trying to Stop Instance {instance_name}-----")

            discorder.send(f"STOPPING...", 
                        "VM stop automatically.", 
                        f"Going to try to Stop...", 
                        username = instance_name,
                        server = "vm")

            credentials: GoogleCredentials = GoogleCredentials.get_application_default()
            compute: Resource = build('compute', 'v1', credentials=credentials)
            instance: dict = compute.instances().get(project=project, zone=zone, instance=instance_name).execute()
            result: dict = compute.instances().stop(project=project, zone=zone, instance=instance['name']).execute()

            # Wait Terminated
            while True:
                instance: dict = compute.instances().get(project=project, zone=zone, instance=instance_name).execute()
                logging.info(instance["status"])
                #  RUNNING -> STOPPING -> TERMINATED
                if instance["status"] == "TERMINATED":
                    break
                time.sleep(5)

            logging.warning(f"\n----- Stopped -----")

            discorder.send(f"STOPPED", 
                        "VM STOPPED automatically.", 
                        f"Stopped Successfully", 
                        username = instance_name,
                        server = "vm")

        except Exception as e:
            logging.warning(f"\n----- FAILD to Stop Instance -----")

            discorder.send(f"Virtual Machine STOPPING ERROR!...", 
                        "VM FAILD to STOP automatically.", 
                        f"FAILD to Stop... reason -> {e}", 
                        username = instance_name,
                        server = "error")

            

# # ---------  aws  ----------

# aws_access_key_id       = config.aws_access_key_id
# aws_secret_access_key   = config.aws_secret_access_key
# aws_region              = config.aws_region
# aws_instance            = config.aws_instance


# def aws_start(instance_id):
#     aws_client = boto3.client(  'ec2',
#                                 aws_access_key_id     = aws_access_key_id,
#                                 aws_secret_access_key = aws_secret_access_key,
#                                 region_name           = aws_region)
#     aws_client.start_instances(InstanceIds=[instance_id])
#     logging.info("stopping aws Instances now")


# def aws_stop(instance_id):
#     aws_client = boto3.client(  'ec2',
#                                 aws_access_key_id     = aws_access_key_id,
#                                 aws_secret_access_key = aws_secret_access_key,
#                                 region_name           = aws_region)
#     aws_client.stop_instances(InstanceIds=[instance_id])
#     logging.info("stopping aws Instances now")


# #------------------------------------
# if __name__ == "__main__":
#     aws_stop(aws_instance)
