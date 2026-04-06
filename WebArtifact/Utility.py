import os
import subprocess

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
        if not os.path.isfile(ApplicationPath):                                                                                     # Verifie que le fichier existe bien
            LogModule.SayError(ApplicationPath+" isn't a valid Path")
        SubprocessResult = subprocess.run([ApplicationPath, "--version"],capture_output=True,text=True)                         # Verifie que le fichier specifié est reelement une application
        if SubprocessResult.returncode != 0:
            LogModule.SayError("Unexpected Error : "+SubprocessResult.stderr+"\n≠≠>"+SubprocessResult.stdout)
        TempLine = SubprocessResult.stdout.splitlines()[0]
        if ApplicationName not in TempLine.lower():                                                                             # Verifie que le nom de l'application ets bien présent dans la reponse
            LogModule.SayError(TempLine+" isn't "+ApplicationName)
        LogModule.Say("--> "+TempLine)


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




