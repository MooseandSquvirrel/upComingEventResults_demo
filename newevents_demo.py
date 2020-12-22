import selenium
import requests
import pprintpp as pp
import json
bandObj = __import__('bandClass')
cardObj = __import__('cardObj')
tk = __import__('tk')

# PAGINATION IS NOT ACCOUNTED FOR IN EACH BAND'S POST COUNT FOR ADMINS AND MEMBERS (COULD BE ADDED WITH BAND API CALL INVOVLING 'NEXT' IN DOCS)
# CURRENTLY COUNTING POSTS --AND-- COMMENTS AS BOTH POSTS (ASIDE FROM HAVING commentCount AS ITS OWN VARIABLE)

def args():
    args_check, args_check2 = "", "", ""

    while args_check != 'y':
        commandline_name = input("\n\n\n\nPress 'l' for LGS or 'v' for Varsity Trello:\n")
        if (commandline_name != 'l') and (commandline_name != 'v'):
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

    return commandline_name, commandline_list

def lists_id(name_partner):
    if name_partner == "l":
        board_id = "111111111"
    if name_partner == "v":
        board_id = "222222222"
    lists_response = requests.get('https://api.trello.com/1/boards/' + board_id + '/lists' + tk.keyAndTokenParams)
    lists_raw = json.loads(lists_response.text)
    lists_ids = [(items['id'], items['name']) for items in lists_raw if 'name' and 'id' in items]
    return lists_ids

def cards(lists):
    list_ids, cards_arr, upComingEvents, liveEvents = [], [], [], []
    count = 0
    list_ids = lists[0][0], lists[1][0]

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

    print(f"upComingEvents:\n{upComingEvents}\n\n")
    print(f"liveEvents:\n{liveEvents}\n\n")
    return upComingEvents, liveEvents

def get_bands(names):
    bands_obj_arr = []
    bands_response = requests.get('https://openapi.band.us/v2.1/bands?access_token=' + tk.bandToken)
    bands = json.loads(bands_response.text)
    result_data =  bands['result_data']['bands']
    print(f"-get_bands- names of bands from names list from Trello: {names}")
    for band in result_data:
        if band['name'] in names:
            # 0 CURRENT postsCount, commentCount, adminCount FROM BAND FOR INITIALIZATION/INSTANCE
            band = bandObj.Bandaid(band, 0, 0, 0, band['member_count'])
            bands_obj_arr.append(band)
    return bands_obj_arr

def counter(result_data):
    total_posts, admin_posts, comments = 0, 0, 0
    for posts in result_data:
        if posts['post_key']:
            if posts['author']['role'] != 'member':
                admin_posts += 1
                comments += posts['comment_count']
            elif posts['author']['role'] == 'member':
                total_posts += 1
                comments += posts['comment_count']
            total_posts = total_posts + admin_posts
    return total_posts, admin_posts, comments

def get_post_counts(bands_obj_arr):
    for band in bands_obj_arr:
        band_id = band.apiResult['band_key']
        bands_response_raw = requests.get('https://openapi.band.us/v2/band/posts?access_token=' + tk.bandToken + '&band_key=' + band_id + '&locale=en_US')
        bands_response= json.loads(bands_response_raw.text)
        result_data = bands_response['result_data']['items']
        print(result_data)
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
    adminActiviy, totalActivity = "", ""
    noActivity = 0
    lowActivity = range(1, 5)
    goodActivity = range(6, 10)
    greatActivity = range(10, 100)
    for band in results:
        if band.adminCount == noActivity:
            band.set_adminActivity("No Posts in Band")
        elif band.adminCount in lowActivity:
            band.set_adminActivity("Low Activity")
        elif band.adminCount in goodActivity:
            band.set_adminActivity("Good Activity")
        elif band.adminCount in greatActivity:
            band.set_adminActivity("Great Activity")
        print(f"UPCOMINGEVENTS: band.get_adminActivity(): " + band.get_adminActivity() + " for " + band.apiResult['name'] + " band")
    for band in results:
        if band.adminCount == noActivity:
            band.set_totalActivity("No Posts in Band")
        elif band.adminCount in lowActivity:
            band.set_totalActivity("Low Activity")
        elif band.adminCount in goodActivity:
            band.set_totalActivity("Good Activity")
        elif band.adminCount in greatActivity:
            band.set_totalActivity("Great Activity")
        print(f"UPCOMINGEVENTS: band.get_totalActivity(): " + band.get_totalActivity() + " for " + band.apiResult['name'] + " band")
    return results
        
def judge_liveEvents(results):
    adminActiviy, memberActivity = "", ""
    noActivity = 0
    lowActivity = range(1, 7)
    goodActivity = range(8, 14)
    greatActivity = range(15, 100)
    for band in results:
        if band.adminCount == noActivity:
            band.set_adminActivity("No Posts in Band")
        elif band.adminCount in lowActivity:
            band.set_adminActivity("Low Activity")
        elif band.adminCount in goodActivity:
            band.set_adminActivity("Good Activity")
        elif band.adminCount in greatActivity:
            band.set_adminActivity("Great Activity")
        print(f"LIVEEVENTS: band.get_adminActivity: " + band.get_adminActivity() + " for " + band.apiResult['name'] + " band")
    for band in results:
        if band.postsCount == noActivity:
            band.set_totalActivity("No Posts in Band")
        elif band.postsCount in lowActivity:
            band.set_totalActivity("Low Activity")
        elif band.postsCount in goodActivity:
            band.set_totalActivity("Good Activity")
        elif band.postsCount in greatActivity:
            band.set_totalActivity("Great Activity")
        print(f"LIVEEVENTS: band.get_totalActivity: " + band.get_totalActivity() + "for " + band.apiResult['name'] + " band")
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
            f.write("Activity: ")
            f.write(band.get_totalActivity() + '\n')
            f.write("Admin Activity: ")
            f.write(band.get_adminActivity() + '\n\n')

def main():
    ## THIS IS JUST EXAMPLE OF OBJEC FOR CARDS THAT WILL COLLECT NAME OF EVENT AND URL FROM EACH CARD IN LISTS
    name_partner, which_list = args()
    lists_ids = lists_id(name_partner)
    upComingEvents, eventsLive = cards(lists_ids)
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