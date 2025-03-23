import pygame
import gym
import numpy as np
import pickle
import time

# -------------------- CONFIGURASI DASAR --------------------
GRID_SIZE = 4              # Frozen Lake 4x4
TILE_SIZE = 100            # Ukuran tile (piksel)
PANEL_WIDTH = 200          # Lebar panel samping (untuk skor, dsb.)
WINDOW_WIDTH = TILE_SIZE * GRID_SIZE + PANEL_WIDTH
WINDOW_HEIGHT = TILE_SIZE * GRID_SIZE

FPS = 60                   # Frame rate
ANIMATION_STEPS = 15       # Jumlah langkah animasi saat agen berpindah
AUTO_DELAY = 0.5           # Delay antar langkah jika auto-sim aktif

# Warna latar panel
PANEL_BG_COLOR = (220, 220, 220)

# -------------------- MUAT Q-TABLE --------------------
with open('Q_table_Frozen_Lake.model', 'rb') as f:
    Q_table_all = pickle.load(f)

# -------------------- PETA FROZEN LAKE --------------------
peta = [
    ['SFFF','FHFH','FFFH','HFFG'],
    ['SFFF','FFHF','HFFF','HFFG'],
    ['SHFF','FHFH','FFFH','HHFG'],
    ['SFFF','HHFF','FFFF','HFFG'],
    ['SFFH','FFFH','HFFH','HHFG']
]

# Pilih peta yang ingin dimainkan
index_peta = 0

# Buat environment gym
env = gym.make("FrozenLake-v0", is_slippery=False, desc=peta[index_peta])
env.reset()

# Ambil Q-table sesuai peta
Q_table = Q_table_all[index_peta]

# -------------------- INISIALISASI PYGAME --------------------
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Frozen Lake - Advanced RL Game")
clock = pygame.time.Clock()

# Font
font_small = pygame.font.SysFont("Arial", 20)
font_medium = pygame.font.SysFont("Arial", 28)
font_large = pygame.font.SysFont("Arial", 40)

# -------------------- LOAD GAMBAR TILE --------------------
# Pastikan file-file gambar (start.png, frozen.png, hole.png, goal.png) ada di folder yang sama
try:
    tile_start = pygame.image.load("start.png")
    tile_frozen = pygame.image.load("frozen.png")
    tile_hole = pygame.image.load("hole.png")
    tile_goal = pygame.image.load("goal.png")
except:
    # Jika gambar tidak ditemukan, kita pakai warna solid (fallback)
    tile_start = pygame.Surface((TILE_SIZE, TILE_SIZE))
    tile_start.fill((50, 205, 50))
    tile_frozen = pygame.Surface((TILE_SIZE, TILE_SIZE))
    tile_frozen.fill((173, 216, 230))
    tile_hole = pygame.Surface((TILE_SIZE, TILE_SIZE))
    tile_hole.fill((139, 69, 19))
    tile_goal = pygame.Surface((TILE_SIZE, TILE_SIZE))
    tile_goal.fill((255, 215, 0))

# Resize agar pas dengan TILE_SIZE
tile_start = pygame.transform.scale(tile_start, (TILE_SIZE, TILE_SIZE))
tile_frozen = pygame.transform.scale(tile_frozen, (TILE_SIZE, TILE_SIZE))
tile_hole = pygame.transform.scale(tile_hole, (TILE_SIZE, TILE_SIZE))
tile_goal = pygame.transform.scale(tile_goal, (TILE_SIZE, TILE_SIZE))

# Dictionary tile
TILE_IMAGES = {
    'S': tile_start,
    'F': tile_frozen,
    'H': tile_hole,
    'G': tile_goal
}

# -------------------- (OPSIONAL) LOAD EFEK SUARA --------------------
# Pastikan file suara .wav / .mp3 tersedia jika ingin pakai
# pygame.mixer.init()
# sound_move = pygame.mixer.Sound("move.wav")
# sound_win = pygame.mixer.Sound("win.wav")
# sound_lose = pygame.mixer.Sound("lose.wav")

# -------------------- VARIABEL GAME --------------------
agent_state = 0
game_over = False
message = ""
simulate = False            # Mode auto
wins = 0                    # Jumlah menang
losses = 0                  # Jumlah kalah
steps_current = 0           # Langkah di episode saat ini

# -------------------- FUNGSI-FUNGSI --------------------
def decode_map(desc):
    """Konversi env.desc jadi list 2D string normal."""
    return [[char.decode('utf-8') if isinstance(char, bytes) else char for char in row] 
            for row in desc]

def draw_grid(env, agent_state, agent_pos_anim):
    """Gambar grid 4x4 dan agen di posisi animasi (agent_pos_anim)."""
    grid = decode_map(env.desc)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            tile_type = grid[i][j]
            tile_img = TILE_IMAGES.get(tile_type, tile_frozen)
            screen.blit(tile_img, (j * TILE_SIZE, i * TILE_SIZE))

    # Gambar agen sebagai lingkaran merah di agent_pos_anim
    pygame.draw.circle(screen, (255, 0, 0), agent_pos_anim, TILE_SIZE // 4)

def get_tile_center(state):
    """Dapatkan posisi (x, y) pusat tile berdasarkan state (0..15)."""
    row, col = divmod(state, GRID_SIZE)
    center_x = col * TILE_SIZE + TILE_SIZE // 2
    center_y = row * TILE_SIZE + TILE_SIZE // 2
    return (center_x, center_y)

def animate_agent_move(start_state, end_state):
    """Animasi perpindahan agen dari start_state ke end_state."""
    start_pos = get_tile_center(start_state)
    end_pos = get_tile_center(end_state)
    for step in range(1, ANIMATION_STEPS + 1):
        t = step / ANIMATION_STEPS
        # Interpolasi linear (x, y)
        current_x = start_pos[0] + t * (end_pos[0] - start_pos[0])
        current_y = start_pos[1] + t * (end_pos[1] - start_pos[1])
        # Gambar
        screen.fill((0, 0, 0))  # clear
        draw_grid(env, agent_state, (current_x, current_y))
        draw_panel()
        pygame.display.flip()
        clock.tick(FPS)

def draw_panel():
    """Gambar panel skor dan info di sisi kanan."""
    panel_rect = pygame.Rect(TILE_SIZE * GRID_SIZE, 0, PANEL_WIDTH, WINDOW_HEIGHT)
    pygame.draw.rect(screen, PANEL_BG_COLOR, panel_rect)

    # Teks Info
    txt_wins = font_medium.render(f"Wins: {wins}", True, (0, 0, 0))
    txt_losses = font_medium.render(f"Losses: {losses}", True, (0, 0, 0))
    txt_steps = font_small.render(f"Langkah saat ini: {steps_current}", True, (0, 0, 0))
    txt_auto = font_small.render(f"Auto: {simulate}", True, (0, 0, 0))

    # Petunjuk
    instructions = [
        "Space: Langkah manual",
        "A: Toggle Auto",
        "R: Reset"
    ]
    
    # Tampilkan
    screen.blit(txt_wins, (TILE_SIZE*GRID_SIZE + 10, 10))
    screen.blit(txt_losses, (TILE_SIZE*GRID_SIZE + 10, 50))
    screen.blit(txt_steps, (TILE_SIZE*GRID_SIZE + 10, 90))
    screen.blit(txt_auto, (TILE_SIZE*GRID_SIZE + 10, 120))

    offset_y = 160
    for instr in instructions:
        txt = font_small.render(instr, True, (0, 0, 0))
        screen.blit(txt, (TILE_SIZE*GRID_SIZE + 10, offset_y))
        offset_y += 25

    # Jika game over, tampilkan pesan
    if game_over:
        txt_gameover = font_large.render(message, True, (200, 0, 0))
        rect_gameover = txt_gameover.get_rect(center=(TILE_SIZE*GRID_SIZE + PANEL_WIDTH//2, WINDOW_HEIGHT//2))
        screen.blit(txt_gameover, rect_gameover)

def reset_game():
    """Reset state game."""
    global env, agent_state, game_over, message, steps_current
    env = gym.make("FrozenLake-v0", is_slippery=False, desc=peta[index_peta])
    env.reset()
    agent_state = 0
    game_over = False
    message = ""
    steps_current = 0

def agent_step():
    """Agen melakukan 1 langkah berdasarkan Q-table."""
    global agent_state, game_over, message, wins, losses, steps_current

    if game_over:
        return

    current_state = agent_state
    best_action = np.argmax(Q_table[current_state])
    next_state, reward, done, _ = env.step(best_action)
    
    # (OPSIONAL) Mainkan efek suara move
    # sound_move.play()

    # Animasi perpindahan
    animate_agent_move(current_state, next_state)

    agent_state = next_state
    steps_current += 1

    if done:
        game_over = True
        if reward == 1:
            message = "MENANG!"
            wins += 1
            # sound_win.play()   # contoh efek suara menang
        else:
            message = "KALAH!"
            losses += 1
            # sound_lose.play()  # contoh efek suara kalah

# -------------------- LOOP UTAMA --------------------
running = True
while running:
    screen.fill((0, 0, 0))
    # Gambar grid
    draw_grid(env, agent_state, get_tile_center(agent_state))
    # Gambar panel
    draw_panel()
    pygame.display.flip()

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not game_over:
                    agent_step()
            elif event.key == pygame.K_a:
                simulate = not simulate
            elif event.key == pygame.K_r:
                reset_game()

    # Jika auto-sim aktif
    if simulate and not game_over:
        agent_step()
        # Tambahkan sedikit delay agar tidak terlalu cepat
        time.sleep(AUTO_DELAY)

    clock.tick(FPS)

pygame.quit()
