class ClientStation:
    """Клиент точки доступа. Атрибуты:
        - MAC
        - curent_ip
        - info(результат работы nmap)
        - trusted_essids
        - nick"""

    def __init__(self, mac):
        self.mac = mac
        self.last_ip = ''
        self.nick = ''
        self.info = dict()
        self.trasted_essid = []

    def __str__(self):
        """Возвращает строку: MAC:current_ip:nick"""
        return 'mac:{}, ip:{}, nick:{}'.format(self.mac, self.ip, self.nick)

    def set_signal(self, signal):
        self.info['signal'] = signal

    def set_ip(self, ip):
        self.last_ip = ip

    def set_nick(self, nick):
        self.nick = nick

    def add_trasted_essid(self, essid):
        self.trasted_essid.append(essid)

    def get_full_info(self):
        info = ' mac:{}, ip:{}, nick:{}\n' \
               '\tдоверенные сети: {}\n' \
               '\tдополнительная информация: ' \
               '{}'.format(self.mac, self.last_ip, self.nick, self.trasted_essid, self.info)
        return info
