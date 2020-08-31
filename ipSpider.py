import requests
from bs4 import BeautifulSoup

class ipSpider:
    base_url = 'https://www.7yip.cn/free/?action=china&page='

    def get_url(self,page):
        self.base_url = self.base_url+str(page)
        response = requests.get(self.base_url)
        soup = BeautifulSoup(response.text,'lxml')
        return soup

    def get_ips(self):
        ips = []
        for i in range(1,6):
            soup = self.get_url(i)
            ip_s = soup.find_all('tr')
            for ip in ip_s[1:]:
                ip_temp = ip.find_all('td')
                if ip_temp[3].text == 'HTTP':
                    ips.append({'http': ip_temp[0].text + ':' + ip_temp[1].text})
        return ips

if __name__ == '__main__':
    ips = ipSpider()
    ips_s = ips.get_ips()
    for ip in ips_s:
        print(ip)
