import logging
import yaml
from logging_args import logging_args
# log to console and file
# log with line numbers
# add date and time

with open('logging_config.yaml') as f:
	args_dict = yaml.load(f, Loader=yaml.FullLoader)


print(args_dict)
logging.basicConfig(filename='test', **logging_args)
print(logging)

def log_test():
	logging.debug("debugged")
#	logging.info("info")
#	logging.warning("warning")
#	logging.error("error")
#	logging.critical(f"the test arg is {test_arg}")
	
log_test()
#print(str([1,2,3]))
