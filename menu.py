class Menu:
    def __init__(self):
        self.items_box = dict()
        self.items_box[1] = 'Показать клиентов сети'
        self.items_box[2] = 'Изменить список сайтов для переадресации'
        self.items_box[3] = 'Добавить сайт в список'
        self.items_box[4] = 'Удалить сайт из списка'
        self.items_box[5] = 'Очистить список'
        self.items_box[0] = 'Завершить работу'

        self.current_items = []

    def clear_current_items(self):
        self.current_items.clear()

    def set_items(self, items):
        self.current_items = items

    def show(self):
        print('')
        print('Возможные действия:')
        for item in self.current_items:
            print('{}. {}'.format(item, self.items_box[item]))
        print('Выберите пункт нужный пункт меню:  ')

    def get_choose(self, item):
        try:
            item = int(item)
        except Exception:
            raise TypeError
        if item not in self.items_box.keys():
            raise ValueError
        return item


