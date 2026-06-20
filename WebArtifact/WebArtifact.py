# import requests
# import subprocess
# import time
# import socket
import sys

from .Log import LogManager,ConsoleColor
from .Error import GlobalE


class S:
    def __init__(self) -> None:
        
        self.Data = {
            "Session":{
                "OpenDriverTimeout":5,
                "BrowserOpen":False,
                "ShutDownOtherSession":True,
            },
            "Log":{
                "Save":"both",
                "Mode":"test"
            }
        }
        self.InternalData = {
            "UsedPort":[],
            "PreUsedPort":[],
            "SessionName":0
        }
        self.Browsers = {

        }
        self.GLog = LogManager(mode=self.Data["Log"]["Mode"],save=self.Data["Log"]["Save"]) 
        self.GLog.Say("Log module loaded")


    def Firefox(self,GeckodriverPath:str="geckodriver.exe",FirefoxPath:str=r"C:\Program Files\Mozilla Firefox\firefox.exe",ProfilPath:str="",ProfilName:str="Temp",Port="auto",SessionName:str="$") -> None:
        """
        Create New Firefox session and verify user settings.
        
        :param GeckodriverPath: path to geckodriver.exe
        :param FirefoxPath: binary of firefox.exe
        :param ProfilPath: path to any firefox profil
        :param ProfilName: name of a profil in profiles.ini
        :param Port: port to open geckodriver
        :param SessionName: session name
        
        """# :return: somme des deux nombres 
                       
        self.GLog.Changecategory("None")
        if "WebArtifact.Firefox" not in sys.modules:
            from .Firefox import FirefoxManager
        else:
            FirefoxManager = sys.modules["WebArtifact.Firefox"].FirefoxManager

        if SessionName == "$":
            SessionName = str(self.InternalData["SessionName"])
            self.InternalData["SessionName"] += 1
        elif type(SessionName) != str:
            raise GlobalE.BadUtilisation(self.GLog,
                                         "Custom Session name need to be str value",0,
                                         DetailedContext=f"'{SessionName}' is an {type(SessionName)} value and not str",
                                         SessionNameGot=SessionName,SessionNameType=type(SessionName))
        if SessionName in self.Browsers:
            raise GlobalE.BadUtilisation(self.GLog,
                                         "Session name specified is already used",0,
                                         DetailedContext=f"SessionName '{SessionName}' have already been created : '{[x for x in self.Browsers]}'",
                                         SessionNameGot=SessionName,SessionNameUsed=[x for x in self.Browsers])
            
        self.CurrentWorkingSession = SessionName

        self.GLog.Say("Creating a new Firefox session : ",(SessionName,ConsoleColor.PURPLE),StartSpace=1)
        self.GLog.Changecategory("Firefox profil verif")
        self.Browsers[SessionName] = {
            "Module":FirefoxManager({
                            "DriverPath":GeckodriverPath,
                            "BrowserPath":FirefoxPath,
                            "ProfilPath":ProfilPath,
                            "ProfilName":ProfilName,
                            "Port":Port
                           },
                           self.GLog,
                           self.Data["Session"],
                           self.Comm),
            "Browser":"Firefox",
            "Statu":0}
        
        self.Browsers[SessionName]["Statu"] = 1


    def Comm(self,mode="Get",data=None):
        if mode == "Get":
            return self.InternalData
        elif mode == "Set":
            self.InternalData[data[0]] = data[1]
        elif mode == "Add":
            self.InternalData[data[0]].append(data[1])


    def OpenDriver(self,SessionName="$") -> None:
        
        if not len(self.Browsers) > 0:
            raise GlobalE.BadUtilisation(self.GLog,
                                         "No Session created",0,
                                         DetailedContext=f"You need to create a session before opening it's driver")
        
        if SessionName == "$":
            SessionName = self.CurrentWorkingSession
        elif SessionName not in self.Browsers:
            raise GlobalE.BadUtilisation(self.GLog,
                                         f"No sessionname named '{SessionName}'",0,
                                         DetailedContext=f"SessionName '{SessionName}' haven't been created : '{[x for x in self.Browsers]}'",
                                         SessionNameGot=SessionName,SessionNameUsed=[x for x in self.Browsers])
        
        if self.Browsers[SessionName]["Statu"] != 1:
            raise GlobalE.BadUtilisation(self.GLog,
                                         f"Session {SessionName} hasn't a valid statu code",0,
                                         DetailedContext=f"Session {SessionName} statu isn't equal to 1 : {self.Browsers[SessionName]["Statu"]}",
                                         SessionName=SessionName,SessionStatu=self.Browsers[SessionName]["Statu"])
        
        self.Browsers[SessionName]["Statu"] = 2

        match self.Browsers[SessionName]["Browser"]:
            case "Firefox":
                self.GLog.Changecategory("Geckodriver luanch")
                self.Browsers[SessionName]["Module"].OpenGeckodriver()

            case "Chrome":
                None

        self.Browsers[SessionName]["Statu"] = 3
            
        

    def OpenBrowser(self,SessionName="$"):
        None


    def Luanch(self,SessionName="$"):
        None





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

    # def VerifySocket(self):
    #     self.GLog.Say("Starting Anylising port : "+self.UserData["Port"])
    #     try:
    #         RawStrResult = subprocess.run("netstat -ano | findstr :"+self.UserData["Port"],shell=True,capture_output=True,text=True)    # Enregistre les données sur le port choisie
    #     except subprocess.CalledProcessError as T:
    #         self.GLog.SayError("--> Unexpected Error : returned with code "+T.returncode+"\n≠≠> "+T.stderr)
    #     RawListResult = RawStrResult.stdout.split("\n")

    #     if len(RawListResult) > 0:                                                                                                  # Verifie si le port est déja utilisé ou non
    #         ListResult = []
    #         for Line in RawListResult:
    #             Temp = Decompose(Line)
    #             if len(Temp) > 1:
    #                 Temp[-1] = Temp[-1].replace("\r","").replace("\n","")                                                           # Affine l'affichage/enregistrement des données
                    
    #                 try :
    #                     TempPID = subprocess.run("wmic process where processid="+Temp[-1]+" get ExecutablePath",capture_output=True,text=True) # Recherche le chemin d'eexcution de touts le sprogrammes associés aux ports
    #                 except subprocess.CalledProcessError as T:
    #                     self.GLog.SayError("--> Unexpected Error : returned with code "+T.returncode+"\n≠≠> "+T.stderr)
    #                 TempPID = TempPID.stdout.replace("\n","").replace("\r","")
    #                 TempPID = Decompose(TempPID)

    #                 ListResult.append({"Type":Temp[0],"LocalAdress":Temp[1],"DistantAdress":Temp[2],"Statu":(Temp[3] if Temp[0] == "TCP" else ""),"PID":Temp[-1],"Path":(TempPID[-1] if len(TempPID) > 1 else "")})
    #                 self.GLog.Say("--> "+str(ListResult[-1]))

    #         for Line in ListResult:                                                                                 
    #             if Line["PID"] != "0" and Line["Path"] != "":
    #                 if Line["Type"] == "TCP":
    #                     if os.path.basename(Line["Path"]).lower() not in ("python.exe","geckodriver.exe"):                          # Verifie si l'application associé aux ports est geckodriver
    #                         self.GLog.SayError("Another application is already using this port (Name)")
    #                     else:
    #                         self.GLog.Say("--> Geckodriver already use the port "+self.UserData["Port"])
    #                         try:
    #                             SubprocessResult = subprocess.run(f"taskkill /PID {Line['PID']} /F") # Ferme le processus Geckodriver
    #                         except subprocess.CalledProcessError as T:
    #                             self.GLog.SayError("--> Unexpected Error : returned with code "+T.returncode+"\n≠≠> "+T.stderr)
    #                         self.GLog.Say("==> Shutted down the old Geckodriver")
    #                 else:
    #                     self.GLog.SayError("Another application is already using this port (Protocol)")
    #     else:
    #         self.GLog.Say("==> This port has no application associeted with")
    #     self.GLog.Say("Port "+self.UserData["Port"]+" can be used\n")
        
    
    # def WaitOpenDriver(self):
    #     TempStart = time.time()
    #     while time.time() - TempStart < self.Data["OpenDriverTimeout"]:                                                             # Tant que le timeout n'a pas atteitn sa limite
    #         try:
    #             with socket.create_connection(("localhost", int(self.UserData["Port"])),timeout=0.1):                               # Tante de creer une conneciton avec le port choisie pour geckodriver
    #                 return str(time.time() - TempStart)
    #         except OSError:
    #             time.sleep(0.1)
    #     self.GLog.SayError("GeckoDriver took too long time to luanch : "+str(self.Data["OpenDriverTimeout"])+"s")                        # Renvoie une erreur si le timeout a atteint sa limite

    # def CloseDriver(self):
    #     self.CloseBrowser()                                                                                                         # Ferme l'application firefox
    #     self.Driver.terminate()                                                                                                     # Envoie un signal de demande d'arret
    #     self.Driver.wait()                                                                                                          # Attend que le driver se ferme
    #     self.GLog.Say("Driver have been closed properly")

    # def KillDriver(self):
    #     self.CloseBrowser()                                                                                                         # Ferme l'application firefox
    #     self.Driver.kill()                                                                                                          # Tue le processus
    #     self.GLog.Say("Driver have been killed")

    # def CloseBrowser(self):                                                                                                         # A modif
    #     if self.Data["BrowserOpen"]:
    #         requests.delete(f"http://localhost:{self.UserData['Port']}/session/{self.Data['SessionID']}")
    #         self.Data["BrowserOpen"] = False
    #         self.GLog.Say("Browser have been closed")
    #     else:
    #         self.GLog.Say("No browser is actually running")

    # def GetHTML(self):
    #     None

    # def RequestPost(self,link,data):                                                                            
    #     TempSessionResponse = requests.post(link,json=data)
    #     if TempSessionResponse.status_code != 200:
    #         self.GLog.SayError(f"Session Response havn't a valid statu_code : {TempSessionResponse.status_code}\n≠≠> {TempSessionResponse.text}")
    #     self.GLog.Say("<< "+link+" >> returned with code "+str(TempSessionResponse.status_code))
    #     return TempSessionResponse

    # def RequestGet(self,data):
    #     None

    

    



    # def CustomError(self,Type,Value,Traceback):
    #     print("\033[31mERROR OCCURED\033[0m")
    #     try:
    #         TempData = json.loads(str(Value))
    #         for TempKey,TempValue in TempData["value"].items():
    #             print(f"\033[32m{TempKey}\033[0m : \033[31m{TempValue}\033[0m")
    #     except Exception:
    #         print(Value)

