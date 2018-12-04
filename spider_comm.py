import requests
from lxml import etree
from bs4 import BeautifulSoup


class SpiderJD:
    """
    爬取京东商品信息
    """
    def __init__(self):
        self.base_url = 'https://search.jd.com/Search?keyword=%E7%AC%94%E8%AE%B0%E6%9C%AC%E5%86%85%E5%AD%98%E6%9D%A1&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E7%AC%94%E8%AE%B0%E6%9C%AC%E5%86%85%E5%AD%98%E6%9D%A1&page=1&s=1&click=0'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Referer': 'https://search.jd.com/Search?keyword=%E7%AC%94%E8%AE%B0%E6%9C%AC%E5%86%85%E5%AD%98%E6%9D%A1&enc=utf-8&wq=%E7%AC%94%E8%AE%B0%E6%9C%AC%E5%86%85%E5%AD%98%E6%9D%A1&pvid=a31e221f599440868f39b9794da8d579'
        }
        self.goods = []
        self.remaining = 'https://search.jd.com/s_new.php?keyword=笔记本内存条&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&psort=3&page=3&s=27&scrolling=y&log_id=1543829593.84658&tpl=1_M'

    def send_request(self):
        response = requests.get(self.base_url, self.headers)
        data = response.content.decode('utf-8')
        return data

    def save_file(self, data):
        with open('jd.html', 'w', encoding='utf-8') as f:
            f.write(data)

    def get_detailed(self, data):
        """
        得到详细数据
        :return:
        """
        html = etree.HTML(data)
        res_list = html.xpath('//*[@id="J_goodsList"]/ul')
        for res in res_list:
            result = etree.tostring(res).decode('utf-8')
            print('====================================')
        # 保存前30个商品信息
        soup = BeautifulSoup(result)
        li_list = soup.find_all('li')
        for comm in li_list:
            comm_id = comm['data-sku']
            comm_name = comm.find('div', class_='p-name p-name-type-2').a.em.get_text()
            comm_price = '￥' + comm.find('div', class_='p-price').i.get_text()
            comm_img = comm.a.img['source-data-lazy-img']
            comm_intro = comm.find('div', class_='p-name p-name-type-2').a['title']

            temp = {
                'comm_id': comm_id,
                'comm_name': comm_name,
                'comm_price': comm_price,
                'comm_img': comm_img,
                'comm_intro': comm_intro
            }
            self.goods.append(temp)

    def get_detailedlater(self):
        """
        保存后30个商品的信息
        :return:
        """
        response = requests.get(self.remaining, headers=self.headers)
        data = response.content.decode('utf-8')
        with open('jd02.html', 'w', encoding='utf-8') as f:
            f.write(data)
        # 保存后30个商品信息
        soup = BeautifulSoup(data)
        li_list = soup.find_all('li')
        for comm in li_list:
            comm_id = comm['data-sku']
            comm_name = comm.find('div', class_='p-name p-name-type-2').a.em.get_text()
            comm_price = '￥' + comm.find('div', class_='p-price').i.get_text()
            comm_img = comm.a.img['source-data-lazy-img']
            comm_intro = comm.find('div', class_='p-name p-name-type-2').a['title']

            temp = {
                'comm_id': comm_id,
                'comm_name': comm_name,
                'comm_price': comm_price,
                'comm_img': comm_img,
                'comm_intro': comm_intro
            }
            self.goods.append(temp)

    def run(self):
        data = self.send_request()
        self.get_detailed(data)
        self.save_file(data)
        self.get_detailedlater()
        print(self.goods)
        print('-------------------------------------')


if __name__ == '__main__':
    SpiderJD().run()
