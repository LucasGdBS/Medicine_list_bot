import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver

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
        self.lista_remedios_pagmen = []
        self.lista_remedios_drogasil = {}

    def __init_driver(self):
        self.driver = webdriver.Chrome(options=self.chrome_options)  
    
    def set_remedios(self, lista_remedios: list):
        self.lista_remedios = lista_remedios
    
    def __parse_string_to_url(self, string: str, replace: str = '+'):
        return string.replace(' ', replace).upper()

    def get_remedios_pague_menos(self):

        for remedio in self.lista_remedios:
            self.__init_driver()

            # Acessa o site
            self.driver.get(self.url_pague_menos + self.__parse_string_to_url(remedio, '%20'))
            self.driver.implicitly_wait(2)
            html = self.driver.page_source

            # Converte o html para um objeto BeautifulSoup
            soup = bs(html, 'html.parser')

            # Procura os produtos
            produtos = soup.find_all('div', class_='paguemenos-store-theme-2-x-search-custom-products-galerryItem')

            # Procura o nome e o preço dos produtos
            for item in produtos:
                nome_produto = item.find('span', class_='paguemenos-store-theme-2-x-search-custom-products-name-span').text
                if remedio.lower() in nome_produto.lower():
                    preco = item.find('div', class_='paguemenos-store-theme-2-x-price').text
                    preco = preco.replace('\xa0', ' ').strip()
                    self.lista_remedios_pagmen.append({'Nome': nome_produto, 'Preço': preco})

            self.driver.quit()

        print(self.lista_remedios_pagmen)
    
    def get_remedios_drogasil(self):
        
        for remedio in self.lista_remedios:
            self.__init_driver()

            # Acessa o site
            self.driver.get(self.url_drogasil + self.__parse_string_to_url(remedio))
            self.driver.implicitly_wait(2)
            html = self.driver.page_source

            # Seta o dicionario
            self.lista_remedios_drogasil.update({remedio: []})

            # Converte o html para um objeto BeautifulSoup
            soup = bs(html, 'html.parser')

            # Procura os produtos
            produtos = soup.find_all('div', class_='ProductCardstyles__ProductCardStyle-iu9am6-6')

            # Procura o nome e o preço dos produtos
            for item in produtos:
                nome_produto = soup.find('a', class_='LinkNextstyles__LinkNextStyles-t73o01-0 cpRdBZ LinkNext', attrs={'data-qa': 'caroussel_item_btn_buy'})
                nome_produto = nome_produto.get('title') if nome_produto else None

                if nome_produto and remedio.lower() in nome_produto.lower():
                    preco = item.find('div', class_='Pricestyles__ProductPriceStyles-sc-118x8ec-0')
                    preco = f'R$ {preco.text.strip() if preco else 'Não consta'}'
                    self.lista_remedios_drogasil[remedio].append({'Nome': nome_produto, 'Preço': preco})
            
            self.driver.quit()
        
        print(self.lista_remedios_drogasil)


            
            
    
buscaMed = BuscaMed()
buscaMed.set_remedios(['dual'])

buscaMed.get_remedios_drogasil()
# buscaMed.get_remedios_pague_menos()
    

    
