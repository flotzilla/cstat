# CStat
Трекер статистики COVID-19 по Украине по данным МОЗ на NodeMCU и microPython

![cover_image](https://user-images.githubusercontent.com/3332506/77623848-88677a00-6f49-11ea-9d0b-65767c19d6d7.jpg)

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
`esptool.py --chip esp8266 --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect -fm dio 0 esp8266-20191220-v1.12.bin`
* update `ssid` and `password` to your network settings
* update password for webrepl access in `webrepl_cfg.py`
* driver for SSD1306 OLED was found [here](https://github.com/micropython/micropython/blob/master/drivers/display/ssd1306.py). If you want to use latest version, please, update local ssd1306.py file
* upload all files with `http://micropython.org/webrepl/` or console utils, like `ampy --port /dev/ttyUSB0 put <filename>`

# Display stats
* first line - date of last update from ministry of health
* second line 
    * A - active cases total
    * R - recovered total
    * D - deaths - total deaths
* third line - addition for each column by last day 

# About
Statistics will update once in a hour from this url `https://cdn.pravda.com/cdn/covid-19/ukraine.json`, provided by ukrainian news site [Украинская правда](pravda.com.ua)

Also, you can modify to some different data source. Don't forget to update `parse_data` function afterwards.
