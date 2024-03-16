from typing import List
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from models import Medicine
from excel_handler import ExcelHandler

class BuscaMed:
    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--disable-gpu')
        self.chrome_options.add_argument('--disable-notifications')
        self.chrome_options.add_argument('--incognito')
        self.chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")

        self.url_drogasil = 'https://www.drogasil.com.br/search?w='
        self.url_pague_menos = 'https://www.paguemenos.com.br/busca?termo='
        self.lista_remedios = []
        self.lista_remedios_pagmen = {}
        self.lista_remedios_drogasil = {}

    def __init_driver(self):
        self.driver = webdriver.Chrome(options=self.chrome_options)  
    
    def set_remedios(self, lista_remedios: List[Medicine]):
        self.lista_remedios = lista_remedios
    
    def __parse_string_to_url(self, medicine: Medicine, replace: str = '+'):
        return str(medicine).replace(' ', replace)

    def get_remedios_pague_menos(self):

        for remedio in self.lista_remedios:
            self.__init_driver()

            # Acessa o site
            self.driver.get(f'{self.url_pague_menos}{self.__parse_string_to_url(remedio, '%20')}')
            self.driver.implicitly_wait(2)
            html = self.driver.page_source

            # Seta o dicionario
            self.lista_remedios_pagmen.update({remedio.name: []})

            # Converte o html para um objeto BeautifulSoup
            soup = bs(html, 'html.parser')

            # Procura os produtos
            produtos = soup.find_all('div', class_='paguemenos-store-theme-2-x-search-custom-products-galerryItem')

            # Procura o nome e o preço dos produtos
            for item in produtos:
                link_produto = item.find('a', class_='paguemenos-store-theme-2-x-search-custom-button').get('href')
                nome_produto = item.find('span', class_='paguemenos-store-theme-2-x-search-custom-products-name-span').text
                                    

                if (remedio.name.lower() in nome_produto.lower() and\
                str(remedio.mg) in nome_produto.lower() and\
                (remedio.pills is None or str(remedio.pills) in nome_produto.lower())):
                    
                    price = item.find('div', class_='paguemenos-store-theme-2-x-price').text
                    price = price.replace('\xa0', ' ').strip()

                    remedio.price = price
                    remedio.link = f'https://www.paguemenos.com.br{link_produto}'

                    self.lista_remedios_pagmen[remedio.name].append(Medicine(
                        remedio.name, remedio.mg, remedio.pills, remedio.price, remedio.link)
                    )

            self.driver.quit()

        return self.lista_remedios_pagmen
    
    def get_remedios_drogasil(self):
        
        for remedio in self.lista_remedios:
            self.__init_driver()

            # Acessa o site
            self.driver.get(f'{self.url_drogasil}{self.__parse_string_to_url(remedio)}')
            self.driver.implicitly_wait(2)
            html = self.driver.page_source

            # Seta o dicionario
            self.lista_remedios_drogasil.update({remedio.name: []})

            # Converte o html para um objeto BeautifulSoup
            soup = bs(html, 'html.parser')

            # Procura os produtos
            produtos = soup.find_all('div', class_='ProductCardstyles__ProductCardStyle-iu9am6-6')

            # Procura o nome e o preço dos produtos
            for item in produtos:
                produto = item.find('a', class_='LinkNextstyles__LinkNextStyles-t73o01-0 cpRdBZ LinkNext', attrs={'data-qa': 'caroussel_item_btn_buy'})
                nome_produto = item.find('div', class_='product-brand')

                nome_produto = nome_produto.text.strip() if nome_produto else None
                link_produto = produto.get('href') if produto else None
                titulo_produto = produto.get('title') if produto else None

                if (nome_produto and titulo_produto and remedio.name.lower() in nome_produto.lower() and\
                f'{remedio.mg}mg' in titulo_produto.lower() and\
                (remedio.pills is None or str(remedio.pills) in titulo_produto.lower())):
                    
                    preco = item.find('div', attrs={'data-qa': 'price_final_item'})
                    preco = f'{preco.text.strip() if preco else 'Não consta'}'

                    remedio.price = preco
                    remedio.link = f'https://www.drogasil.com.br{link_produto}'

                    self.lista_remedios_drogasil[remedio.name].append(
                        Medicine(remedio.name, remedio.mg, remedio.pills, remedio.price, remedio.link)
                    )
            
            self.driver.quit()
        
        return self.lista_remedios_drogasil

    
buscaMed = BuscaMed()
remedios = ExcelHandler.load_from_excel('remedios.xlsx')
buscaMed.set_remedios(remedios[0:1])
drogasil = buscaMed.get_remedios_drogasil()
paguemen = buscaMed.get_remedios_pague_menos()

medicamentos_drogasil = [med for sublist in drogasil.values() for med in sublist]
medicamentos_paguemenos = [med for sublist in paguemen.values() for med in sublist]
