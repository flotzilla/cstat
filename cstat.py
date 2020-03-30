from machine import I2C, Pin, Timer
import ssd1306
import network
import urequests
import gc


class CStat:
    def __init__(self):
        self.url = 'https://covid-19-coronavirus-statistics.p.rapidapi.com/v1/stats?country=Ukraine'
        self.x_rapidapi_key = ''  # modify this line
        self.ssid = ''  # modify this line
        self.password = ''  # modify this line

        self.confirmed = 0
        self.recovered = 0
        self.deaths = 0
        self.updated = ''

        self.display = self.tim = None

        i2c = I2C(-1, Pin(5), Pin(4))
        self.display = ssd1306.SSD1306_I2C(128, 32, i2c)
        self.display.fill(0)
        self.display.text('Connecting...', 1, 1, 1)
        self.display.show()

        self.tim = Timer(-1)
        self.do_connect()

    def do_connect(self):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        if not wlan.isconnected():
            print('connecting to network...')
            wlan.connect(self.ssid, self.password)
            while not wlan.isconnected():
                pass
        print('network config:', wlan.ifconfig())

    def parse_country_data(self, json):
        self.confirmed = json['data']['covid19Stats'][0]['confirmed']
        self.recovered = json['data']['covid19Stats'][0]['recovered']
        self.deaths = json['data']['covid19Stats'][0]['deaths']
        self.updated = json['data']['covid19Stats'][0]['lastUpdate']

    def grab_api_data(self):
        headers = {
            'content-type': 'application/json',
            'x-rapidapi-host': 'covid-19-coronavirus-statistics.p.rapidapi.com',
            'x-rapidapi-key': self.x_rapidapi_key
        }
        resp = urequests.get(self.url, headers=headers)

        if resp.status_code is 200:
            self.parse_country_data(resp.json())
        else:
            print('Sorry, cannot connect')
            print(resp.status_code)
            print(resp.text)

    def display_results(self):
        self.display.fill(0)
        self.display.text(self.updated, 1, 1, 1)

        self.display.text('A' + str(self.confirmed), 1, 10, 1)
        self.display.text('R' + str(self.recovered), 50, 10, 1)
        self.display.text('D' + str(self.deaths), 90, 10, 1)

        self.display.show()

    def grab_data(self):
        try:
            print('update function called')
            self.grab_api_data()
            self.display_results()
            gc.collect()
        except Exception as e:
            print(e)

    def start(self):
        self.grab_data()
        self.tim.init(period=60000, mode=Timer.PERIODIC, callback=lambda f: self.grab_data())
