from busca_med import BuscaMed
from excel_handler import ExcelHandler

buscaMed = BuscaMed()
remedios = ExcelHandler.load_from_excel('remedios.xlsx')
buscaMed.set_remedios(remedios)
drogasil = buscaMed.get_remedios_drogasil()
paguemen = buscaMed.get_remedios_pague_menos()

# medicamentos_drogasil = [med for sublist in drogasil.values() for med in sublist]
# medicamentos_paguemenos = [med for sublist in paguemen.values() for med in sublist]

remedios_mais_baratos_drogasil = {}
remedios_mais_baratos_paguemenos = {}

for tipo, lista in drogasil.items():
    remedio_mais_barato = min(lista, key=lambda x: x.price)
    remedios_mais_baratos_drogasil[tipo] = remedio_mais_barato

for tipo, lista in paguemen.items():
    remedio_mais_barato = min(lista, key=lambda x: x.price)
    remedios_mais_baratos_paguemenos[tipo] = remedio_mais_barato

print(remedios_mais_baratos_drogasil)
print(remedios_mais_baratos_paguemenos)

ExcelHandler.write_to_excel('remedios.xlsx', remedios_mais_baratos_drogasil, remedios_mais_baratos_paguemenos)