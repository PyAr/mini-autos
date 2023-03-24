import pyglet
import random
import math
from pyglet.window import key


width = 1280
height = 768

window = pyglet.window.Window(width, height)
image = pyglet.resource.image('graficos/auto.png')
background = pyglet.resource.image('graficos/background.png')
image.anchor_x = image.width / 2
image.anchor_y = image.height / 2

explosion_sound = pyglet.media.load('audio/explosion.mp3', streaming=False)
music = pyglet.media.load('audio/music.mp3', streaming=False)

player = pyglet.media.Player()
player.queue(music)
player.eos_action = 'loop'

player.volume = 0.4

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
labels = {}

camera_x = 0
camera_y = 0
dx = 0
dy = 0
shake = 0

start_game = pyglet.text.Label("Pulsa alguna tecla para comenzar",
            font_name='Arial',
            color=(0, 0, 0, 180),
            font_size=40,
            x=width/2, y=height/2,
            anchor_x='center', anchor_y='center')


@window.event
def on_draw():
    window.clear()
    background.blit(camera_x + dx * shake, camera_y + dy * shake)

    for car in cars:
        sprite = sprites[car["symbol"]]
        sprite.x = car["x"] + dx * shake
        sprite.y = car["y"] + dy * shake
        sprite.rotation = car["rotation"]
        sprite.draw()

        # labels
        label = labels[car["symbol"]]
        label.x = car["x"] + dx * shake
        label.y = car["y"] + dy * shake - 45
        label.draw()

    for sprite in fx:
        sprite.x = sprite.original_x + dx * shake
        sprite.y = sprite.original_y + dx * shake
        sprite.draw()

    if not cars:
        start_game.draw()


def get_letter_from_symbol(symbol):
    dictionary = {
        key.A:  'A',
        key.B:  'B',
        key.C:  'C',
        key.D:  'D',
        key.E:  'E',
        key.F:  'F',
        key.G:  'G',
        key.H:  'H',
        key.I:  'I',
        key.J:  'J',
        key.K:  'K',
        key.L:  'L',
        key.M:  'M',
        key.N:  'N',
        key.O:  'O',
        key.P:  'P',
        key.Q:  'Q',
        key.R:  'R',
        key.S:  'S',
        key.T:  'T',
        key.U:  'U',
        key.V:  'V',
        key.W:  'W',
        key.X:  'X',
        key.Y:  'Y',
        key.Z:  'Z',

        key._1: '1',
        key._2: '2',
        key._3: '3',
        key._4: '4',
        key._5: '5',
        key._6: '6',
        key._7: '7',
        key._8: '8',
        key._9: '9',
        key._0: '0',
    }

    if symbol in dictionary:
        return dictionary[symbol]


@window.event
def on_key_press(symbol, modifiers):
    # intenta obtener la tecla que se pulsó
    letter = get_letter_from_symbol(symbol)

    # pyglet no nos retorna la representación
    # de la tecla como texto, pero como nosotros
    # necesitamos esa representación para indicarle
    # al jugador cual es su auto, usamos esta variable
    # letter. Si no podemos determinar la tecla, evitamos
    # crear o manejar una auto.
    if not letter:
        return

    # intenta hacer doblar un auto
    for car in cars:
        if symbol == car['symbol']:
            car['press'] = True
            return

    # Solo pone música si no hay autos en
    # la escena.
    if not cars:
        player.seek(0)
        player.play()

    # si no se encontró un auto creado, debe crear uno nuevo.
    cars.append({
        "x": random.randint(0, width),
        "y": random.randint(0, height),
        "symbol": symbol,
        "speed": 200,
        "press": False,
        "rotation": random.randint(0, 360),
        "radio": 12,
        "letra": letter,
        "live": True,
    })

    sprites[symbol] = pyglet.sprite.Sprite(image, 0, 0)
    labels[symbol] = pyglet.text.Label(letter,
            font_name='Arial',
            color=(0, 0, 0, 180),
            font_size=14,
            x=0, y=0,
            anchor_x='center', anchor_y='center')


@window.event
def on_key_release(symbol, modifiers):
    for car in cars:
        if symbol == car['symbol']:
            car['press'] = False


def update(dt):
    global cars, shake, dx, dy

    # Lleva shake a 0, de modo tal que detenga
    # la vibración de la pantalla.
    if shake > 0:
        shake -= dt * 10
    else:
        shake = 0

    # variables para indicar que deber moverse la pantalla
    dx = random.randint(-10, 10) / 5.0
    dy = random.randint(-10, 10) / 5.0

    for car in cars:

        # aumentamos la velocidad
        if car['speed'] < 300:
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
                    ani = pyglet.image.Animation.from_image_sequence(
                            explosion,
                            duration=0.05, 
                            loop=False)
                    sprite = pyglet.sprite.Sprite(img=ani)
                    sprite.original_x = car['x']
                    sprite.original_y = car['y']
                    fx.append(sprite)

                    # reproduce el sonido de explosión
                    explosion_sound.play()

                    # hace que la cámara vibre.
                    shake = 8

    # solo nos quedamos con los autos vivos.
    cars = [car for car in cars if car['live']]
    
    if not cars:
        player.pause()


pyglet.clock.schedule_interval(update, 1/60.0)
pyglet.app.run()
