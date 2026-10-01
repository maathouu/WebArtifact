import subprocess

from .Global import Utility,GlobalFunction
from .Log import ConsoleColor
from .Error import FlexError,CantOpenDriver
from .WebDriver import WebDriver


class FirefoxManager:

    def __init__(self,UserData:dict,LogModule,Data,Comm) -> None:
        
        self.LogModule = LogModule
        self.Data = Data 
        self.Comm = Comm

        self.UserData = GlobalFunction.VerifyUserSettings(self.LogModule,UserData,Comm,"geckodriver.exe","firefox",UserData["InstanceName"])

    def OpenGeckodriver(self):

        GlobalFunction.VerifySocket(self.LogModule,self.UserData["Port"],self.Data["ShutDownOtherSession"],"geckodriver.exe",self.UserData["InstanceName"])
        
        self.LogModule.Say(("Launching Driver : ",ConsoleColor.BLUE),(self.UserData["DriverPath"],ConsoleColor.PURPLE),StartSpace=1)
        try:
            self.Driver = subprocess.Popen([self.UserData["DriverPath"],"--port",str(self.UserData["Port"])],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        except Exception as E:
            raise CantOpenDriver(self.LogModule,"",self.UserData["InstanceName"],"geckodriver",self.UserData["Port"],
                                 ErrorModule=E,Unexpected="Subprocess",
                                 Command=f"{self.UserData["DriverPath"]} --port {self.UserData["Port"]}")  # TT
        
        try:TimeTook = Utility.WaitOpenDriver(self.UserData["Port"],self.Data["OpenDriverTimeout"])
        except FlexError as E:raise CantOpenDriver(self.LogModule,self.UserData["InstanceName"],"geckodriver",self.UserData["Port"],
                                                   DetailedContext=E.DetailedContext,
                                                   TimeTook=E.TimeTook,Timeout=self.Data["OpenDriverTimeout"])  # TT

        self.LogModule.Say("--> Geckdoriver took ",(TimeTook,ConsoleColor.ORANGE)," secondes to luanch")
        self.LogModule.Say(("Finished Opening geckodriver",ConsoleColor.CYAN),StartSpace=1)


    def NewSession(self) -> None:

        self.LogModule.Say("Creating new Firefox session on port : ",(self.UserData["Port"],ConsoleColor.PURPLE))
        try:
            Message = WebDriver.GetStatus(self.UserData["Port"])
        except Exception as E:
            raise Exception()

        try:
            WebDriver.NewSession()
        except Exception as E:
            raise Exception()

        try:
            Message = WebDriver.GetStatus(self.UserData["Port"])
        except Exception as E:
            raise Exception()



        



        
        # self.GLog.Say("Creating a new Firefox session : ",(SessionName,ConsoleColor.PURPLE),StartSpace=1)
























    # def OpenDriver(self):
    #     self.VerifySocket()                                                                                                         # Verifie que le port demandé n'est pas occupé
    #     self.GLog.Say("Launching Driver : "+os.path.basename(self.UserData["GeckoDriverPath"]))
    #     self.Driver = subprocess.Popen([self.UserData["GeckoDriverPath"],"--port",self.UserData["Port"]],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    #     # Lance GeckoDriver / stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL = aucun message dans la console
    #     TempTime = self.WaitOpenDriver()                                                                                            # Attend le lancement de Geckodriver
    #     self.GLog.Say("Geckdoriver took "+TempTime+" secondes to luanch\n")

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