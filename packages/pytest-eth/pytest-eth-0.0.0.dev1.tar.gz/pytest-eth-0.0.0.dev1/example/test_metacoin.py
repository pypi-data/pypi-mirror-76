# MetaCoin Testing


# cobra is pytest fixture
def test_metacoin(eth):
    # Getting Contract Factory by name
    metacoin = eth.contract('MetaCoin')
    # Getting Contract Instance of MetaCoin
    metacoin = metacoin.deploy()

    assert metacoin.getBalance(eth.accounts[0]) == 10000
