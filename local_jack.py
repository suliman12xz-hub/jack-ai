import os

while True:
    cmd = input("Jack> ").lower()

    if "open safari" in cmd:
        os.system("open -a Safari")

    elif "open chrome" in cmd:
        os.system('open -a "Google Chrome"')

    elif "open calculator" in cmd:
        os.system("open -a Calculator")

    elif cmd == "exit":
        break

    else:
        print("I don't know that command yet.")
