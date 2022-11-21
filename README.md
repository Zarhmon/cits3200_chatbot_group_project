<p align="center">
  <img src="./documents/robot-circle.png" alt="Sitting robot" width="100" height="100">
</p>

# cits3200-project
A repo for our CITS3200 project

## Setup

To install dependencies for the chatbot **you must use Python 3.7**.  It is best to create a venv for this.  Run these commands in the repo folder. **If on Windows RUN POWERSHELL AS ADMINISTRATOR.**

```Powershell
# Create a venv called venv
python -m venv venv

# Activate venv on Windows
. ./venv/Scripts/activate

# Activate venv on macOS/Linux
. ./venv/bin/activate

# Install dependencies (will take a few mins and may have pyyaml error, seems to not matter)
pip install -r ./chatbot/requirements.txt

# May need to be run as sudo on macOS/Linux
python -m spacy download en
```

Then you'll need to install dependencies for Cairo.

Windows download: https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases ([direct download](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases/download/2022-01-04/gtk3-runtime-3.24.31-2022-01-04-ts-win64.exe))
 

Important Dates
 - Sprint 1 due 5pm Wednesday 17th August (to client, copy to cssubmit, due 11:59pm)
 - Personal Relfection due 11:59pm Friday 19th August (to cssubmit)
 - SPARKPLUS peer assessment to SPARKPLUS web site, due 11:59pm Friday 19th August 
 - Professional Development Portfolio due 11:59pm Monday 12th September (to cssubmit)
 - Sprint 2 due 5pm Wed 21st September (to client, copy to cssubmit, due 11:59pm)
 - Personal Relfection due 11:59pm Friday 23rd September (to cssubmit)
 - SPARKPLUS peer assessment due 11:59pm Friday 23rd September (to SPARKPLUS web site)
 - All work on project stops 5:00pm Monday 17th October.
 - Handover to Client of project deliverables, system demonstration, Client Retrospective
 - cssubmit Sprint 3 system and retrospective 11:59pm Wednesday 19th October
 - Personal Relfection due 11:59pm Friday 21st October (to cssubmit)
 - SPARKPLUS peer assessment due 11:59pm Friday 21st October (to SPARKPLUS web site) 

Useful links
 - [Project Homepage](https://teaching.csse.uwa.edu.au/units/CITS3200/project.html)
 - [Project Instructions](https://teaching.csse.uwa.edu.au/units/CITS3200/project/instructions.html)
