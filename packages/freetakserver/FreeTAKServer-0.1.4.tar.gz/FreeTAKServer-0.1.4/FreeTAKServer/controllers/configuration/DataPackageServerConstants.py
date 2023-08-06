import os
import pathlib


class DataPackageServerConstants:
    def __init__(self):
        # http server config
        self.DATABASE = 'FreeTAKServerDataPackageDataBase.db'
        self.APIPORT = '8080'
        self.DEFAULTRETURN = 'other'
        self.GET = 'GET'
        self.PUT = 'PUT'
        self.POST = 'POST'
        self.DATAPACKAGEFOLDER = 'FreeTAKServerDataPackageFolder'
        self.HTTPDEBUG = False
        self.HTTPMETHODS = ['POST', 'GET', 'PUT']
        self.IP = "0.0.0.0"
        self.versionInfo = 'FreeTAKServer-1.0RC1'
        self.NodeID = 'FTS'
        self.VERSIONJSON = '{"version":"2","type":"ServerConfig", "data":{"version": "%s", "api": "2","hostname":"%s"}, "nodeId":"%s"}' % (
            self.versionInfo, "0.0.0.0", self.NodeID)
