import csv
import pickle

import matplotlib.pyplot as plt
import networkx as nx
from pony.orm.core import select
from wordcloud import WordCloud

from model.db import db_session, Message, User

stopwords = set()


def get_reply_network():
    G = nx.DiGraph()

    current_user = [1, 2, 3, 4, 5]
    reply_user = []



    with db_session:
        all_users = list(select((user.tg_user_id, user.tg_user_username) for user in User))
        # G.add_nodes_from(all_users)

        net = []
        all_messages = list(select(msg.tg_update_full for msg in Message if msg.tg_msg_is_reply == 1))

        user_net = dict((user[0], (user[1], [])) for user in all_users)
        for msg in all_messages:
            msg = pickle.loads(msg)
            current_user = msg.message.from_user.id
            replied_user = msg.message.reply_to_message.from_user.id
            user_net[current_user][1].append(replied_user)

        user_net_id_first_20 = sorted(user_net, key=lambda x: len(user_net[x][1]), reverse=True)[:10]
        for id in user_net_id_first_20:
            for ru in user_net[id][1]:
                # G.add_node(user_net[id][0])
                if ru not in user_net_id_first_20:
                    continue
                try:
                    G.add_edge(user_net[id][0], user_net[ru][0])
                except KeyError:
                    pass

        d = nx.degree(G)
        # nx.write_gexf(G, 'test.gexf')
        # nx.draw(G, with_labels=True, node_size=[v * 100 for v in d.values()])
        nx.draw(G, with_labels=True)
        # nx.draw_networkx_edge_labels(G, with_labels=True)
        plt.show()
            # print(msg)

    with open('cut_result.csv', 'w') as cf:
        writer = csv.DictWriter(cf, ["word", "count"])
        writer.writeheader()
        for w in sorted(words, key=words.get, reverse=True):
            writer.writerow({"word": w, "count": words[w]})

    wd = {}

    with open("cut_result.csv") as f:
        reader = csv.DictReader(f)
        for i in reader:
            wd[i["word"]] = int(i["count"])

    wordcloud = WordCloud(width=1024, height=1024, font_path="/Library/Fonts/SourceHanSans-Normal.ttc",
                          color_func=lambda *args, **kwargs: (140, 184, 255)).generate_from_frequencies(wd)

    image = wordcloud.to_image()
    image.show()
