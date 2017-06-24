PROJECT_DIR = '/home/intercepter/PycharmProjects/wifiWorker/adminka/'

CONFIGS_DIR_NAME = PROJECT_DIR + 'configs/'
LOGS_DIR_NAME = PROJECT_DIR + 'logs/'
CHANNEL = 6
PUBLIC_DNS = "8.8.8.8"
NETWORK_IP = "192.168.74.0"
NETWORK_MASK = "255.255.255.0"
NETWORK_GW_IP = "192.168.74.1"

DHCP_LEASE = "192.168.74.2,192.168.74.100,12h"

WIFI_BROADCAST = "ff:ff:ff:ff:ff:ff"
WIFI_INVALID = "00:00:00:00:00:00"

DB_NAME = 'wifiWorker'

LINES_OUTPUT = 3
DN = open(LOGS_DIR_NAME + 'log_output.txt', 'w')
ER = open(LOGS_DIR_NAME + 'log_error.txt', 'w')
