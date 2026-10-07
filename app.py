import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import sqlite3
import requests
import io
import urllib.parse
import json
import base64
from datetime import datetime

# ── Configuração da Página Streamlit ──────────────────────────────────────────
st.set_page_config(
    page_title="Plataforma Geradora de Conteúdo Cristão & Motivacional",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Estilização Personalizada (CSS) ───────────────────────────────────────────
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stButton>button {
        background: linear-gradient(135deg, #d4af37 0%, #aa7c11 100%);
        color: #000000 !important;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.4);
    }
    .card-box {
        background-color: #1a1f2c;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #2d3548;
        margin-bottom: 20px;
    }
    .gold-header {
        color: #d4af37;
        font-family: 'Georgia', serif;
        font-weight: bold;
    }
    .tag-badge {
        background-color: #262c3a;
        color: #d4af37;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 12px;
        border: 1px solid #3d465c;
    }
</style>
""", unsafe_allow_html=True)

# ── Inicialização do Banco de Dados SQLite ────────────────────────────────────
DB_FILE = "banco_conteudo.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS conteudos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT,
            titulo TEXT,
            texto TEXT,
            legenda TEXT,
            hashtags TEXT,
            prompt_ia TEXT,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_to_db(tipo, titulo, texto, legenda="", hashtags="", prompt_ia=""):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        INSERT INTO conteudos (tipo, titulo, texto, legenda, hashtags, prompt_ia)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (tipo, titulo, texto, legenda, hashtags, prompt_ia))
    conn.commit()
    conn.close()

def get_all_contents(filter_tipo=None, search_query=None):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    query = "SELECT id, tipo, titulo, texto, legenda, hashtags, prompt_ia, data_criacao FROM conteudos WHERE 1=1"
    params = []
    
    if filter_tipo and filter_tipo != "Todos":
        query += " AND tipo = ?"
        params.append(filter_tipo)
        
    if search_query:
        query += " AND (titulo LIKE ? OR texto LIKE ? OR legenda LIKE ?)"
        params.extend([f"%{search_query}%", f"%{search_query}%", f"%{search_query}%"])
        
    query += " ORDER BY id DESC"
    c.execute(query, params)
    rows = c.fetchall()
    conn.close()
    return rows

init_db()

# ── Motor de Renderização de Imagens com Texto (Pillow) ───────────────────────
def generate_procedural_background(width, height, style="Dourado Celestial"):
    img = Image.new("RGB", (width, height), color=(15, 18, 25))
    draw = ImageDraw.Draw(img)
    
    if style == "Dourado Celestial":
        for y in range(height):
            r = int(15 + (45 - 15) * (y / height))
            g = int(18 + (35 - 18) * (y / height))
            b = int(25 + (20 - 25) * (y / height))
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        # Partículas de luz
        import random
        random.seed(42)
        for _ in range(120):
            rx = random.randint(0, width)
            ry = random.randint(0, height)
            rad = random.randint(2, 6)
            opacity = random.randint(50, 200)
            draw.ellipse([rx - rad, ry - rad, rx + rad, ry + rad], fill=(212, 175, 55, opacity))
            
    elif style == "Tempestade e Luz":
        for y in range(height):
            r = int(10 + (25 - 10) * (y / height))
            g = int(15 + (40 - 15) * (y / height))
            b = int(30 + (60 - 30) * (y / height))
            draw.line([(0, y), (width, y)], fill=(r, g, b))
            
    elif style == "Pôr do Sol no Monte":
        for y in range(height):
            r = int(70 + (20 - 70) * (y / height))
            g = int(35 + (15 - 35) * (y / height))
            b = int(25 + (30 - 25) * (y / height))
            draw.line([(0, y), (width, y)], fill=(r, g, b))
            
    else: # Quarto de Oração / Escuro Minimalista
        for y in range(height):
            v = int(10 + (25 - 10) * (y / height))
            draw.line([(0, y), (width, y)], fill=(v, v, v + 5))
            
    return img

def fetch_pollinations_image(prompt_text, aspect_ratio="1:1"):
    if aspect_ratio == "1:1":
        w, h = 1080, 1080
    else:
        w, h = 1080, 1920
        
    encoded = urllib.parse.quote(prompt_text)
    url = f"https://image.pollinations.ai/prompt/{encoded}?width={w}&height={h}&nologo=true&seed=123"
    try:
        res = requests.get(url, timeout=6)
        if res.status_code == 200:
            return Image.open(io.BytesIO(res.content)).convert("RGB")
    except Exception:
        pass
    return None

def render_post_card(title, text, cta, handle, bg_image=None, bg_style="Dourado Celestial", 
                     aspect_ratio="1:1", font_color=(255, 215, 0), dark_overlay=160, border_style="Dourado Elegante"):
    if aspect_ratio == "1:1":
        width, height = 1080, 1080
    else:
        width, height = 1080, 1920
        
    if bg_image:
        base_img = bg_image.convert("RGB").resize((width, height))
    else:
        base_img = generate_procedural_background(width, height, style=bg_style)
        
    # Overlay escuro para contraste
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, dark_overlay))
    base_img.paste(overlay, (0, 0), overlay)
    
    draw = ImageDraw.Draw(base_img)
    
    # Carregamento de Fontes
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", int(width * 0.042))
        text_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", int(width * 0.032))
        sub_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf", int(width * 0.024))
    except Exception:
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
        sub_font = ImageFont.load_default()
        
    # Moldura Decorativa
    if border_style == "Dourado Elegante":
        draw.rectangle([35, 35, width - 35, height - 35], outline=(212, 175, 55), width=3)
        draw.rectangle([42, 42, width - 42, height - 42], outline=(212, 175, 55), width=1)
    elif border_style == "Minimalista":
        draw.rectangle([40, 40, width - 40, height - 40], outline=(180, 180, 180), width=2)

    # Renderização do Título (Em Destaque)
    if title:
        draw.text((width // 2, int(height * 0.12)), title.upper(), fill=font_color, font=title_font, anchor="mm")
        
    # Quebra de Linhas Automática para o Texto Principal
    if text:
        words = text.split()
        lines = []
        current_line = []
        max_line_width = width - 180
        
        for word in words:
            current_line.append(word)
            test_line = " ".join(current_line)
            bbox = draw.textbbox((0, 0), test_line, font=text_font)
            if bbox[2] > max_line_width:
                current_line.pop()
                lines.append(" ".join(current_line))
                current_line = [word]
        if current_line:
            lines.append(" ".join(current_line))
            
        y_start = height // 2 - (len(lines) * int(width * 0.022))
        for line in lines:
            draw.text((width // 2, y_start), line, fill=(255, 255, 255), font=text_font, anchor="mm")
            y_start += int(width * 0.048)
            
    # Chamada para Ação (CTA)
    if cta:
        draw.text((width // 2, int(height * 0.84)), cta.upper(), fill=(212, 175, 55), font=sub_font, anchor="mm")
        
    # Identificação / Chave PIX / Handle
    if handle:
        draw.text((width // 2, int(height * 0.91)), handle, fill=(190, 190, 190), font=sub_font, anchor="mm")
        
    return base_img

# ── BARRA LATERAL (NAV E CONFIGURAÇÕES) ───────────────────────────────────────
st.sidebar.markdown("<h2 class='gold-header'>✨ Mãos Amigas Studio</h2>", unsafe_allow_html=True)
st.sidebar.markdown("Plataforma de Criação de Conteúdo Cristão & Motivacional")

chave_pix_input = st.sidebar.text_input("Chave PIX Cadastrada:", value="maosamigasrelogiofinal@gmail.com")
handle_input = st.sidebar.text_input("Assinatura / Instagram:", value="@MãosAmigas")

st.sidebar.markdown("---")
st.sidebar.info("💡 **Dica de Escala:** Esta plataforma gera artes com texto integrado, legendas prontas e salva tudo no seu Banco de Dados local.")

# ── CABEÇALHO PRINCIPAL ───────────────────────────────────────────────────────
st.title("🚀 Central de Criação de Conteúdo em Grande Escala")
st.markdown("Crie posts completos de imagem com texto integrado, roteiros de vídeos, devocionais e gerencie todo o seu acervo.")

# ── ABAS DA APLICAÇÃO ────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "🎨 1. Criador 1-Clique",
    "🖼️ 2. Estúdio Visual & Upload",
    "🎬 3. Gerador de Vídeos",
    "📚 4. Banco de Dados",
    "📘 5. E-books & Devocionais",
    "💬 6. Disparos WhatsApp/Telegram",
    "💛 7. Monetização & PIX"
])

# ── ABA 1: CRIADOR 1-CLIQUE ───────────────────────────────────────────────────
with tab1:
    st.markdown("<h3 class='gold-header'>Gerador Completo de Post com Imagem e Texto Integrado</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        categoria_tema = st.selectbox("Escolha o Tema do Conteúdo:", [
            "Davi e Golias - Superando Gigantes",
            "Daniel na Cova dos Leões - Fidelidade",
            "A Oração no Quarto Escuro - Intimidade",
            "Silêncio de Deus - A Sabedoria da Espera",
            "Ansiedade e Paz - Cuidado Divino",
            "Força do Recomeço - Resiliência e Fé",
            "A Mulher do Fluxo de Sangue - Fé Corajosa",
            "O Filho Pródigo - O Amor e o Perdão do Pai",
            "Personalizado (Digite o seu tema abaixo)"
        ])
        
        tema_custom = st.text_input("Tema Personalizado (opcional):", placeholder="Ex: Vitória no Deserto, A Força do Trabalho...")
        
        aspecto_ratio = st.radio("Formato da Imagem:", ["1:1 (Feed Instagram/Facebook)", "9:16 (Stories/Reels)"])
        estilo_fundo = st.selectbox("Estilo do Fundo Visual:", [
            "Dourado Celestial", 
            "Tempestade e Luz", 
            "Pôr do Sol no Monte", 
            "Quarto de Oração Escuro",
            "IA Generativa (Pollinations Online)"
        ])
        
        btn_gerar_tudo = st.button("✨ Gerar Post Completo em 1 Clique")
        
    with col2:
        if btn_gerar_tudo:
            tema_final = tema_custom if tema_custom else categoria_tema
            
            # Lógica do Banco de Dados de Conteúdo
            if "Davi" in tema_final:
                titulo_post = "VOCÊ VAI VENCER ESSE GIGANTE"
                texto_post = "O tamanho do seu problema não importa quando a sua fé está firmada naquele que criou os céus e a terra."
                legenda_post = "Não olhe para a força do gigante, olhe para a grandeza daquele que luta por você. Digite AMÉM se você crê na vitória!"
                hashtags = "#daviaegolias #fémovetanhas #vitoriaemdeus #cristao #deusnocomando"
                prompt_ia = "Ancient David facing giant Goliath in rocky valley sunset cinematic lighting 8k"
            elif "Ansiedade" in tema_final or "Paz" in tema_final:
                titulo_post = "ACALME O SEU CORAÇÃO HOJE"
                texto_post = "A paz mental é o presente de Deus para quem aprende a entregar o amanhã nas mãos de quem tudo pode."
                legenda_post = "Deus já está cuidando do que você não consegue resolver. Respire fundo e confie. Salve este post para rever quando precisar!"
                hashtags = "#pazinterior #ansiedadetemcura #deuscuidadetime #palavradedeus"
                prompt_ia = "Serene person standing by calm reflective lake at dawn warm sunlight rays cinematic 8k"
            else:
                titulo_post = "DEUS TEM UM RECOMEÇO PARA VOCÊ"
                texto_post = "O seu passado não limita o seu futuro. Quando Deus decide abrir uma porta, ninguém pode fechar."
                legenda_post = "Prepare-se para o novo ciclo de bênçãos na sua vida. Compartilhe esta mensagem com alguém que precisa de esperança!"
                hashtags = "#recomeço #esperança #fe #mensagemdedeus #devocionaldiario"
                prompt_ia = "Glorious ray of heavenly light piercing through dark clouds over a mountain peak 8k"

            st.success("Post gerado com sucesso!")
            
            ratio_code = "1:1" if "1:1" in aspecto_ratio else "9:16"
            
            # Tentar IA se selecionado
            bg_img_obj = None
            if estilo_fundo == "IA Generativa (Pollinations Online)":
                with st.spinner("Gerando imagem via Inteligência Artificial..."):
                    bg_img_obj = fetch_pollinations_image(prompt_ia, aspect_ratio=ratio_code)
                    
            card_img = render_post_card(
                title=titulo_post,
                text=texto_post,
                cta="DIGITE AMÉM E COMPARTILHE",
                handle=handle_input,
                bg_image=bg_img_obj,
                bg_style=estilo_fundo,
                aspect_ratio=ratio_code
            )
            
            # Exibir Imagem Renderizada
            st.image(card_img, caption="Arte do Post Renderizada com Sucesso", use_column_width=True)
            
            # Botão de Download PNG
            img_byte_arr = io.BytesIO()
            card_img.save(img_byte_arr, format='PNG')
            st.download_button(
                label="📥 Baixar Imagem do Post (PNG Alta Qualidade)",
                data=img_byte_arr.getvalue(),
                file_name=f"post_cristao_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                mime="image/png"
            )
            
            # Exibir Legenda e Hashtags
            st.markdown("**📝 Legenda Pronta para Redes Sociais:**")
            st.code(f"{legenda_post}\n\n{hashtags}")
            
            # Salvar no Banco de Dados
            save_to_db("Post Imagem", titulo_post, texto_post, legenda_post, hashtags, prompt_ia)

# ── ABA 2: ESTÚDIO VISUAL & UPLOAD DE REFERÊNCIA ──────────────────────────────
with tab2:
    st.markdown("<h3 class='gold-header'>Estúdio Visual - Faça Upload e Crie Seu Próprio Card</h3>", unsafe_allow_html=True)
    
    c_up1, c_up2 = st.columns([1, 1])
    
    with c_up1:
        uploaded_file = st.file_uploader("Suba sua imagem de fundo / referência (PNG ou JPG):", type=["png", "jpg", "jpeg"])
        
        title_custom = st.text_input("Título da Arte:", value="PROMESSA DE DEUS")
        text_custom = st.text_area("Texto / Versículo Principal:", value="Tudo posso naquele que me fortalece. Não temais, porque Eu sou contigo.")
        cta_custom = st.text_input("Chamada para Ação (CTA):", value="SALVE E COMPARTILHE")
        
        overlay_darkness = st.slider("Escuridão do Fundo (Para Dar Leitura):", 0, 255, 160)
        aspect_ratio_edit = st.selectbox("Formato:", ["1:1 (Feed)", "9:16 (Stories)"])
        
    with c_up2:
        if uploaded_file is not None:
            user_bg = Image.open(uploaded_file)
            r_code = "1:1" if "1:1" in aspect_ratio_edit else "9:16"
            
            edited_card = render_post_card(
                title=title_custom,
                text=text_custom,
                cta=cta_custom,
                handle=handle_input,
                bg_image=user_bg,
                aspect_ratio=r_code,
                dark_overlay=overlay_darkness
            )
            
            st.image(edited_card, caption="Sua Imagem com Texto Editado", use_column_width=True)
            
            img_b = io.BytesIO()
            edited_card.save(img_b, format='PNG')
            st.download_button(
                label="📥 Baixar Sua Arte Personalizada (PNG)",
                data=img_b.getvalue(),
                file_name="sua_arte_custom.png",
                mime="image/png"
            )
        else:
            st.info("👆 Faça o upload de uma foto acima para transformar na sua arte com texto!")

# ── ABA 3: GERADOR DE VÍDEOS & ROTEIROS ───────────────────────────────────────
with tab3:
    st.markdown("<h3 class='gold-header'>Gerador de Roteiros e Prompts para Vídeos Curtos</h3>", unsafe_allow_html=True)
    
    v_col1, v_col2 = st.columns([1, 1])
    
    with v_col1:
        tipo_video = st.selectbox("Estilo do Vídeo:", ["Lição Bíblica Narrada", "Motivacional de Superação", "Oração e Conforto"])
        tema_video = st.text_input("Tema do Vídeo:", value="Neemias e a Reconstrução dos Muros")
        
        if st.button("🎬 Gerar Pacote Completo de Vídeo"):
            hook_v = "Não desça do muro para responder quem só quer te ver parar!"
            script_v = "Quando Neemias estava reconstruindo os muros de Jerusalém, zombadores tentaram fazê-lo parar. Mas ele permaneceu focado na missão. O seu sucesso em Deus é a melhor resposta para qualquer crítica."
            cta_v = "Digite AMÉM se você vai continuar firme no seu propósito!"
            prompt_v = "A determined builder standing on high stone city ramparts at sunset heroic perspective 8k"
            
            st.session_state['v_out'] = {
                'hook': hook_v, 'script': script_v, 'cta': cta_v, 'prompt': prompt_v, 'tema': tema_video
            }
            save_to_db("Vídeo Roteiro", tema_video, f"Gancho: {hook_v} | Roteiro: {script_v}", cta_v, "#reels #shorts #cristao", prompt_v)
            
    with v_col2:
        if 'v_out' in st.session_state:
            vo = st.session_state['v_out']
            st.markdown("<div class='card-box'>", unsafe_allow_html=True)
            st.markdown(f"**📌 Tema:** {vo['tema']}")
            st.markdown(f"**⚡ Gancho Viral (0-3s):** {vo['hook']}")
            st.markdown(f"**🗣️ Narração (3-15s):** {vo['script']}")
            st.markdown(f"**👉 Chamada (15-20s):** {vo['cta']}")
            st.markdown(f"**🖼️ Prompt para IA (CapCut/Luma/Runway):** `{vo['prompt']}`")
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Gerar Thumbnail do Vídeo
            thumb_img = render_post_card(
                title="VÍDEO VIRAL",
                text=vo['hook'],
                cta=vo['cta'],
                handle=handle_input,
                aspect_ratio="9:16",
                bg_style="Tempestade e Luz"
            )
            st.image(thumb_img, width=280, caption="Capa / Thumbnail Gerada em 9:16")

# ── ABA 4: BANCO DE DADOS & HISTÓRICO ─────────────────────────────────────────
with tab4:
    st.markdown("<h3 class='gold-header'>📚 Banco de Dados Local & Histórico de Conteúdos</h3>", unsafe_allow_html=True)
    
    b_col1, b_col2 = st.columns([1, 2])
    with b_col1:
        filtro_tipo = st.selectbox("Filtrar por Tipo:", ["Todos", "Post Imagem", "Vídeo Roteiro", "Devocional"])
    with b_col2:
        busca_txt = st.text_input("Buscar no Banco de Dados:", placeholder="Digite uma palavra-chave...")
        
    registros = get_all_contents(filter_tipo=filtro_tipo, search_query=busca_txt)
    
    st.markdown(f"**Total de Conteúdos Encontrados:** {len(registros)}")
    
    for reg in registros:
        r_id, r_tipo, r_titulo, r_texto, r_legenda, r_tags, r_prompt, r_data = reg
        with st.expander(f"[{r_tipo}] {r_titulo} - ({r_data})"):
            st.markdown(f"**Texto:** {r_texto}")
            if r_legenda:
                st.markdown(f"**Legenda:** {r_legenda}")
            if r_tags:
                st.markdown(f"**Hashtags:** {r_tags}")
            if r_prompt:
                st.markdown(f"**Prompt IA:** `{r_prompt}`")

# ── ABA 5: E-BOOKS & DEVOCIONAIS ──────────────────────────────────────────────
with tab5:
    st.markdown("<h3 class='gold-header'>📘 Gerador de E-books e Devocionais de 30 Dias</h3>", unsafe_allow_html=True)
    
    d_dias = st.slider("Quantidade de Dias do Plano:", 1, 30, 7)
    d_tema = st.text_input("Tema do Devocional:", value="Jornada de Fé e Restauração")
    
    if st.button("📖 Gerar Estrutura de Devocional"):
        st.markdown(f"### E-book: {d_tema} ({d_dias} Dias)")
        for dia in range(1, d_dias + 1):
            st.markdown(f"#### 🗓️ Dia {dia}: A Força do Cuidado Divino")
            st.markdown("**Versículo:** *'O Senhor te guiará continuamente e fartará a tua alma em lugares secos.' (Isaías 58:11)*")
            st.markdown("**Reflexão:** Mesmo no deserto das dúvidas, a mão de Deus permanece estendida. Não desanime diante dos obstáculos temporários.")
            st.markdown("**Oração:** Senhor, renova minhas forças e me concede sabedoria para caminhar em paz hoje. Amém.")
            st.markdown("---")

# ── ABA 6: DISPAROS WHATSAPP / TELEGRAM ────────────────────────────────────────
with tab6:
    st.markdown("<h3 class='gold-header'>💬 Mensagens para Disparo em Grupos (Anti-Spam)</h3>", unsafe_allow_html=True)
    
    link_divulgacao = st.text_input("Cole o Link do seu Vídeo ou Canal:", value="https://www.facebook.com/share/v/1C8dhnShhE/")
    
    st.markdown("### 📩 3 Variações de Mensagens Curtas e Acolhedoras:")
    
    v1 = f"Deus mandou te dizer isso hoje... 🙏✨\nSe você está precisando de paz e uma resposta para o seu coração, assista a este vídeo de 20 segundos:\n👇\n{link_divulgacao}\n\n*Que essa palavra abençoe seu dia!*"
    v2 = f"Uma palavra rápida de fé para a sua semana! 🌾🏼\nNão passe o dia sem ouvir esse recado de esperança:\n👉 {link_divulgacao}\n\nComente AMÉM e compartilhe com alguém especial!"
    v3 = f"Você não leu isso por acaso hoje... 📖❤️\nSepare 15 segundos para renovar a sua esperança com esta reflexão:\n🔗 {link_divulgacao}"
    
    st.text_area("Variação 1 (WhatsApp/Telegram):", value=v1, height=120)
    st.text_area("Variação 2 (Facebook/Grupos):", value=v2, height=120)
    st.text_area("Variação 3 (Direto/Direct):", value=v3, height=120)

# ── ABA 7: MONETIZAÇÃO & PIX ──────────────────────────────────────────────────
with tab7:
    st.markdown("<h3 class='gold-header'>💛 Painel de Doações PIX & Monetização</h3>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class='card-box'>
        <h3>🤝 Apoie o Projeto Mãos Amigas</h3>
        <p>Se esta plataforma e nossos conteúdos abençoaram sua vida, ajude-nos a continuar produzindo e levando mensagens de fé para milhares de pessoas.</p>
        <h4>Chave PIX: <span style='color: #d4af37;'>{chave_pix_input}</span></h4>
        <p><i>'Cada um contribua segundo propôs no seu coração... porque Deus ama ao que dá com alegria.' (2 Coríntios 9:7)</i></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Gerar Card de Doação PIX em PNG
    pix_card = render_post_card(
        title="APOIE ESTE PROJETO",
        text=f"Ajude nosso trabalho a continuar abençoando vidas. Faça sua contribuição voluntária de qualquer valor via PIX.",
        cta=f"CHAVE PIX: {chave_pix_input}",
        handle=handle_input,
        bg_style="Dourado Celestial"
    )
    
    st.image(pix_card, caption="Card de Apoio PIX para Divulgar nos Stories/PDFs", use_column_width=True)
    
    img_pix_b = io.BytesIO()
    pix_card.save(img_pix_b, format='PNG')
    st.download_button(
        label="📥 Baixar Card PIX (PNG)",
        data=img_pix_b.getvalue(),
        file_name="card_doacao_pix.png",
        mime="image/png"
    )

