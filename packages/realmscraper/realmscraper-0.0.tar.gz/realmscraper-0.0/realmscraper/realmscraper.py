class get_pages_from_search:
    def req(self, ques):
        URL = 'https://www.realmeye.com/wiki-search?q=' + ques.replace(" ", "%20")
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
        page = requests.get(URL, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        body = soup.find('body')
        pages = body.find_all('p', class_="wiki-search-result")
        outputs = []
        for page in pages:
            link = page.find('a')
            outputs.append('https://www.realmeye.com' + link['href'])
        outputs = {i+1: value for i, value in enumerate(outputs)}
        return outputs
    def info(self):
        print('t')

class get_player_info:
    def req(self, player):
        try:
            URL = 'https://www.realmeye.com/player/'+player
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
            page = requests.get(URL, headers=headers)
            soup = BeautifulSoup(page.content, 'html.parser')
            summ = soup.find('table', class_='summary')
            info = summ.find_all('td')
            infotext = []
            for inf in info:
                infotext.append(inf.text)
            infotext = {infotext[i] : infotext[i+1] for i in range(0, len(infotext), 2)}
            return infotext
        except:
            return None
    def info(self):
        print('t')

class get_realmeye_response:
    def req(self, term):
        URL = 'https://www.realmeye.com/wiki/realm-eye-responses'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
        page = requests.get(URL, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        body = soup.find('body')
        page_wiki = body.find('div', class_='wiki-page')
        responses = page_wiki.findChildren("p", recursive=True)

        for response in responses:
            try:
                name = response.find("a").text
                content = response.text
                if name == term:
                    title = content.split('\n')[0]
                    results = ''.join(content.split('\n')[1:])
                    return {'key': title, 'result': results}
            except:
                pass
    def info(self):
        print('t')

class get_servers:
    def req(self):
        URL = 'https://www.realmeye.com/servers-by-active-guilds'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
        page = requests.get(URL, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        body = soup.find('body')
        tbodies = soup.find_all('tbody')[0]
        servs = tbodies.find_all('td')
        servers = []
        for i in range(0, len(servs), 9):
            toadd = []
            for j in range(1, 8):
                toadd.append(servs[i+j].text)
            servers.append(toadd)
        server_list = {}
        for serve in servers:
            server_list[serve[0]] = int(serve[2])
        final = {k: v for k, v in sorted(server_list.items(), key=lambda item: item[1], reverse=True)}
        return final
    def info(self):
        print('t')

class get_wiki_page:
    def req(self, url_):
        finalout = []
        URL = url_
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
        page = requests.get(URL, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        body = soup.find('body')
        main = body.find('div', class_='table-responsive')
        name = main.find('img')['title']
        page_wiki = body.find('div', class_='wiki-page')
        children = page_wiki.findChildren("div", class_="table-responsive", recursive=False)
        first = children[0]
        tds = first.find_all('td')
        description = tds[1].text


        #checking if has reskin
        child2 = children[1]
        child3 = child2.find('th')
        if (child3.text) == 'Reskin(s)':
            stats = children[2].find_all('tr')
            notes = page_wiki.findChildren("p", recursive=False)
        else:
            stats = children[1].find_all('tr')
            notes = page_wiki.findChildren("p", recursive=False)
        notemessage = ''
        for note in notes:
            notemessage += note.text + '\n'

        tier_ = stats[0]
        tier_step = (tier_.find_all('th'))
        statlist = []
        tier = (tier_step[0].text + ': ' + tier_step[1].text)
        statlist.append(tier)
        stats.pop(0)
        for stat in stats:
            part1 = stat.find('th').text
            part2 = stat.find('td').text
            if part1 == 'Soulbound':
                combined = part1
            else:
                combined = part1 + ': ' + part2
            statlist.append(combined)
        finalout.append(name)
        finalout.append(statlist)
        finalout.append(description)
        finalout.append(notemessage)
        final = {}
        attrs = finalout[1]
        final['name'] = finalout[0]
        sb = False
        for attr in attrs:
            if attr != 'Soulbound':
                final[attr.split(': ')[0]] = attr.split(': ')[1]
            else:
                sb = True
        if sb:
            final['soulbound'] = True
        else:
            final['soulbound'] = False

        final['description'] = finalout[2]
        final['notes'] = finalout[]

        return final
    def info(self):
        print('t')
