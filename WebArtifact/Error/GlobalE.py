import json
import subprocess

class InvalidSocket(Exception):
    def __init__(self,
                LogModule:object,
                Context:str,
                Port:str,
                Driver:str,
                ParentModule:str,
                Line:int,

                ErrorModule:object=None,
                DetailedContext:str=None,
                Unexpected:str=None,
                **Param
                ) -> None:
        """
        Param: commands / Process ID / UsedPort / Processus Information
        """
        self.GlobalContext = f"Error while analysing port {Port} for {Driver} in {ParentModule}"
        if Unexpected == "Subprocess":
            self.Context,self.DetailedContext = UnexpectedError.InvalidSubprocess(ErrorModule,Param["Command"])
        else:
            self.Context = Context
            self.DetailedContext = DetailedContext

        self.ErrorModule = ErrorModule
        self.Port = int(Port)
        self.Line = Line
        self.Param = Param
        super().__init__(self.Context)
        LogModule.SayError(self)

class InvalidUserSettings(Exception):
    def __init__(self,
                LogModule:object,
                Context:str,
                Driver:str,
                ParentModule:str,
                Line:int,
                
                ErrorModule:object=None,
                DetailedContext:str=None,
                Unexpected:str=None,
                **Param) -> None:
        """
        Param: 
        """
        self.GlobalContext = f"Error while analysing user settings for {Driver} in {ParentModule}"
        if Unexpected == "File":
            self.Context,self.DetailedContext = UnexpectedError.InvalidFile(ErrorModule,Param["File"])
        elif Unexpected == "Subprocess":
            self.Context,self.DetailedContext = UnexpectedError.InvalidSubprocess(ErrorModule,Param["Command"])
        else:
            self.Context = Context
            self.DetailedContext = DetailedContext
        self.ErrorModule = ErrorModule
        self.Line = Line
        self.Param = Param
        super().__init__(self.Context)
        LogModule.SayError(self)


# class InvalidFile(Exception):
#     def __init__(self,
#                 LogModule:object,
#                 File:str,
#                 Driver:str,
#                 ParentModule:str,
#                 Line:int,
#                 ErrorModule:object) -> None:
        

        
class UnexpectedError:
    def InvalidFile(ErrorModule,File):
        if isinstance(ErrorModule,FileNotFoundError):
            Context = f"Invalid Path : '{File}' -> Path dosn't exist"
        elif isinstance(ErrorModule,PermissionError):
            Context = f"Invalid Path : '{File}' -> Invalid Permission"
        elif isinstance(ErrorModule,OSError):
            Context = f"Invalid Path : '{File}' -> ..."
        elif isinstance(ErrorModule,json.JSONDecodeError):
            Context = f"Invalid File Content : '{File}' -> Can't convert file content into dict"
            DetailedContext = ErrorModule.msg

        if isinstance(ErrorModule,(FileNotFoundError,PermissionError,OSError)):
            DetailedContext = ErrorModule.strerror

        return Context,DetailedContext

    def InvalidSubprocess(ErrorModule,command):
        if isinstance(ErrorModule,subprocess.CalledProcessError):
            Context = ""
            DetailedContext = ErrorModule.stderr
        elif isinstance(ErrorModule,PermissionError):
            Context = ""
        elif isinstance(ErrorModule,OSError):
            Context = ""
        elif isinstance(ErrorModule,FileNotFoundError):
            Context = ""
        
        if isinstance(ErrorModule,(FileNotFoundError,PermissionError,OSError)):
            DetailedContext = ErrorModule.strerror
        
        return Context,DetailedContext
        
