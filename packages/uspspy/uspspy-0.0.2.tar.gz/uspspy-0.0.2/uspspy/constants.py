SAFE = " -_"
REQUEST_TIMEOUT = 5

DPV_MAP = {
    "Y": "Both primary and secondary DPV confirmed.",
    "D": "Primary DPV confirmed, secondary missing.",
    "S": "Primary DPV confirmed, secondary present but not verified.",
    "N": "Neither primary or secondary DPV confirmed."
}

DPV_FOOTNOTES = {
    "AA": "Input address matched to Zip4+ file.",
    "A1": "Input address not matched to Zip4+ file.",
    "BB": "Matched all components to DPV.",
    "CC": "Secondary Number present but invalid.",
    "N1": "High-rise address missing secondary number.",
    "M1": "Primary number missing.",
    "M3": "Primary number invalid.",
    "P1": "Input Address RR or HC Box number missing.",
    "P3": "Input Address PO, RR, or HC Box number invalid.",
    "F1": "Input Address Matched to a Military Address.",
    "G1": "Input Address Matched to a General Delivery Address.",
    "U1": "Input Address Matched to a Unique ZIP Code",
}

FOOTNOTES = {
    "A": "Zip Code Corrected",
    "B": "City / State Spelling Corrected",
    "C": "Invalid City / State / Zip",
    "D": "NO ZIP+4 Assigned",
    "E": "Zip Code Assigned for Multiple Response",
    "F": "Address could not be found in the National Directory File Database",
    "G": "Information in Firm Line used for matching",
    "H": "Missing Secondary Number",
    "I": "Insufficient/Incorrect Address Data",
    "J": "Dual Address",
    "K": "Multiple Response due to Cardinal Rule",
    "L": "Address component changed",
    "LI": "Match has been converted via LACS",
    "M": "Street Name changed",
    "N": "Address Standardized",
    "O": "Lowest +4 Tie-Breaker",
    "P": "Better address exists",
    "Q": "Unique Zip Code match",
    "R": "No match due to EWS",
    "S": "Incorrect Secondary Address",
    "T": "Multiple response due to Magnet Street Syndrome",
    "U": "Unofficial Post Office name",
    "V": "Unverifiable City/State",
    "W": "Invalid Delivery Address",
    "X": "No match due to out of range alias",
    "Y": "Military match",
    "Z": "Match made using the ZIPMOVE product data",
}
