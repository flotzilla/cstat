# CStat
COVID-19 statistics tracker project using NodeMCU and microPython

NodeMCU COVID-19 tracker, written in python (microPython). Data came from rapidapi.com (required auth)
 
![photo_2020-03-30_22-23-34](https://user-images.githubusercontent.com/3332506/77953041-4d60a000-72d5-11ea-94ad-0fafef8a7a6e.jpg)

## Requirements
* NodeMCU or esp8266 or esp32
* 0.91` SSD1306 OLED display or any display from SSD1306 family with minimal resolution 128*32

## Assembly
* connect display to microcontroller
    * for esp8266: SDA -> D2 (GPIO 4), SCK -> D1 (GPIO 5)
    * for esp32: SDA -> D2 (GPIO 21), SCK -> D1 (GPIO 22)

## Install
* update esp bootloader to microPython, you can get it from [here](http://micropython.org/download#esp8266). For esp32 see different bootloader image.
* upload .bin file with esptool
`esptool.py --chip esp8266 --port /dev/ttyUSB0 --baud 460800 erase_flash`
`esptool.py --chip esp8266 --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect -fm dio 0 esp8266-20191220-v1.12.bin`
* update `ssid` and `password` in `cstat.py` to your network settings
* Obtain api key from [rapidapi.com](https://rapidapi.com/KishCom/api/covid-19-coronavirus-statistics) and update `x_rapidapi_key` in `cstat.py`
* update password for webrepl access in `webrepl_cfg.py`
* driver for SSD1306 OLED was found [here](https://github.com/micropython/micropython/blob/master/drivers/display/ssd1306.py). If you want to use latest version, please, update local ssd1306.py file
* upload all files with `http://micropython.org/webrepl/` or console utils, like `ampy --port /dev/ttyUSB0 put <filename>`

# Display stats
* first line - date of last update from ministry of health
* second line 
    * A - active cases total
    * R - recovered total
    * D - deaths - total deaths 

# About
Statistics will update once in a hour from this url `https://covid-19-coronavirus-statistics.p.rapidapi.com/v1/stats?country=Ukraine`
You can modify to your country stats, just change country value in URL

More info about api [here](https://rapidapi.com/KishCom/api/covid-19-coronavirus-statistics) 
