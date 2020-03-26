url = 'https://cdn.pravda.com/cdn/covid-19/ukraine.json'
ssid = ''
password = ''
confirmed = confirmed_by_last_day = recovered = recovered_by_last_day = deaths = deaths_by_last_day = 0
updated = ''

display = tim = None


def init():
    from machine import I2C, Pin, Timer
    import ssd1306

    global display, tim
    i2c = I2C(-1, Pin(5), Pin(4))
    display = ssd1306.SSD1306_I2C(128, 32, i2c)
    display.fill(0)
    display.show()

    tim = Timer(-1)

    do_connect()


def do_connect():
    import network
    global ssid, password
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())


def parse_data(json):
    global confirmed, confirmed_by_last_day, recovered, recovered_by_last_day, deaths, deaths_by_last_day, updated
    confirmed = json['confirmed'][-1]
    confirmed_by_last_day = json['confirmed'][-1] - json['confirmed'][-2]

    recovered = json['recovered'][-1]
    recovered_by_last_day = json['recovered'][-1] - json['recovered'][-2]

    deaths = json['deaths'][-1]
    deaths_by_last_day = json['deaths'][-1] - json['deaths'][-2]

    updated = json['display_updated']


def get_data():
    import urequests
    resp = urequests.get(url)
    if resp.status_code is 200:
        parse_data(resp.json())


def display_results():
    global confirmed, confirmed_by_last_day, recovered, recovered_by_last_day, deaths, deaths_by_last_day, updated
    display.fill(0)
    display.text(updated, 1, 1, 1)

    display.text('A' + str(confirmed), 1, 10, 1)
    display.text('+' + str(confirmed_by_last_day), 1, 20, 1)

    display.text('R' + str(recovered), 50, 10, 1)
    display.text('+' + str(recovered_by_last_day), 50, 20, 1)

    display.text('D' + str(deaths), 90, 10, 1)
    display.text('+' + str(deaths_by_last_day), 90, 20, 1)

    display.show()


def grab_data():
    get_data()
    display_results()
    print('update function called')


def start():
    from machine import Timer
    global tim

    grab_data()

    tim.init(period=60000, mode=Timer.PERIODIC, callback=lambda f: grab_data())
