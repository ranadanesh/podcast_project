from pprint import pprint

import xmltodict
import requests
from podcast.models import Episode, Rss

episode_key_dict = {
    'guid': 'guid',
    'enclosure': 'enclosure',
    'title': 'title',
    'duration': 'itunes:duration',
    'description': 'description',
    'publish_date': 'pubDate',
    'explicit': 'itunes:explicit',
    'summary': 'itunes:summary',
    'keyword': 'itunes:keywords',
    'image': 'itunes:image',
}

rss_key_dict = {
    'link': 'link',
    'title': 'title',
    'owner': 'generator',
    'summary': 'itunes:summary',
    'image': 'image',
    'copyright': 'copyright',
    'explicit': 'itunes:explicit',
    'language': 'language',

}


def parserview(url):
    url = requests.get(url)
    xml_content = xmltodict.parse(url.content, encoding='utf-8')

    rss_content = xml_content.get('rss')

    rss_dict = {}

    channel_content = rss_content.get('channel')

    channel_keys = channel_content.keys()
    # print(channel_keys)

    for k, v in rss_key_dict.items():
        rss_dict[k] = channel_content[v]

    rss = Rss.objects.create(**rss_dict)

    episode_dict = {}
    episode_list = []

    item_content = channel_content.get('item')
    for item in item_content:
        # print(item)

        for k, v in episode_key_dict.items():
            episode_dict[k] = item[v]

        episode = Episode(**episode_dict)
        episode_list.append(episode)

    Episode.objects.bulk_create(episode_list, ignore_conflicts=True)
