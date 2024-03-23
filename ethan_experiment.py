import numpy as np
import random
import matplotlib.pyplot as plt

class MapGenerator:
    def __init__(self, size: tuple[int, int], scale=100.0, octaves=6, persistence=0.5, lacunarity=2.0, seed=None):
        self.len, self.wid = size
        self.scale = scale
        self.octaves = octaves
        self.persistence = persistence
        self.lacunarity = lacunarity
        self.seed = seed if seed is not None else random.randint(0, 1000000)

        self.tilemap = self.generate_perlin_noise()
        
    def apply_threshold(self):
        self.tilemap = np.where(self.tilemap < 0, 0, 1)

    def visualize_grid(self):
        plt.imshow(self.tilemap, cmap='ocean', interpolation='nearest')
        plt.colorbar(ticks=[0, 1], label='Land (1) - Water (0)')
        plt.title('Grid Visualization')
        plt.xlabel('Columns')
        plt.ylabel('Rows')
        plt.show()

    def generate_perlin_noise(self):
        def fade(t):
            return 6 * t ** 5 - 15 * t ** 4 + 10 * t ** 3

        def lerp(a, b, t):
            return a + t * (b - a)

        def gradient(hash, x, y):
            directions = np.array([[1, 1], [-1, 1], [1, -1], [-1, -1],
                                   [1, 0], [-1, 0], [0, 1], [0, -1]])
            h = hash & 7
            return directions[h][0] * x + directions[h][1] * y

        def perlin_noise(x, y):
            x0, x1 = int(x), int(x) + 1
            y0, y1 = int(y), int(y) + 1

            xf = x - int(x)
            yf = y - int(y)

            u = fade(xf)
            v = fade(yf)

            n00 = gradient(self.p[x0 % self.wid + self.perm[y0 % self.len]], xf, yf)
            n01 = gradient(self.p[x0 % self.wid + self.perm[y1 % self.len]], xf, yf - 1)
            n10 = gradient(self.p[x1 % self.wid + self.perm[y0 % self.len]], xf - 1, yf)
            n11 = gradient(self.p[x1 % self.wid + self.perm[y1 % self.len]], xf - 1, yf - 1)

            x1_interp = lerp(n00, n10, u)
            x2_interp = lerp(n01, n11, u)
            y_interp = lerp(x1_interp, x2_interp, v)
            return y_interp

        # Generate permutation table based on seed
        np.random.seed(self.seed)
        self.perm = np.random.permutation(np.arange(self.len * 2))
        self.p = np.arange(256, dtype=int)
        np.random.seed(self.seed)
        np.random.shuffle(self.p)

        # Duplicate permutation table to avoid buffer overflow
        self.p = np.concatenate((self.p, self.p))

        # Generate perlin noise
        noise_map = np.zeros((self.len, self.wid), dtype=float)
        for y in range(self.len):
            for x in range(self.wid):
                amplitude = 1
                frequency = 1
                value = 0
                for _ in range(self.octaves):
                    value += perlin_noise(x * frequency / self.scale, y * frequency / self.scale) * amplitude
                    frequency *= self.lacunarity
                    amplitude *= self.persistence
                noise_map[y][x] = value

        return noise_map

# Example usage:
map_size = (100, 100)  # Adjust the size of the map as needed
generator = MapGenerator(map_size)
generator.apply_threshold()
generator.visualize_grid()