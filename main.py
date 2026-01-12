import pygame
import os
import random

# 1. Configurações e Caminho
pygame.init()
diretorio = r'C:\Users\vinic\OneDrive\Área de Trabalho\Projeto_Lu'
tela = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Lu-gotchi: O Ciclo da Vida")
relogio = pygame.time.Clock()

# 2. Definição de Fontes
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
img_fundo = carregar_img("fundo.png", (600, 400))

# 4. Função para Resetar o Jogo (Posição Central Fixa)
def resetar_jogo():
    # x=240, y=140 centraliza o gato de 120x120 na tela de 600x400
    return 240, 140, 0, 0, 100, 100, True, 0 

# Inicializando variáveis
x, y, vel_x, fome, felicidade, saude, vivo, segundos_vividos = resetar_jogo()
frames_contados = 0
imagem_atual = img_feliz

# --- ESTADOS E BOTÕES ---
estado_atual = "MENU" 
rect_iniciar = pygame.Rect(200, 130, 200, 45)
rect_tutorial = pygame.Rect(200, 190, 200, 45)
rect_sair = pygame.Rect(200, 250, 200, 45)
rect_voltar = pygame.Rect(200, 330, 200, 45)
rect_gato = pygame.Rect(240, 150, 120, 120)
rect_sair_jogo = pygame.Rect(500, 350, 80, 30)

rodando = True
while rodando:
    eventos = pygame.event.get()
    
    if estado_atual == "MENU":
        tela.fill((100, 149, 237))
        pygame.draw.rect(tela, (50, 50, 200), rect_iniciar)
        pygame.draw.rect(tela, (50, 50, 200), rect_tutorial)
        pygame.draw.rect(tela, (200, 50, 50), rect_sair)
        tela.blit(fonte_grande.render("INICIAR", True, (255, 255, 255)), (255, 140))
        tela.blit(fonte_grande.render("TUTORIAL", True, (255, 255, 255)), (245, 200))
        tela.blit(fonte_grande.render("SAIR", True, (255, 255, 255)), (275, 260))

        for evento in eventos:
            if evento.type == pygame.QUIT: rodando = False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if rect_iniciar.collidepoint(evento.pos): estado_atual = "SKINS"
                if rect_tutorial.collidepoint(evento.pos): estado_atual = "TUTORIAL"
                if rect_sair.collidepoint(evento.pos): rodando = False

    elif estado_atual == "TUTORIAL":
        tela.fill((50, 50, 50))
        tela.blit(fonte_grande.render("COMO JOGAR", True, (255, 255, 255)), (230, 40))
        linhas_tutorial = ["Cuide do Lu!", "Pressione [C] Comida", "Pressione [A] Carinho", "Pressione [R] Remedio"]
        pos_y = 100
        for linha in linhas_tutorial:
            tela.blit(fonte_pequena.render(linha, True, (255, 255, 255)), (120, pos_y))
            pos_y += 35
        pygame.draw.rect(tela, (100, 100, 100), rect_voltar)
        tela.blit(fonte_grande.render("VOLTAR", True, (255, 255, 255)), (260, 340))
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if rect_voltar.collidepoint(evento.pos): estado_atual = "MENU"

    elif estado_atual == "SKINS":
        tela.fill((144, 238, 144))
        tela.blit(fonte_grande.render("ESCOLHA SEU PET", True, (0, 0, 0)), (210, 50))
        tela.blit(img_feliz, (240, 150))
        pygame.draw.rect(tela, (0, 0, 0), rect_gato, 2)
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if rect_gato.collidepoint(evento.pos): estado_atual = "JOGO"

    elif estado_atual == "JOGO":
        tela.blit(img_fundo, (0, 0))

        for evento in eventos:
            if evento.type == pygame.QUIT: rodando = False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if rect_sair_jogo.collidepoint(evento.pos):
                    x, y, vel_x, fome, felicidade, saude, vivo, segundos_vividos = resetar_jogo()
                    estado_atual = "MENU"
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

        # --- LÓGICA DE SOBREVIVÊNCIA (Sempre roda se estiver vivo) ---
        if vivo:
            frames_contados += 1
            if frames_contados >= 60:
                segundos_vividos += 1
                frames_contados = 0

            # Degradação dos status (O que faz as barras mudarem)
            fome += 0.08
            felicidade -= 0.05
            if random.randint(1, 1500) == 1: saude = 30
            if fome > 85 or felicidade < 15: saude -= 0.15 

            if saude <= 0:
                saude = 0
                vivo = False

            # Seleção da imagem baseada no status
            if saude < 50: imagem_atual, txt_status, cor_txt = img_doente, "LU DOENTE! [R]", (200, 0, 0)
            elif fome > 70: imagem_atual, txt_status, cor_txt = img_fome, "LU COM FOME! [C]", (255, 100, 0)
            elif felicidade < 40: imagem_atual, txt_status, cor_txt = img_triste, "LU TRISTE... [A]", (0, 0, 150)
            else: imagem_atual, txt_status, cor_txt = img_feliz, "Lu feliz!", (0, 120, 0)
            
            # O X e Y NÃO são alterados aqui, mantendo o gato parado.

        else:
            imagem_atual, txt_status, cor_txt = img_morto, f"Game Over! {segundos_vividos}s", (0, 0, 0)

        # --- DESENHOS ---
        tela.blit(imagem_atual, (x, y)) # Desenha no centro fixo (240, 140)
        tela.blit(fonte_grande.render(txt_status, True, cor_txt), (20, 20))
        tela.blit(fonte_pequena.render(f"Tempo: {segundos_vividos}s", True, (50, 50, 50)), (20, 80))
        
        # Barras de Status Atualizadas
        pygame.draw.rect(tela, (255, 255, 255), (450, 20, 100, 15))
        pygame.draw.rect(tela, (255, 255, 255), (450, 45, 100, 15))
        
        cor_barra_saude = (0, 200, 0) if saude > 40 else (255, 0, 0)
        pygame.draw.rect(tela, cor_barra_saude, (450, 20, int(max(0, saude)), 15))
        pygame.draw.rect(tela, (0, 100, 255), (450, 45, int(max(0, felicidade)), 15))

        tela.blit(fonte_status.render("SAÚDE", True, (0, 0, 0)), (390, 20))
        tela.blit(fonte_status.render("FELIZ", True, (0, 0, 0)), (390, 45))

        # Botão Menu
        pygame.draw.rect(tela, (200, 50, 50), rect_sair_jogo)
        tela.blit(fonte_status.render("MENU", True, (255, 255, 255)), (520, 358))

        if not vivo:
            tela.blit(fonte_grande.render("Pressione [ESPAÇO] para Reiniciar", True, (200, 0, 0)), (140, 180))

    pygame.display.flip()
    relogio.tick(60)

pygame.quit()
