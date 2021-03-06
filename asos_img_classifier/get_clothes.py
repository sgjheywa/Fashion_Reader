####4 get_clothes.py
#import reader
import random
import pandas as pd
import reader

headers = {
        'authority': '',
        'method': 'GET',
        'path': '',
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
}

training_folder = 'training_data/'

asos_reader = reader.AsosReader(headers, 'asos', training_folder)
asos_reader.set_authority('www.asos.com')

clothing_types = {'hoodies':"https://www.asos.com/men/hoodies-sweatshirts/cat/?cid=5668&nlid=mw|clothing|shop+by+product",
                 'shorts':"https://www.asos.com/men/shorts/cat/?cid=7078&nlid=mw|clothing|shop+by+product"}

print("reading asos data from website")
hoodies_urls = asos_reader.get_sub_urls(clothing_types['hoodies'])
shorts_urls = asos_reader.get_sub_urls(clothing_types['shorts'])
print("finished")

samp = 100
hoodies_subset = random.sample(hoodies_urls,samp)
shorts_subset = random.sample(shorts_urls,samp)

print("building individual items")
h_clothes = asos_reader.get_items(hoodies_subset, label='hoodies')
s_clothes = asos_reader.get_items(shorts_subset, label='shorts')
clothes = h_clothes +s_clothes
print("finished")

random.shuffle(clothes)

labels = []
for obj in clothes:
    labels.append(obj.get_info())

#print(labels[0:5])

df = pd.DataFrame(labels, columns=['title', 'id', 'fname', 'label'])
df = df.drop(columns=['title'])
df.to_csv(training_folder + 'labels.csv',index=False)
