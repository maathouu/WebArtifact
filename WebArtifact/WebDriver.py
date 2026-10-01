import requests



class WebDriver:

    def NewSession(Port,Browser):
        Resp = requests.post(f"http://127.0.0.1:{Port}/session", json={
            "capabilities": {
                "alwaysMatch": {
                    "browserName": Browser
                }
            }
        })
        Data = Resp.json()
        return Data
        print(Data)


    def GetStatus(Port):
        Resp = requests.get(f"http://127.0.0.1:{Port}/status")
        Data = Resp.json()
        return Data
        print(Data)



# WebDriver.NewSession(4444,"firefox")
#WebDriver.GetStatus(4444)