from machine import I2C, Pin, Timer
import ssd1306
import network
import urequests


class CStat:
    def __init__(self):
        self.url = 'https://cdn.pravda.com/cdn/covid-19/ukraine.json'
        self.ssid = ''
        self.password = ''

        self.confirmed = self.confirmed_by_last_day = 0
        self.recovered = self.recovered_by_last_day = 0
        self.deaths = self.deaths_by_last_day = 0

        self.updated = ''

        self.display = self.tim = None

        i2c = I2C(-1, Pin(5), Pin(4))
        self.display = ssd1306.SSD1306_I2C(128, 32, i2c)
        self.display.fill(0)
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

    def parse_data(self, json):
        self.confirmed = json['confirmed'][-1]
        self.confirmed_by_last_day = json['confirmed'][-1] - json['confirmed'][-2]

        self.recovered = json['recovered'][-1]
        self.recovered_by_last_day = json['recovered'][-1] - json['recovered'][-2]

        self.deaths = json['deaths'][-1]
        self.deaths_by_last_day = json['deaths'][-1] - json['deaths'][-2]

        self.updated = json['display_updated']

    def get_data(self):
        resp = urequests.get(self.url)
        if resp.status_code is 200:
            self.parse_data(resp.json())

    def display_results(self):
        self.display.fill(0)
        self.display.text(self.updated, 1, 1, 1)

        self.display.text('A' + str(self.confirmed), 1, 10, 1)
        self.display.text('+' + str(self.confirmed_by_last_day), 1, 20, 1)

        self.display.text('R' + str(self.recovered), 50, 10, 1)
        self.display.text('+' + str(self.recovered_by_last_day), 50, 20, 1)

        self.display.text('D' + str(self.deaths), 90, 10, 1)
        self.display.text('+' + str(self.deaths_by_last_day), 90, 20, 1)

        self.display.show()

    def grab_data(self):
        self.get_data()
        self.display_results()
        print('update function called')

    def start(self):
        self.grab_data()
        self.tim.init(period=60000, mode=Timer.PERIODIC, callback=lambda f: self.grab_data())
