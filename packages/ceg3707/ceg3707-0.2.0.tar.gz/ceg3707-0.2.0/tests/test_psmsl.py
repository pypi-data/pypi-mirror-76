import ceg3707.psmsl as psmsl

def test_psmsl():
    '''
    test load psmsl
    '''
    data = psmsl.load_rlr("1")
    print(data.head())

    return

