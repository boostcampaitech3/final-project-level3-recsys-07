from tokenize import String
import streamlit as st
import numpy as np
import pandas as pd

ITEM_PATH = "/opt/ml/input/data/raw_codishop/item.xlsx"
ITEM_DATA = pd.read_excel(ITEM_PATH,engine='openpyxl')

def paginator(label, items, items_per_page=10, on_sidebar=True):
    """Lets the user paginate a set of items.
    Parameters
    ----------
    label : str
        The label to display over the pagination widget.
    items : Iterator[Any]
        The items to display in the paginator.
    items_per_page: int
        The number of items to display per page.
    on_sidebar: bool
        Whether to display the paginator widget on the sidebar.
        
    Returns
    -------
    Iterator[Tuple[int, Any]]
        An iterator over *only the items on that page*, including
        the item's index.
    Example
    -------
    This shows how to display a few pages of fruit.
    >>> fruit_list = [
    ...     'Kiwifruit', 'Honeydew', 'Cherry', 'Honeyberry', 'Pear',
    ...     'Apple', 'Nectarine', 'Soursop', 'Pineapple', 'Satsuma',
    ...     'Fig', 'Huckleberry', 'Coconut', 'Plantain', 'Jujube',
    ...     'Guava', 'Clementine', 'Grap    e', 'Tayberry', 'Salak',
    ...     'Raspberry', 'Loquat', 'Nance', 'Peach', 'Akee'
    ... ]
    ...
    ... for i, fruit in paginator("Select a fruit page", fruit_list):
    ...     st.write('%s. **%s**' % (i, fruit))
    """

    # Figure out where to display the paginator
    if on_sidebar:
        location = st.sidebar.empty()
    else:
        location = st.empty()

    # Display a pagination selectbox in the specified location.
    items = list(items)
    n_pages = len(items)
    n_pages = (len(items) - 1) // items_per_page + 1
    page_format_func = lambda i: "Page %s" % (i+1)
    page_number = location.selectbox(label, range(n_pages), format_func=page_format_func)

    # Iterate over the items in the page to let the user display them.
    min_index = page_number * items_per_page
    max_index = min_index + items_per_page
    import itertools
    return itertools.islice(enumerate(items), min_index, max_index)

def demonstrate_paginator():
    fruit_list = [
        'Kiwifruit', 'Honeydew', 'Cherry', 'Honeyberry', 'Pear',
        'Apple', 'Nectarine', 'Soursop', 'Pineapple', 'Satsuma',
        'Fig', 'Huckleberry', 'Coconut', 'Plantain', 'Jujube',
        'Guava', 'Clementine', 'Grape', 'Tayberry', 'Salak',
        'Raspberry', 'Loquat', 'Nance', 'Peach', 'Akee'
    ]
    for i, fruit in paginator("Select a fruit page", fruit_list):
        st.write('%s. **%s**' % (i, fruit))


if __name__ == '__main__':
    demonstrate_paginator()

def get_images_url(item_ids: list) -> dict:
    image_dict = dict()
    
    for id in item_ids:
        image_dict[id] = ITEM_DATA[ITEM_DATA['id'] == id]['img_url'].unique().tolist()[0]
    
    return image_dict

def get_clothes_name(item_id: int) -> str:
    name = ITEM_DATA[ITEM_DATA['id'] == item_id]['name'].values[0]
    return name

def get_codi(item_ids:list):
    codi_data=ITEM_DATA.groupby('codi_id')['id'].apply(list)

    codi_ids=list()
    for i in range(len(codi_data)):
        if item_ids in codi_data.iloc[i]:
            codi_ids.append(codi_data.index[i])
    return codi_ids

def get_codi_images_url(codi_ids:list):
    codi_dict=dict()

    for id in codi_ids:
        codi_dict[id]=ITEM_DATA[ITEM_DATA['codi_id'] == id]['img_url'].unique().tolist()[0]

    return codi_dict
    