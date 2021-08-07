# internal
import data
import db
import woocommerce


def get_name(category, categories):
    if not category['parent']:
        return category['name']
    parent = None
    for cat in categories:
        if cat['id'] == category['parent']:
            parent = cat
    return get_name(parent, categories) + '--->' + category['name'] if parent else ''


def imp(categories):
    # sort categories by parent id
    sorted_categories = sorted(categories, key=lambda category: category['parent'] or 0)
    # create connection
    conn = db.connection()
    # keep track
    m = dict()
    for category in sorted_categories:
        parent_id = m.get(category['parent'])
        category_id = db.add_category(conn, category['name'], parent_id)
        m[category['id']] = category_id
    # commit changes
    conn.commit()
    conn.close()


def export():
    # create woocommerce category instance
    wc_cat = woocommerce.Category([])
    # create connection
    conn = db.connection()
    # keep track
    m = dict()
    # get all categories from Categories table
    categories = db.all_categories(conn)
    for category in categories:
        parent_id = m.get(category[2])
        wc_category = wc_cat.create(category[1], parent_id)
        m[category[0]] = wc_category['id']
    # check woocommerce categories
    return wc_cat.all()


if __name__ == '__main__':
    # remove old database
    db.remove_old_db()
    # get hierarchy categories name
    for category in data.CATEGORIES:
        print(get_name(category, data.CATEGORIES))
    print(''.ljust(50, '='))
    # import
    imp(data.CATEGORIES)
    # export
    wc_categories = export()
    for category in wc_categories:
        print(get_name(category, wc_categories))
