import pygame
import gym
import numpy as np
import pickle
import time

# Muat Q_table yang telah dilatih sebelumnya
with open('Q_table_Frozen_Lake.model', 'rb') as f:
    Q_table_all = pickle.load(f)

# Daftar peta yang digunakan
peta = [
    ['SFFF','FHFH','FFFH','HFFG'],
    ['SFFF','FFHF','HFFF','HFFG'],
    ['SHFF','FHFH','FFFH','HHFG'],
    ['SFFF','HHFF','FFFF','HFFG'],
    ['SFFH','FFFH','HFFH','HHFG']
]

# Pilih peta yang akan dimainkan (misalnya index 0)
index_peta = 0
env = gym.make("FrozenLake-v0", is_slippery=False, desc=peta[index_peta])
env.reset()

# Konfigurasi tampilan grid dan kontrol
TILE_SIZE = 100             # Ukuran tiap petak dalam piksel
GRID_SIZE = 4               # Ukuran grid 4x4
PANEL_HEIGHT = 100          # Tinggi panel kontrol
WIDTH = TILE_SIZE * GRID_SIZE
HEIGHT = TILE_SIZE * GRID_SIZE + PANEL_HEIGHT

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Frozen Lake - Reinforcement Learning Game")

# Warna untuk tiap jenis petak
COLORS = {
    'S': (50, 205, 50),     # hijau untuk Start
    'F': (173, 216, 230),   # biru muda untuk Frozen
    'H': (139, 69, 19),     # coklat untuk Hole
    'G': (255, 215, 0)      # emas untuk Goal
}

# Dapatkan Q_table untuk peta yang dipilih
Q_table = Q_table_all[index_peta]

# Inisialisasi variabel game
agent_state = 0
game_over = False
message = ""
simulate = False         # Mode auto simulasi (toggle dengan tombol A)
simulate_delay = 0.5     # Delay antar langkah pada mode auto (detik)

pygame.init()
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)
big_font = pygame.font.SysFont("Arial", 36)

def draw_grid(env, agent_state):
    # Konversi grid (env.desc) menjadi list 2D string
    grid = [[tile.decode('utf-8') if isinstance(tile, bytes) else tile for tile in row] for row in env.desc]
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            tile = grid[i][j]
            color = COLORS.get(tile, (200, 200, 200))
            rect = pygame.Rect(j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 2)
    # Gambar agen sebagai lingkaran merah
    agent_pos = np.unravel_index(agent_state, (GRID_SIZE, GRID_SIZE))
    center_x = agent_pos[1] * TILE_SIZE + TILE_SIZE // 2
    center_y = agent_pos[0] * TILE_SIZE + TILE_SIZE // 2
    pygame.draw.circle(screen, (255, 0, 0), (center_x, center_y), TILE_SIZE // 4)

def reset_game():
    global agent_state, game_over, message, env
    env = gym.make("FrozenLake-v0", is_slippery=False, desc=peta[index_peta])
    env.reset()
    agent_state = 0
    game_over = False
    message = ""

# Loop utama game
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Kontrol keyboard
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                # Lakukan satu langkah simulasi manual
                best_action = np.argmax(Q_table[agent_state])
                next_state, reward, done, _ = env.step(best_action)
                agent_state = next_state
                if done:
                    game_over = True
                    message = "MENANG!" if reward == 1 else "KALAH!"
            elif event.key == pygame.K_r:
                reset_game()
            elif event.key == pygame.K_a:
                simulate = not simulate  # Toggle auto simulasi

    # Jika mode auto aktif dan game belum selesai
    if simulate and not game_over:
        best_action = np.argmax(Q_table[agent_state])
        next_state, reward, done, _ = env.step(best_action)
        agent_state = next_state
        if done:
            game_over = True
            message = "MENANG!" if reward == 1 else "KALAH!"
        time.sleep(simulate_delay)
    
    # Gambar ulang layar
    screen.fill((255, 255, 255))
    draw_grid(env, agent_state)
    
    # Gambar panel kontrol di bagian bawah
    panel_rect = pygame.Rect(0, TILE_SIZE * GRID_SIZE, WIDTH, PANEL_HEIGHT)
    pygame.draw.rect(screen, (220, 220, 220), panel_rect)
    
    # Tampilkan petunjuk kontrol
    instructions = [
        "Tekan SPACE: Langkah manual",
        "Tekan A: Toggle Auto Simulation",
        "Tekan R: Reset Game"
    ]
    for idx, text in enumerate(instructions):
        txt_surface = font.render(text, True, (0, 0, 0))
        screen.blit(txt_surface, (10, TILE_SIZE * GRID_SIZE + 10 + idx * 25))
    
    # Jika game selesai, tampilkan pesan kemenangan atau kekalahan di tengah grid
    if game_over:
        txt_gameover = big_font.render(message, True, (0, 0, 0))
        text_rect = txt_gameover.get_rect(center=(WIDTH // 2, (TILE_SIZE * GRID_SIZE) // 2))
        screen.blit(txt_gameover, text_rect)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
