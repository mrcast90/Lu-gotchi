
import pygame
import os

# 1. Configurações Iniciais
pygame.init()
pygame.mixer.init()
diretorio = os.path.dirname(__file__) 
tela = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Lu-gotchi: O Ciclo da Vida")
relogio = pygame.time.Clock()

# 2. Definição de Fontes
fonte_grande = pygame.font.SysFont("Arial", 22, bold=True)
fonte_status = pygame.font.SysFont("Arial", 14, bold=True)
fonte_pequena = pygame.font.SysFont("Arial", 16)

# 3. Função para Carregar Imagens
def carregar_img(nome, tamanho=(120, 120)):
    try:
        caminho = os.path.join(diretorio, nome)
        if not "." in nome: caminho += ".png"
        img = pygame.image.load(caminho).convert_alpha()
        return pygame.transform.scale(img, tamanho)
    except:
        surface = pygame.Surface(tamanho)
        surface.fill((200, 200, 200))
        return surface

# --- CARREGAMENTO DE ATIVOS ---
skins = {
    "gato": {
        "feliz": carregar_img("lu_feliz"),
        "triste": carregar_img("lu_triste"),
        "doente": carregar_img("lu_doente"),
        "fome": carregar_img("lu_fome"),
        "morto": carregar_img("lu_morto")
    },
    "cao": {
        "feliz": carregar_img("Lu_cao_feliz"), 
        "triste": carregar_img("lu_cao_triste"),
        "doente": carregar_img("lu_cao_doente"),
        "fome": carregar_img("lu_cao_fome"),
        "morto": carregar_img("lu_cao_morto")
    }
}

img_fundo_jogo = carregar_img("fundo", (600, 400))
img_fundo_menu = carregar_img("tela inicial", (600, 400))

# Sons (FASE 4)
try:
    som_gato = pygame.mixer.Sound(os.path.join(diretorio, "Audio Gato.mp3"))
    som_cao = pygame.mixer.Sound(os.path.join(diretorio, "Audio Cao.mp3"))
except:
    print("Aviso: Sons de seleção não encontrados.")

# 4. Variáveis de Estado
def resetar_status():
    return 0.0, 100.0, 100.0, True, 0

fome, felicidade, saude, vivo, segundos_vividos = resetar_status()
x, y = 240, 130
frames_contados = 0
pet_escolhido = "gato"
estado_atual = "MENU"
musica_atual = ""

# --- DEFINIÇÃO DE BOTÕES ---
rect_iniciar = pygame.Rect(70, 335, 135, 45)   
rect_tutorial = pygame.Rect(235, 335, 135, 45) 
rect_sair = pygame.Rect(400, 335, 135, 45)      
rect_voltar = pygame.Rect(200, 330, 200, 45)    

# BOTÃO MENU (Embaixo à direita)
rect_sair_jogo = pygame.Rect(460, 340, 120, 50) 

btn_comida = pygame.Rect(20, 340, 120, 50)
btn_carinho = pygame.Rect(160, 340, 120, 50)
btn_remedio = pygame.Rect(300, 340, 120, 50)

rodando = True
while rodando:
    # --- LÓGICA DE ÁUDIO ---
    if estado_atual in ["MENU", "TUTORIAL", "SKINS"]:
        if musica_atual != "abertura":
            try:
                pygame.mixer.music.load(os.path.join(diretorio, "Audio Pagina Inicial.mp3"))
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)
                musica_atual = "abertura"
            except: pass
    elif estado_atual == "JOGO":
        if musica_atual != "jogo":
            try:
                pygame.mixer.music.load(os.path.join(diretorio, "Audio Jogo.mp3"))
                pygame.mixer.music.set_volume(0.4)
                pygame.mixer.music.play(-1)
                musica_atual = "jogo"
            except: pass

    eventos = pygame.event.get()
    for evento in eventos:
        if evento.type == pygame.QUIT:
            rodando = False
            
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if estado_atual == "MENU":
                if rect_iniciar.collidepoint(evento.pos): estado_atual = "SKINS"
                elif rect_tutorial.collidepoint(evento.pos): estado_atual = "TUTORIAL"
                elif rect_sair.collidepoint(evento.pos): rodando = False
            elif estado_atual == "TUTORIAL":
                if rect_voltar.collidepoint(evento.pos): estado_atual = "MENU"
            elif estado_atual == "SKINS":
                if evento.pos[0] < 300:
                    pet_escolhido = "gato"
                    try: som_gato.play()
                    except: pass
                else:
                    pet_escolhido = "cao"
                    try: som_cao.play()
                    except: pass
                estado_atual = "JOGO"
            elif estado_atual == "JOGO":
                if vivo:
                    if btn_comida.collidepoint(evento.pos): fome = 0
                    if btn_carinho.collidepoint(evento.pos): felicidade = 100
                    if btn_remedio.collidepoint(evento.pos): saude = 100
                if rect_sair_jogo.collidepoint(evento.pos):
                    fome, felicidade, saude, vivo, segundos_vividos = resetar_status()
                    estado_atual = "MENU"

    # --- DESENHO DAS TELAS ---
    if estado_atual == "MENU":
        tela.blit(img_fundo_menu, (0, 0))

    elif estado_atual == "TUTORIAL":
        tela.fill((40, 40, 40))
        tela.blit(fonte_grande.render("COMO JOGAR", True, (255, 255, 255)), (240, 40))
        pygame.draw.rect(tela, (100, 100, 100), rect_voltar, border_radius=5)
        tela.blit(fonte_grande.render("VOLTAR", True, (255, 255, 255)), (260, 340))

    elif estado_atual == "SKINS":
        tela.fill((245, 245, 245))
        tela.blit(fonte_grande.render("ESCOLHA SEU AMIGO", True, (0, 0, 0)), (200, 50))
        # Gatinho
        tela.blit(skins["gato"]["feliz"], (120, 150))
        tela.blit(fonte_grande.render("GATINHO", True, (0, 0, 0)), (135, 280))
        # Cachorrinho
        tela.blit(skins["cao"]["feliz"], (360, 150))
        tela.blit(fonte_grande.render("CACHORRINHO", True, (0, 0, 0)), (345, 280))

    elif estado_atual == "JOGO":
        tela.blit(img_fundo_jogo, (0, 0))
        if vivo:
            frames_contados += 1
            if frames_contados >= 60: segundos_vividos += 1; frames_contados = 0
            fome += 0.1; felicidade -= 0.05
            if fome > 80 or felicidade < 20: saude -= 0.1
            if saude <= 0: saude, vivo = 0, False
            status = "feliz"
            if saude < 50: status = "doente"
            elif fome > 70: status = "fome"
            elif felicidade < 40: status = "triste"
            imagem_pet = skins[pet_escolhido][status]
        else: imagem_pet = skins[pet_escolhido]["morto"]

        tela.blit(imagem_pet, (x, y))
        tela.blit(fonte_pequena.render(f"Tempo: {segundos_vividos}s", True, (0, 0, 0)), (20, 20))

        # --- RECOLOCANDO OS NOMES DAS BARRAS ---
        pygame.draw.rect(tela, (255, 255, 255), (450, 40, 100, 15))
        pygame.draw.rect(tela, (0, 200, 0), (450, 40, int(max(0, saude)), 15))
        tela.blit(fonte_status.render("SAUDE", True, (0, 0, 0)), (390, 40))

        pygame.draw.rect(tela, (255, 255, 255), (450, 65, 100, 15))
        pygame.draw.rect(tela, (0, 100, 255), (450, 65, int(max(0, felicidade)), 15))
        tela.blit(fonte_status.render("FELIZ", True, (0, 0, 0)), (390, 65))

        pygame.draw.rect(tela, (255, 255, 255), (450, 90, 100, 15))
        pygame.draw.rect(tela, (255, 140, 0), (450, 90, int(min(100, fome)), 15))
        tela.blit(fonte_status.render("FOME", True, (0, 0, 0)), (390, 90))

        # --- BOTÕES E RODAPÉ ---
        pygame.draw.rect(tela, (220, 220, 220), (0, 330, 600, 70))
        pygame.draw.rect(tela, (255, 165, 0), btn_comida, border_radius=8)
        pygame.draw.rect(tela, (0, 191, 255), btn_carinho, border_radius=8)
        pygame.draw.rect(tela, (220, 20, 60), btn_remedio, border_radius=8)
        pygame.draw.rect(tela, (150, 150, 150), rect_sair_jogo, border_radius=8)
        
        tela.blit(fonte_status.render("COMIDA (C)", True, (255, 255, 255)), (35, 355))
        tela.blit(fonte_status.render("CARINHO (A)", True, (255, 255, 255)), (175, 355))
        tela.blit(fonte_status.render("REMEDIO (R)", True, (255, 255, 255)), (315, 355))
        tela.blit(fonte_status.render("MENU", True, (255, 255, 255)), (500, 355))

    pygame.display.flip()
    relogio.tick(60)
pygame.quit()
