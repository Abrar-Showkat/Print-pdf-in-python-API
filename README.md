# Python-print-pdf-http-server

#  About 

This is http-server for printing pdf using python <br />
Check the .python-version for python version used in this project <br />
You can switch the versions using pyenv module<br />

# Description
In this project there are 5 endpoints

# GET requests
'/status' is for checking the status of server
# Response
```json
{"message": "Printing service is running"}
```

'/printers' is for getting the all printers installed in local system
# Response
```json
[{"pServerName": "", "pShareName": "", "pComment": "", "pLocation": "", "pSepFile": "", "pParameters": "", "pSecurityDescriptor": null, "Attributes": "", "StartTime": "", "UntilTime": "", "cJobs": "", "name": "", "portName": "", "driverName": "", "printProcessor": "", "datatype": "", "status": "", "priority": "", "defaultPriority": "", "averagePPM": ""}]
```

'/printers/default is for getting the default printer
# Response
```json 
{"name": ""}
```
'printers/<printername>' is for getting the details of printer passed in url
# Response
```json 
{"pServerName": "", "pShareName": "", "pComment": "", "pLocation": "", "pSepFile": "", "pParameters": "", "Attributes": "", "StartTime": 0, "UntilTime": 0, "cJobs": 0, "Name": "", "portName": "", "driverName": "", "printProcessor": "", "datatype": "", "status": 0, "priority": 1, "defaultPriority": 0, "averagePPM": 0}
```
# POST request
'/print' is for posting the pdf for print to printer

# Payload

# Empty strings are optional.Their default values are set
```json
{"printData":"pdfFile","printerName":"","options"{"orientation":"","scale":""}}
```

# Response 

/status HTTP/1.1" 200


