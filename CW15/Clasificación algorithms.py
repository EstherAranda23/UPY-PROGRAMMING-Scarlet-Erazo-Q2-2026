# Classwork 15 - Sorting Algorithms: Bubble Sort Visualized


import stddraw
import color
import time
import pygame

# Inicialización de Pygame Mixer
pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)

def beep(freq=440, duration=100):
    import numpy as np
    sample_rate = 44100
    frames = int(duration * sample_rate / 1000)
    t = np.linspace(0, duration/1000, frames, False)
    wave = (np.sin(2 * np.pi * freq * t) * 32767).astype(np.int16)
    wave = np.column_stack([wave, wave])
    sound = pygame.sndarray.make_sound(wave)
    sound.play()

# ── INPUT ────────────────────────────────────────────────────


array = [5, 3, 8, 4, 2, 7, 1, 6]
n     = len(array)

# Visualization settings
WIDTH  = 1.0
HEIGHT = 1.0
DELAY  = 0.6   # seconds between frames

# Colors
COL_BAR      = color.BOOK_BLUE       # default bar color
COL_COMPARE  = color.ORANGE          # pair being compared
COL_SWAP     = color.RED             # bars being swapped
COL_SORTED   = color.DARK_GREEN      # finalized bars
COL_BG       = color.WHITE           # background
COL_TEXT     = color.BLACK           # label text



def draw_array(arr, compare=(-1,-1), swapped=False, sorted_from=None):
    """Draw the current state of the array as vertical bars."""
    stddraw.clear(COL_BG)

    bar_w = WIDTH / n

    for i, val in enumerate(arr):
        # Choose bar color based on state
        if sorted_from is not None and i >= sorted_from:
            c = COL_SORTED
        elif swapped and i in compare:
            c = COL_SWAP
        elif i in compare:
            c = COL_COMPARE
        else:
            c = COL_BAR

        
        x      = (i + 0.5) * bar_w
        height = val / (max(arr) + 1) * HEIGHT * 0.85
        stddraw.setPenColor(c)
        stddraw.filledRectangle(x - bar_w * 0.4, 0.05, bar_w * 0.8, height)

        # Draw value label above bar
        stddraw.setPenColor(COL_TEXT)
        stddraw.setFontSize(14)
        stddraw.text(x, height + 0.07, str(val))

    stddraw.show(DELAY * 1000)

# ── PROCESS: 

stddraw.setXscale(0, WIDTH)
stddraw.setYscale(0, HEIGHT)
stddraw.setCanvasSize(600, 400)

comparisons = 0
swaps       = 0

# Draw initial state
draw_array(array)

for paso in range(n - 1):
    swapped_any = False

    for j in range(n - 1 - paso):
        comparisons += 1

        # Sonido de comparación (600 Hz)
        beep(freq=600, duration=100)

        # Highlight the pair being compared
        draw_array(array, compare=(j, j+1), swapped=False,
                   sorted_from=n - paso)

        if array[j] > array[j + 1]:
            # Swap
            array[j], array[j + 1] = array[j + 1], array[j]
            swaps      += 1
            swapped_any = True

            # Sonido de intercambio / swap (300 Hz)
            beep(freq=300, duration=150)

            # Show the swap in red
            draw_array(array, compare=(j, j+1), swapped=True,
                       sorted_from=n - paso)

    # Draw end-of-pass state with one more element finalized
    draw_array(array, sorted_from=n - paso - 1)

    # Early exit if no swaps this pass
    if not swapped_any:
        break

# Final sorted state — all green
draw_array(array, sorted_from=0)

# ── OUTPUT ───────────────────────────────────────────────────

print(f"Sorted array   : {array}")
print(f"Total passes   : {paso + 1}")
print(f"Comparisons    : {comparisons}")
print(f"Swaps          : {swaps}")

stddraw.show()