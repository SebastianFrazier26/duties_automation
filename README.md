# Duties Automation
## Sebastian Frazier
### Purpose
The aim of this directory is to provide a way of automating the assignment of duties for events. This is intended to make assignment easier, cleaner, and more fair as it is purely random and objective.
### Requirements
The code was all built with Python 3.9.6 and may require updating for newer Python kernels. It also requires pandas, random, and datetime libraries (all standard).
### Running
To run the code, simply run the main file in a linux/bash terminal or click run on vscode. All files needed to run the code are provided.

#### duties.csv - The duties.csv must be compiled by the user and will change from term to term (or even moment to moment). All categories should be filled in at the start of a term and updated throughout (such as is_double).
- name: self-explanatory
- year: self-explanatory
- is_on: is [name] on campus
- is_tips: is [name] TIPS trained
- is_double: does [name] have double duties, and how many
- is_exempt: can [name] have duties, e.g. are they risk, social, special exemptions

#### Event types - Events are divided into a few categories. Their sheets can be visualized in the Event.py file. To run them:
- tails: input tails when prompted
- registered: input registered when prompted
- double: for a pregame/registered event, input double when prompted
- setup: input setup when prompted, then the time frame needed, then the # of workers
- rush: for events with only balc, input rush, then the time frame needed
- greenkey: input greenkey when prompted.
- Any other input will result in an error

#### Groupme - The program will automatically ask if you request for your sheet to be sent into the groupme. It will then send a png of the duty's sheet as well as an automatic @mention to all members listed on the sheet. It will throw warnings if certain members are not present on the sheet.

### Implementation

* Preference: The code utilizes a preference system that first tries to give duties to anyone with double duties and second tries to assign duties to those who have done the FEWEST thus far in the term. Double duties are given more weight. If two people have double duties, preference is given to the person with less duties completed thus far (preference being assignment to a duty). For individuals with the same number of duties done and amount of double duties, the choice is randomized.

* Bar: Bar duties are assigned first as the fewest people are capable of doing them. To prevent unfair assignments, tips trained members of the house can ONLY do bar, as this duty is uniquely important. Bar is assigned with the same preference treatment for TIPS trained persons as other duties.

* Events: Events (described above) are implemented as subclasses of a class Event in the Event.py file. Events have their own unique "sheet" assigned to them that will be filled in with names. A 0 on the sheet indicates a space needing an assignment, an empty string ("") indicates that that space should be skipped/isn't needed.

* Tracking: At the end of a run, the duties.csv file is updated (recorded as master) and values like num_duties and is_double are incremented to reflect duties assignments. This csv serves as the sole way of determining how duties should be assigned and as such should be treated with immense care and remain secured.

* sender.py: This program is made using the groupme API and was assisted by @DeepSeek. The program automatically sends the image/mention list to groupme using their official rest API. It requires authentication credentials from the user. To get credentials use: https://dev.groupme.com

### Future Work

It is possible that more event categories will be needed in the future. As such, the Event.py file should be expanded to support more capabilities as is necessary (e.g. dartys or unique events)