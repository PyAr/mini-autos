import pyglet
import random
import math

width = 1280
height = 768

window = pyglet.window.Window(width, height)
image = pyglet.resource.image('graficos/auto.png')
background = pyglet.resource.image('graficos/background.png')
image.anchor_x = image.width / 2
image.anchor_y = image.height / 2

explosion = [
  pyglet.resource.image(f'graficos/boom_{str(n).zfill(3)}.png') for n in
  range(1, 17)
]

for fx in explosion:
    fx.anchor_x = fx.width / 2
    fx.anchor_y = fx.height / 2


cars = [
]

fx = []
sprites = {}


@window.event
def on_draw():
    window.clear()
    background.blit(0, 0)

    for car in cars:
        sprite = sprites[car["symbol"]]
        sprite.x = car["x"]
        sprite.y = car["y"]
        sprite.rotation = car["rotation"]

        sprite.draw()

    for sprite in fx:
        sprite.draw()


@window.event
def on_key_press(symbol, modifiers):

    # intenta hacer doblar un auto
    for car in cars:
        if symbol == car['symbol']:
            car['press'] = True
            return

    # si no se encontró
    cars.append({
        "x": random.randint(0, width),
        "y": random.randint(0, height),
        "symbol": symbol,
        "speed": 200,
        "press": False,
        "rotation": random.randint(0, 360),
        "radio": 12,
        "live": True,
    })
    sprites[symbol] = pyglet.sprite.Sprite(image, 0, 0)


@window.event
def on_key_release(symbol, modifiers):
    for car in cars:
        if symbol == car['symbol']:
            car['press'] = False


def update(dt):
    global cars

    for car in cars:

        # aumentamos la velocidad
        car['speed'] += 20 * dt

        # Evita procesar un auto que ha colisionado.
        if not car['live']:
            continue
 
        rotation = (car['rotation'] * math.pi) / 180.0

        # Aplica la rotación al jugador
        if car['press']:
            car['rotation'] += (200 + car['speed'] * 0.25) * dt

        # Hace que avance en la dirección a la que está mirando
        car['x'] += math.cos(rotation) * car['speed'] * dt
        car['y'] -= math.sin(rotation) * car['speed'] * dt

        # evita que salga por los bordes izquierdo y derecho
        if car['x'] > width + 30:
            car['x'] = -30

        if car['x'] < -30:
            car['x'] = width + 30

        # evita que salga por los bordes de arriba y abajo
        if car['y'] > height + 30:
            car['y'] = 0 - 30

        if car['y'] < - 30:
            car['y'] = height + 30

        # Busca colisiones
        for other in cars:
            if other['symbol'] != car['symbol']:
                xa = car['x']
                xb = other['x']
                ya = car['y']
                yb = other['y']

                d = math.sqrt(math.pow(xb - xa, 2) + math.pow(yb - ya, 2))

                ratio_sum =  car['radio'] + other['radio']

                if d < ratio_sum:
                    car['live'] = False
                    other['live'] = False
                        
                    ani = pyglet.image.Animation.from_image_sequence(explosion, \
                            duration=0.05, loop=False)
                    sprite = pyglet.sprite.Sprite(img=ani)
                    sprite.x = car['x']
                    sprite.y = car['y']
                    fx.append(sprite)
                    
                
    # solo nos quedamos con los autos vivos.
    cars = [car for car in cars if car['live']]
        
        


pyglet.clock.schedule_interval(update, 1/60.0)

pyglet.app.run()
