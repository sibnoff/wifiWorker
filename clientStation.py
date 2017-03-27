class ClientStation:
    """Клиент точки доступа. Атрибуты:
        - MAC
        - curent_ip
        - info(результат работы nmap)
        - trusted_essids
        - nick"""
    def __init__(self):
        raise NotImplementedError

    def __str__(self):
        """Возвращает строку: MAC:current_ip"""
        raise NotImplementedError
