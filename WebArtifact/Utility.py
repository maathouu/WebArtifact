import time
import socket
import subprocess
from .Log import ConsoleColor

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
    
def IsValidApplication(LogModule,ApplicationPath:str,ApplicationName:str) -> None:
        try:
            SubprocessResult = subprocess.run([ApplicationPath,"--version"],capture_output=True,text=True)                         # Verifie que le fichier specifié est reelement une application
        except Exception as E:
            LogModule.SayError(E,("Utility","IsValidAppli"),path=ApplicationPath)
        TempLine = SubprocessResult.stdout.splitlines()[0]
        if ApplicationName not in TempLine.lower():                                                                             # Verifie que le nom de l'application ets bien présent dans la reponse
            LogModule.SayError("WrongAppliName",("Utility","IsValidAppli"),Result=TempLine.lower(),AppliNeeded=ApplicationName)
        LogModule.Say("--> ",(TempLine,ConsoleColor.PURPLE))


def ReadIni(LogModule,FilePath:str) -> dict:
    result = {}
    with open(FilePath,"r") as f:
        File = f.readlines()

    ActualSection = None
    for Line in File:
        Line = SupFLSpace(Line).replace("\n","")
        if len(Line) > 0:
            if Line[0] == "[" and Line[-1] == "]":
                ActualSection = Line[1:-1]
                result[ActualSection] = {}
            elif Line[0] != ";":
                Line = Line.split("=")
                result[ActualSection][Line[0]] = Line[1]
    return result

def IsValidPort(LogModule,Port,PortUsed) -> int:
    try:
        Port = int(Port)
    except Exception as E:
        LogModule.SayError(E,("Utility","IsValidPort"))
    if not 1024 < Port < 65536:
        LogModule.SayError("InvalidRange",("Utility","IsValidPort"),port=Port)
    if Port in PortUsed:
        LogModule.SayError("AlreadyUsed",("Utility","AlreadyUsed"),port=Port,portused=PortUsed)
    LogModule.Say("--> ",(str(Port),ConsoleColor.PURPLE))
    return Port

def VerifySocket(LogModule,Port):
    LogModule.Say(("Verifying port ",ConsoleColor.BLUE),(str(Port),ConsoleColor.PURPLE),mode="Space")
    try:
        SubprocessResult = subprocess.run("netstat -ano | findstr :"+str(Port),shell=True,capture_output=True,text=True)
    except Exception as E:
        LogModule.SayError(E,("Utility","InvalidSocket"))
    SubprocessResult = SubprocessResult.stdout.split("\n")

    if SubprocessResult != ['']:
        ProcList = []
        for Line in SubprocessResult:
            DecomposedLine = Decompose(Line)
            
            if len(DecomposedLine) > 1:
                DecomposedLine[-1] = DecomposedLine[-1].replace("\r","").replace("\n","")
                try:
                    SocketPID = subprocess.run("wmic process where processid="+DecomposedLine[-1]+" get ExecutablePath",capture_output=True,text=True)
                except Exception as E:
                    LogModule.SayError(E,("Utility","InvalidSocket"))
                
                SocketPID = SocketPID.stdout.replace("\r","").replace("\n","")
                SocketPID = Decompose(SocketPID)
                ProcList.append({"Type":DecomposedLine[0],"LocalAdress":DecomposedLine[1],"DistantAdress":DecomposedLine[2],"Statu":(DecomposedLine[3] if DecomposedLine[0] == "TCP" else ""),"PID":DecomposedLine[-1],"Path":(SocketPID[1] if len(SocketPID) > 1 else None)})
                LogModule.Say("--> ",(str(ProcList[-1]),ConsoleColor.PURPLE))

        return ProcList
    return SubprocessResult

def WaitOpenDriver(LogModule,Port,TimeOut,Driver):
    
    TimeStart = time.time()
    Finished = False
    while time.time() - TimeStart < TimeOut and  not Finished:
        try:
            with socket.create_connection(("localhost", Port),timeout=0.1):
                return str(time.time() - TimeStart)
        except OSError:
            time.sleep(0.1)
        except Exception as E:
            LogModule.SayError(E,("Utility","WaitOpenDriver"))
    LogModule.SayError("TooLong",("Utility","WaitOpenDriver"),driver=Driver,timetook=str(time.time() - TimeStart),timemax=TimeOut)

# def VerifySocket(LogModule,Port):
#     LogModule.Say("Starting Anylising port : "+Port)
#     try:
#         RawStrResult = subprocess.run("netstat -ano | findstr :"+Port,shell=True,capture_output=True,text=True)    # Enregistre les données sur le port choisie
#     except subprocess.CalledProcessError as T:
#         LogModule.SayError("--> Unexpected Error : returned with code "+T.returncode+"\n≠≠> "+T.stderr)
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
#                     LogModule.SayError("--> Unexpected Error : returned with code "+T.returncode+"\n≠≠> "+T.stderr)
#                 TempPID = TempPID.stdout.replace("\n","").replace("\r","")
#                 TempPID = Decompose(TempPID)

#                 ListResult.append({"Type":Temp[0],"LocalAdress":Temp[1],"DistantAdress":Temp[2],"Statu":(Temp[3] if Temp[0] == "TCP" else ""),"PID":Temp[-1],"Path":(TempPID[-1] if len(TempPID) > 1 else "")})
#                 LogModule.Say("--> "+str(ListResult[-1]))

#         for Line in ListResult:                                                                                 
#             if Line["PID"] != "0" and Line["Path"] != "":
#                 if Line["Type"] == "TCP":
#                     if os.path.basename(Line["Path"]).lower() not in ("python.exe","geckodriver.exe"):                          # Verifie si l'application associé aux ports est geckodriver
#                         LogModule.SayError("Another application is already using this port (Name)")
#                     else:
#                         LogModule.Say("--> Geckodriver already use the port "+Port)
#                         try:
#                             SubprocessResult = subprocess.run(f"taskkill /PID {Line['PID']} /F") # Ferme le processus Geckodriver
#                         except subprocess.CalledProcessError as T:
#                             LogModule.SayError("--> Unexpected Error : returned with code "+T.returncode+"\n≠≠> "+T.stderr)
#                         LogModule.Say("==> Shutted down the old Geckodriver")
#                 else:
#                     self.GLog.SayError("Another application is already using this port (Protocol)")
#     else:
#         self.GLog.Say("==> This port has no application associeted with")
#     self.GLog.Say("Port "+self.UserData["Port"]+" can be used\n")
