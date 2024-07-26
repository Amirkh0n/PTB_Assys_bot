
def list_page(list, page_number):
    return [list[i:i+page_number] for i in range(0, len(list), page_number)]
