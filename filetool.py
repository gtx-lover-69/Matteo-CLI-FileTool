import os.path
import time
import getpass
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter
from datetime import datetime

from colorama import Fore, Style

adminpass = 1234
admin = False

# File opener
def openfile(name,first):
    global admin
    admin = False
    file = open(name, 'r')
    content = file.read()
    file.close()
    if content.startswith('.adminfile'):
        admin = True
        while True:
            attempt = input(Style.BRIGHT + "This file requires admin privileges. Enter the admin password: " + Style.RESET_ALL)
            if attempt == str(adminpass):
                cleaned = content.replace('.adminfile', '')
                if first.endswith('.py'):
                    highlighted_code = highlight(cleaned, PythonLexer(), TerminalFormatter())
                    print(highlighted_code)
                else:
                    print(cleaned.strip())
                break
            else:
                print(Style.BRIGHT + Fore.RED + "Incorrect password. Please try again." + Style.RESET_ALL)
    else:
        if first.endswith('.py'):
            highlighted_code = highlight(content, PythonLexer(), TerminalFormatter())
            print(highlighted_code)
        else:
            print(content.strip())

# Action menu
def opensequence():
    while True:
        first = input("Enter the file you want to open: ")
        if first.strip():
            break
        print(Style.BRIGHT + Fore.RED + "File name cannot be empty. Please try again." + Style.RESET_ALL)
    if first.endswith('.txt') or first.endswith('.py'):
        query = first
    elif os.path.exists(first + '.py'):
        query = first + '.py'
        print(Style.BRIGHT + "Python File" + Style.RESET_ALL)
    else:
        query = first + '.txt'
        print(Style.BRIGHT + "Text Document (.txt)" + Style.RESET_ALL)

    if os.path.isfile(query):
        openfile(query,query)
        input("Press " + Style.BRIGHT + "enter " + Style.RESET_ALL + "for more options.")
        try:
            print(Style.BRIGHT + "Action menu" + Style.RESET_ALL)
            actionchoice = int(input("""    What would you like to do?
    1 - Write in document
    2 - Find in document
    3 - Delete document
    4 - Extras
    0 - Nothing
    """))
        except ValueError:
            print("Please enter a valid choice.")
            time.sleep(1)
            start()
            return

        if actionchoice == 1:
            print("Type CANCEL to cancel the action")
            writechoice = input("Complete rewrite (w) or just add to the end? (a) ")
            if writechoice.upper().strip() == 'W':
                with open(query, "w", encoding="utf-8") as f:
                    if ".py" in query:
                        print("Python File")
                    newcontent = input("Enter some text for your file. ")
                    formatted = newcontent.replace("\\n ", "\n").replace("\\t", "\t").encode().decode("unicode_escape")
                    if admin:
                        f.write(".adminfile\n")
                    f.write(formatted.strip() + "\n")
                    f.flush()
                print(Style.BRIGHT + "Done." + Style.RESET_ALL)
                input("Press " + Style.BRIGHT + "enter " + Style.RESET_ALL + "to go back.")
                start()
            elif writechoice.upper().strip() == 'A':
                with open(query, "a", encoding="utf-8") as f:
                    newcontent = input("Enter some text for your file. ")
                    formatted = newcontent.replace("\\n ", "\n").replace("\\t", "\t").encode().decode("unicode_escape")
                    f.write(formatted.strip() + "\n")
                print(Style.BRIGHT + "Done." + Style.RESET_ALL)
                input("Press " + Style.BRIGHT + "enter " + Style.RESET_ALL + "to go back.")
                start()
            elif writechoice.upper().strip() == 'CANCEL':
                opensequence()

        elif actionchoice == 2:
            print("Type CANCEL to cancel the action")
            findchoice = input("Enter the string you want to find: ")
            if findchoice.upper().strip() == 'CANCEL':
                opensequence()
            else:
                with open(query, "r") as f:
                    lines = f.readlines()
                    found = False
                    for i, line in enumerate(lines):
                        if findchoice.upper().strip() in line.upper():
                            print("Found!", line.strip().replace(findchoice, Style.BRIGHT + findchoice + Style.RESET_ALL), "<- Line", i + 1)
                            found = True
                    if not found:
                        print("That text is nowhere to be found :(")
                input("Press " + Style.BRIGHT + "enter " + Style.RESET_ALL + "to go back.")
                start()

        elif actionchoice == 3:
            confirm = input("Are you sure? " + Style.DIM + "(Y/n) " + Style.RESET_ALL)
            if confirm.upper().strip() == 'Y' or not confirm:
                while True:
                    try:
                        os.remove(query)
                        print("Obliterated.")
                        time.sleep(3)
                        start()
                        break
                    except PermissionError:
                        continue
            elif confirm.upper().strip() == 'N':
                input("Okay! Press " + Style.BRIGHT + "enter " + Style.RESET_ALL + "to go back.")
                start()

        elif actionchoice == 4:
            print(Style.BRIGHT + "Extras" + Style.RESET_ALL)
            extrachoice = int(input("""    1 - Show file metadata
    2 - Show character count
    0 - Go back
    """))
            if extrachoice == 1:
                filesize = os.path.getsize(query)
                modtime = os.path.getmtime(query)
                acctime = os.path.getatime(query)

                print(f'File name: {os.path.basename(query)}')
                print(f'File size: {filesize} Bytes')
                print(f'Last modification time: {datetime.fromtimestamp(modtime)}')
                print(f'Last access time: {datetime.fromtimestamp(acctime)}')
                input("Press " + Style.BRIGHT + "enter " + Style.RESET_ALL + "to go back.")
                start()

            elif extrachoice == 2:
                with open(query, 'r') as f:
                    contents = f.read()

                words = len(contents.split())
                print(f'Character count: {len(contents)}')
                print(f'Words: {words}')
                input("Press " + Style.BRIGHT + "enter " + Style.RESET_ALL + "to go back.")
                start()

        elif actionchoice == 0:
            print("Alright, going back.")
            time.sleep(1)
            start()
        else:
            print("Please enter a valid choice")

    else:
        choice = input("This file doesn't exist. Would you like to create it? " + Style.DIM + "(Y/n) " + Style.RESET_ALL)
        if choice.upper().strip() == 'Y' or not choice:
            open(query, "x", encoding="utf-8")
            print("Created file " + Style.BRIGHT + query + Style.RESET_ALL)
            with open(query, "w", encoding="utf-8") as f:
                content = input("Enter some text for your file. " + Style.DIM + "(Press enter to leave empty) " + Style.RESET_ALL)
                formatted = content.replace("\\n ", "\n").replace("\\t", "\t").encode().decode("unicode_escape")
                f.write(formatted.strip() + "\n")
                f.flush()
            print(Style.BRIGHT + "Done." + Style.RESET_ALL)
            input("Press " + Style.BRIGHT + "enter " + Style.RESET_ALL + "to go back.")
            start()
        elif choice.upper().strip() == 'N':
            print("Alright, exiting...")
            time.sleep(1)
            start()
        else:
            print("It was a yes or no question...")
            time.sleep(1)
            start()

# Main menu
def start():
    print(Fore.BLUE + Style.BRIGHT + "Matteo's CLI FileTool (v0.6)    " + Fore.RESET + "User: " + getpass.getuser() + Style.RESET_ALL)
    try:
        print(Style.BRIGHT + "Main menu" + Style.RESET_ALL)
        menuchoice = int(input("""    1 - Read help menu """ + Style.DIM + """(suggested for first-time users)""" + Style.RESET_ALL + """
    2 - Open a file """ + Style.DIM + """(the Action Menu)""" + Style.RESET_ALL + """
    3 - Open Changelog """ + Style.DIM + """(see what changed)""" + Style.RESET_ALL + """
    0 - Exit
    """))
    except ValueError:
        print("Please enter a valid choice.")
        time.sleep(1)
        start()
        return

    if menuchoice == 1:
        print(Style.BRIGHT + "Help menu" + Style.RESET_ALL)
        print("""	This program is designed to help you open text documents.
        As of """ + Style.BRIGHT + """v0.2""" + Style.RESET_ALL + """, you can also create files if the file you want doesn't exist.
        To create an """ + Style.BRIGHT + """admin-locked file""" + Style.RESET_ALL + """, simply add ".adminfile" in the 
        beginning of the document.""")
        input("Press " + Style.BRIGHT + "enter" + Style.RESET_ALL + " to go back")
        start()
    elif menuchoice == 2:
        opensequence()
    elif menuchoice == 3:
        print(Style.BRIGHT + "Changelog" + Style.RESET_ALL)
        print(Style.BRIGHT + "v0.1: " + Style.RESET_ALL + "Bare minimum. Allowed opening and creating files.")
        print(Style.BRIGHT + "v0.2: " + Style.RESET_ALL + "Added main menu. Added the ability to write in new files.")
        print(Style.BRIGHT + "v0.3: " + Style.RESET_ALL + "Added the Changelog. Added the ability to write in any file. Squashed bugs.")
        print(Style.BRIGHT + "v0.4: " + Style.RESET_ALL + "Major update. Added multiple extra options when opening a file. Squashed bugs.")
        print(Style.BRIGHT + "v0.5: " + Style.RESET_ALL + "Added the ability to cancel choice and squashed bugs.")
        print(Style.BRIGHT + "v0.5.1: " + Style.RESET_ALL + "Fixed a bug where \\n and \\t didn't work as newline and tab.")
        print(Style.BRIGHT + "v0.5.2: " + Style.RESET_ALL + "Fixed a formatting error related to creation and editing of files.")
        print(Style.BRIGHT + "v0.5.3: " + Style.RESET_ALL + "Fixed a bug where the CANCEL operation didn't work. Added minor optimizations.")
        print(Style.BRIGHT + "v0.5.4: " + Style.RESET_ALL + "Optimized further and removed bugs")
        print(Style.BRIGHT + "v0.6: " + Style.RESET_ALL + "Made the program prettier, added automatic file type detection, and added code syntax highlighting.")
        input("Press " + Style.BRIGHT + "enter" + Style.RESET_ALL + " to go back")
        start()
    elif menuchoice == 0:
        print("That's all, folks!")
        exit()
    else:
        print("Please enter a valid choice")
        time.sleep(1)
        start()

start()