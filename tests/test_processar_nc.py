import unittest
from scripts.processar_nc import dividir_titulo, extrair_categoria_nc
class TestETL(unittest.TestCase):
    def test_order(self):
        d,u,p,review=dividir_titulo('L02 - Produto 03 - 10/01/2025')
        self.assertEqual((u,p,review),('L02','PRODUTO 03',False)); self.assertEqual(d.year,2025)
    def test_missing(self):
        self.assertTrue(dividir_titulo('Produto 03')[-1])
    def test_label(self):
        self.assertEqual(extrair_categoria_nc('Outra, VALIDADE'),('VALIDADE',False))
    def test_ambiguous(self):
        self.assertTrue(extrair_categoria_nc('VALIDADE, AVARIAS DE TRANSPORTE')[1])
    def test_invalid_date(self):
        self.assertTrue(dividir_titulo('31/02/2025 - L01 - Produto 01')[-1])
if __name__=='__main__': unittest.main()
