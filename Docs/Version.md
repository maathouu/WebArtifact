# Roadmap

## Global category

Global category is the first digit of a version and represent the actual project guideline.\
Change of a global category is extremely rare.

| Global Category   | Update                                |
|-------------------|---------------------------------------|
| 0                 | Geckodriver / Mozilla                 |
| 1                 | Chromium Driver / Chromium browsers   |
| 2                 | Linux version                         |
| 2                 | ...                                   |

## Global subCategory

Global Subcategory is the second digit of a version and represent a massive update.\
It's the gathering of all the previous Micro Versions; it's for new **finished** mains functions.

### Global Categoy 0

| 0 Global subCategory  | Update                                                    |
|-----------------------|-----------------------------------------------------------|
| 0                     | Creation of the core structure                            |
| 1                     | New firefox functions : OpenDriver, LuanchDriver          |
| 2                     | New main function : NewSession / Improve session manager  |
| 3                     | New firefox functions : GetPage                           |

## Micro versions

Micro versions is the third and last digit of a verison and represent minor update/change.\
It's for any minor change: creating a new function / improving a function / correct documents ...

No roadmap have been Created for this category, but you can see last change of any of these in the Versions folder.\

# Versions

<details>
<summary>Global category 0</summary>

**Dedicated to the mozilla module and the main module.**\
New function for the main module is added at the same time as firefox module.

> [!IMPORTANT]  
> This category is actually in developpment.


<details>
<summary>Global Subcategory 0</summary>
**Dedicated to the core structure / firefox functions / main function**

Added core Structure

```
+-- WebArtifact
      |    +-- Docs
      |    |    +-- change.txt
      |    |    +-- Error.md
      |    |    +-- HardDocumentation.md
      |    |    +-- SimpleDocumentation.md
      |    |    +-- Version.md
      |    |    +-- Versions
      |    |    |   +-- GS0-0
      |    |    |   +-- GS0-1
      |    +-- WebArtifact
      |    |    +-- Error
      |    |    |    +-- __init__.py
      |    |    |    +-- FirefoxE.py
      |    |    |    +-- GlobalE.py
      |    |    +-- __init__.py
      |    |    +-- Firefox.py
      |    |    +-- Global.py
      |    |    +-- Log.py
      |    |    +-- WebArtifact.py
      |    +-- .gitignore
      |    +-- LICENSE
      |    +-- README.md
```

Added a Log system which work on the console or file\
Added custom errors
Started the geckodriver manager
Created the main environment and variables


</details>


<details>
<summary>Global Subcategory 1</summary>

**This category is actually in developpment**

</details>
</details>







<!-- For more informations you can check the Versions folder which can provide you all updates news  -->