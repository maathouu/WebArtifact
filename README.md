# WebArtifact

Early development version (v0.0-b)

WebArtifact is a lightweight multi browser automation library designed to interact with web browsers programmatically.
Created to allow interaction with multiple sessions from multiple browsers using the same module in the same time

## Project Status

This project is currently in very early development.

Core architecture is not finalized
Many features are incomplete or unstable
Breaking changes are very soon expected
For more information about the structure/function you can check the HardDocumentation or SimpleDocumentation in /Docs


## Features

### General

- Basic environment variable set for multiple session and browser

### Firefox 

- Basic user settings:
  - Port
  - Firefox path
  - Profile path
  - Profil Name
  - Geckodriver path
  - SessionName

### Chrome

> Not comming soon

### Microsoft Edge

> Not comming soon


## Installation

> Not available yet (manual setup required)

## News

- Basic Added Functionabilities 
  - Create multiple session in the same time 
  - User settings checker beta finished

- Reworked on the core structure
  - New File and class
    - ./Firefox.py
    - ./Log.py
    - ./Utility.py
    - ./Docs/SimpleDocumentation.md

- Subprocess.run settings have been reworked too : deleted useless param and added usefull to upgrade lisibility

- Full code have been temporary deleted to totaly rework the main structure : Some file have been created to devide sector in multiple place and not in only one file

- Creation of 3 new fonctions in .Utility
  - SupFLSpace() : delete all space at the start and end of a str value 
  - ReadIni() : Get .ini file info and set it in a dict
  - UserSettingsVer() : verif user settings for firefox

## Roadmap

- Comming Soon :
  - Improve stability on the current code
  - Improve current code readability and structure
  - Add Temporary general error handling 

- Next Steps
  - Refactor main class (S -> proper naming)
  - Add proper error handling 
  - Multi-tab support
  - Multi-instance support
  - Rework lisibility of HardDocumentation
  - Do SimpleDocumentation 

- Future Goals
  - Advanced configuration system
  - Full logging system
  - Robust error handling system
  - Interaction API (tabs, elements, navigation)


## Disclaimer

This project is not ready for production use.
It is currently a learning and experimental student project.
