import matplotlib.pyplot as plt
import os
import json
import re

current_path = os.path.abspath(__file__)
path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + "..")


def load_json():
    """
    加载数据
    """
    with open(path+'\\spider_allpage\\jd_list.json', 'r', encoding='utf-8') as f:
        js_data = json.load(f)
    # 计算种类,数量
    dict_category = {}
    for item in js_data:
        if item['comm_name'] not in dict_category:
            dict_category[item['comm_name']] = 1
        dict_category[item['comm_name']] += 1

    # 简化数据
    new_dict = {}
    for key, value in dict_category.items():
        res = re.match(r'\S+', key).group()
        if res not in new_dict:
            new_dict[res] = value
        new_dict[res] = new_dict[res] + value

    # 更好的匹配
    end_dict = {'协德': 0}
    for key, value in new_dict.items():
        res = re.search(r"\u91d1\u58eb\u987f|\u5341\u94e8|\u534f\u5fb7|\u4e09\u661f|\u91d1\u767e\u8fbe|\u5a01\u521a|\u82f1\u777f\u8fbe", key).group()
        if res not in new_dict:
            end_dict[res] = value
        end_dict[res] = end_dict[res] + value

    return end_dict


def image_pie(dict_goods):
    """
    画饼状图
    :return:
    """
    goods_name = [i for i in dict_goods.keys()]
    print(goods_name)
    goods_value = [j for j in dict_goods.values()]
    print(goods_value)
    explode = (0, 0, 0.05, 0, 0, 0, 0)
    plt.figure(figsize=(20, 8), dpi=100)
    plt.pie(goods_value, explode=explode, labels=goods_name, autopct="%1.2f%%")

    plt.legend()
    plt.title('内存条排行占比')
    plt.show()


if __name__ == '__main__':
    dict_goods = load_json()
    image_pie(dict_goods)

