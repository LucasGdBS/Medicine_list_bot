import json

class Medicine:
    '''Classe que representa um medicamento, com nome, quantidade de comprimidos, miligramas, link e preço.'''
    def __init__(self, name:str, mg:float, pills:int=None, price:float=0.0, link: str=None):
        self.name = name
        self.mg = mg
        self.pills = pills
        self.price = price
        self.link = link
    
    def __str__(self) -> str:
        '''Retorna uma string com os atributos da classe Medicine'''
        return f'{self.name} {self.mg}mg {self.pills}'
    
    def __repr__(self) -> str:
        '''Retorna uma string com os atributos da classe Medicine'''
        return f'{self.name} {self.mg}mg {self.pills} {self.price} {self.link}'
    
    def to_json(self):
        '''Retorna um json com os atributos da classe Medicine'''
        return json.dumps(self.__dict__)


