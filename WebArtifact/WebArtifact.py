# import requests
# import subprocess
# import time
# import socket
# import sys
# import os

from .Log import LogManager


    
            
class S:
    def Firefox(self,GeckodriverPath="geckodriver.exe",FirefoxPath=r"C:\Program Files\Mozilla Firefox\firefox.exe",ProfilPath="",ProfilName="Temp",port="4445"):
        
        from .Firefox import UserSettingsVer

        self.UniversalUserData = {
            "DriverPath":GeckodriverPath,
            "BrowserPath":FirefoxPath,
            "ProfilPath":ProfilPath,
            "ProfilName":ProfilName,
            "Port":port
        }
        self.UniversalData = {
            "OpenDriverTimeout":5,
            "BrowserOpen":False
        }

        self.GLog = LogManager(mode="test") 
        self.GLog.Say("Log module loaded\n")
        self.GLog.Say("Firefox webdriver selected")
        self.FirefoxOptions = UserSettingsVer(self.GLog,self.UniversalUserData)


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

