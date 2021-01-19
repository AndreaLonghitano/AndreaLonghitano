import requests
from bs4 import BeautifulSoup
import os
import re


SITE = 'https://andrealonghitano.github.io/online-cv/'
PROJECTS = 'projects-section'
GITHUB_PAGE = 'https://github.com/AndreaLonghitano'
README_FILE = os.path.join(os.getcwd(),'README.md')


def fetch_projects():

    global SITE,PROJECTS

    page = requests.get(SITE)
    soup = BeautifulSoup(page.text, 'html.parser')
    project_section = soup.find('section', {"class": PROJECTS}) 
    projects = list()
    for _,item in enumerate(project_section.find_all("div", class_="item")):
        ## fetch the title
        title = item.find('span',class_='project-title')

        ## link
        link = title.find('a',href = True)

        link = link['href'] if link is not None else GITHUB_PAGE
        ##
        ## fetch the description
        description = item.find('span',class_='project-tagline')

        proj = dict ()
        proj['title'] = title.text
        proj['description'] = description.text
        proj['link'] = link

        ## append to all the projects
        projects.append(proj)

    return projects

def create_markdown_projects():
    
    projects = fetch_projects()

    markdown = '\n'.join([f'* [{ele["title"]}]({ele["link"]}) - {ele["description"]}' for ele in projects])

    return markdown


def replace_chunk(content, marker, chunk, inline=False):
    r = re.compile(
        r'<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->'.format(marker, marker),
        re.DOTALL,
    )
    if not inline:
        chunk = '\n{}\n'.format(chunk)
    chunk = '<!-- {} starts -->{}<!-- {} ends -->'.format(marker, chunk, marker)
    return r.sub(chunk, content)


if __name__=='__main__':

    with open(README_FILE,'r',encoding='utf-8') as f:
        readme = f.read()

    markdown_projects = create_markdown_projects()

    ## projects
    new_readme = replace_chunk(readme,marker = 'projects', chunk = markdown_projects)

    ## website
    new_readme = replace_chunk(new_readme,marker='website',chunk = f'[my website]({SITE})')

    with open(README_FILE,'w',encoding='utf-8') as f:
        f.write(new_readme)



