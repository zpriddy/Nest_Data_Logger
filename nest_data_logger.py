#! /usr/bin/python
#################################################
#			Nest Data Logger					#
#################################################
# Zachary Priddy - 2015 						#
# me@zpriddy.com 								#
#												#
# Features: 									#
#	- XXXXXX									#
#	- XXXXXX 									#
#################################################
#################################################


#########
#IMPORTS
#########
import argparse
import nest
import utils
import pickle
from datetime import * 
import dateutil.parser


#########
#VARS
#########
programName="INSERT PROGRAM NAME"
programDescription="INSERT PROGRAM DESCRIPTION"



##################################################
#FUNCTIONS
##################################################

###########
# GET ARGS
##########
def getArgs():
	parser = argparse.ArgumentParser(prog=programName, description=programDescription)
	parser.add_argument("-u","--username",help="Nest Account Username",required=False)
	parser.add_argument("-p","--password",help="Nest Account Password",required=False)
	parser.add_argument("-f","--accountfile",help="Nest Account Ifno Saved In File",required=False)


	return parser.parse_args()

	###############################################
	# OTHER NOTES 
	# 
	# For groups of args [in this case one of the two is required]:
	# group = parser.add_mutually_exclusive_group(required=True)
	# group.add_argument("-a1", "--arg1", help="ARG HELP")
	# group.add_argument("-a2", "--arg2", help="ARG HELP")
	#
	# To make a bool thats true:
	# parser.add_argument("-a","--arg",help="ARG HELP", action="store_true")
	#
	###############################################

##############
# END OF ARGS
##############


def readUserFromFile(user,filename):
	print "Read Account File"

def nestAuth(user):
	myNest = nest.Nest(user.username,user.password,cache_ttl=0)
	return myNest

def dataLoop(nest):
	dayLog = []
	log_filename = 'logs/' + str(datetime.now().year) + '-' + str(datetime.now().month) + '-' + str(datetime.now().day) + '.log'
	try:
		dayLog = pickle.load(open(log_filename, 'rb'))
		dayLogIndex = len(dayLog)
	except:
		print "No Current Log File"
		dayLogIndex = 0 


	log = {}
	data = nest.devices[0]
	structure = nest.structures[0]
	deviceData(data,log)
	sharedData(data, log)
	weatherData(data,log)

	structureData(structure,log)

	calcTotals(log,dayLog)

	if(dayLogIndex != 0):
		if(log['$timestamp'] != dayLog[dayLogIndex-1]['$timestamp']):
			dayLog.append(log)
		else:
			print "No chnage in timestamp recieved.. No new data logged."
	else:
		dayLog.append(log)

	try:
		pickle.dump(dayLog,open(log_filename,'wb'))
	except:
		print "Error Saving Log"

	for x in range(0,len(dayLog)):
		print dayLog[x]

	#print dayLog

def deviceData(data,log):
	deviceData = data._device
	log['$timestamp'] = datetime.fromtimestamp(deviceData['$timestamp']/1000).isoformat()
	

def sharedData(data,log):
	sharedData = data._shared
	log['target_type'] = sharedData['target_temperature_type']
	log['target_temperature'] = utils.c_to_f(sharedData['target_temperature'])
	log['current_temperature'] = utils.c_to_f(sharedData['current_temperature'])
	log['ac_state'] = sharedData['hvac_ac_state']

def weatherData(data,log):
	weatherData = data.weather._current
	log['outside_temperature'] = weatherData['temp_f']

def structureData(structure,log):
	structureData = structure._structure
	log['away'] = structureData['away']

def calcTotals(log, dayLog):
	dayLogLen = len(dayLog)
	if(dayLogLen == 0):
		log['total_run_time'] = 0
		log['total_run_time_home'] = 0
		log['total_run_time_away'] = 0
		log['total_trans_time'] = 0
		log['trans_time'] = False
	else:
		index = dayLogLen - 1 #list(dayLog)[dayLogLen-1]
		if(log['ac_state'] == False and dayLog[index]['ac_state'] == False):
			log['total_run_time'] = dayLog[index]['total_run_time']
			log['total_run_time_home'] = dayLog[index]['total_run_time_home']
			log['total_run_time_away'] = dayLog[index]['total_run_time_away']
			log['trans_time'] = False
			log['total_trans_time'] = dayLog[index]['total_trans_time']
		elif(log['ac_state'] == True and dayLog[index]['ac_state'] == False):
			log['total_run_time'] = dayLog[index]['total_run_time']
			log['total_run_time_home'] = dayLog[index]['total_run_time_home']
			log['total_run_time_away'] = dayLog[index]['total_run_time_away']
			log['trans_time'] = False
			log['total_trans_time'] = dayLog[index]['total_trans_time']
		else:
			lastTime = dateutil.parser.parse(dayLog[index]['$timestamp'])
			currentTime = dateutil.parser.parse(log['$timestamp'])
			diff = float((currentTime - lastTime).seconds)/60
			log['total_run_time'] = dayLog[index]['total_run_time'] + diff

			if(log['away']):
				log['total_run_time_away'] = dayLog[index]['total_run_time_away'] + diff
				log['total_run_time_home'] = dayLog[index]['total_run_time_home']
			elif(not log['away']):
				log['total_run_time_home'] = dayLog[index]['total_run_time_home'] + diff
				log['total_run_time_away'] = dayLog[index]['total_run_time_away']

			if(log['away'] == False and dayLog[index]['away'] == True and log['ac_state'] == True):
				log['trans_time'] = True
				log['total_trans_time'] = dayLog[index]['total_trans_time'] + diff
			elif(log['away'] == False and dayLog[index]['away'] == False and dayLog[index]['trans_time'] == True):
				log['trans_time'] = True
				log['total_trans_time'] = dayLog[index]['total_trans_time'] + diff
			else:
				log['trans_time'] = False
				log['total_trans_time'] = dayLog[index]['total_trans_time']








#############
# MAIN
#############
def main(args):
	nestUser = User(username=args.username,password=args.password,filename=args.accountfile)
	myNest = nestAuth(nestUser)

	dataLoop(myNest)



#############
# END OF MAIN
#############

#############
# USER CLASS
#############
class User:
	def __init__(self,username=None,password=None,filename=None):
		self.username = username
		self.password = password
		self.filename = filename








###########################
# PROG DECLARE
###########################
if __name__ == '__main__':
	args = getArgs()
	main(args)