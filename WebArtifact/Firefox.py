import subprocess

from .Global import Utility,GlobalFunction
from .Log import ConsoleColor
from .Error import FirefoxE


class FirefoxManager:

    def __init__(self,UserData:dict,LogModule,Data,Comm) -> None:
        """
        Create session and verify user settings.
        
        :param GeckodriverPath: path to geckodriver.exe
        :param FirefoxPath: binary of firefox.exe
        :param ProfilPath: path to any firefox profil
        :param ProfilName: name of a profil in profiles.init
        :param Port: port to open geckodriver
        :param SessionName: session name
        
        :return: somme des deux nombres
        """
        self.LogModule = LogModule
        self.Data = Data 
        self.Comm = Comm
        self.UserData = GlobalFunction.VerifyUserSettings(self.LogModule,UserData,Comm,"Driver","firefox")

    def OpenGeckodriver(self):
        GlobalFunction.VerifySocket(self.LogModule,self.UserData["Port"],self.Data["ShutDownOtherSession"],"geckodriver.exe","firefox")
        
        self.LogModule.Say(("Launching Driver : ",ConsoleColor.BLUE),(self.UserData["DriverPath"],ConsoleColor.PURPLE),mode="Space")
        try:
            self.Driver = subprocess.Popen([self.UserData["DriverPath"],"--port",str(self.UserData["Port"])],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        except Exception as E:
            self.LogModule.SayError(E,("Firefox","OpenDriver","Driver"))
        
        TimeTook = Utility.WaitOpenDriver(self.LogModule,self.UserData["Port"],self.Data["OpenDriverTimeout"],"geckodriver")
        
        self.LogModule.Say("--> Geckdoriver took ",(TimeTook,ConsoleColor.ORANGE)," secondes to luanch")
        self.LogModule.Say(("Finished Opening geckodriver",ConsoleColor.CYAN),mode="Space")

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