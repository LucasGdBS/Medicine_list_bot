import pandas as pd
from typing import List
from models import Medicine

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
    def write_to_excel(file_path, medicines:List[Medicine], sheet_name):
        df = pd.DataFrame([medicine.__dict__ for medicine in medicines])

        df = df.rename(columns={
            'name': 'Nome',
            'mg': 'Miligramas',
            'pills': 'Comprimidos',
            'price': 'Preço',
            'link': 'Link'})

        df.to_excel(file_path, index=False, sheet_name=sheet_name)
            