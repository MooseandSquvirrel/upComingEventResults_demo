import json


def main():
    # MAKE FILE NAME VARIABLE TO OPEN ANY FILE REQUIRED (UPCOMING/LIVEEVENTS)
    filename = 'file_eventsLive.txt'

    commands = {}
    with open(filename) as fh:
        for line in fh:
            command = line.strip().split(':')
            print(command)
            print(command[0])
            print(command[1])
            commands[line] = "#{command[0]}"
            commands[line] = command[1]

    # print(json.dumps(commands, indent=2, sort_keys=True))

main()