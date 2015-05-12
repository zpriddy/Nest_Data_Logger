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

## Notes
When used without the debug option, the code will poll the nest every two minutes. It uses threading to keep looping the code until you hit ctrl+c. I would suggest running this using screen. 
The debug option will only run once. 

