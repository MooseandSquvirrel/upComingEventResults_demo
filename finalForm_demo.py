import selenium
import requests
from pprint import pprint
import json
import time
bandObj = __import__('bandClass')
cardObj = __import__('cardObj')
tk = __import__('tk')

# PAGINATION IS NOT ACCOUNTED FOR IN EACH BAND'S POST COUNT FOR ADMINS AND MEMBERS (COULD BE ADDED WITH BAND API CALL INVOVLING 'NEXT' IN DOCS)
# CURRENTLY COUNTING POSTS --AND-- COMMENTS AS BOTH POSTS (ASIDE FROM HAVING commentCount AS ITS OWN VARIABLE)

def args():
    args_check, args_check2 = "", ""
    args_check3 = []
    while args_check != 'y':
        commandline_name = input("\n\n\n\nPress 'l' for LGS - 'v' for Varsity - 'a' for AYSO - 'g' for Glazier:\n")
        if (commandline_name != 'l') and (commandline_name != 'v') and (commandline_name != 'a') and (commandline_name != 'g'):
            print("\n\n\n\n\n\n\nPlease type only a 'l' or 'v'.\nDon't be one of those users. You're not that user...\nare you...? \n:)\n")
            continue
        else:
            print("You Entered: " + commandline_name)
            args_check = input("If this is correct enter 'y', otherwise press Enter to try again:\n")
    while args_check2 != 'y':
        commandline_list = input("\n\n\n\nPress '1' Upcoming Events or '2' for Live events stats:\n")
        if (commandline_list != '1') and (commandline_list != '2'):
            print("\n\n\n\n\n\n\nPlease type only a 'l' or 'v'.\nDon't be one of those users. You're not that user...\nare you...? \n:)\n")
            continue
        else:
            print("You Entered: " + commandline_list)
            args_check2 = input("If this is correct enter 'y', otherwise press Enter to try again:\n")
    print(f"commandline_name: {commandline_name}, commandline_list: {commandline_list}")
    while args_check3 != 'y':
        commandline_arr = []
        args_check3 = input("\n\n\n\nDo you have band(s) to ignore - 'y' or 'n'?:\n")
        if (args_check3 != 'y') and (args_check3 != 'n'):
            print("\n\n\n\n\n\n\nPlease type only a 'y' or 'n'.\nDon't be one of those users. You're not that user...\nare you...? \n:)\n")
            continue
        elif args_check3 == 'y':
            args_check3 = ""
            while args_check3 != 'n':
                name = ""
                print("Paste the BAND name:")
                name = input()
                print(name)
                commandline_arr.append(name)
                print(commandline_arr)
                args_check3 = input("Do you have any more bands? 'y' or 'n':\n")
        if args_check3 == 'n':
            break
    return commandline_name, commandline_list, commandline_arr

def lists_id(name_partner):
    if name_partner == "l" or name_partner == "a" or name_partner == "g":
        board_id = "111111"
    if name_partner == "v":
        board_id = "222222"
    lists_response = requests.get('https://api.trello.com/1/boards/' + board_id + '/lists' + tk.keyAndTokenParams)
    print(lists_response)
    lists_raw = json.loads(lists_response.text)
    lists_ids = [(items['id'], items['name']) for items in lists_raw if 'name' and 'id' in items]
    return lists_ids

def v_func(lists, ignore_band_list):
    # list_ids REPRESENT - upcoming events trello list: lists[0][0] 
    # AND live events list: lists[whichever partner was selected by letter][0]
    list_ids = lists[0][0], lists[1][0]

    for ids in list_ids:
        cards_response_raw = requests.get('https://api.trello.com/1/lists/' + ids + '/cards' + tk.keyAndTokenParams)
        cards_response = json.loads(cards_response_raw.text)

        two = 0
        one = 0
        for i in cards_response:
            attachments = i['badges']['attachments']
            print(f"attachments: {attachments}")

            if attachments == 2:
                two += 1
                print(f"TWO: {two}")
                card_id = i['id']
                cards_attachment_json = requests.get('https://api.trello.com/1/cards/' + card_id + '/attachments' + tk.keyAndTokenParams)
                cards_attachment_response = json.loads(cards_attachment_json.text)
                for j in cards_attachment_response:
                    # ERROR CHECK FOR BAND NAME THAT MIGHT HAVE COACHES OR PUBLIC IN IT ON PURPOSE (ACTUAL BAND NAME NOT TRELLO)
                    if j['name'] in ignore_band_list:
                        if count == 0:
                            upComingEvents.append(j['name'])
                        else:
                            liveEvents.append(j['name'])
                    if j['name']:
                        if "Public" in j['name'] or "public" in j['name'] or "Coaches" in j['name'] or "coaches" in j['name'] or "coach" in j['name'] or "Coach" in j['name']:
                            str_lst = j['name'].split()
                            new_lst = str_lst[:len(str_lst) - 2]
                            new_name = " ".join(new_lst)
                            if count == 0:
                                upComingEvents.append(new_name)
                            else:
                                liveEvents.append(new_name)
                        else:
                            if count == 0:
                                upComingEvents.append(j['name'])
                            else:
                                liveEvents.append(j['name'])
                                
            elif attachments == 1:
                one += 1
                if i['name']:
                    if count == 0:
                        upComingEvents.append(i['name'])
                    else:
                        liveEvents.append(i['name'])
        count += 1

def l_func(lists):
    # lists[2][0] LGS Upcoming lists[3][0] ALL Live events
    list_ids = lists[2][0], lists[3][0]
    for ids in list_ids:
        cards_response_raw = requests.get('https://api.trello.com/1/lists/' + ids + '/cards' + tk.keyAndTokenParams)
        cards_response = json.loads(cards_response_raw.text)
        for i in cards_response:
            if i['name']:
                if count == 0:
                    upComingEvents.append(i['name'])
                else:
                    liveEvents.append(i['name'])
        count += 1

def a_func():
    # lists[0][0] LGS Upcoming lists[3][0] ALL Live events
    list_ids = lists[0][0], lists[3][0]
    for ids in list_ids:
        cards_response_raw = requests.get('https://api.trello.com/1/lists/' + ids + '/cards' + tk.keyAndTokenParams)
        cards_response = json.loads(cards_response_raw.text)
        for i in cards_response:
            if i['name']:
                if count == 0:
                    upComingEvents.append(i['name'])
                else:
                    liveEvents.append(i['name'])
        count += 1

def g_func(lists):
    # lists[1][0] LGS Upcoming lists[3][0] ALL Live events
    list_ids = lists[1][0], lists[3][0]
    for ids in list_ids:
        cards_response_raw = requests.get('https://api.trello.com/1/lists/' + ids + '/cards' + tk.keyAndTokenParams)
        cards_response = json.loads(cards_response_raw.text)
        for i in cards_response:
            if i['name']:
                if count == 0:
                    upComingEvents.append(i['name'])
                else:
                    liveEvents.append(i['name'])
        count += 1        

def cards(name_partner, lists, ignore_band_list):
    list_ids, cards_arr, upComingEvents, liveEvents = [], [], [], []
    count = 0
    if name_partner == "v":
        v_func(lists, ignore_band_list)
    if name_partner == "l":
        l_func(lists)
    if name_partner == "a":
        a_func(lists)
    if name_partner == "g":
        g_func(lists)
    return upComingEvents, liveEvents

def get_bands(names):
    bands_obj_arr = []
    bands_response = requests.get('https://openapi.band.us/v2.1/bands?access_token=' + tk.bandToken)
    bands = json.loads(bands_response.text)

    result_data =  bands['result_data']['bands']
    for band in result_data:
        if band['name'] in names:
            # 0 CURRENT postsCount, commentCount, adminCount FROM BAND FOR INITIALIZATION/INSTANCE
            band = bandObj.Bandaid(band, 0, 0, 0, band['member_count'], "", "")
            bands_obj_arr.append(band)
    return bands_obj_arr

def counter(result_data):
    total_posts, admin_posts, comments = 0, 0, 0
    for posts in result_data:
        if posts['post_key']:
            if posts['author']['role'] != 'member':
                admin_posts += 1
                print("admin post == " + posts['content'])
                comments += posts['comment_count']
            elif posts['author']['role'] == 'member':
                total_posts += 1
                print("member post == " + posts['content'])
                comments += posts['comment_count']
    return total_posts, admin_posts, comments

def get_post_counts(bands_obj_arr):
    for band in bands_obj_arr:
        band_id = band.apiResult['band_key']
        bands_response_raw = requests.get('https://openapi.band.us/v2/band/posts?access_token=' + tk.bandToken + '&band_key=' + band_id + '&locale=en_US')
        bands_response= json.loads(bands_response_raw.text)
        result_data = bands_response['result_data']['items']
        #### print(result_data)
        total_posts, admin_posts, comments = counter(result_data)
        band.postsCount = total_posts
        band.adminCount = admin_posts
        band.commentCount = comments
        print("BAND:")
        print("apiResult")
        print(band.apiResult)
        print("postsCount")
        print(band.postsCount)
        print("adminCount")
        print(band.adminCount)
        print("commentCount")
        print(band.commentCount)
    return bands_obj_arr

def judge_upComingEvents(results):
    noActivity = 0
    lowActivity = range(1, 3)
    normalActivity = range(3, 5)
    goodActivity = range(5, 8)
    greatActivity = range(8, 100)
    for band in results:
        if band.adminCount == noActivity:
            band.adminActivity = "No Posts in Band"
        elif band.adminCount in lowActivity:
            band.adminActivity = "Low Activity"
        elif band.adminCount in normalActivity:
            band.adminActivity = "Normal Activity"
        elif band.adminCount in goodActivity:
            band.adminActivity = "Good Activity"
        elif band.adminCount in greatActivity:
            band.adminActivity = "Great Activity"
     #   print(f"UPCOMINGEVENTS: band.get_adminActivity(): " + band.get_adminActivity() + " for " + band.apiResult['name'] + " band")
    for band in results:
        if band.postsCount == noActivity:
            band.totalActivity = "No Posts in Band"
        elif band.postsCount in lowActivity and band.commentCount < 10:
            band.totalActivity = "Very Low Activity"
        elif band.postsCount in lowActivity and band.commentCount > 10:
            band.totalActivity = "Low Activity"
        elif band.postsCount in normalActivity:
            band.totalActivity = "Normal Activity"
        elif band.postsCount in goodActivity or band.commentCount >= 10:
            band.totalActivity = "Good Activity"
        elif band.postsCount in greatActivity or commentCount >= 20:
            band.totalActivity = "Great Activity"
      #  print(f"UPCOMINGEVENTS: band.get_totalActivity(): " + band.get_totalActivity() + " for " + band.apiResult['name'] + " band")
    return results
        
def judge_liveEvents(results):
    noActivity = 0
    lowActivity = range(1, 3)
    normalActivity = range(3, 5)
    goodActivity = range(5, 8)
    greatActivity = range(8, 100)
    for band in results:
        if band.adminCount == noActivity:
            band.adminActivity = "No Posts in Band"
        elif band.adminCount in lowActivity:
            band.adminActivity = "Low Activity"
        elif band.adminCount in normalActivity:
            band.adminActivity = "Normal Activity"
        elif band.adminCount in goodActivity:
            band.adminActivity = "Good Activity"
        elif band.adminCount in greatActivity:
            band.adminActivity = "Great Activity"
    for band in results:
        if band.postsCount == noActivity:
            band.totalActivity = "No Posts in Band"
        elif band.postsCount in lowActivity and band.commentCount < 10:
            band.totalActivity = "Very Low Activity"
        elif band.postsCount in lowActivity and band.commentCount > 10:
            band.totalActivity = "Low Activity"
        elif band.postsCount in normalActivity:
            band.totalActivity = "Normal Activity"
        elif band.postsCount in goodActivity or band.commentCount >= 10:
            band.totalActivity = "Good Activity"
        elif band.postsCount in greatActivity or commentCount >= 20:
            band.totalActivity = "Great Activity"
    return results

def print_results(which_list, final_results):
    file_name = ""
    if which_list == "1":
        file_name = "file_upComingEvents.txt"
    elif which_list == "2":
        file_name = "file_eventsLive.txt"
    with open(file_name, 'w+') as f:
        for band in final_results:
            f.write('Band: ')
            f.write(band.apiResult['name'] + '\n')
            f.write('Member Size: ')
            f.write(str(band.memberCount) + '\n')
            f.write("Member Activity: ")
            f.write(band.totalActivity + '\n')
            f.write("Admin Activity: ")
            f.write(band.adminActivity + '\n\n')

def main():
    ## THIS IS JUST EXAMPLE OF OBJEC FOR CARDS THAT WILL COLLECT NAME OF EVENT AND URL FROM EACH CARD IN LISTS
    name_partner, which_list, ignore_band_list = args()
    lists_ids = lists_id(name_partner)
    upComingEvents, eventsLive = cards(name_partner, lists_ids, ignore_band_list)
    if which_list == '1':
        bands_obj_arr = get_bands(upComingEvents)
        print(f"here {bands_obj_arr}")
    elif which_list == '2':
        bands_obj_arr = get_bands(eventsLive)
    results = get_post_counts(bands_obj_arr)
    if which_list == '1':
        final_results = judge_upComingEvents(results)
    elif which_list == '2':
        final_results = judge_liveEvents(results)
    print_results(which_list, final_results)

if __name__ == "__main__":
    main()