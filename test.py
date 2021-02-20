[urlstringVar] = "[url]"
[htmlVar] = requests.get(html_string)
[soupObjVar] = bs([htmlVar].text, 'html.parser')

