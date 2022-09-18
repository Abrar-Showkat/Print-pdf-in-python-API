from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import win32print
import json
import urllib
from urllib.parse import unquote
import win32api
import uuid
import os
import subprocess


hostname = 'localhost'
port = 48484


class MyServer(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', "*")

        self.send_header('Access-Control-Allow-Credentials', 'true')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, OPTIONS, POST')
        self.send_header("Access-Control-Allow-Headers",
                         "*")
        self.send_header("Access-Control-Allow-Headers",
                         "Content-Type, Authorization, Content-Length")

        self.end_headers()

    def do_GET(self):

        url = unquote(self.path)
        path = url.split('/')

        printerNameParam = urllib.parse.quote(
            path[2].encode('utf-8')) if len(path) >= 3 else None
        url = f'/printers/{printerNameParam}'

        if self.path == '/status':
            try:
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')

                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(
                    {'message': 'Printing service is running'}).encode(encoding='utf-8'))
            except:
                self.send_error(500)

        elif self.path == '/printers':
            try:
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header("content-type", "application/json")
                self.end_headers()
                printers = win32print.EnumPrinters(
                    win32print.PRINTER_ENUM_LOCAL, None, 2)
                for printer in printers:

                    printer['name'] = printer['pPrinterName']
                    del printer['pPrinterName']
                    printer['portName'] = printer['pPortName']
                    del printer['pPortName']
                    printer['driverName'] = printer['pDriverName']
                    del printer['pDriverName']
                    printer['printProcessor'] = printer['pPrintProcessor']
                    del printer['pPrintProcessor']
                    printer['datatype'] = printer['pDatatype']
                    del printer['pDatatype']
                    printer['status'] = printer['Status']
                    del printer['Status']
                    printer['priority'] = printer['Priority']
                    del printer['Priority']
                    printer['defaultPriority'] = printer['DefaultPriority']
                    del printer['DefaultPriority']
                    printer['averagePPM'] = printer['AveragePPM']
                    del printer['AveragePPM']

                for printer in printers:
                    del printer['pDevMode']
                self.wfile.write(json.dumps(
                    printers).encode(encoding='utf-8'))
            except:
                self.send_error(500)

        elif self.path == '/printers/default':
            try:
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header("content-type", "application/json")
                self.end_headers()
                defaultPrinter = win32print.GetDefaultPrinterW()
                self.wfile.write(json.dumps(
                    {'name': defaultPrinter}).encode(encoding='utf-8'))

            except:
                self.send_error(500)

        elif self.path == url:
            try:
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header("content-type", "application/json")
                self.end_headers()
                pyPrintHandler = win32print.OpenPrinter(path[2])
                printer = win32print.GetPrinter(pyPrintHandler, 2)
                printer['Name'] = printer['pPrinterName']
                del printer['pPrinterName']
                printer['portName'] = printer['pPortName']
                del printer['pPortName']
                printer['driverName'] = printer['pDriverName']
                del printer['pDriverName']
                printer['printProcessor'] = printer['pPrintProcessor']
                del printer['pPrintProcessor']
                printer['datatype'] = printer['pDatatype']
                del printer['pDatatype']
                printer['status'] = printer['Status']
                del printer['Status']
                printer['priority'] = printer['Priority']
                del printer['Priority']
                printer['defaultPriority'] = printer['DefaultPriority']
                del printer['DefaultPriority']
                printer['averagePPM'] = printer['AveragePPM']
                del printer['AveragePPM']
                del printer['pDevMode']
                del printer['pSecurityDescriptor']

                self.wfile.write(json.dumps(
                    printer).encode(encoding='utf_8'))

            except:
                # self.send_error(500, message='Printer Not Found')
                # self.send_header("content-type", "application/json")
                # self.end_headers()
                self.wfile.write(json.dumps(
                    {'Error': 'Printer Not Found'}).encode())

        else:

            self.send_error(404)
            print("Specific url not found")

    def do_POST(self):

        try:
            if self.path == '/print':

                content_length = int(self.headers['Content-Length'])
                file_content = self.rfile.read(content_length)
                random_string = str(uuid.uuid4().hex)
                file_name = ''+random_string+'.pdf'

                with open(''+file_name+'', 'wb') as f:
                    f.write(file_content)

                sumatraPdfPath = "helper.exe"

                try:
                    win32print.SetDefaultPrinter('Microsoft Print to PDF')
                    printer = win32print.GetDefaultPrinter()

                    subprocess.run([''+sumatraPdfPath+'', '' +
                                    file_name+'', '-print-to-default'])

                    print("Successfully Printed")
                    # os.remove(''+file_name+'')

                except:

                    print("Not Printing")

                self.send_response(200)
                self.end_headers()
        except:
            self.send_error(500)


if __name__ == "__main__":

    webserver = HTTPServer((hostname, port), MyServer)
    print("Server started http://%s:%s" % (hostname, port))

    try:
        webserver.serve_forever()
    except KeyboardInterrupt:
        webserver.server_close()
        print("Server Stopped")
