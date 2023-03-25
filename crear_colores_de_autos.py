import os

original = "graficos/auto.png"

colores = [
    "#FA8072",
    "#F4A460",
    "#DAA520",
    "#FFFF00",
    "#9ACD32",
    "#7FFF00",
    "#40E0D0",
    "#1E90FF",
    "#8A2BE2",
    "#800080",
    "#FF00FF",
    "#FFFAFA",
    "#FFA07A",
    "#228B22",
    "#7FFFD4",
]

for indice, color in enumerate(colores):
    os.system(f"convert {original} -colorspace gray -fill '{color}' -tint 100 graficos/autos/auto-{indice}.png")
