# Anamika-s-Bot
## A Telegram Bot to maintain a To-Do List

For this project, I have made use of Telegram's API (https://core.telegram.org/) for creating a chatbot which can be used to serve as a To-Do List Manager.
The project was divided into 3 phases:
1) Understand the different API calls inorder for the bot to echo whatever I input.
2) Storing the inputs further into a database (usinf SQLite) so that it serves as a base for To-Do List.
3) Improving UX of the To-Do List Manager by listing the tasks as keys on keyboard, and ddeleteion of tasks can be done swiftly.

Further improvements:
The project currently runs whenever script is called from the Terminal. The script can be deployed to a VPS.

The files of importance are:
#### 1) credentials.py:
        Store the HTTP API access token of your bot here.
#### 2) anamikasbot.py:
        Implements phase 1 of the project.
#### 3) todobot.py:
        Main script for the To-Do List manager.
#### 4) dbhelper.py:
        SQLite script for database.
        
