# WebArtifact

Early development version (0.1.-)

WebArtifact is a lightweight multi browser automation library designed to interact with web browsers programmatically.
Created to allow interaction with multiple sessions from multiple browsers using the same module in the same time

## Project Status

This project is currently in very early development.

Core architecture is not finalized
Many features are incomplete or unstable
<!-- Breaking changes are very soon expected -->
For more information about the structure/function you can check the Documentation in /Docs

## Installation

> Not available yet (manual setup required)

## Features

### General

- Basic environment variable set for multiple session and browser

### Firefox 

- Verification for User settings
- Driver luanch (development)

### Chrome

> Not comming soon

### Microsoft Edge

> Not comming soon

## MAJ

### Versions

WebArtifact use a common managing system used on all my project.

It's a**3 digit versioning system** following the format **`Major.Minor.Patch`**.

The **first digit** (`Major`) represents the **Global Category** of the project. It defines the project's main guidelines and architecture. Changes to this number are **extremely rare**.

The **second digit** (`Minor`) represents the **Global Subcategory**. It is incremented when a **major feature or update** has been completed and groups together all previous Patch versions into a stable release.

The **third digit** (`Patch`) represents a **Micro Version**. It is used for all minor changes such as new small features, function improvements, bug fixes, or documentation updates.

Patch versions do **not** have a dedicated roadmap. Every Patch change is documented in the **Versions** folder.

*For more informations about this system, you can check :*

---

### Latest Global subCategory (0.1)

- Totally reworked the error handling
- Reworked code structure
- Added more verifications
- Added color to the log

- Started to improve stability
- Started to improve code readability

**Comment** : Biggest update so far: All core structure had been reworked to allow the project to expand as much as possible

> Fore more information you can check ./Docs/Versions folder

---

### Roadmap

| Global Category   | Update                                |
|-------------------|---------------------------------------|
| 0                 | Geckodriver / Mozilla                 |
| 1                 | Chromium Driver / Chromium browsers   |
| 2                 | Linux version                         |
| 2                 | ...                                   |

| 0 Global subCategory  | Update                                                    |
|-----------------------|-----------------------------------------------------------|
| 0                     | Creation of the core structure                            |
| 1                     | New firefox functions : OpenDriver, LuanchDriver          |
| 2                     | New main function : NewSession / Improve session manager  |
| 3                     | New firefox functions : GetPage                           |

<!-- - Comming Soon :
  - Improve stability on the current code
  - Improve current code readability and structure

- Next Steps :
  - Refactor main class (S -> proper naming)
  - Do Documentation (Documentation.md / Version.md)
  - Continue to improve stability and readability
  - Add a new function OpenDriver
  - Add a new function OpenBrowser

- Future Goals :
  - Advanced configuration system
  - Robust error handling system
  - Interaction API (tabs, elements, navigation)
  - Multi-tab support
  - Multi-instance support -->


---

## Disclaimer

This project is not ready for production use.
It is currently a learning and experimental student project.
