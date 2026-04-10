import WebArtifact

Pp = r"C:\Users\mathou\AppData\Roaming\Mozilla\Firefox\Profiles\l0fwq2j9.default"
Gp = r"E:\PERSO\Python\Projet\WebArtifact\geckodriver.exe"
Ap = r"E:\DOCU\Pro\CV\CV-BUT-2.pdf"


az = WebArtifact.S()
az.Firefox(GeckodriverPath=Gp,ProfilName="def",ProfilPath=Pp,Port=5000)