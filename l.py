import WebArtifact

# Pp = r"C:\Users\mathou\AppData\Roaming\Mozilla\Firefox\Profiles\l0fwq2j9.default"
Gp = r"E:\PERSO\Python\Projet\WebArtifact\geckodriver.exe"
Pp = r"C:\Users\mathou\AppData\Roaming\Mozilla\Firefox\Profiles\l0fwq2j9.default"



# Ap = r"E:\DOCU\Pro\CV\CV-BUT-2.pdf"


az = WebArtifact.S()
az.Firefox(GeckodriverPath=Gp,ProfilPath=Pp,Port=4445)
# az.OpenDriver()

