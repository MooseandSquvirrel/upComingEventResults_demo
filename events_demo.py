import selenium
import requests
import pprintpp as pp

"""
# CURL TO GRAB TRELLO BOARDS (IDS)
curl 'https://api.trello.com/1/members/me/boards?key=(yourKey)&token=(yourToken)'

# CURL TO GRAB SPECIFIC TRELLO BOARD LISTS
curl 'https://api.trello.com/1/boards/board_num_here/lists?key=key_here&token=token_here' | json_pp
"""

api_key='11111111'
api_secret='2222222'
token='333333'
varsity_board = '4444444'
lgs_board = '55555555'

# UPCOMING EVENTS LIST ID
upComingEvents_id = "66666666"
# EVENTS LIVE NOW/WEEKEND LIST ID
eventsLiveNow = "777777777"

def varsity_client():
    response = requests.get(f"https://api.trello.com/1/boards/{varsity_board}?fields=name,url&key={api_key}&token={token}")
    print(response.text)
    print(dir(response))

def lgs_client():
    requests.get(f"https://api.trello.com/1/boards/{lgs_board}?fields=name,url&key={api_key}&token={token}")

def args():
    args_check = ""
    while args_check != 'y':
        commandline_arg = input("\n\n\n\nPress 'l' for LGS or 'v' for Varsity Trello.\n")
        if (commandline_arg != 'l') and (commandline_arg != 'v'):
            print("\n\n\n\n\n\n\nPlease type only a 'l' or 'v'.\nDon't be one of those users. You're not that user...\nare you...? \n:)\n")
            continue
        else:
            print("You Entered: " + commandline_arg)
            args_check = input("If this is correct enter 'y', otherwise press Enter to try again.\n")
    while args_check != 'y':
        commandline_arg2 = int(input("\n\n\n\nPress 'l' for LGS or 'v' for Varsity Trello.\n"))
        if (commandline_arg2 >= 0 or commandline_arg2 <= 100):
            print("You Entered: " + commandline_arg2)
            args_check = input("If this is correct enter 'y', otherwise press Enter to try again.\n")
        else:
            print("\n\n\n\n\n\n\nPlease type only a Number between 1 - 100 (not 0 or 101 etc.).\nDon't be one of those users. You're not that user...\nare you...? \n:)\n")
            continue
        print("You Entered: " + commandline_arg2)
        args_check = input("If this is correct enter 'y', otherwise press Enter to try again.\n")
    
    return commandline_arg, commandline_arg2

def main():
    varsity_client()
    args()

if __name__ == "__main__":
    main()