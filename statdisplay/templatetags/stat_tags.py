from django import  template

register = template.Library()

@register.simple_tag
def pagination_list(page_length, current, delta=2):
    left = current - delta
    right = current + delta
    page_list = []
    for page_num in range(1, page_length+1):
        if (page_num >= left and page_num <= right) or page_num == 1 or page_num == page_length:
            page_list.append(page_num)
        elif page_num == left - 1 or page_num == right + 1:
            if page_num == 2 or page_num == page_length - 1:
                page_list.append(page_num)
            else:
                page_list.append(0)
    return page_list

@register.filter
def pagination_params(dictionary):
    params = ""
    for key in dictionary:
        if key != "page":
            params += "&" + key + "=" + dictionary[key]
    return params
