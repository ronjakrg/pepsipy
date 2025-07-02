import pandas as pd


TEST_DATA = pd.DataFrame(
    {
        "Sample": [
            "AD01_C1_INSOLUBLE_01",
            "CTR01_C1_INSOLUBLE_01",
            "CTR01_C1_INSOLUBLE_01",
        ],
        "Protein ID": ["A0A075B6S2", "A0A075B6R2", "A0A075B6R2"],
        "Sequence": ["FSGVPDR", "VTISVDK", "VTISVDK"],
        "Intensity": [936840, 33411000, 33411000],
        "PEP": [0.0068633, 0.057623, 0.057623],
    }
)
