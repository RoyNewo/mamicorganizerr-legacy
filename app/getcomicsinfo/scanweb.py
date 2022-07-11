import pprint
import asyncio
from pyppeteer import launch
from icecream import ic



async def get_browser():
    return await launch()

async def get_page(browser, url):
    page = await browser.newPage()
    await page.goto(url)
    return page

async def extract_data(page):
    # Select all articles in div with class post-list-posts
    elements = await page.querySelectorAll('div.post-info')
    # Select all links in each article
    for element in elements:
        links = await element.querySelectorAll('a')    
    result = {}    
    # Extract title and content from each link
    for link in links:
        ic('paso por aqui')
        title, content = await page.evaluate('''(element) => {
            const content = element.getAttribute('href')
            const title = element.textContent
            return [title, content]
        }''',link)
        ic(content)
        result[title] = content
        
    return result
async def extract(browser, name, url):
    page = await get_page(browser, url)
    return {name: await extract_data(page)}

async def extract_all(webpages):
    browser = await get_browser()
    tasks = {}
    for name, url in webpages.items():
        tasks |= await extract(browser, name, url)
    return tasks

def main():
    webpages = {
        'DC': 'https://getcomics.info/tag/dc-week/',
        'Marvel': 'https://getcomics.info/tag/marvel-now/'
    }
    tasks = extract_all(webpages)
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(tasks)
    pprint.pprint(result)