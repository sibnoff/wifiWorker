import subprocess

ER = open('log_error.txt', 'w')


class Chains:
    preroute_chain = 'PREROUTING'
    postroute_chain = 'POSTROUTING'
    fwd_chain = 'FORWARD'
    input_chain = 'INPUT'
    output_chain = 'OUTPUT'


class Firewall:
    def __init__(self):
        pass

    @staticmethod
    def nat(internal_interface, external_interface):
        """Метод добаляет правила, необходимые для работы ТД"""
        subprocess.call(
            ('iptables -t nat -A POSTROUTING -o %s -j MASQUERADE'
             % (external_interface,)),
            shell=True)
        subprocess.call(
            ('iptables -A FORWARD -i %s -o %s -j ACCEPT'
             % (internal_interface, external_interface)),
            shell=True)

    @staticmethod
    def clear_rules():
        """Метод удаляет все правила из всех таблиц"""
        subprocess.call('iptables -F', shell=True)
        subprocess.call('iptables -X', shell=True)
        subprocess.call('iptables -t nat -F', shell=True)
        subprocess.call('iptables -t nat -X', shell=True)

    @staticmethod
    def redirect_port_to_port(dport, to_port):
        """метод перенаправляет трафик следующий
        на dport на localhost:to_port и
        возвращает индекс добавленного правила"""
        rule = 'iptables -t nat -A PREROUTING -p tcp --dport {} -j ' \
               'DNAT --to-destination ' \
               '127.0.0.1:{}'.format(dport, to_port)
        p = subprocess.Popen(["iptables", "-t", "nat", "-L", "PREROUTING", "--line-numbers"],
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=ER)
        out, err = p.communicate()
        cur_count_rules = len(out.decode(encoding='utf-8').split('\n')) - 2
        subprocess.call(rule, shell=True)
        return cur_count_rules

    @staticmethod
    def del_rule_prerouting(rule_index):
        """метод удаляет правило из таблицы nat цепочи PREROUTING
         по индексу, который возвращает метод redirect_port_to_port"""
        cmd = 'iptables -t nat -D PREROUTING {}'.format(rule_index)
        subprocess.call(cmd, shell=True)

    @staticmethod
    def del_rule_postrouting(rule_index):
        """метод удаляет правило из таблицы nat цепочи POSTROUTING
         по индексу"""
        cmd = 'iptables -t nat -D POSTROUTING {}'.format(rule_index)
        subprocess.call(cmd, shell=True)

    def on_exit(self):
        self.clear_rules()

#добавляем последовательно 3 правила и удаляем их по
# индексам, но обязательно в тойже последовательности
# one = Firewall.redirect_port_to_port(666, 777)
# two = Firewall.redirect_port_to_port(665, 776)
# three = Firewall.redirect_port_to_port(664, 775)
# Firewall.del_rule_prerouting(three)
# Firewall.del_rule_prerouting(two)
#Firewall.del_rule_prerouting(one)
