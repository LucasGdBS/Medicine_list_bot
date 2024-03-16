import pandas as pd
from models import Medicine
from openpyxl import load_workbook

class ExcelHandler:
    @staticmethod
    def load_from_excel(file_path):
        medicines = []

        df = pd.read_excel(file_path)

        for index, row in df.iterrows():
            name = row['Nome']
            mg = row['Miligramas']
            pills = row['Comprimidos']

            pills = None if pd.isna(pills) else int(pills)
            
            medicine = Medicine(name, mg, pills)

            medicines.append(medicine)

        return medicines
    
    @staticmethod
    def write_to_excel(file_path, medicines_drogasil:dict, medicines_pague_menos:dict):
        planilha = load_workbook(file_path)

        aba_ativa = planilha.active

        for i, cel in enumerate(aba_ativa['D'][1:]):
            linha = cel.row
            nome_remedio = aba_ativa[f'A{linha}'].value

            if nome_remedio in medicines_drogasil:
                remedio = medicines_drogasil[nome_remedio]

                aba_ativa[f'D{linha}'] = f'{remedio.price}'
                aba_ativa[f'D{linha}'].style = 'Hyperlink'
                aba_ativa[f'D{linha}'].hyperlink = remedio.link
        
        for i, cel in enumerate(aba_ativa['E'][1:]):
            linha = cel.row
            nome_remedio = aba_ativa[f'A{linha}'].value

            if nome_remedio in medicines_drogasil:
                remedio = medicines_pague_menos[nome_remedio]

                aba_ativa[f'E{linha}'] = f'{remedio.price}'
                aba_ativa[f'E{linha}'].style = 'Hyperlink'
                aba_ativa[f'E{linha}'].hyperlink = remedio.link
            

        planilha.save(file_path)
            