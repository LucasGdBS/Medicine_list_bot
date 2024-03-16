import json

class Medicine:
    '''Classe que representa um medicamento, com nome, quantidade de comprimidos, miligramas, link e preço.'''
    def __init__(self, name, pills, mg, link=None, price:float=0.0):
        self.name = name
        self.pills = pills
        self.mg = mg
        self.price = price
        self.link = link
    
    def __str__(self) -> str:
        '''Retorna uma string com os atributos da classe Medicine'''
        return f'Nome: {self.name} {self.mg}mg {self.pills} comprimidos, Preço: {self.price}'
    
    def to_json(self):
        '''Retorna um json com os atributos da classe Medicine'''
        return json.dumps(self.__dict__)


