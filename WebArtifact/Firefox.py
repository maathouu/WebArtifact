import os
import json
import subprocess

from .Utility import IsValidApplication,IsValidPort,ReadIni,VerifySocket,WaitOpenDriver
from .Log import ConsoleColor

class FirefoxManager:

    def __init__(self,UserData:dict,LogModule,Data,Comm) -> None:
        self.UserData = UserData
        self.LogModule = LogModule
        self.Data = Data 
        self.Comm = Comm
        self.UserDataVer()

    def UserDataVer(self):
        self.UserData["FirefoxOptions"] = {"args": []}

        self.LogModule.Say(("Verifying Application Path",ConsoleColor.BLUE),mode="Space")                                                                      
        IsValidApplication(self.LogModule,self.UserData["DriverPath"],"geckodriver")                                                     # Verifie le path geckodriver
        IsValidApplication(self.LogModule,self.UserData["BrowserPath"],"firefox")                                                        # Verifie le path firefox
        self.UserData["FirefoxOptions"]["binary"] = self.UserData["BrowserPath"]
        
        self.LogModule.Say(("Verifying Port",ConsoleColor.BLUE),mode="Space") 
        self.UserData["Port"] = IsValidPort(self.LogModule,self.UserData["Port"],self.Comm()["UsedPort"])

        self.LogModule.Say(("Verifying Firefox Profil Name",ConsoleColor.BLUE),mode="Space")
        if self.UserData["ProfilName"] == "Temp" and self.UserData["ProfilPath"] == "":
            self.LogModule.Say("--> Firefox Profil Name: Temp")
            self.LogModule.Say("==> ",("A temporary file will be created and deleted automatically",ConsoleColor.YELLOW))
        elif self.UserData["ProfilName"] != "Temp":
            FirefoxProfilesIniPath = os.path.join(os.environ.get("APPDATA", ""),"Mozilla","Firefox","profiles.ini")
            if not os.path.isfile(FirefoxProfilesIniPath):
                self.LogModule.Say("==> ",(FirefoxProfilesIniPath,ConsoleColor.PURPLE),("dosn't exist",ConsoleColor.YELLOW))
            else:
                Profiles = ReadIni(self.LogModule,FirefoxProfilesIniPath)
                ProfilesInfos = {}
                for Profile in Profiles:
                    if Profile[:7] == "Profile":
                        self.LogModule.Say("--> Name : ",(f"{Profiles[Profile]["Name"]:<20}",ConsoleColor.PURPLE)," / Path : ",(Profiles[Profile]["Path"],ConsoleColor.PURPLE))
                        ProfilesInfos[Profiles[Profile]["Name"]] = Profiles[Profile]["Path"]
                if self.UserData["ProfilName"] in ProfilesInfos:
                    self.UserData["FirefoxOptions"]["args"] += (["-profile", os.path.join(os.environ.get("APPDATA", ""),"Mozilla","Firefox",ProfilesInfos[self.UserData["ProfilName"]])])
                    self.LogModule.Say("==> ",("Firefox Profil Name: ",ConsoleColor.YELLOW),(self.UserData["ProfilName"],ConsoleColor.PURPLE)," / Profil Path : ",(self.UserData["FirefoxOptions"]["args"][1],ConsoleColor.PURPLE))
                else:
                    if self.UserData["ProfilPath"] != "":
                        self.LogModule.Say("==> ",("No Profil named : ",ConsoleColor.YELLOW),(self.UserData["ProfilName"],ConsoleColor.PURPLE))
                    else:
                        self.LogModule.SayError("NoName",("Firefox","VerifProfil","ProfilName"),profil=self.UserData["ProfilName"])
        
        if len(self.UserData["FirefoxOptions"]["args"]) == 0:
            self.LogModule.Say(("Verifying Firefox Profil Path",ConsoleColor.BLUE),mode="Space")
            if os.path.isdir(self.UserData["ProfilPath"]):
                FirefoxOptionalFiles = {
                    "prefs.js",         # créé au 1er lancement
                    "places.sqlite",    # Historique et favoris
                    "cookies.sqlite",   # Cookies
                    "cert9.db",         # Certificats 
                    "key4.db"           # Mots de passe 
                }
                TimesFilePath = os.path.join(self.UserData["ProfilPath"],"times.json")
                try:
                    with open(TimesFilePath,"r") as File:
                        TimesFile = json.load(File)
                except Exception as E:
                    self.LogModule.SayError(E,("Firefox","VerifProfil","times.json"),path=TimesFilePath)
                
                self.LogModule.Say("--> ",(f"{'times.json':<20}",ConsoleColor.PURPLE),": ",("present",ConsoleColor.BOLD))
                if ("created","firstUse") != tuple(TimesFile.keys()):
                    self.LogModule.SayError("InvalidKey",("Firefox","VerifProfil","times.json"),value=str(tuple(TimesFile.keys())),value_needed="('created','firstUse')")

                for OptionalFIle in FirefoxOptionalFiles:
                    self.LogModule.Say("--> ",(f"{OptionalFIle:<20}",ConsoleColor.PURPLE),": ",(("present" if os.path.isfile(os.path.join(self.UserData["ProfilPath"],OptionalFIle)) else "absent"),ConsoleColor.BOLD))

                if TimesFile["firstUse"] == None:
                    self.LogModule.Say("==> ",(f"{TimesFilePath}",ConsoleColor.PURPLE),(" never been luanch before",ConsoleColor.YELLOW))

            elif os.path.isfile(self.UserData["ProfilPath"]):
                self.LogModule.SayError("IsFile",("Firefox","VerifProfil","ProfilPath"),path=self.UserData["ProfilPath"])
            else:
                self.LogModule.SayError("NoFile",("Firefox","VerifProfil","ProfilPath"),path=self.UserData["ProfilPath"])
        self.LogModule.Say(("Finished verifying User settings",ConsoleColor.CYAN),mode="Space")

    def OpenGeckodriver(self):
        UsedPort = self.Comm()["UsedPort"]
        ProcResult = VerifySocket(self.LogModule,self.UserData["Port"])
        
        if ProcResult != ['']:
            for Line in ProcResult:
                if Line["PID"] != 0 and Line["Path"] != "":
                    if Line["Type"] == "TCP":
                        if Line["Path"] != None and os.path.basename(Line["Path"]).lower() == "geckodriver.exe":
                            if self.UserData["Port"] in UsedPort:
                                self.LogModule.SayError("UsedSessionPort",("Utility","VerifySocket"),port=self.UserData["Port"],data=Line,usedport=UsedPort)
                            self.LogModule.Say("==> ",("Another geckodriver proc is already using this port / Shutdown = ",ConsoleColor.YELLOW),(str(self.Data["ShutDownOtherSession"]),ConsoleColor.PINK))
                            
                            # Try to communicate with other geckodriver, to know who use it and if we can shutdown it
                            
                            if self.Data["ShutDownOtherSession"]:
                                try:
                                    subprocess.run(f"taskkill /PID {Line['PID']} /F",stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                                except Exception as E:
                                    self.LogModule.SayError(E,("Utility","VerifySocket")) 
                                self.LogModule.Say("==> ",("Other geckodriver proc have been shutted down",ConsoleColor.YELLOW))
                            else:
                                self.LogModule.SayError("NoShutdown",("Utility","VerifySocket"),port=self.UserData["Port"],data=Line)
                        elif Line["Path"] != None:
                            self.LogModule.SayError("OtherApplication",("Utility","VerifySocket"),port=self.UserData["Port"],data=Line)
                else:
                    self.LogModule.SayError("WrongProtocol",("Utility","VerifySocket"),port=self.UserData["Port"],data=Line)
        else:
            self.LogModule.Say("==> ",("This socket has no application associated with",ConsoleColor.YELLOW))

        
        self.LogModule.Say(("Launching Driver : ",ConsoleColor.BLUE),(self.UserData["DriverPath"],ConsoleColor.PURPLE),mode="Space")
        try:
            self.Driver = subprocess.Popen([self.UserData["DriverPath"],"--port",str(self.UserData["Port"])],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        except Exception as E:
            self.LogModule.SayError(E,("Firefox","OpenDriver","Driver"))
        
        TimeTook = WaitOpenDriver(self.LogModule,self.UserData["Port"],self.Data["OpenDriverTimeout"],"geckodriver")
        
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