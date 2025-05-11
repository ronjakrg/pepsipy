from peptidefeatures.features.physicochemical import molecular_weight

def test_molecular_weight():
    assert 799.832 == molecular_weight("PEPTIDE")