
![](sitecheck/docs/resources/logo-graphic.png)
# Sitecheck Scanner
#### Intended for Geo-Instruments Internal use

__author__ = Dan Edens
__version__ = 0.8.1.2

---
# Description
This tool provides troubleshooting tools for AMP and QV

Sensor status report in the form of an
[Adaptive Cards](https://docs.microsoft.com/en-us/power-automate/overview-adaptive-cards) to the user through Teams.  

![](sitecheck/docs/resources/Cardexample.jpg)  

This is done through the user's Keller - OneDrive.  


The user can than prompt the Flowbot to ingest the data via the Team's chat, review it,
and than pass it on to the Regional team.
```
run flow 1
```
![](sitecheck/docs/resources/Runflow1.jpg)

---

# Installation

```
pip install sitecheck
```
Than use "run" followed by your options
```
scanner --info -p upsondrivevms
```

---
# Power Automate Import instructions

### Description

[Power Automate](https://docs.microsoft.com/en-us/power-automate/) is the platform that handles ingesting the cards from OneDrive and posting to chat.
It is an included part of our Microsoft package, and functions within the group security policies.

## Flow script Import.

[Follow this link to import the included Package](https://us.flow.microsoft.com/manage/environments/Default-b44eb401-1c30-454c-ae94-78de08e2320c/flows/import)
---

![](sitecheck/docs/resources/Importpackage1.jpg)

Select [Scanner_flow.zip](Flow/Scannerflow.zip) file from your desktop
---

![](sitecheck/docs/resources/Importpackage2.jpg)


Select "create as new" and add your email to the connectors.
---
![](sitecheck/docs/resources/Importpackage3.jpg)

Follow the link in the success message.
```
  All package resouces were successfully imported.
The Flow has been created succesfully. Run the flow to make sure it's working. Open Flow
```

![](sitecheck/docs/resources/Importpackage4.jpg)

---

Change the value in "Intialize variable 2" to your Username.
Can be tested by running the following in cmd
```
echo %USERPROFILE%
```

---
![](sitecheck/docs/resources/Importpackage5.jpg)

This needs to match to your Onedrive path.
```
C:\Users\%USERPROFILE%\OneDrive - Keller\scanner
C:\Users\Dan.Edens\OneDrive - Keller\scanner
```
---


Please report any bugs to Dan.Edens@geo-instruments.com


