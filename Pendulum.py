import os
import pygame as pg
import numpy as np

# CONSTANTS:
FPS = 240


# Make worlds most accurate pendulum simulator, shape size / area input, material, air density, length of string...
# Show the wave in a box in the program.


def ToPyGameCoordsC(x, y, radius, width, height):
    return (int(x * (width-radius)), int((height-radius)-y * height + radius))


def DrawCircle(pos, color, screen, radius):
    """
    Function to draw circle, given a position and a color
    """
    pg.draw.line(screen, (255, 255, 255), (400, 400), pos)
    pg.draw.circle(screen, color, pos, radius)


def main():
    # PyGame stuffs:
    pg.font.init()
    font_size = 16
    font = pg.font.SysFont('Consolas', font_size)

    # Initial Values:
    g = 9.81  # m/s^2
    dt = 0.01  # s
    time = 100.0  # s
    D = 0.0018  # Unit-less
    L = 0.5  # m
    m = 10000  # kg
    theta_0 = np.radians(45)
    i = 0

    # Initializing lists
    n = int(round(time / dt))
    t = np.zeros(n, float)
    s = np.zeros(n, float)
    v = np.zeros(n, float)
    x = np.zeros(n, float)
    y = np.zeros(n, float)

    v[0] = 0.0
    s[0] = theta_0

    # Initialize Pygame
    pg.init()

    # Set up the display
    flags = pg.DOUBLEBUF
    screen = pg.display.set_mode((800, 800), flags)
    clock = pg.time.Clock()

    # Main loop
    running = True
    while running:
        # Handle events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False

        # Update game state here

        # If numpy array has been filled completely, just start overwriting from beginning again.
        if i >= n - 1:
            i = 0
            t[0] = t[n-1]
            v[0] = v[n-1]
            s[0] = s[n-1]
            x[0] = L - L * (np.sin(s[0] / L))
            y[0] = L - L * (np.cos(s[0] / L))

        # Euler's Method:
        t[i + 1] = t[i] + dt
        a = -D / m * v[i] * abs(v[i]) - g * np.sin(s[i] / L)    # Acceleration function
        v[i + 1] = v[i] + a * dt    # Velocity according to acceleration
        s[i + 1] = s[i] + v[i + 1] * dt     # Position according to velocity

        # Just calculating current x and y coordinates from position:
        x[i+1] = L - L * (np.sin(s[i+1] / L))
        y[i+1] = L - L * (np.cos(s[i+1] / L))


        screen.fill((0, 0, 0))  # Clear the screen with black
        velocity = font.render(f"Velocity: {v[i]:.2f}", True, (255, 255, 255))
        acceleration = font.render(f"Acceleration: {a:.2f}", True, (255, 255, 255))
        amplitude = font.render(f"Amplitude: {y[i]:.2f}", True, (255, 255, 255))
        time = font.render(f"Running time: {t[i]:.2f}", True, (255, 255, 255))
        screen.blit(velocity, (0, 0))   # Draws the velocity at coordinates 0, 0
        screen.blit(acceleration, (0, font_size))   # Draws the acceleration at coordinates 0, font_size (16)
        screen.blit(amplitude, (0, font_size*2))    # Draws the amplitude at coordinates 0, font_size*2 (32)
        screen.blit(time, (0, font_size*3))     # Draws the time at coordinates 0, font_size*3 (48)


        # Draw the rod from the origin aswell:
        # Somehow ...
        DrawCircle(ToPyGameCoordsC(x[i+1], y[i+1], 10, screen.get_width(), screen.get_height()), (235, 244, 123), screen, 10)

        i += 1

        if a == 0 and v[i+1] == 0:
            print(t[i])

        # Update the display
        pg.display.flip()

        # Cap the frame rate
        clock.tick(60)

    pg.quit()
    os._exit(0)


if __name__ == '__main__':
    main()

