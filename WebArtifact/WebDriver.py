import requests
from .Error import DriverError



class WebDriver:

    def NewSession(Port,Browser):
        try:
            Resp = requests.post(f"http://127.0.0.1:{Port}/session", json={
                "capabilities": {
                    "alwaysMatch": {
                        "browserName": Browser
                    }
                }
            })
        except:
            raise FLexError()

        try:
            Data = Resp.json()
        except:
            raise FlexError()

        return Data


    def GetStatus(Port):
        Resp = requests.get(f"http://127.0.0.1:{Port}/status")
        Data = Resp.json()
        return Data
        



# WebDriver.NewSession(4444,"firefox")
#WebDriver.GetStatus(4444)