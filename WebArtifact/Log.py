import time
import os

class LogManager:                                                                                                      
    def __init__(self,mode="normal",save="console"):                                                                                # save="console" : retranscrit dans la console / save="file" : retranscrit dans un fichier
        # sys.excepthook = self.CustomError                                                                                         # A faire
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
                File.write(f"[{ActualTime}] : ≠≠> {message}\n")
        else:
            print(f"[{ActualTime}] : {message}")
        
        raise Exception(message)

    def Console(self,message):
        print(message)