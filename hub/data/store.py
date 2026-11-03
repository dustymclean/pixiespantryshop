"""Pixie's Pantry's own products featured on the hub homepage.

Images use the store's own 600x600 copies (the originals run up to 5 MB).
Every price and claim here was copied from the live product page on pixies-pantry.com
(checked 2026-11-03). When a box changes on the store, change it here too -- this file is
also the source for the Product structured data, so a stale price is a wrong rich result.
"""

STORE = "https://pixies-pantry.com"
LOGO = "https://pixies-pantry.com/wp-content/uploads/2025/12/Designer-67-1.png"
SAME_AS = ["https://pixies-pantry.com/", "https://www.instagram.com/pixiespantryshop/",
           "https://www.pinterest.com/pixiespantryshop/"]
CHECKED = "2026-11-03"

FEATURED = {
    "name": "The Mystery Surprise Box",
    "url": f"{STORE}/product/mystery-box/",
    "img": f"{STORE}/wp-content/uploads/2026/11/01_mystery-box-trio_white-600x600.jpg",
    "price": "55.00",
    "availability": "PreOrder",
    "eyebrow": "Pre-order now · Ships Nov–Dec 2026",
    "lines": ["$55 of 100% brand-name smoking gear from 21 partner brands",
              "No auto-renew — buy one, or gift one forward",
              "Free shipping"],
}

BOXES = [
    {"name": "The Flower Box", "url": f"{STORE}/product/thca-flower-box/",
     "img": f"{STORE}/wp-content/uploads/2026/10/pixies-pantry-flower-1-600x600.jpg",
     "price": "75.00", "from": "From $75",
     "blurb": "1 or 2 named THCa strains, lab report on every jar. Half oz $75, ounce $120 with a free grinder."},
    {"name": "The Flower + Glass Box", "url": f"{STORE}/product/thca-flower-glass-box/",
     "img": f"{STORE}/wp-content/uploads/2026/10/Human-Grade-Water-Pipe-Packaging-Display-2-600x600.png",
     "price": "150.00", "from": "$150",
     "blurb": "A full ounce of named THCa flower plus a new water pipe. Breakage replaced free."},
    {"name": "The Dab Box", "url": f"{STORE}/product/thca-dab-box/",
     "img": f"{STORE}/wp-content/uploads/2026/10/pixies-pantry-dab-2-600x600.jpg",
     "price": "45.00", "from": "From $45",
     "blurb": "Solventless live rosin in 1 g jars with a Res-Tip and dab tool. 1 g $45, 2 g $80, 3.5 g $105."},
    {"name": "The Gear Box", "url": f"{STORE}/product/smoking-accessories-box/",
     "img": f"{STORE}/wp-content/uploads/2026/10/pixies-pantry-gear-box-600x600.jpg",
     "price": "55.00", "from": "$55",
     "blurb": "A new glass piece plus everything to keep it clean, matched to how you smoke. No THC, ships nationwide."},
    {"name": "The Name Your Price Box", "url": f"{STORE}/product/name-your-price-box/",
     "img": f"{STORE}/wp-content/uploads/2026/01/pixies-pantry-mystery-box-copy-600x600.png",
     "price": "10.00", "from": "From $10",
     "blurb": "Tell me your budget and your hero device. I pick the tray and fill it with gear that goes together. No curation fee."},
    {"name": "The Ms. Pixie Box", "url": f"{STORE}/product/ms-pixie-box/",
     "img": f"{STORE}/wp-content/uploads/2026/10/image-600x600.png",
     "price": "210.00", "from": "From $210",
     "blurb": "Your Puffco plus a Focus V Saber hot knife, hand-packed into a gasket-sealed hard case with cleaning gear."},
]


# Temporarily hidden from the affiliate storefront.
# Original product records are preserved above.
HIDDEN_BOXES = {
    "The Flower Box",
    "The Flower + Glass Box",
    "The Dab Box",
}
BOXES = [box for box in BOXES if box["name"] not in HIDDEN_BOXES]

LINKS = [
    ("Shop everything", f"{STORE}/shop/"),
    ("Hemp & THCa flower", f"{STORE}/product-category/flower-hemp-thca-3/"),
    ("Compare the boxes", f"{STORE}/compare-monthly-boxes/"),
    ("Events & workshops", f"{STORE}/north-mississippi-events-experiences/"),
    ("Wholesale for retailers", f"{STORE}/wholesale/"),
    ("Lab reports (COAs)", f"{STORE}/coas/"),
]
