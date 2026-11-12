import subprocess

from .Global import Utility,GlobalFunction
from .Log import ConsoleColor
from .Error import DriverError,UsageError
from .WebDriver import WebDriver


class FirefoxManager:

    def __init__(self,UserData:dict,LogModule,Data,Comm) -> None:
        
        self.LogModule = LogModule
        self.Data = Data 
        self.Comm = Comm

        self.UserData = GlobalFunction.VerifyUserSettings(self.LogModule,Comm,UserData,"geckodriver.exe","firefox",UserData["InstanceName"])

    def OpenGeckodriver(self):

        GlobalFunction.VerifySocket(self.LogModule,self.Comm,self.UserData["Port"],self.Data["ShutDownOtherSession"],"geckodriver.exe",self.UserData["InstanceName"])
        
        self.LogModule.Say(("Launching Driver : ",ConsoleColor.BLUE),(self.UserData["DriverPath"],ConsoleColor.PURPLE),StartSpace=1)
        try:
            self.Driver = subprocess.Popen([self.UserData["DriverPath"],"--port",self.UserData["Port"]],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        except Exception as E:
            raise DriverError(f"Cannot start '{Path}': {E.strerror}",
                              Details={"Command":f"{Path} --port {self.UserData["Port"]}","Port":self.UserData["Port"]}) from E
        self.Comm("Add",("UsedPort",self.UserData["Port"]))

        TimeTook = Utility.WaitOpenDriver(self.UserData["Port"],self.Data["OpenDriverTimeout"])
        
        self.LogModule.Say("--> Geckdoriver took ",(TimeTook,ConsoleColor.ORANGE)," secondes to luanch")
        self.LogModule.Say(("Finished Opening geckodriver",ConsoleColor.CYAN),StartSpace=1)


    def NewSession(self) -> None:

        self.LogModule.Say("Creating new Firefox session on port : ",(self.UserData["Port"],ConsoleColor.PURPLE))
        Resp = WebDriver.GetStatus(self.UserData["Port"])

        
        # try:
        #     Resp = WebDriver.GetStatus(self.UserData["Port"])
        #     DriverReady = Resp["value"]["ready"]
        # except Exception as E:
        #     raise DriverConnection(self.LogModule,"")
        # except Exception as E:
        #     None
            
        # Message["value"["ready"]]
        

        # try:
        #     WebDriver.NewSession()
        # except Exception as E:
        #     raise Exception()

        # try:
        #     Message = WebDriver.GetStatus(self.UserData["Port"])
        # except Exception as E:
        #     raise Exception()

    def GetData(self,Key:str):
        
        if Key not in self.UserData:
            raise UsageError(f"Key '{Key}' isn't present in UserData of this module",
                             Details={"key":Key,"UserData":self.UserData})
        return self.UserData[Key]

            

        
        # self.GLog.Say("Creating a new Firefox session : ",(SessionName,ConsoleColor.PURPLE),StartSpace=1)


    # def OpenBrowser(self):
    #     self.GLog.Say("Launching Browser : "+os.path.basename(self.UserData["FirefoxPath"]))
    #     TempActualTime = time.time()
    #     TempSessionResponse = self.RequestPost(          
    #         f"http://localhost:{self.UserData['Port']}/session",
    #         {
    #             "capabilities": {
    #                 "alwaysMatch": {
    #                     "browserName": "firefox",
    #                     "moz:firefoxOptions":self.FirefoxOptions
    #         }}}
    #     )

    #     self.GLog.Say("Geckdoriver took "+str(time.time()-TempActualTime)+" secondes to luanch")
    #     self.Data["SessionID"] = TempSessionResponse.json()["value"]["sessionId"]
    #     self.Data["BrowserOpen"] = True
    #     self.GLog.Say("Session ID : "+self.Data["SessionID"]+"\n")