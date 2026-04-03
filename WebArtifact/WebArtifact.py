import requests
import subprocess
import time
import socket
import sys
import os
# import json

def Decompose(Text):
    Start = 0
    Result= []
    Index = 0
    while Index < len(Text):
        if Text[Index] == " ":
            if Start != Index:
                Result.append(Text[Start:Index])
            while Text[Index] == " " and Index < len(Text)-1:
                Index+=1
            Start = Index
        Index += 1
    if len(Text) > 0 and Text[Index-1] != " ":
        Result.append(Text[Start:Index])
    return Result


class Log:                                                                                                      
    def __init__(self,mode="normal",save="console"):                                                                                # save="console" : retranscrit dans la console / save="file" : retranscrit dans un fichier
        self.Save = save
        if self.Save=="file":
            if not os.path.isdir("Log"):
                os.makedirs("Log")
            if mode == "normal":
                self.File = f"{time.strftime('%Y-%m-%d_%H:%M', time.localtime())}.log"
            elif mode == "test":
                self.File = "Log/Test.log"
            with open(self.File,"w") as TempFile:
                TempFile.write("")

    def Say(self,message):
        ActualTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())                                                           # Affiche la date et l'heure de chaque action
        if self.Save == "file":
            with open(self.File, "a") as File:
                File.write(f"[{ActualTime}] : {message}\n")
        else:
            print(f"[{ActualTime}] : {message}")
    
    def SayError(self,message):
        ActualTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())                                                           # Affiche la date et l'heure de chaque action
        if self.Save == "file":
            with open(self.File, "a") as File:
                File.write(f"[{ActualTime}] : {message}\n")
        else:
            print(f"[{ActualTime}] : {message}")
        
        raise Exception(message)

    def Console(self,message):
        print(message)
            
class S:
    def __init__(self,GeckodriverPath="geckodriver.exe",FirefoxPath=r"C:\\Program Files\\Mozilla Firefox\\firefox.exe",ProfilPath="$Temp",port="4445"):
        # sys.excepthook = self.CustomError                                                                                         # A faire
        self.UserData = {
            "GeckoDriverPath":GeckodriverPath,
            "FirefoxPath":FirefoxPath,
            "ProfilPath":ProfilPath,
            "Port":port
        }
        self.Data = {
            "OpenDriverTimeout":5,
            "BrowserOpen":False
        }
        self.FirefoxOptions = {
            "args": []
        }

        self.GLog = Log(mode="test") 
        self.GLog.Say("Log module loaded\n")
        self.VerInit()

    def VerInit(self):                                                                                                              
        self.GLog.Say("Sarting Verifying User Data")
                                                                                  
        self.IsValidApplication(self.UserData["GeckoDriverPath"],"geckodriver")                                                     # Verifie le path geckodriver
        self.IsValidApplication(self.UserData["FirefoxPath"],"firefox")                                                             # Verifie le path firefox
        self.FirefoxOptions["binary"] = self.UserData["FirefoxPath"]

        if self.UserData["ProfilPath"] == "$Temp":                                                                                  
            # self.FirefoxOptions["profile"] = "Base64-Encoded-Profil"                                                              # Utilise un profil temporaire
            self.GLog.Say("--> Firefox Profil : temp\n")
        else:
            try:
                SubprocessResult = subprocess.run([self.UserData["FirefoxPath"], "-profile", self.UserData["ProfilPath"], "-headless", "-no-remote"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=5)   # Verifie que le profils existe bien
                self.GLog.Say("--> Profile ",SubprocessResult.stdout," can be used by Firefox")
                self.FirefoxOptions["args"] += (["-profile", self.UserData["ProfilPath"]])
            except Exception:
                self.GLog.SayError("Profile cannot be used by Firefox")

    def OpenDriver(self):
        self.VerifySocket()                                                                                                         # Verifie que le port demandé n'est pas occupé
        self.GLog.Say("Launching Driver : "+os.path.basename(self.UserData["GeckoDriverPath"]))
        self.Driver = subprocess.Popen([self.UserData["GeckoDriverPath"],"--port",self.UserData["Port"]],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        # Lance GeckoDriver / stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL = aucun message dans la console
        TempTime = self.WaitOpenDriver()                                                                                            # Attend le lancement de Geckodriver
        self.GLog.Say("Geckdoriver took "+TempTime+" secondes to luanch\n")

    def OpenBrowser(self):
        self.GLog.Say("Launching Browser : "+os.path.basename(self.UserData["FirefoxPath"]))
        TempActualTime = time.time()
        TempSessionResponse = self.RequestPost(          
            f"http://localhost:{self.UserData['Port']}/session",
            {
                "capabilities": {
                    "alwaysMatch": {
                        "browserName": "firefox",
                        "moz:firefoxOptions":self.FirefoxOptions
            }}}
        )

        self.GLog.Say("Geckdoriver took "+str(time.time()-TempActualTime)+" secondes to luanch")
        self.Data["SessionID"] = TempSessionResponse.json()["value"]["sessionId"]
        self.Data["BrowserOpen"] = True
        self.GLog.Say("Session ID : "+self.Data["SessionID"]+"\n")

    def VerifySocket(self):
        self.GLog.Say("Starting Anylising port : "+self.UserData["Port"])
        RawStrResult = subprocess.run("netstat -ano | findstr :"+self.UserData["Port"],shell=True,capture_output=True)              # Enregistre les données sur le port choisie
        StrResult = RawStrResult.stdout.decode("cp850", errors="ignore")
        RawListResult = StrResult.split("\n")

        if len(RawListResult) > 0:                                                                                                  # Verifie si le port est déja utilisé ou non
            ListResult = []
            for Line in RawListResult:
                Temp = Decompose(Line)
                if len(Temp) > 1:
                    Temp[-1] = Temp[-1].replace("\r","").replace("\n","")                                                           # Affine l'affichage/enregistrement des données
                    
                    TempPID = subprocess.run("wmic process where processid="+Temp[-1]+" get ExecutablePath",shell=True,capture_output=True) # Recherche le chemin d'eexcution de touts le sprogrammes associés aux ports
                    TempPID = TempPID.stdout.decode("cp850", errors="ignore")
                    TempPID = TempPID.replace("\n","").replace("\r","")
                    TempPID = Decompose(TempPID)

                    ListResult.append({"Type":Temp[0],"LocalAdress":Temp[1],"DistantAdress":Temp[2],"Statu":(Temp[3] if Temp[0] == "TCP" else ""),"PID":Temp[-1],"Path":(TempPID[-1] if len(TempPID) > 1 else "")})
                    self.GLog.Say("--> "+str(ListResult[-1]))

            for Line in ListResult:                                                                                 
                if Line["PID"] != "0" and Line["Path"] != "":
                    if Line["Type"] == "TCP":
                        if os.path.basename(Line["Path"]).lower() not in ("python.exe","geckodriver.exe"):                          # Verifie si l'application associé aux ports est geckodriver
                            self.GLog.SayError("Another application is already using this port (Name)")
                        else:
                            self.GLog.Say("--> Geckodriver already use the port "+self.UserData["Port"])
                            try:
                                SubprocessResult = subprocess.run(f"taskkill /PID {Line['PID']} /F")                                # Ferme le processus Geckodriver
                                self.GLog.Say("==> Shutted down the old Geckodriver")
                            except Exception:
                                self.GLog.SayError("--> Unexpected Error : "+SubprocessResult.stderr+"\n≠≠> "+SubprocessResult.stdout)
                    else:
                        self.GLog.SayError("Another application is already using this port (Protocol)")
        else:
            self.GLog.Say("==> This port has no application associeted with")
        self.GLog.Say("Port "+self.UserData["Port"]+" can be used\n")
        
    
    def WaitOpenDriver(self):
        TempStart = time.time()
        while time.time() - TempStart < self.Data["OpenDriverTimeout"]:                                                             # Tant que le timeout n'a pas atteitn sa limite
            try:
                with socket.create_connection(("localhost", int(self.UserData["Port"])),timeout=0.1):                               # Tante de creer une conneciton avec le port choisie pour geckodriver
                    return str(time.time() - TempStart)
            except OSError:
                time.sleep(0.1)
        self.GLog.SayError("GeckoDriver took too long time to luanch : "+str(self.Data["OpenDriverTimeout"])+"s")                        # Renvoie une erreur si le timeout a atteint sa limite

    def CloseDriver(self):
        self.CloseBrowser()                                                                                                         # Ferme l'application firefox
        self.Driver.terminate()                                                                                                     # Envoie un signal de demande d'arret
        self.Driver.wait()                                                                                                          # Attend que le driver se ferme
        self.GLog.Say("Driver have been closed properly")

    def KillDriver(self):
        self.CloseBrowser()                                                                                                         # Ferme l'application firefox
        self.Driver.kill()                                                                                                          # Tue le processus
        self.GLog.Say("Driver have been killed")

    def CloseBrowser(self):                                                                                                         # A modif
        if self.Data["BrowserOpen"]:
            requests.delete(f"http://localhost:{self.UserData['Port']}/session/{self.Data['SessionID']}")
            self.Data["BrowserOpen"] = False
            self.GLog.Say("Browser have been closed")
        else:
            self.GLog.Say("No browser is actually running")

    def GetHTML(self):
        None

    def RequestPost(self,link,data):                                                                            
        TempSessionResponse = requests.post(link,json=data)
        if TempSessionResponse.status_code != 200:
            self.GLog.SayError(f"Session Response havn't a valid statu_code : {TempSessionResponse.status_code}\n≠≠> {TempSessionResponse.text}")
        self.GLog.Say("<< "+link+" >> returned with code "+str(TempSessionResponse.status_code))
        return TempSessionResponse

    def RequestGet(self,data):
        None

    def IsValidApplication(self,ApplicationPath,ApplicationName):
        if not os.path.isfile(ApplicationPath):                                                                                     # Verifie que le fichier existe bien
            self.GLog.SayError("--> << "+ApplicationPath+" >> isn't a valid Path")
        try:
            SubprocessResult = subprocess.run([ApplicationPath, "--version"],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=3)  # Verifie que le fichier specifié est reelement une application
            if SubprocessResult.returncode != 0:
                self.GLog.SayError("--> Unexpected Error : "+SubprocessResult.stderr+"\n≠≠>",SubprocessResult.stdout)
            TempLine = SubprocessResult.stdout.splitlines()[0]
            if ApplicationName not in TempLine.lower():                                                                             # Verifie que le nom de l'application ets bien présent dans la reponse
                self.GLog.SayError("--> "+TempLine+" isn't << "+ApplicationName+" >>")
            self.GLog.Say("--> "+TempLine)
        except Exception:
            self.GLog.SayError("--> << "+ApplicationPath+" >> isn't a valid "+ApplicationName+" Version/Apllication")



    # def CustomError(self,Type,Value,Traceback):
    #     print("\033[31mERROR OCCURED\033[0m")
    #     try:
    #         TempData = json.loads(str(Value))
    #         for TempKey,TempValue in TempData["value"].items():
    #             print(f"\033[32m{TempKey}\033[0m : \033[31m{TempValue}\033[0m")
    #     except Exception:
    #         print(Value)

az = S()

Profil = r"C:\\Users\\mathou\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\nnfkm13r.default-release"

az.OpenDriver()
az.OpenBrowser()
time.sleep(5)
az.CloseDriver()