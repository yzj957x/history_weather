# 这是一个示例 Python 脚本。
# import csv
import csv

import requests
from bs4 import BeautifulSoup


# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。

def get_url():
    print("开始生成链接")
    todo_urls = []
    area = 70669
    year = 2022
    # year = time.get_clock_info()
    for month in range(1, 12):
        todo_urls.append("http://tianqi.2345.com/Pc/GetHistory?areaInfo%5BareaId%5D=" + str(
            area) + "&areaInfo%5BareaType%5D=2&date%5Byear%5D=" + str(year) + "&date%5Bmonth%5D=" + str(
            month))
        print("生成链接")
    return todo_urls


def save_data(urls):
    print("开始访问")
    htmls = []
    header = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, sdch",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.235"
    }
    for url in urls:
        r = requests.get(url, headers=header)
        if r.status_code != 200:
            raise Exception("NO!!!")
        htmls.append(r.text.encode('utf-8').decode('unicode_escape').replace('\\/', "/")[27:-2:])
    print("访问完成")
    return htmls


def read_data(htmls):
    print("开始解读")
    all_datas = []
    for html in htmls:
        bs = BeautifulSoup(html, "html.parser")
        all_datas.append(bs)
    print("解读完成")
    return all_datas


def save_file(final):
    print("开始生成文件")
    file_name = "pinglu_weather.csv"
    with open(file_name, "w", errors="ignore", newline="") as f:
        f_csv = csv.writer(f)
        f_csv.writerows(final)
    f.close()
    print("保存成功")


def get_data(all_datas):
    final = []
    print("正在分析数据…………")
    title = all_datas[0].select('th')

    t = []
    for i in title:
        t.append(i.string)
    final.append(t)
    for soup in all_datas:

        id_a = soup.find_all('td')
        td = []
        for i in id_a:
            td.append(i.string)

        date = td[0::6]
        high_Temp = td[1::6]
        low_Temp = td[2::6]
        weather = td[3::6]
        wind = td[4::6]
        air = td[5::6]

        for i in range(0, len(date)):
            temp = [date[i], high_Temp[i], low_Temp[i], weather[i], wind[i], air[i]]
            final.append(temp)
    print("分析完成")
    return final


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    print("开始运行")
    save_file(
        get_data(
            read_data(
                save_data(
                    get_url()
                )
            )
        )
    )
