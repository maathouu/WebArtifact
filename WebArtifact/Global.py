import time
import socket
import subprocess
import os
import json

import requests # Temp

from .Log import ConsoleColor
from .Error import GlobalE

class Utility:
    def Decompose(Text:str) -> list:
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

    def SupFLSpace(Text:str) -> str:
        if len(Text) > 1:
            Index = 0
            while Text[Index] == " " and Index < len(Text):
                Index+=1
            Start = Index
            Index = len(Text)-1
            while Text[Index] == " " and Index != 0:
                Index-=1
            return Text[Start:Index+1]
        else:
            return Text
        
    def IsValidApplication(ApplicationPath:str,ApplicationName:str,ModuleInfo:tuple) -> bool:
            try:
                SubprocessResult = subprocess.run([ApplicationPath,"--version"],capture_output=True,text=True)
            except Exception as E:
                raise ModuleInfo[0](ModuleInfo[1],"",ModuleInfo[2],ModuleInfo[3],0,
                                    ErrorModule=E,Unexpected="Subprocess",Command=f"{ApplicationPath} --version")
            TempLine = SubprocessResult.stdout.splitlines()[0]
            return ApplicationName.lower() in TempLine.lower(),TempLine.lower()

    def ReadIniFile(FilePath:str) -> dict:
        result = {}
        with open(FilePath,"r") as f:
            File = f.readlines()

        ActualSection = None
        for Line in File:
            Line = Utility.SupFLSpace(Line).replace("\n","")
            if len(Line) > 0:
                if Line[0] == "[" and Line[-1] == "]":
                    ActualSection = Line[1:-1]
                    result[ActualSection] = {}
                elif Line[0] != ";":
                    Line = Line.split("=")
                    result[ActualSection][Line[0]] = Line[1]
        return result

    def WaitOpenDriver(Port:str,TimeOut:int,ModuleInfo:tuple) -> int:
        TimeStart = time.time()
        Finished = False
        while time.time() - TimeStart < TimeOut and  not Finished:
            try:
                with socket.create_connection(("localhost", Port),timeout=0.1):
                    return str(time.time() - TimeStart)
            except OSError:
                time.sleep(0.1)
            except Exception as E:
                raise ModuleInfo[0](ModuleInfo[1])
        raise ModuleInfo[0](ModuleInfo[1])  #ToDo

    def ReadJsonFile(LogModule:object,ErrorModule:object,FilePath:str,Driver:str,ParentModule:str) -> dict:
        try:
            with open(FilePath, "r") as File:
                return json.load(File)
        except Exception as E:
            raise ErrorModule(LogModule,"",Driver,ParentModule,0,ErrorModule=E,Unexpected="File",File=FilePath)

class GlobalFunction:
    def VerifySocket(LogModule,Port,ShutDownOtherSession,Driver,ParentModule):
        ModuleInfo = (GlobalE.InvalidSocket,LogModule,Driver,ParentModule)
        LogModule.Say(("Verifying port ",ConsoleColor.BLUE),(str(Port),ConsoleColor.PURPLE),mode="Space")
        try:
            SubprocessResult = subprocess.run("netstat -ano | findstr :"+str(Port),shell=True,capture_output=True,text=True,check=True)
        except subprocess.CalledProcessError as E:
            raise GlobalE.InvalidSocket(LogModule,
                                        "Analysing port "+Port,
                                        Port,Driver,ParentModule,0,
                                        ErrorModule=E,
                                        Command="netstat -ano | findstr :"+Port) # TT
        except Exception as E:
            raise GlobalE.UnexpectedError() # ToDo
        SubprocessResult = SubprocessResult.stdout.split("\n")

        if SubprocessResult != ['']:
            ProcList = []
            for Line in SubprocessResult:
                DecomposedLine = Utility.Decompose(Line)
                
                if len(DecomposedLine) > 1:
                    DecomposedLine[-1] = DecomposedLine[-1].replace("\r","").replace("\n","")
                    try:
                        SocketPID = subprocess.run("wmic process where processid="+DecomposedLine[-1]+" get ExecutablePath",capture_output=True,text=True,check=True)
                    except subprocess.CalledProcessError as E:
                        raise GlobalE.InvalidSocket(LogModule,
                                                    f"Getting executable path of PID {DecomposedLine[-1]}",
                                                    Port,Driver,ParentModule,0,ErrorModule=E,
                                                    Command=f"wmic process where processid={DecomposedLine[-1]} get ExecutablePath",
                                                    ProcessID=DecomposedLine[-1]) # ToTest
                    except Exception as E:
                        raise GlobalE.InvalidSocket(LogModule,"",Port,Driver,ParentModule,0,ErrorModule=E,Command=f"wmic process where processid={DecomposedLine[-1]} get ExecutablePath",
                                                    ProcessID=DecomposedLine[-1])
                    SocketPID = SocketPID.stdout.replace("\r","").replace("\n","")
                    SocketPID = Utility.Decompose(SocketPID)
                    ProcList.append({"Type":DecomposedLine[0],"LocalAdress":DecomposedLine[1],"DistantAdress":DecomposedLine[2],"Statu":(DecomposedLine[3] if DecomposedLine[0] == "TCP" else ""),"PID":DecomposedLine[-1],"Path":(SocketPID[1] if len(SocketPID) > 1 else None)})
                    LogModule.Say("--> ",(str(ProcList[-1]),ConsoleColor.PURPLE))

                for Line in ProcList:
                    if Line["Type"] == "UDP":
                        raise GlobalE.InvalidSocket(LogModule,
                                                    f"Verifying processus informations on port {Port}",
                                                    Port,Driver,ParentModule,0,
                                                    DetailedContext=f"Port {Port} have already an UDP connection",
                                                    ProcInfo=Line)
                    else:
                        if Line["Statu"] in ("LISTENING","ESTABLISHED","CLOSE_WAIT","SYN_SENT","SYN_RECEIVED"):
                            if os.path.basename(Line["Path"]).lower() in (Driver,os.path.splitext(Driver)[0]):
                                None # ToDo
                                # try:
                                #     response = requests.post(f"http://localhost:{Port}/session", json={
                                #         "capabilities": {
                                #             "alwaysMatch": {
                                #                 "browserName": "firefox"
                                #             }}})
                                # except Exception as E:
                                #     raise # Special error for request ConnectionError / Timeout / RequestException as E | unexpected error
                                # if response.status_code != 200:
                                #     raise GlobalE.InvalidSocket()
                            else:
                                raise GlobalE.InvalidSocket(LogModule,
                                                            f"'{os.path.basename(Line["Path"]).lower()}' isn't '{Driver}'",
                                                            Port,Driver,ParentModule,0,
                                                            DetailedContext=f"'{os.path.basename(Line["Path"]).lower()}' isn't equal to '{Driver}' or '{os.path.splitext(Driver)[0]}'",
                                                            ApplicationName=os.path.basename(Line["Path"]).lower(),ProcInfo=Line)
                        elif Line["Statu"] == "TIME_WAIT":
                            None # ToDo
            else:
                LogModule.Say("==> ",("This socket has no application associated with",ConsoleColor.YELLOW))

    def VerifyUserSettings(LogModule,UserData,Comm,Driver,ParentModule):
        ModuleInfo = (GlobalE.InvalidUserSettings,LogModule,Driver,ParentModule)
        if ParentModule == "firefox":
            UserData["FirefoxOptions"] = {"args": []}
        elif ParentModule == "chrome":
            ...

        UsedPort = Comm()["UsedPort"]

        LogModule.Say(("Verifying Application Path",ConsoleColor.BLUE),mode="Space")
        for AppliPath,AppliName in ((UserData["DriverPath"],os.path.splitext(Driver)[0]),(UserData["BrowserPath"],ParentModule)):
            Result = Utility.IsValidApplication(AppliPath,AppliName,ModuleInfo)
            if Result[0]:
                LogModule.Say("--> ",(Result[1],ConsoleColor.PURPLE))
            else:
                raise GlobalE.InvalidUserSettings(LogModule,
                                                  f"Invalid '{AppliName}' Path",
                                                  Driver,ParentModule,0,
                                                  DetailedContext=f"{Result[1]} isn't a valid application name for {AppliName}",
                                                  ApplicationNeeded=AppliName,ApplicationGot=Result[1],ApplicationPath=AppliPath)
        if ParentModule == "firefox":
            UserData["FirefoxOptions"]["binary"] = UserData["BrowserPath"]
        elif ParentModule == "chrome":
            ...
        
        LogModule.Say(("Verifying Port",ConsoleColor.BLUE),mode="Space") 
        try:
            Port = int(UserData["Port"])
        except ValueError as E:
            raise GlobalE.InvalidUserSettings(LogModule,
                                            f"Can't convert '{Port}' to an int value",
                                            Driver,ParentModule,0,ErrorModule=E,
                                            DetailedContext=f"ValueError : '{Port}' type is '{type(Port)}' and can't be an int value",
                                            Port=Port)
        except OverflowError as E:
            raise GlobalE.InvalidUserSettings(LogModule,
                                            f"Can't convert '{Port}' to an int value",
                                            Driver,ParentModule,0,ErrorModule=E,
                                            DetailedContext=f"OverflowError : '{Port}' is an too hight number to be converted",
                                            Port=Port)
        if not 1024 < Port < 65536:
            raise GlobalE.InvalidUserSettings(LogModule,
                                            f"Incorrect Port number selected",
                                            Driver,ParentModule,0,
                                            DetailedContext=f"Port need to be between 1024 and 65536 not included",
                                            Port=Port)
        if Port in UsedPort:
            raise GlobalE.InvalidUserSettings(LogModule,
                                            f"Port '{Port}' is already used in this module by another session",
                                            Driver,ParentModule,0, 
                                            DetailedContext=f"'{Port}' is present in {str(UsedPort)}",
                                            UsedPort=UsedPort,Port=Port)
        LogModule.Say("--> ",(str(Port),ConsoleColor.PURPLE))

        LogModule.Say(("Verifying Firefox Profil Name",ConsoleColor.BLUE),mode="Space")
        if UserData["ProfilName"] == "Temp" and UserData["ProfilPath"] == "":
            LogModule.Say("--> Firefox Profil Name: Temp")
            LogModule.Say("==> ",("A temporary file will be created and deleted automatically",ConsoleColor.YELLOW))
        elif UserData["ProfilName"] != "Temp":
            if ParentModule == "firefox":
                FirefoxProfilesIniPath = os.path.join(os.environ.get("APPDATA", ""),"Mozilla","Firefox","profiles.ini")
                if not os.path.isfile(FirefoxProfilesIniPath):
                    LogModule.Say("==> ",(FirefoxProfilesIniPath,ConsoleColor.PURPLE),("dosn't exist",ConsoleColor.YELLOW))
                else:

                    Profiles = Utility.ReadIniFile(FirefoxProfilesIniPath)
                    ProfilesInfos = {}
                    for Profile in Profiles:
                        if Profile[:7] == "Profile":
                            LogModule.Say("--> Name : ",(f"{Profiles[Profile]['Name']:<20}",ConsoleColor.PURPLE)," / Path : ",(Profiles[Profile]["Path"],ConsoleColor.PURPLE))
                            ProfilesInfos[Profiles[Profile]["Name"]] = Profiles[Profile]["Path"]
                    if UserData["ProfilName"] in ProfilesInfos:
                        UserData["FirefoxOptions"]["args"] += (["-profile", os.path.join(os.environ.get("APPDATA", ""),"Mozilla","Firefox",ProfilesInfos[UserData["ProfilName"]])])
                        LogModule.Say("==> ",("Firefox Profil Name: ",ConsoleColor.YELLOW),(UserData["ProfilName"],ConsoleColor.PURPLE)," / Profil Path : ",(UserData["FirefoxOptions"]["args"][1],ConsoleColor.PURPLE))
                    else:
                        if UserData["ProfilPath"] != "":
                            LogModule.Say("==> ",("No Profil named : ",ConsoleColor.YELLOW),(UserData["ProfilName"],ConsoleColor.PURPLE))
                        else:
                            raise GlobalE.InvalidUserSettings(LogModule,
                                                            f"No profil named '{UserData["ProfilName"]}' for firefox",
                                                            Driver,ParentModule,0,
                                                            DetailedContext=f"'{UserData['ProfilName']}' isn't present in {FirefoxProfilesIniPath}",
                                                            ProfilName=UserData["ProfilName"],IniProfil=Profiles,IniProfilPath=FirefoxProfilesIniPath)
            elif ParentModule == "Chrome":
                ...
                    
        else:
            LogModule.Say("--> No profil name set")
            LogModule.Say(("Verifying Firefox Profil Path",ConsoleColor.BLUE),mode="Space")
            if os.path.isdir(UserData["ProfilPath"]):
                if ParentModule == "firefox":
                    FirefoxOptionalFiles = {
                        "prefs.js",         # créé au 1er lancement
                        "places.sqlite",    # Historique et favoris
                        "cookies.sqlite",   # Cookies
                        "cert9.db",         # Certificats 
                        "key4.db"           # Mots de passe 
                    }
                    TimesFilePath = os.path.join(UserData["ProfilPath"],"times.json")
                    TimesFile = Utility.ReadJsonFile(LogModule,GlobalE.InvalidUserSettings,TimesFilePath,Driver,ParentModule)
 
                    LogModule.Say("--> ",(f"{'times.json':<20}",ConsoleColor.PURPLE),": ",("present",ConsoleColor.BOLD))
                    if ("created","firstUse") != tuple(TimesFile.keys()):
                        raise GlobalE.InvalidUserSettings(LogModule,
                                                          f"Invalid times.json content",
                                                          Driver,ParentModule,0,
                                                          DetailedContext=f"times.json keys : '{tuple(TimesFile.keys())}' isn't equal to '{('created','firstUse')}'",
                                                          TimeKeys=tuple(TimesFile.keys()),TimeKeysNeeded=tuple(TimesFile.keys()))
                    for OptionalFile in FirefoxOptionalFiles:
                        LogModule.Say("--> ",(f"{OptionalFile:<20}",ConsoleColor.PURPLE),": ",(("present" if os.path.isfile(os.path.join(UserData["ProfilPath"],OptionalFile)) else "absent"),ConsoleColor.BOLD))

                    if TimesFile["firstUse"] == None:
                        LogModule.Say("==> ",(f"{TimesFilePath}",ConsoleColor.PURPLE),(" never been luanch before",ConsoleColor.YELLOW))
                
                elif ParentModule == "chrome":
                    ...

            elif os.path.isfile(UserData["ProfilPath"]):
                raise NotADirectoryError("",f"'{UserData['ProfilPath']}' isn't a directory but a file")
            else:
                raise FileNotFoundError("",f"'{UserData['ProfilPath']}' isn't a valid path")
        LogModule.Say(("Finished verifying User settings",ConsoleColor.CYAN),mode="Space")