# Web Artifact - lightweight multi browser automation

## Heading

### General Info

**Source Code** :[Web Artifact](https://github.com/maathouu/WebArtifact)

Web Artifact is an open source project which aims to be a Python librairy in the future\
This module provides a portable way to automate interaction with web browsers programmatically\
The structure is designed to be able of managing multi browsers and tab at the same time

For more details you can also see HardDocumentation.md

### Actual Version note

| OS       | Status                         |
|----------|--------------------------------|
| Windows  | Currently working on           |
| Linux    | Planned after V2.0             |
| Android  | Probably never coming          |
| iOS      | Probably never coming          |

| Browser           | Driver        | Status                         |
|-------------------|---------------|--------------------------------|
| Firefox           | Geckodriver   | Currently working on           |
| Chrome            | ChromeDriver  | Planned after V1.0             |
| Microsoft Edge    | msedgedriver  | Not planned soon               |
| Opera             | OperaDriver   | Not planned soon               |
| Safari            | SafariDriver  | Probably never coming          |

### How to install / import

For the moment, you can only download the module from [Github](https://github.com/maathouu/WebArtifact/releases/tag/v0.0)

After installing WebArtifact, it may be imported into Python code like:
```python
import WebArtifact as wa
```

## Mains

### Commands

#### `S()`
Load the module and main systems variables

```python
browser = wa.S()
```
> Added in version 0.0-a\
> Changed in version 0.0

#### `Firefox()`
Create new firefox session on the module

```python
browser.Firefox()
```

**Parameters:**
- `GeckodriverPath` (str):          Path to the geckodriver executable (default: "geckodriver.exe")
- `FirefoxPath`     (str):          Path to the Firefox executable (default: r"C:\Program Files\Mozilla Firefox\firefox.exe")
- `ProfilPath`      (str):          Custom Firefox profile directory (default: None)
- `ProfilName`      (str):          Profile name used with profiles.ini (default : Temporary file)
- `Port`            (int | str):    Port used by the driver (default: 4445)
- `SessionName`     (str | int):    Name used for multi-session management (default: managed by WebArtifact)


> Added in version 0.0-b\
> Changed in version 0.0

### Error handling