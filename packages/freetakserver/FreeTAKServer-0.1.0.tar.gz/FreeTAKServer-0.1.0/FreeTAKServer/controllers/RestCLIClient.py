import http
import json
from FreeTAKServer.controllers.CreateStartupFilesController import CreateStartupFilesController
from FreeTAKServer.controllers.Orchestrator import Orchestrator
from FreeTAKServer.controllers.DataPackageServer import FlaskFunctions
from FreeTAKServer.controllers.configuration.RestAPIVariables import RestAPIVariables as vars
from FreeTAKServer.controllers.configuration.OrchestratorConstants import OrchestratorConstants
from FreeTAKServer.controllers.configuration.DataPackageServerConstants import DataPackageServerConstants
from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.controllers.CreateLoggerController import CreateLoggerController
from FreeTAKServer.controllers.AsciiController import AsciiController
from FreeTAKServer.controllers.model.FTS import FTS
from FreeTAKServer.controllers.model.RestAPIService import RestAPIService

loggingConstants = LoggingConstants()
logger = CreateLoggerController("CLI").getLogger()

json_content = vars()
json_content.default_values()
json_content.json_content()
connectionIP = str(RestAPIService().RestAPIServiceIP)
connectionPort = int(RestAPIService().RestAPIServicePort)

class RestCLIClient:

    def __init__(self):
        self.killSwitch = False
        self.conn = http.client.HTTPConnection(connectionIP, connectionPort)

    def change_connection_info(self):
        global connectionIP, connectionPort
        ip = str(input('please enter desired IP for connection[' + str(connectionIP) + ']') or connectionIP)
        port = int(input('please enter desired Port for connection[' + str(connectionPort) + ']') or connectionPort)
        connectionIP = ip
        connectionPort = port
        return 1
    def start_CoT_service(self):
        try:
            self.CoTIP = str(
                input('enter CoT_service IP[' + str(OrchestratorConstants().IP) + ']: ')) or OrchestratorConstants().IP
            self.CoTPort = input('enter CoT_service Port[' + str(OrchestratorConstants().COTPORT) + ']: ') or int(
                OrchestratorConstants().COTPORT)
            self.CoTPort = int(self.CoTPort)
            #send start COT to API
            body = json.dumps({"CoTService": {"IP": str(self.CoTIP), "PORT": int(self.CoTPort)}})
            self.conn.request("POST", "/CoTService",  body, {"Content-type": "application/json", "Accept": "text/plain"})
            response = self.conn.getresponse()
            return 1
        except Exception as e:
            logger.error('an exception has been thrown in CoT service startup ' + str(e))
            return -1

    def stop_CoT_service(self):
        try:
            self.conn.request("DELETE", "/CoTService")
            response = self.conn.getresponse()
            return 1
        except Exception as e:
            logger.error("there's been an exception in the stopping of CoT Service " + str(e))
            return -1

    def start_data_package_service(self):
        try:

            self.APIPort = str(input('enter DataPackage_Service Port[' + str(
                DataPackageServerConstants().APIPORT) + ']: ')) or DataPackageServerConstants().APIPORT
            self.APIPort = int(self.APIPort)
            self.APIIP = str(input('enter DataPackage_Service IP[' + str(
                DataPackageServerConstants().IP) + ']: ')) or DataPackageServerConstants().IP
            #send start request
            conn = http.client.HTTPConnection(connectionIP, connectionPort)
            body = json.dumps({"DataPackageService":{"IP": str(self.APIIP), "PORT": int(self.APIPort)}})
            conn.request("POST", "/DataPackageService", body, {"Content-type": "application/json", "Accept": "text/plain"})
            response = conn.getresponse()
            return 1
        except Exception as e:
            logger.error('there has been an exception in the indevidual starting of the Dwata Packages Service')
            return -1

    def stop_data_package_service(self):
        try:
            conn = http.client.HTTPConnection(connectionIP, connectionPort)
            conn.request("DELETE", "/DataPackageService")
            response = conn.getresponse()
            return 1
        except Exception as e:
            logger.error("there's been an exception in the termination of DataPackage Service " + str(e))
            return -1

    def start_all(self):
        try:
            json_content.setdefaultCoTIP(input('Please enter the CoT service IP [' + str(FTS().CoTService.CoTServiceIP) + ']: ') or FTS().CoTService.CoTServiceIP)
            json_content.setdefaultCoTPort(input('Please enter the CoT service Port [' + str(FTS().CoTService.CoTServicePort) + ']: ') or FTS().CoTService.CoTServicePort)
            json_content.setdefaultDataPackagePort(input('Please enter the Data Package service Port [' + str(FTS().DataPackageService.DataPackageServicePort) + ']: ') or FTS().DataPackageService.DataPackageServicePort)
            json_content.setdefaultDataPackageIP(input('Please enter the Data Package service IP [' + str(FTS().DataPackageService.DataPackageServiceIP) + ']: ') or FTS().DataPackageService.DataPackageServiceIP)
            body = json.dumps(json_content.getJsonStatusStartAll())
            conn = http.client.HTTPConnection(connectionIP, connectionPort)
            conn.request("POST", "/changeStatus", body, {"Content-type": "application/json", "Accept": "text/plain"})
            response = conn.getresponse()
            conn.close()
            return 1
        except Exception as e:
            logger.error('there has been an exception in RestCLIClient start_all ' + str(e))
            return -1
    
    def stop_all(self):
        try:
            conn = http.client.HTTPConnection(connectionIP, connectionPort)
            body = json.dumps({"CoTService": {"STATUS": "stop"},
                               "DataPackageService": {"STATUS": "stop"}})
            conn.request("POST", "/changeStatus", body, {"Content-type": "application/json", "Accept": "text/plain"})
            response = conn.getresponse()
            return 1
        except Exception as e:
            logger.error('there has been an exception in RestCLIClient stop_all ' + str(e))
            return -1

    def help(self):
        print('start_all: to begin all services type')
        print('start_CoT_service: to begin CoT service type')
        print('start_data_package_service: to begin data package service  type')
        print('stop_all: to terminate all services type')
        print('stop_CoT_service: to terminate CoT service type')
        print('stop_data_package_service: to begin data package service type')
        print('check_service_status: to check the status of the services type')
        print('show_users: to show connected user information type')
        print('kill: to kill the full server type')
        return 1

    def check_service_status(self):
        pass
        return 1

    def show_client_array(self):
        print(self.clientInformationArray)
        print('length is ' + len(self.clientInformationArray))
        return 1

    def show_users(self):
        try:
            conn = http.client.HTTPConnection(connectionIP, connectionPort)
            conn.request("GET", "/Clients")
            data = conn.getresponse()
            conn.close()
            data = data.read().decode('utf-8')
            data = json.loads(data)
            data.insert(0, {'ip': 'IP', 'team': 'TEAM', 'callsign': 'CALLSIGN'})
            col_width = max(len(word) for row in data for word in row.values()) + 2  # padding
            for row in data:
                print("".join(word.ljust(col_width) for word in row.values()))
            return 1

        except Exception as e:
            print(e)

    def ServerGeochat(self):
        try:
            conn = http.client.HTTPConnection(connectionIP, connectionPort)
            text = input('enter message: ')
            body = json.dumps({"detail": {'remarks': {"INTAG": text}}})
            conn.request("POST", "/SendGeoChat", body, {"Content-type": "application/json", "Accept": "application/json"})
            data = conn.getresponse()
            conn.close()
            data = data.read().decode('utf-8')
        except Exception as e:
            pass

    def verify_output(self, input, example=None):
        try:
            if example == None:
                if input == None or input == -1:
                    return False
                else:
                    return True

            else:
                if isinstance(input, example):
                    return True
                else:
                    return False
        except Exception as e:
            logger.error('there has been an exception in RestCLIClient verifying output ' + str(e))
            return False

    def kill(self):
        try:
            self.killSwitch = True
            return 1
        except Exception as e:
            logger.error('error in kill function '+str(e))

    def empty(self):
        return 1

    def receive_input(self):
        conn = http.client.HTTPConnection(connectionIP, connectionPort)
        while self.killSwitch == False:
            try:
                self.UserCommand = str(input('FTS$ ')) or 'empty'
                try:
                    function = getattr(self, self.UserCommand)
                except:
                    logger.error('this is not a valid command')
                functionOutput = function()
                if self.verify_output(functionOutput):
                    pass
                else:
                    raise Exception('function returned bad data')
            except Exception as e:
                logger.error('error in processing your request ' + str(e))
        self.stop_all()


if __name__ == "__main__":
    RestCLIClient().receive_input()