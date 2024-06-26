import os, time, sys, shutil, ctypes, datetime, logging, atexit, getpass

filepath = sys.argv[0]
user = getpass.getuser()
os.system("title Admin check...")
if not os.path.exists("C:/Cleaner"):
    os.mkdir("C:/Cleaner")
    os.mkdir("C:/Cleaner/Logs")


t = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
final = "C:/Cleaner/Logs/log_" + t + ".txt"
features = """Make sure to run as admin (right click the file and press run as admin)
1. Clean files
Description: Cleans the files in C:\Windows\Temp (If there are any)
These files are temporaray files used by other programs that can be deleted without causing any trouble
2. Scan disk
Description: Uses the command sfc/scannow to perform a scan on the device. Locates and repairs corrupt files
3. Exit
Description: Exits the program using sys.exit()
4. Custom clean
Description: Cleans a folder/file by asking for the file path from the user. If the file/folder exists then it will delete it. 
If you by accidentally delete a critical file then its not my problem. Only recommended for big folders. 
5. Clear DNS resolver cache
Description: Clears DNS resolver cache by using the command ipconfig/flushdns. 
This can sometimes make the connection faster and might be able to fix some internet issues. 
6. Run everything
Description: Runs everything
7. Clear recycle bin
Description: If your're lazy and can't click twice use this option
"""

if not os.path.exists("C:/Cleaner/Features"):
    os.mkdir("C:/Cleaner/Features")
g = open("C:/Cleaner/Features/Features.txt", "w")
g.write(features)
g.close()

logging.basicConfig(filename=final, filemode="x",format= "%(asctime)s | Cleaner | %(levelname)s | %(lineno)d | %(message)s", level=logging.INFO)
logger = logging.getLogger("Cleaner")
# this is for the logging, which records which commands you used and possible errors.


def admincheck():
    try:
        logging.info("Passed admin check")
        logging.info("Welcome %s" % user)
        is_admin = (os.getuid() == 0)
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin
# Checks if the program is running as admin
# NOTE: THIS IS NOT MY CODE


if not admincheck():
    logging.error("Failed admin check")
    logging.info("Closing in 2 seconds")
    print("Run as admin for this to work")
    print("Closing in 2 seconds")
    time.sleep(2)
    sys.exit()


def exitlog():
    logging.info("Exited program")


atexit.register(exitlog)


def cleanfiles():
    os.system("title Cleaning files...")
    path = "C:/Windows/Temp"
    print("Cleaning %s" % path)
    file_count = sum(len(files) for _, _, files in os.walk(r"%s" % path))
    print("Found %s files in C:/Windows/Temp" % file_count)
    logging.info("Found %s files in C:/Windows/Temp" % file_count)
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
                print("Deleted", filename, "from C:/Windows/Temp")
                logging.info("Deleted %s from C:/Windows/Temp" % filename)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            logging.error("Couldn't delete %s from C:/Windows/Temp" % filename)
            logging.exception(e)
            logging.info("You can try to manually delete files by pressing windows key + r and search temp")
            print("Couldnt delete", filename, "from C:/Windows/Temp (Permission error?)")
    file_countafter = sum(len(files) for _, _, files in os.walk(r"%s" % path))
    filescleaned = int(file_count) - int(file_countafter)
    print("Cleaned %s files in C:/Windows/Temp" % filescleaned)
    logging.info("Cleaned %s files in C:/Windows/Temp" % filescleaned)


def customclean():
    try:
        os.system("title Custom clean, enter a path")
        logging.info("User selected option 5")
        custompath = input("Enter a file/folder to delete: ")
        logging.info("User searched for path %s" % custompath)
        logging.info("Locating file/folder...")
        os.system("title Locating path")
        print("Locating path...")
        if os.path.exists(custompath):
            print("Found path", custompath)
            logging.info("Located file/folder")
            logging.info("Found file/folder")
            confirm = input("Are you sure you want to clean this file/folder? (Y/N): ")
            if confirm == "Y":
                print("Deleting", custompath)
                logging.info("Deleting file/folder")
                shutil.rmtree(custompath)
                logging.info("Deleted file/folder")
                print("Finished deleting", custompath)
                print("Returning to menu")
                time.sleep(3)
                start()
            elif confirm == "N":
                logging.info("Returning to menu")
                print("Returning to menu")
                time.sleep(3)
                start()
            else:
                print("Invalid input")
                logging.error("Invalid input")
                logging.info("Returning to menu")
                print("Returning to menu")
                time.sleep(3)
                start()
        if not os.path.exists(custompath):
            print("Stop trying to troll me that path doesn't exist")
            logging.error("User chose a path that doesn't exist (BRUH)")
            logging.info("Returning to menu")
            print("Returning to menu")
            time.sleep(3)
            start()
    except Exception as e:
        print("Couldn't delete file/folder %s" % custompath)
        logging.error("Couldn't delete file/folder", custompath, "Reason:", e)


def scan():
    try:
        task = "Scanning disk..."
        os.system("title %s" % task)
        print("Scanning %s" % task)
        logging.info("%s" % task)
        os.system("sfc/scannow")
        taskcomplete = "Finished scanning disk"
        print("%s" % taskcomplete)
        os.system("title %s" % taskcomplete)
        logging.info("%s" % taskcomplete)
    except Exception as e:
        logging.info(e)
        print("Couldn't scan disk %s" % e)


def clearcache():
    try:
        task2 = "Clearing DNS resolver cache"
        os.system("title %s" % task2)
        print("%s" % task2)
        logging.info("%s" % task2)
        os.system("ipconfig/flushdns")
        task2complete = "Finished clearing DNS resolver cache"
        os.system("title %s" % task2complete)
        print("%s" % task2complete)
        logging.info("%s" % task2complete)
    except Exception as e:
        logging.error(e)
        print("Couldn't clear DNS resolver cache %s" % e)


def recyclebin():
    try:
        task3 = "Cleaning recyclebin"
        os.system("title %s" % task3)
        print("%s" % task3)
        logging.info("%s" % task3)
        os.system("rd /s %systemdrive%\$Recycle.bin")
        task3complete = "Finished cleaning recycle bin"
        os.system("title %s" % task3complete)
        print("%s" % task3complete)
        logging.info("%s" % task3complete)
    except Exception as e:
        logging.info(e)
        print("Couldn't clean recycle bin %s" % e)


def everything():
    logging.info("Running everything, this may take a while")
    print("Running everything, this may take a while")
    cleanfiles()
    scan()
    recyclebin()
    logging.info("Finished running everything")
    print("Finished running everything")


def start():
    logging.info("Loaded menu")
    os.system("cls")
    os.system("title Menu")
    print("""
░█████╗░██╗░░░░░███████╗░█████╗░███╗░░██╗███████╗██████╗░
██╔══██╗██║░░░░░██╔════╝██╔══██╗████╗░██║██╔════╝██╔══██╗
██║░░╚═╝██║░░░░░█████╗░░███████║██╔██╗██║█████╗░░██████╔╝
██║░░██╗██║░░░░░██╔══╝░░██╔══██║██║╚████║██╔══╝░░██╔══██╗
╚█████╔╝███████╗███████╗██║░░██║██║░╚███║███████╗██║░░██║
░╚════╝░╚══════╝╚══════╝╚═╝░░╚═╝╚═╝░░╚══╝╚══════╝╚═╝░░╚═╝  
1. Clean files
2. Scan disk
3. Exit
4. Custom clean
5. Clear DNS resolver cache 
6. Run all options (runs everything)
7. Clean recycle bin
"""
          )
    choice = input("Select an option: ")
    if not choice.isdigit():
        logging.error("Invalid input")
        print("Invlalid input")
        print("Returning to menu")
        logging.info("Returning to menu")
        time.sleep(3)
        start()
        return
    if choice == "1":
        logging.info("User selected option 1 (Clean files)")
        cleanfiles()
        print("Finished cleaning files")
        logging.info("Finished cleaning files")
        print("You can try to manually delete files by pressing windows key + r and search temp")
        logging.info("Returning to menu")
        print("Returning to menu")
        time.sleep(3)
        start()
    elif choice == "2":
        logging.info("User selected option 2 (Scan disk)")
        scan()
        logging.info("Returning to menu")
        print("Returning to menu")
        time.sleep(3)
        start()
    elif choice == "3":
        logging.info("User selected option 3 (Exit)")
        leave = input("Are you sure you want to exit (Y/N): ")
        if leave == "Y":
            sys.exit()
        elif leave == "N":
            logging.info("Returning to menu")
            print("Returning to menu")
            time.sleep(3)
            start()
        else:
            logging.error("Invalid input")
            print("Invalid input")
            logging.info("Returning to menu")
            print("Returning to menu")
            time.sleep(3)
            start()
    elif choice == "4":
        logging.info("User selected option 4 (Custom clean)")
        customclean()
        logging.info("Returning to menu")
        print("Returning to menu")
        time.sleep(3)
        start()
    elif choice == "5":
        clearcache()
        logging.info("User selected option 5")
        logging.info("Returning to menu")
        print("Returning to menu")
        time.sleep(3)
        start()
    elif choice == "6":
        logging.info("User selected option 6 (Run everything)")
        sure = input("Are you sure you want to run everything? (Y/N): ")
        if sure == "Y":
            everything()
        elif sure == "N":
            logging.info("Returning to menu")
            print("Returning to menu")
            time.sleep(3)
            start()
        else:
            logging.error("Invalid input")
            logging.info("Returning to menu")
            print("Returning to menu")
            time.sleep(3)
            start()
    elif choice == "8":
        recyclebin()
        logging.info("Returning to menu")
        print("Returning to menu")
        time.sleep(3)
        start()
    else:
        print("Invalid input")
        logging.error("Invalid input")
        print("Returning to menu")
        logging.info("Returning to menu")
        time.sleep(3)
        start()
        # error checking


print("""Version: 0.18
Release 10/22/2021""")
print("Welcome", user)
time.sleep(3)
os.system("cls")
start()











