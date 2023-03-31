import requests
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from bs4 import BeautifulSoup, GuessedAtParserWarning
import argparse
import re
import warnings


headers = {
    'authority': 'ruz.spbstu.ru',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
    'cache-control': 'max-age=0',
    'cp-extension-installed': 'Yes',
    'dnt': '1',
    'if-none-match': 'W/"4572-/gWM6lbAcF3C27JTQrrrDEjNqVU"',
    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Microsoft Edge";v="110"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63',
}

def my_plotter(ax, data1, data2, param_dict):
    """
    A helper function to make a graph.
    """
    out = ax.plot(data1, data2, **param_dict)
    return out

def parse_page(args):
    response = requests.get('https://ruz.spbstu.ru/faculty/122/groups', headers=headers)
    response.encoding = 'utf-8'
    str = response.text
    i = str.find(args.mode)
    grp = ""
    if(i!= -1):
        #print (i)
        while(str[i] != '{'):
            i-=1
        i+=6
        #print (i)
        while(str[i]!= ','):
            grp += str[i]
            i+=1
    #print(grp)
    params = {'date': args.date}
    response = requests.get('https://ruz.spbstu.ru/faculty/122/groups/'+grp, headers=headers, params=params)
    response.encoding = 'utf-8'
    '''
    f = open("page.html","w", encoding="utf-8")
    
    #print(response.text)
    f.write(response.text)
    
    f.close()
    '''
    soup = BeautifulSoup(response.text, 'html.parser')
    #warnings.filterwarnings('ignore', category=GuessedAtParserWarning)

    week = soup.findAll('span', string  = re.compile("неделя"))
    if(week):
        print(week[0].text)
    time = ""
    days = soup.findAll('li', attrs={"class":"schedule__day"})
    dct = {}
    for day in days:
        count = 0
        #print(args.date[8:10])
        if(day.findAll('div',string  = re.compile(args.date[8:10]), attrs={"class":"schedule__date"})):
            day_date = day.find('div',string  = re.compile(args.date[8:10]), attrs={"class":"schedule__date"})
            print("\t",day_date.text)
            lessons = day.findAll('li', attrs={"class":"lesson"})
            numb = 1
            for les in lessons:
                time = les.findAll('span', attrs={"class":"lesson__time"})
                print("Номер пары = ", numb)
                numb+=1
                print("\tВремя:", end="")
                for t in time:
                    print(t.text)
                subj = les.findAll('span')
                print("\tПредмет:",subj[5].text)
                typee =  les.find('div',  attrs={"class":"lesson__type"})
                print("\tТип пары: ", typee.text)
                teach = les.find('div', attrs={"class":"lesson__teachers"})
                print("\tПреподаватель:",teach.text)
                place = les.find('div', attrs={"class":"lesson__places"})
                print("\tМесто",place.text)
            #arr[i] = numb - 1
            #i+=1
            dct[day_date.text] = numb -1
            continue
        day_date = day.find('div', attrs={"class":"schedule__date"})
        lessons = day.findAll('li', attrs={"class":"lesson"})
        count = 0
        for les in lessons:
            count+=1

        dct[day_date.text] = count
        count = 0
    if(dct):
        fig, ax = plt.subplots()  # Create a figure containing a single axes.
        ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
        ax.set_xlabel('date')
        ax.set_ylabel('count')
        ax.set_ylim(0, max(list(dct.values())) + 1)
        my_plotter(ax, list(dct.keys()), list(dct.values()), {'marker': 'o'})
        plt.show()
def print_er():
    print("Error")
    exit()
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script for working with group \
        and teacher")
    parser.add_argument('-m', dest="mode", type=str, const=None, help="number group or name of teacher")
    parser.add_argument('-d', dest="date",  type=str, const=None, help = "date YYYY-MM-DD")
    args = parser.parse_args()
    if(args.mode != None and args.date != None):
        parse_page(args)
    else:
        print_er()
    


