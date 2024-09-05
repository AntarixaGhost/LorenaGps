import json
import requests
import time
import os
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from sys import stderr

Bl = '\033[30m'  # Black
Re = '\033[1;31m'  # Red
Gr = '\033[1;32m'  # Bright Green (diganti nanti)
Ye = '\033[1;33m'  # Yellow
Blu = '\033[1;34m'  # Blue
Mage = '\033[1;35m'  # Magenta
Cy = '\033[1;36m'  # Cyan
Wh = '\033[1;37m'  # White

# utilities

def box_text(text):
    lines = text.split('\n')
    max_length = max(len(line) for line in lines)
    border = f"{Cy}+{'-' * (max_length + 2)}+"
    result = f"{border}\n"
    for line in lines:
        result += f"{Cy}| {Wh}{line.ljust(max_length)} {Cy}|\n"
    result += f"{border}\n"
    return result


def clear():
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')
    # for mac and linux
    else:
        _ = os.system('clear')


def call_option(opt):
    if not is_in_options(opt):
        raise ValueError('Option not found')
    for option in options:
        if option['num'] == opt:
            if 'func' in option:
                option['func']()
            break


def is_in_options(opt):
    for option in options:
        if option['num'] == opt:
            return True
    return False


def get_user_option():
    while True:
        opt = input(f"{Wh}Please select one option : {Cy}")
        try:
            opt = int(opt)
        except ValueError:
            print(f'{Re}Please enter a valid number')
            continue
        if not is_in_options(opt):
            print(f'{Re}Option not found')
            continue
        return opt


def run_banner():
    clear()
    print(f"""
    {Wh}__                                      {Re}______{Wh}
   / /   ____ _________  ____  ____ _      {Re}/ ____/___  _____{Wh}
  / /   / __ `/ ___/ _ \/ __ \/ __ `/_____{Re}/ / __/ __ \/ ___/{Wh}
 / /___/ /_/ / /  /  __/ / / / /_/ /_____{Re}/ /_/ / /_/ (__  ){Wh}
/_____/\__,_/_/   \___/_/ /_/\__,_/      {Re}\____/ .___/____/{Wh}
                                             {Re}/_/{Wh}Antarixa v 1.0         {Wh}

            {Blu}Contact Information:
  {Wh}GitHub   : {Cy}https://github.com/AntarixaGhost
    """)


def main_menu():
    while True:
        run_banner()
        for option in options:
            print(f"{Cy}| {option['num']}. {Wh}{option['text']}")
        print(f"{Cy}+{'-' * 24}+")
        user_opt = get_user_option()
        call_option(user_opt)


def IP_Track():
    print(f"{Wh}IP Tracker function called")
    ip = input(f"{Wh}\n Enter IP target : {Cy}")  # INPUT IP ADDRESS
    print()
    print(box_text(f'SHOW INFORMATION IP ADDRESS'))
    req_api = requests.get(f"http://ipwho.is/{ip}")  # API IPWHOIS.IS
    ip_data = json.loads(req_api.text)
    time.sleep(2)
    output = f"""
IP target       : {ip}
Type IP         : {ip_data["type"]}
Country         : {ip_data["country"]}
Country Code    : {ip_data["country_code"]}
City            : {ip_data["city"]}
Continent       : {ip_data["continent"]}
Continent Code  : {ip_data["continent_code"]}
Region          : {ip_data["region"]}
Region Code     : {ip_data["region_code"]}
Latitude        : {ip_data["latitude"]}
Longitude       : {ip_data["longitude"]}
Maps            : https://www.google.com/maps/@{ip_data['latitude']},{ip_data['longitude']},8z
EU              : {ip_data["is_eu"]}
Postal          : {ip_data["postal"]}
Calling Code    : {ip_data["calling_code"]}
Capital         : {ip_data["capital"]}
Borders         : {ip_data["borders"]}
Country Flag    : {ip_data["flag"]["emoji"]}
ASN             : {ip_data["connection"]["asn"]}
ORG             : {ip_data["connection"]["org"]}
ISP             : {ip_data["connection"]["isp"]}
Domain          : {ip_data["connection"]["domain"]}
ID              : {ip_data["timezone"]["id"]}
ABBR            : {ip_data["timezone"]["abbr"]}
DST             : {ip_data["timezone"]["is_dst"]}
Offset          : {ip_data["timezone"]["offset"]}
UTC             : {ip_data["timezone"]["utc"]}
Current Time    : {ip_data["timezone"]["current_time"]}
    """
    print(box_text(output))
    input(f"{Wh}Press Enter to return to the main menu...")


def phoneGW():
    print(f"{Wh}Phone Number Tracker function called")
    User_phone = input(f"\n {Wh}Enter phone number target {Cy}Ex [+6281xxxxxxxxx] {Wh}: {Cy}")  # INPUT NUMBER PHONE
    default_region = "ID"

    parsed_number = phonenumbers.parse(User_phone, default_region)
    region_code = phonenumbers.region_code_for_number(parsed_number)
    jenis_provider = carrier.name_for_number(parsed_number, "en")
    location = geocoder.description_for_number(parsed_number, "id")
    is_valid_number = phonenumbers.is_valid_number(parsed_number)
    is_possible_number = phonenumbers.is_possible_number(parsed_number)
    formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    formatted_number_for_mobile = phonenumbers.format_number_for_mobile_dialing(parsed_number, default_region, with_formatting=True)
    number_type = phonenumbers.number_type(parsed_number)
    timezone1 = timezone.time_zones_for_number(parsed_number)
    timezoneF = ', '.join(timezone1)

    output = f"""
Location             : {location}
Region Code          : {region_code}
Timezone             : {timezoneF}
Operator             : {jenis_provider}
Valid number         : {is_valid_number}
Possible number      : {is_possible_number}
International format : {formatted_number}
Mobile format        : {formatted_number_for_mobile}
Original number      : {parsed_number.national_number}
E.164 format         : {phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)}
Country code         : {parsed_number.country_code}
Local number         : {parsed_number.national_number}
Type                 : {'This is a mobile number' if number_type == phonenumbers.PhoneNumberType.MOBILE else 'This is a fixed-line number' if number_type == phonenumbers.PhoneNumberType.FIXED_LINE else 'This is another type of number'}
    """
    print(box_text(output))
    input(f"{Wh}Press Enter to return to the main menu...")


def TrackLu():
    print(f"{Wh}Username Tracker function called")
    try:
        username = input(f"\n {Wh}Enter Username : {Cy}")
        results = {}
        social_media = [
            {"url": "https://www.facebook.com/{}", "name": "Facebook"},
            {"url": "https://www.twitter.com/{}", "name": "Twitter"},
            {"url": "https://www.instagram.com/{}", "name": "Instagram"},
            {"url": "https://www.linkedin.com/in/{}", "name": "LinkedIn"},
            {"url": "https://www.github.com/{}", "name": "GitHub"},
            {"url": "https://www.pinterest.com/{}", "name": "Pinterest"},
            {"url": "https://www.tumblr.com/{}", "name": "Tumblr"},
            {"url": "https://www.youtube.com/{}", "name": "Youtube"},
            {"url": "https://soundcloud.com/{}", "name": "SoundCloud"},
            {"url": "https://www.snapchat.com/add/{}", "name": "Snapchat"},
            {"url": "https://www.tiktok.com/@{}", "name": "TikTok"},
            {"url": "https://www.behance.net/{}", "name": "Behance"},
            {"url": "https://www.medium.com/@{}", "name": "Medium"},
            {"url": "https://www.quora.com/profile/{}", "name": "Quora"},
            {"url": "https://www.flickr.com/people/{}", "name": "Flickr"},
            {"url": "https://www.twitch.tv/{}", "name": "Twitch"},
        ]
        for media in social_media:
            url = media["url"].format(username)
            response = requests.get(url)
            if response.status_code == 200:
                results[media["name"]] = url
            else:
                results[media["name"]] = "Not found"
        output = f"{Wh}Username Results:\n"
        for key, value in results.items():
            output += f"{Cy}{key} : {Wh}{value}\n"
        print(box_text(output))
    except Exception as e:
        print(f"{Re}Error occurred: {e}")
    input(f"{Wh}Press Enter to return to the main menu...")


def get_my_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        ip_data = response.json()
        ip = ip_data['ip']
        print(box_text(f"Your Public IP Address: {ip}"))
    except Exception as e:
        print(f"{Re}Error occurred: {e}")
    input(f"{Wh}Press Enter to return to the main menu...")


options = [
    {"num": 1, "text": "IP Tracker", "func": IP_Track},
    {"num": 2, "text": "Phone Number Tracker", "func": phoneGW},
    {"num": 3, "text": "Username Tracker", "func": TrackLu},
    {"num": 4, "text": "Get My IP", "func": get_my_ip},
    {"num": 5, "text": "Exit", "func": exit},
]

if __name__ == "__main__":
    main_menu()
