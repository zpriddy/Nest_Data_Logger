# A Nest Data Logger
##### Credits:
*Credit given to: Filippo Valsorda – https://github.com/FiloSottile for nest_thermostat and Scott M Baker for pynest  http://www.smbaker.com/  https://github.com/smbaker/pynest/blob/master/nest.py*

## Requirements
*Dateutil*
'[sudo] pip install dateutil'
*Pygal*
'[sudo] pip install pygal'

## Usage
````
Syntax: nest_data_logger.py [-h] -u USERNAME -p PASSWORD [-d]

optional arguments:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        Nest Account Username
  -p PASSWORD, --password PASSWORD
                        Nest Account Password
  -d, --debug           Debug Mode - One Time Run and Debug Info
````
## Info
Data Logged and Graphed:
 * Inside Temperature
 * Target Temperature
 * Outside Temperature
 * Total Run Time of the AC
  * Total Run Time in Home Mode
  * Total Run Time in Away Mode
  * Total Run Time to Transition from Away To Home ( in the hopes of seeing how adjusting the away temperature would effect the total run time of the day..)

Data Logged But Not Graphed:
 * AC Fan State
 * Away Status
 * Nest Leaf Temparature
  
Current Features:
 * Graphing of Current Day Usage
 * Polls Nest for new data every 2 minutes
 * Uses pickle to store log files of daily data. (one file per day – Not deleted)

Features in Progress:
 * Simple python web framework (cherryPy?)
 * Ability to render graphs for any day that data was collected
 * **Maybe** Using mongodb to store data



## Notes
When used without the debug option, the code will poll the nest every two minutes. It uses threading to keep looping the code until you hit ctrl+c. I would suggest running this using screen. 
The debug option will only run once. 

