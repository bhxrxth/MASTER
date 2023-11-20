command = ""
print("Hello let's Begin")
started = False
while True:
    command = input("> ").lower()
    if command == "start":
        if started:
            print("Car already started😁.")
        else:
            started = True
            print("Car Started... Ready to Go! ")
    elif command == "stop":
        if not started:
            print("Car already stopped😒.")
        else:
            started = False
            print("Car Stopped. ")
    elif command == "exit":
        print("Thank you For Playing!!! ")
        break
    elif command == "help":
        print(
            """
Start- Star the Car
Stop- Stop the Car
Exit- Quit the Game""")

    else:
        print("I don't understand that")
