from pyModeS.decoder import tell

messages = [
    "8D406B902015A678D4D220AA4BDA",
    "8FC8200A3AB8F5F893096B000000",
    "8D40058B58C901375147EFD09357",
    "8D485020994409940838175B284F",
    "A000083E202CC371C31DE0AA1CCF",
    "A8001E2520053332C1A820363386",
    "A000029C85E42F313000007047D3",
    "A5DC282C2A0108372CA6DA9693B0",
    "A00015B8C26A00328400004242DA",
    "A000139381951536E024D4CCF6B5",
    "A00004128F39F91A7E27C46ADC21",
]

for m in messages:
    tell(m)
    print("-" * 50)
