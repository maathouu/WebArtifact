import json
import subprocess

class FlexError(Exception):
    def __init__(self,**kwargs):
        for Key,Value in kwargs.items():
            setattr(self,Key,Value)

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