import pygame
import os

# 1. Configurações Iniciais
pygame.init()
pygame.mixer.init()

diretorio_base = os.path.dirname(__file__)
# Caminhos das pastas atualizados
pasta_lu = r"C:\Users\vinic\OneDrive\Área de Trabalho\Projeto_Lu\Images\Lu"
pasta_ze = r"C:\Users\vinic\OneDrive\Área de Trabalho\Projeto_Lu\Images\Ze"
pasta_other = r"C:\Users\vinic\OneDrive\Área de Trabalho\Projeto_Lu\Images\Other"
pasta_sounds = os.path.join(diretorio_base, "Sounds")

tela = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Lu-gotchi: Lu & Zé")
relogio = pygame.time.Clock()

fonte_grande = pygame.font.SysFont("Arial", 22, bold=True)
fonte_status = pygame.font.SysFont("Arial", 14, bold=True)
fonte_pequena = pygame.font.SysFont("Arial", 16)

def carregar_img(pasta, nome, tamanho=(120, 120)):
    try:
        # Mantém a extensão se já houver, senão adiciona .png
        nome_arquivo = nome if "." in nome else nome + ".png"
        caminho = os.path.join(pasta, nome_arquivo)
        img = pygame.image.load(caminho).convert_alpha()
        return pygame.transform.scale(img, tamanho)
    except:
        surface = pygame.Surface(tamanho)
        surface.fill((150, 150, 150)) 
        return surface

# --- CARREGAMENTO DE ATIVOS ---
skins = {
    "gato": {
        "feliz": carregar_img(pasta_lu, "Lu_feliz"),
        "triste": carregar_img(pasta_lu, "Lu_triste"),
        "doente": carregar_img(pasta_lu, "Lu_doente"),
        "fome": carregar_img(pasta_lu, "Lu_fome"),
        "morto": carregar_img(pasta_lu, "Lu_morto"),
        "sono": carregar_img(pasta_lu, "Lu_sono"),
        "comendo": carregar_img(pasta_lu, "Lu_comendo")
    },
    "cao": {
        "feliz": carregar_img(pasta_ze, "Ze_feliz"),
        "triste": carregar_img(pasta_ze, "Ze_triste"),
        "doente": carregar_img(pasta_ze, "Ze_doente"),
        "fome": carregar_img(pasta_ze, "Ze_fome"),
        "morto": carregar_img(pasta_ze, "Ze_morto"),
        "sono": carregar_img(pasta_ze, "Ze_sono"),
        "comendo": carregar_img(pasta_ze, "Ze_comendo")
    }
}

# --- IMAGENS DE FUNDO (AGORA NA PASTA OTHER) ---
img_fundo_menu = carregar_img(pasta_other, "Tela Inicial", (600, 400))
img_fundo_skins = carregar_img(pasta_other, "Fundo", (600, 400)) 
img_fundo_dia = carregar_img(pasta_other, "Fundo Dia", (600, 400))
img_fundo_noite = carregar_img(pasta_other, "Fundo Noite", (600, 400))

try:
    som_gato = pygame.mixer.Sound(os.path.join(pasta_sounds, "Audio Gato.mp3"))
    som_cao = pygame.mixer.Sound(os.path.join(pasta_sounds, "Audio Cao.mp3"))
except: pass

def resetar_status():
    return 0.0, 100.0, 100.0, True, 8, 0, 0

fome, felicidade, saude, vivo, hora_jogo, minuto_jogo, dias_passados = resetar_status()
timer_comendo = 0
pet_escolhido = "gato"
estado_atual = "MENU"
musica_atual = ""

rect_iniciar = pygame.Rect(70, 335, 135, 45)   
rect_sair_jogo = pygame.Rect(460, 340, 120, 50) 
rect_voltar_skins = pygame.Rect(20, 340, 100, 40)
btn_comida = pygame.Rect(20, 340, 120, 50)
btn_carinho = pygame.Rect(160, 340, 120, 50)
btn_remedio = pygame.Rect(300, 340, 120, 50)

rodando = True
while rodando:
    if estado_atual in ["MENU", "SKINS"]:
        if musica_atual != "abertura":
            try:
                pygame.mixer.music.load(os.path.join(pasta_sounds, "Audio Pagina Inicial.mp3"))
                pygame.mixer.music.play(-1); musica_atual = "abertura"
            except: pass
    elif estado_atual == "JOGO":
        if musica_atual != "jogo":
            try:
                pygame.mixer.music.load(os.path.join(pasta_sounds, "Audio Jogo.mp3"))
                pygame.mixer.music.play(-1); musica_atual = "jogo"
            except: pass

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT: rodando = False
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if estado_atual == "MENU":
                if rect_iniciar.collidepoint(evento.pos): estado_atual = "SKINS"
            elif estado_atual == "SKINS":
                if rect_voltar_skins.collidepoint(evento.pos): estado_atual = "MENU"
                elif evento.pos[1] < 340:
                    pet_escolhido = "gato" if evento.pos[0] < 300 else "cao"
                    try: (som_gato if pet_escolhido == "gato" else som_cao).play()
                    except: pass
                    estado_atual = "JOGO"
            elif estado_atual == "JOGO":
                if vivo:
                    if btn_comida.collidepoint(evento.pos): 
                        fome = max(0, fome - 30); timer_comendo = 90
                    if btn_carinho.collidepoint(evento.pos): felicidade = min(100, felicidade + 20)
                    if btn_remedio.collidepoint(evento.pos): saude = min(100, saude + 30)
                if rect_sair_jogo.collidepoint(evento.pos):
                    fome, felicidade, saude, vivo, hora_jogo, minuto_jogo, dias_passados = resetar_status()
                    estado_atual = "MENU"

    if estado_atual == "MENU":
        tela.blit(img_fundo_menu, (0, 0))
    elif estado_atual == "SKINS":
        tela.blit(img_fundo_skins, (0, 0))
        pygame.draw.rect(tela, (150, 150, 150), rect_voltar_skins, border_radius=5)
        tela.blit(fonte_status.render("VOLTAR", True, (255, 255, 255)), (40, 352))
        cor_texto_skins = (40, 40, 60)
        tela.blit(fonte_grande.render("ESCOLHA SEU AMIGO", True, cor_texto_skins), (200, 50))
        
        # --- LU ---
        tela.blit(skins["gato"]["feliz"], (120, 180)) 
        pygame.draw.rect(tela, (255, 255, 255, 180), (125, 305, 110, 30), border_radius=5)
        tela.blit(fonte_grande.render("LU", True, cor_texto_skins), (165, 310))
        
        # --- ZÉ ---
        tela.blit(skins["cao"]["feliz"], (360, 230))
        pygame.draw.rect(tela, (255, 255, 255, 180), (345, 355, 150, 30), border_radius=5)
        tela.blit(fonte_grande.render("ZÉ", True, cor_texto_skins), (405, 360))

    elif estado_atual == "JOGO":
        fundo = img_fundo_dia if 6 <= hora_jogo < 18 else img_fundo_noite
        tela.blit(fundo, (0, 0))
        if vivo:
            minuto_jogo += 1 
            if minuto_jogo >= 60: minuto_jogo = 0; hora_jogo += 1
            if hora_jogo >= 24: hora_jogo = 0; dias_passados += 1
            fome += 0.05; felicidade -= 0.03
            if fome > 80 or felicidade < 20: saude -= 0.05
            if saude <= 0: vivo = False
            if timer_comendo > 0: status = "comendo"; timer_comendo -= 1
            elif not (6 <= hora_jogo < 22): status = "sono"
            elif saude < 50: status = "doente"
            elif fome > 70: status = "fome"
            elif felicidade < 40: status = "triste"
            else: status = "feliz"
            imagem_pet = skins[pet_escolhido][status]
        else: imagem_pet = skins[pet_escolhido]["morto"]

        nome_display = "LU" if pet_escolhido == "gato" else "ZÉ"
        cor_txt = (0,0,0) if 6 <= hora_jogo < 18 else (255,255,255)
        tela.blit(fonte_grande.render(nome_display, True, cor_txt), (280, 20))
        tela.blit(imagem_pet, (240, 130))
        tela.blit(fonte_pequena.render(f"DIA: {dias_passados}  HORA: {hora_jogo:02d}:00", True, cor_txt), (20, 20))
        for i, (lbl, val, col) in enumerate([("SAUDE", saude, (0, 200, 0)), ("FELIZ", felicidade, (0, 100, 255)), ("FOME", fome, (255, 140, 0))]):
            pygame.draw.rect(tela, (255, 255, 255), (450, 40 + i*25, 100, 15))
            pygame.draw.rect(tela, col, (450, 40 + i*25, int(max(0, min(100, val))), 15))
            tela.blit(fonte_status.render(lbl, True, cor_txt), (390, 40 + i*25))

        pygame.draw.rect(tela, (220, 220, 220), (0, 330, 600, 70))
        for btn, label, cor in [(btn_comida, "COMIDA", (255, 165, 0)), (btn_carinho, "CARINHO", (0, 191, 255)), (btn_remedio, "REMEDIO", (220, 20, 60)), (rect_sair_jogo, "MENU", (150, 150, 150))]:
            pygame.draw.rect(tela, cor, btn, border_radius=8)
            tela.blit(fonte_status.render(label, True, (255, 255, 255)), (btn.x + 30, btn.y + 15))

    pygame.display.flip()
    relogio.tick(60)
pygame.quit()
