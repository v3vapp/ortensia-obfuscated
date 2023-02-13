import sys

import sys, pathlib
outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent # Outside
working_dir = pathlib.Path(__file__).resolve().parent.parent #Bankof3v
current_dir = pathlib.Path(__file__).resolve().parent 
sys.path.append(str(working_dir))

from pprint import pprint 
pprint(sys.path)

from global_module.config import config


print(config.aws_access_key_id)