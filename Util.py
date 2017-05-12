import json

# URL Constants
ROOT_URL = "https://www.tribalwars.us"
LOGIN_URL = ROOT_URL + "/page/auth"

# Hack-API Constants
VILLAGE_DATA_START = "TribalWars.updateGameData("
VILLAGE_DATA_END = ")"
MAP_DATA_START = "TWMap.sectorPrefech ="
MAP_DATA_END = ";"
VILLAGE_DATA_CHR_LIMIT = 100000
EXPECTED_PLAY_PAGE = "/game.php"

# Proxies for burp-debugging
PROXIES = {
    "http" : "http://localhost:8080",
    "https" : "https://localhost:8080"
}
# Determine whether to send requests through proxies
DEBUG = True


def carveJSON(page_text, start_str, end_str, char_limit): # TODO: more robust data carving
    raw_data = ""
    start_idx = page_text.index(start_str) + len(start_str)
    outside_of_double_quotes = True

    for idx in range(start_idx, start_idx + char_limit):  # Hack-y, but works for now
        curr_chr = page_text[idx]

        if curr_chr == "\"":
            outside_of_double_quotes = not outside_of_double_quotes

        if outside_of_double_quotes:  # Be looking for end_str ending character when not within quoted text
            if curr_chr != end_str:
                raw_data += curr_chr
            else:
                break
        else:  # Blindly add data to raw_data object if within double-quoted string
            raw_data += curr_chr

    return json.loads(raw_data)


def parseMap(raw_map):
    """
    :param raw_map:
        * list of 20x20 sectors (1, 2, 3, ...)
            * sector top-left x coord (x)
            * sector top-left y coord (y)
            * data object (data)
                * sector top-left x coord (x)
                * sector top-left y coord (y)
                * villages object (villages)
                    * x coord (1, 2, 3, ...)
                        * y coord (1, 2, 3, ...)
                            * 0 : ???
                            * 1 : ???
                            * 2 : village name
                            * 3 : village pts.
                            * 4 : ???
                            * 5 : ???
                            * 6 : ???
                            * 7 : ???
    :return:
        * list of villages (1, 2, 3, ...)
            * village name
            * village pts.
            * x coord
            * y coord
    """

    ret = list()

    for sector in raw_map:
        for x_coord in sector['data']['villages']:
            for y_coord in sector['data']['villages'][x_coord]:
                curr_village = sector['data']['villages'][x_coord][y_coord]
                ret.append({
                    'name' : curr_village[2],
                    'points' : int(curr_village[3].replace('.', '')),
                    'x' : int(x_coord) + int(sector['x']),
                    'y' : int(y_coord) + int(sector['y'])
                })


    return ret

def request_post_wrapper(sess, url, debug=False, **kwargs):
    if debug:
        return sess.post(url, proxies=PROXIES, verify=False, **kwargs)
    else:
        return sess.post(url, kwargs)

def request_get_wrapper(sess, url, debug=False, **kwargs):
    if debug:
        return sess.get(url, proxies=PROXIES, verify=False, **kwargs)
    else:
        return sess.post(url, kwargs)

class LoginError(Exception):

    def __init__(self, final_response):
        self.final_response = final_response