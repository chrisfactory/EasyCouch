import traceback

from datetime import datetime
from bs4 import BeautifulSoup
from couchpotato.core.helpers.encoding import toUnicode
from couchpotato.core.helpers.variable import tryInt
from couchpotato.core.logger import CPLog
from couchpotato.core.media._base.providers.torrent.base import TorrentProvider
import re

log = CPLog(__name__)


class Base(TorrentProvider):

    urls = {
        'login' : 'https://www.hdts.ru/login.php',
        'detail' : 'https://www.hdts.ru/details.php?id=%s',
        'search' : 'https://www.hdts.ru/torrents.php?search=%s&active=1',
        'home' : 'https://www.hdts.ru/%s',
    }

    http_time_between_calls = 1 #seconds

    def _search(self, media, quality, results):

        url = self.urls['search'] % (media['identifiers']['imdb'])#, cats[0])
        data = self.getHTMLData(url)
        
        if data:
          
          # Remove HDTorrents NEW list
          split_data = data.partition('<!-- Show New Torrents After Last Visit -->\n\n\n\n')
          data = split_data[2]

          html = BeautifulSoup(data)
          try:
              #Get first entry in table
              entries = html.find_all('td', attrs={'align' : 'center'})

              if len(entries) < 21:
                  return

              base = 21
              extend = 0

              try:
                  torrent_id = entries[base].find('div')['id']
              except:
                  extend = 2
                  torrent_id = entries[base + extend].find('div')['id']

              torrent_age = datetime.now() - datetime.strptime(entries[15 + extend].get_text()[:8] + ' ' + entries[15 + extend].get_text()[-10::], '%H:%M:%S %d/%m/%Y')
              
              results.append({
                              'id': torrent_id,
                              'name': entries[20 + extend].find('a')['title'].strip('History - ').replace('Blu-ray', 'bd50'),
                              'url': self.urls['home'] % entries[13 + extend].find('a')['href'],
                              'detail_url': self.urls['detail'] % torrent_id,
                              'size': self.parseSize(entries[16 + extend].get_text()),
                              'age': torrent_age.days,
                              'seeders': tryInt(entries[18 + extend].get_text()),
                              'leechers': tryInt(entries[19 + extend].get_text()),
                              'get_more_info': self.getMoreInfo,
              })

              #Now attempt to get any others
              result_table = html.find('table', attrs = {'class' : 'mainblockcontenttt'})

              if not result_table:
                  return

              entries = result_table.find_all('td', attrs={'align' : 'center', 'class' : 'listas'})

              if not entries:
                  return

              for result in entries:
                  block2 = result.find_parent('tr').find_next_sibling('tr')
                  if not block2:
                      continue
                  cells = block2.find_all('td')
                  try:
                      extend = 0
                      detail = cells[1 + extend].find('a')['href']
                  except:
                      extend = 1
                      detail = cells[1 + extend].find('a')['href']
                  torrent_id = detail.replace('details.php?id=', '')
                  torrent_age = datetime.now() - datetime.strptime(cells[5 + extend].get_text(), '%H:%M:%S %d/%m/%Y')

                  results.append({
                                  'id': torrent_id,
                                  'name': cells[1 + extend].find('b').get_text().strip('\t ').replace('Blu-ray', 'bd50'),
                                  'url': self.urls['home'] % cells[3 + extend].find('a')['href'],
                                  'detail_url': self.urls['home'] % cells[1 + extend].find('a')['href'],
                                  'size': self.parseSize(cells[6 + extend].get_text()),
                                  'age': torrent_age.days,
                                  'seeders': tryInt(cells[8 + extend].get_text()),
                                  'leechers': tryInt(cells[9 + extend].get_text()),
                                  'get_more_info': self.getMoreInfo,
                  })

          except:
              log.error('Failed getting results from %s: %s', (self.getName(), traceback.format_exc()))

    def getMoreInfo(self, item):
        full_description = self.getCache('hdtorrents.%s' % item['id'], item['detail_url'], cache_timeout = 25920000)
        html = BeautifulSoup(full_description)
        nfo_pre = html.find('div', attrs = {'id':'details_table'})
        description = toUnicode(nfo_pre.text) if nfo_pre else ''

        item['description'] = description
        return item

    def getLoginParams(self):
        return {
            'uid': self.conf('username'),
            'pwd': self.conf('password'),
            'Login': 'submit',
        }

    def loginSuccess(self, output):
        return "if your browser doesn\'t have javascript enabled" or 'logout.php' in output.lower()

    loginCheckSuccess = loginSuccess


config = [{
    'name': 'hdtorrents',
    'groups': [
        {
            'tab': 'searcher',
            'list': 'torrent_providers',
            'name': 'HDTorrents',
            'description': 'See <a href="https://hdts.ru">HDTorrents</a>',
            'wizard': True,
            'icon' : 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABfElEQVR4nM2SO47CMBCGx47zUhJeAiHRIp4NRSo6kCi4Aj0NBZwDUXMJLoI4AAVFCiQeBYIghMBxMPYWYVlg65X27zyebzz6fwP8O6HXg2VZpmlKKQFAfgshRCkNguATKBaL5XL5dDopisI555wHQSCEUFXVtm3P81ar1c9sRVEajQZCCGMMAAghAEgmk9lsFgAwxs1mM7oiEaCqqu/7uq4PBoPRaNTpdOLxuOu6lNLNZjMcDu/3OyEkDEP82AwhwzAwxplMxrZty7ISicRsNuv3+6lUynXd8/kcdb4BjLFarTYej9vt9uFw4JwDwHQ6TafTl8slMgO/uqTruud5vV5vMplIKY/HIwDkcrntdht1vwGMMSHEer2mlO73e9/38/l8t9tljM3nc03TngwAACGk1WohhGKxWPSUYRiFQqFUKkUL1+v1h4FPplKpVKvV3W5HCLndblLKMAwBQNM0x3EWi8VyufxM2nEc0zSFEFHSzzql9Hq9/volf6QvVr6n2OEjGOYAAAAASUVORK5CYII=',
            'options': [
                {
                    'name': 'enabled',
                    'type': 'enabler',
                    'default': False,
                },
                {
                    'name': 'username',
                    'default': '',
                },
                {
                    'name': 'password',
                    'default': '',
                    'type': 'password',
                },
                {
                    'name': 'seed_ratio',
                    'label': 'Seed ratio',
                    'type': 'float',
                    'default': 1,
                    'description': 'Will not be (re)moved until this seed ratio is met.',
                },
                {
                    'name': 'seed_time',
                    'label': 'Seed time',
                    'type': 'int',
                    'default': 40,
                    'description': 'Will not be (re)moved until this seed time (in hours) is met.',
                },
                {
                    'name': 'extra_score',
                    'advanced': True,
                    'label': 'Extra Score',
                    'type': 'int',
                    'default': 20,
                    'description': 'Starting score for each release found via this provider.',
                }
            ],
        },
    ],
}]