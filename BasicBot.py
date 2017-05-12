import requests

from Util import *


class BasicBot:

    def __init__(self):
        print("[+] Colonel Mustard, reporting for duty")
        self.session = requests.session()
        self.session.headers.update({"User-Agent": "Colonel Mustard"})
        self.logged_in = False
        self.state = {}
        self.neighbors = []

        try:
            with open(".env.json", 'r') as f:
                env = json.load(f)
                self.NAME = env["NAME"]
                self.PASSWORD = env["PASSWORD"]
                self.WORLD = env["WORLD"]
                self.DEBUG = env["DEBUG"]
        except FileNotFoundError:
            print("[-] .env.json file not found in current directory.")
            raise
        except KeyError as e:
            print("[-] Missing data in .env.json.")
            raise

        self.MAP_OVERVIEW_URL = "https://us" + self.WORLD + ".tribalwars.us/game.php?village=10126&screen=map"
        self.PLAY_WORLD_URL = ROOT_URL + "/page/play/us" + self.WORLD

    def _do_saved_login(self):
        with open(".saved_cookie.json", 'r') as f:
            saved_session = json.load(f)

        necessary_cookies = ["us_auth", "cid", "ref", "PHPSESSID", "remember_output"]

        for cookie_name in saved_session:
            if cookie_name in necessary_cookies:
                self.session.cookies.set(cookie_name, saved_session[cookie_name])

        resp = request_get_wrapper(self.session, self.PLAY_WORLD_URL, debug=self.DEBUG)

        if EXPECTED_PLAY_PAGE in resp.url:
            print("[+] Soft login (session restore) successful")
        else:
            raise LoginError(resp)

    def do_login(self):
        try:
            self._do_saved_login()
        except LoginError:
            print("[-] Soft login failed; attempting hard login")

            request_get_wrapper(self.session, ROOT_URL, debug=self.DEBUG)

            login_post_data = {
                "username": self.NAME,
                "password": self.PASSWORD,
                "remember": "1",
            }

            custom_headers = {"X-Requested-With": "XMLHTTPRequest"}
            request_post_wrapper(
                self.session,
                LOGIN_URL,
                data=login_post_data,
                headers=custom_headers,
            )

            resp = request_get_wrapper(self.session, self.PLAY_WORLD_URL, debug=self.DEBUG)

            if EXPECTED_PLAY_PAGE in resp.url and resp.status_code == 200:
                print("[+] Hard login successful.")
                self.logged_in = True

                with open(".saved_cookie.json", 'w') as f:  # Save auth cookie in file
                    json.dump(self.session.cookies.get_dict(), f)
            else:
                print("[-] Hard login failed")
                raise LoginError(resp)

    def update_state(self):
        print("[*] Fetching village status...")

        resp = request_get_wrapper(self.session, self.MAP_OVERVIEW_URL, debug=self.DEBUG)

        self.state = carveJSON(resp.text, VILLAGE_DATA_START, VILLAGE_DATA_END, VILLAGE_DATA_CHR_LIMIT)
        raw_map_data = carveJSON(resp.text, MAP_DATA_START, MAP_DATA_END, VILLAGE_DATA_CHR_LIMIT)
        self.neighbors = parseMap(raw_map_data)

        print("[+] Village state and neighbors updated")

    def attack_send(self, tgt_x, tgt_y, spears=0, swords=0, axes=0, scouts=0, lc=0, hc=0, rams=0, cats=0, paladin=0, nobles=0):
        # TODO
        pass

    def support_send(self, tgt_x, tgt_y, spears=0, swords=0, axes=0, scouts=0, lc=0, hc=0, rams=0, cats=0, paladin=0, nobles=0):
        # TODO
        pass

    def recruit(self, spears=0, swords=0, axes=0, scouts=0, lc=0, hc=0, rams=0, cats=0, paladin=0, nobles=0):
        # TODO
        pass

    def hq_build(self):
        # TODO
        pass

    def barracks_build(self):
        # TODO
        pass

    def stable_build(self):
        # TODO
        pass

    def smithy_build(self):
        # TODO
        pass

    def statue_build(self):
        # TODO
        pass

    def market_build(self):
        # TODO
        pass

    def _build_by_name(self):
        # TODO
        pass
