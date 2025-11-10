'''Tämä luokka sisältää testit'''

import unittest
from varasto import Varasto

# Huom. AI:n käyttö: testien lisäyksessä käytetty hyödyksi tekoälyn tuottamia
# esimerkkejä sivulta https://ohjelmistotuotanto-hy.github.io/genai/#viikko-1---teht%C3%A4v%C3%A4-8
# Huom2.AI:n käyttö: testikattavuuden ollessa 98 % tehty ChatGPT:lle kysely:
# "Minulla on seuraava koodi_ varasto.py. Koodille teen seuraavat testit. Testikattavuus on 98 %.
# Mikä testi jää puuttumaan? varasto_test.py" Vastauksen perusteella lisätty yksi testi koskien
# sitä, palautuuko oikea arvo, kun varastosta yritetään ottaa enemmän kuin siellä on.
# Ensimmäinen yritys ei kuitenkaan parantunut testikattavuutta, joten totestin test
# coveragen olevan silti edelleen 98 %, jolloin sain ehdotuksia erilaisten reunatapausten
# tutkimiseen etenkin kontruktoriin liittyen.
# Tämäkään ei tuottanut haluttua tulosta. Tutkin tarkemmin coverage-kattavuusraporttia ja
# huomasin, että tulostuksen oikeellisuuden testi puuttui. Tämän jälkeen annoin
# vielä kehotteen "Kyse olisiitä, että tulostuksen oikeellisuus (viimeinen kohta) jäi testaamatta.
# Kirjoita tätä varten testi."

class TestVarasto(unittest.TestCase):
    '''Alustetaan testivarasto, tilavuus = 10'''
    def setUp(self):
        self.varasto = Varasto(10)

    def test_konstruktori_luo_tyhjan_varaston(self):
        '''Testataan että luotu varasto tyhjä'''
        # https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertAlmostEqual
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_uudella_varastolla_oikea_tilavuus(self):
        '''Testataan että uudella varastolla tilavuus = 10'''
        self.assertAlmostEqual(self.varasto.tilavuus, 10)

    def test_lisays_lisaa_saldoa(self):
        '''Testataan että lisäys menee varastoon oikein'''
        self.varasto.lisaa_varastoon(8)

        self.assertAlmostEqual(self.varasto.saldo, 8)

    def test_lisays_lisaa_pienentaa_vapaata_tilaa(self):
        '''Testataan, että lisäys vähentää vapaata tilaa'''
        self.varasto.lisaa_varastoon(8)

        # vapaata tilaa pitäisi vielä olla tilavuus-lisättävä määrä eli 2
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 2)

    def test_ottaminen_palauttaa_oikean_maaran(self):
        '''Kun poistetaan varastosta, katsotaan että saadaan oikea tilavuus ulos'''
        self.varasto.lisaa_varastoon(8)

        saatu_maara = self.varasto.ota_varastosta(2)

        self.assertAlmostEqual(saatu_maara, 2)

    def test_ottaminen_lisaa_tilaa(self):
        '''Testataan että tyhjä tila lisääntyy, kun otetaan varastosta pois'''
        self.varasto.lisaa_varastoon(8)

        self.varasto.ota_varastosta(2)

        # varastossa pitäisi olla tilaa 10 - 8 + 2 eli 4
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 4)

    def test_liikaa_ei_voi_lisata(self):
        '''Testataan että varastoon ei voi lisätä enempää kuin tilavuus'''
        self.varasto.lisaa_varastoon(11)
        self.assertAlmostEqual(self.varasto.saldo, 10)

    def test_tyhjasta_ei_voi_ottaa(self):
        '''Testataan että jos varasto on tyhjä, sieltä ei voi ottaa'''
        self.varasto.ota_varastosta(1)
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_liikaa_ei_voi_ottaa(self):
        '''Testataan, ettei saada enempää kuin on on ja varasto tyhjenee'''
        self.varasto.lisaa_varastoon(8)
        saatu_maara = self.varasto.ota_varastosta(10)
        self.assertAlmostEqual(saatu_maara, 8)
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_negatiivista_ei_voi_lisata(self):
        '''Testataan ettei negatiivista tilavuutta voi lisätä'''
        self.varasto.lisaa_varastoon(-1)
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_negatiivista_maaraa_ei_voi_ottaa(self):
        '''Testataan ettei poisto voi olla negatiivinen'''
        self.varasto.ota_varastosta(-2)
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_negatiivinen_lisays_ei_lisaa_tilaa(self):
        '''Testataan ettei neg. lisäys lisää tilaa'''
        self.varasto.lisaa_varastoon(-3)
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 10)

    def test_negatiivisen_ottaminen_ei_lisaa_tilaa(self):
        '''Testataan ettei negatiivisten poisto lisää tilaa'''
        self.varasto.lisaa_varastoon(8)
        self.varasto.ota_varastosta(-2)
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 2)

    def test_konstruktori_nollaa_negatiivisen_tilavuuden(self):
        '''Testataan ettei tilavuus voi olla lähtökohtaisesti -1'''
        varasto = Varasto(-1)
        self.assertAlmostEqual(varasto.tilavuus, 0)

    def test_konstruktori_ei_lisaa_negatiivista_tilavuutta_alussa(self):
        '''Testaus, ei voi lisätä lähtökohtaisesti neg. tilavuutta'''
        varasto = Varasto(5, -5)
        self.assertAlmostEqual(varasto.paljonko_mahtuu(), 5)

    def test_konstruktori_ei_anna_negatiivista_saldoa_alussa(self):
        '''Palautuva saldo ei voi olla negatiivinen'''
        varasto = Varasto(5, -5)
        self.assertAlmostEqual(varasto.saldo, 0)

    def test_konstruktori_ei_lisaa_liikaa_sisaltoa_alussa(self):
        '''Alussa ei voi lisätä liikaa sisältöä'''
        varasto = Varasto(5, 10)
        self.assertAlmostEqual(varasto.saldo, 5)

    def test_konstruktori_jos_tilavuus_nolla_ei_voi_lisata(self):
        '''Jos tilavuus = 0, ei voi lisätä mitään'''
        varasto = Varasto(0)
        varasto.lisaa_varastoon(5)
        self.assertAlmostEqual(varasto.saldo, 0)

    def test_tulostus_oikein(self):
        '''Tarkistetaan että tulostus menee oikein'''
        self.varasto.lisaa_varastoon(2)
        tuloste = "saldo = 2, vielä tilaa 8"
        self.assertAlmostEqual(str(self.varasto), tuloste)
