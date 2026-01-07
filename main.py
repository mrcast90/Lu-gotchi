import pygame
import os
import random

# 1. Configurações e Caminho
pygame.init()
diretorio = r'C:\Users\vinic\OneDrive\Área de Trabalho\Projeto_Lu'
tela = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Lu-gotchi: O Ciclo da Vida")
relogio = pygame.time.Clock()

# 2. Definição de Fontes (Fora do loop para evitar bugs)
fonte_grande = pygame.font.SysFont("Arial", 22, bold=True)
fonte_status = pygame.font.SysFont("Arial", 14, bold=True)
fonte_pequena = pygame.font.SysFont("Arial", 16)

# 3. Carregar as Imagens
def carregar_img(nome, tamanho=(120, 120)):
    try:
        img = pygame.image.load(os.path.join(diretorio, nome)).convert_alpha()
        return pygame.transform.scale(img, tamanho)
    except:
        surface = pygame.Surface(tamanho)
        surface.fill((200, 200, 200))
        return surface

img_feliz = carregar_img("lu_feliz.png")
img_triste = carregar_img("lu_triste.png")
img_doente = carregar_img("lu_doente.png")
img_fome = carregar_img("lu_fome.png")
img_morto = carregar_img("lu_morto.png")
# Tenta carregar o fundo (600x400)
img_fundo = carregar_img("fundo.png", (600, 400))

# 4. Função para Resetar o Jogo
def resetar_jogo():
    return 250, 240, 2, 0, 100, 100, True, 0 # x, y, vel, fome, felicidade, saude, vivo, tempo

# Inicializando variáveis
x, y, vel_x, fome, felicidade, saude, vivo, segundos_vividos = resetar_jogo()
frames_contados = 0

rodando = True
while rodando:
    # DESENHO DO FUNDO (Substitui o tela.fill)
    tela.blit(img_fundo, (0, 0))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        
        if evento.type == pygame.KEYDOWN:
            if vivo:
                if evento.key == pygame.K_c: fome = 0
                if evento.key == pygame.K_a: felicidade = 100
                if evento.key == pygame.K_r: 
                    if saude < 100: saude = 100
            else:
                if evento.key == pygame.K_SPACE:
                    x, y, vel_x, fome, felicidade, saude, vivo, segundos_vividos = resetar_jogo()
                    frames_contados = 0

    if vivo:
        # Lógica de Tempo
        frames_contados += 1
        if frames_contados >= 60:
            segundos_vividos += 1
            frames_contados = 0

        # Lógica de Degradação
        fome += 0.08
        felicidade -= 0.05
        if random.randint(1, 1500) == 1: saude = 30
        if fome > 85 or felicidade < 15: saude -= 0.15 

        if saude <= 0:
            saude = 0
            vivo = False

        # Troca de Imagens
        if saude < 50:
            imagem_atual = img_doente
            txt_status, cor_txt = "LU ESTÁ DOENTE! [R]", (200, 0, 0)
        elif fome > 70:
            imagem_atual = img_fome
            txt_status, cor_txt = "LU ESTÁ COM FOME! [C]", (255, 100, 0)
        elif felicidade < 40:
            imagem_atual = img_triste
            txt_status, cor_txt = "LU ESTÁ TRISTE... [A]", (0, 0, 150)
        else:
            imagem_atual = img_feliz
            txt_status, cor_txt = "Lu está saudável e feliz!", (0, 120, 0)

        # Movimento
        x += vel_x
        if x > 480 or x < 0: vel_x *= -1
    else:
        imagem_atual = img_morto
        txt_status = f"Fim de jogo! Sobreviveu: {segundos_vividos}s"
        cor_txt = (0, 0, 0)
        vel_x = 0

    # --- DESENHO DA INTERFACE ---
    tela.blit(imagem_atual, (x, y))
    
    # Status e Tempo (Com uma leve sombra para ler melhor sobre o fundo)
    tela.blit(fonte_grande.render(txt_status, True, cor_txt), (20, 20))
    tela.blit(fonte_pequena.render(f"Tempo de Vida: {segundos_vividos}s", True, (50, 50, 50)), (20, 80))
    
    # Barras de Status
    pygame.draw.rect(tela, (255, 255, 255), (450, 20, 100, 15)) # Fundo branco das barras
    pygame.draw.rect(tela, (255, 255, 255), (450, 45, 100, 15))
    
    cor_barra_saude = (0, 200, 0) if saude > 40 else (255, 0, 0)
    pygame.draw.rect(tela, cor_barra_saude, (450, 20, int(max(0, saude)), 15))
    pygame.draw.rect(tela, (0, 100, 255), (450, 45, int(max(0, felicidade)), 15))

    tela.blit(fonte_status.render("SAÚDE", True, (0, 0, 0)), (390, 20))
    tela.blit(fonte_status.render("FELIZ", True, (0, 0, 0)), (390, 45))

    if not vivo:
        tela.blit(fonte_grande.render("Pressione [ESPAÇO] para Reiniciar", True, (200, 0, 0)), (140, 180))

    pygame.display.flip()
    relogio.tick(60)

pygame.quit()
