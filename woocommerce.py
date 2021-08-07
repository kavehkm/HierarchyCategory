class Category(object):
    """WooCommerce Category Model"""
    def __init__(self, categories):
        self._current_id = 0
        self._categories = categories

    def get(self, cid):
        for category in self._categories:
            if cid == category['id']:
                return category

    def all(self):
        return self._categories

    def create(self, name, parent):
        self._current_id += 1
        new_cat = {
            'id': self._current_id,
            'name': name,
            'parent': parent
        }
        self._categories.append(new_cat)
        return new_cat

    def delete(self, cid):
        index = None
        for i in range(len(self._categories)):
            if self._categories[i]['id'] == cid:
                index = i
        if index is not None:
            del self._categories[index]
            for category in self._categories:
                if cid == category['parent']:
                    category['parent'] = None
        else:
            raise Exception('cid not found')
