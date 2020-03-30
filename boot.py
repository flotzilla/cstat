# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import uos, machine
#uos.dupterm(None, 1) # disable REPL on UART(0)
import gc
import webrepl
import cstat
webrepl.start()
gc.enable()
gc.collect()

try:
    c = cstat.CStat()
except Exception as e:
    print('Sorry, an error occurred during initialization')
    print(e)
else:
    c.start()