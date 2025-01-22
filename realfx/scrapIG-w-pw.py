from playwright.async_api import async_playwright

produt = 'cafe 500g'

urls = {
    "ig": f"https://irmaosgoncalves.com.br/pesquisa?q={produt.replace(' ', '+')}&p=7&o=valor&t=asc"}

async def main():
    await search_ig()

async def search_ig():
    with async_playwright() as p:
        browser = await p.