"""
    This program is generated to plot word cloud from a text fime of whatsapp chats. 
    Export the chats to text and put the file to the same dir as the file and name it
    appropriately
    """

from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd

# reads whatsapp test file
with open(r"/home/siro/Downloads/ACR.txt", encoding="latin-1") as f:
    text = f.readlines()

comment_words = []
names = []
stopwords = set(STOPWORDS)

for val in text:
    tokens = []
    # Create token by splitting on the -. This separates date and name/message
    date, *name_message = val.split(' - ')
    comment_words.extend(name_message)

t = []
for w in comment_words:
    name, *message = w.split(':')  # separates sender and message
    names.append(name)
    t.extend(message)

post_words = " ".join(
    w for w in " ".join(t).split() if w.isalpha()
)

plot_words = post_words
# plot_words = " ".join(names)
wordcloud = WordCloud(width=800, height=800,
                      background_color='white',
                      stopwords=stopwords,
                      min_font_size=10).generate(plot_words)

# plot the WordCloud image
plt.figure(figsize=(8, 8), facecolor=None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad=0)

plt.show()
