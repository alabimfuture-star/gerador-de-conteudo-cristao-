import streamlit as st
import random
import datetime

# Configuração da página
st.set_page_config(
    page_title="Gerador de Conteúdo Cristão & Motivacional",
    page_icon="✨",
    layout="wide"
)

# Estilo personalizado
st.markdown("""
<style>
    .main-header { font-size: 2.2rem; color: #D4AF37; font-weight: bold; text-align: center; margin-bottom: 0px; }
    .sub-header { font-size: 1.1rem; color: #555555; text-align: center; margin-bottom: 20px; }
    .stButton>button { background-color: #D4AF37; color: white; font-weight: bold; border-radius: 8px; border: none; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">✨ Plataforma Geradora de Conteúdo em Grande Escala</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Crie roteiros de vídeos, prompts de imagem IA, legendas virais, devocionais e mensagens em massa.</div>', unsafe_allow_html=True)

# Navegação por Abas
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🎬 Roteiros de Vídeo", 
    "🖼️ Prompts de Imagem IA", 
    "📝 Posts & Legendas Virais", 
    "📘 E-books & Devocionais", 
    "📲 Disparos WhatsApp/Telegram",
    "💛 Chave PIX & Doações"
])

# -------------------------------------------------------------------
# ABA 1: ROTEIROS DE VÍDEO
# -------------------------------------------------------------------
with tab1:
    st.header("🎬 Gerador de Roteiros para Vídeos Curtos (Reels/Shorts/TikTok)")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        nicho = st.selectbox("Selecione o Nicho", ["Histórias Bíblicas", "Motivacional & Mente", "Paz & Oração"])
        tempo = st.slider("Duração do Vídeo (Segundos)", 15, 60, 18)
        estilo_gancho = st.selectbox("Estilo do Gancho (0-3s)", ["Pergunta Provocativa", "Curiosidade/Segredo", "Afirmação Ousada"])
        btn_roteiro = st.button("⚡ Gerar Roteiro de Vídeo")
        
    with col2:
        if btn_roteiro:
            ganchos_biblicos = [
                "Deus não usa os preparados; Ele prepara aqueles que decide chamar...",
                "Quando o mundo não entender as suas lágrimas, lembre-se de quem te escuta...",
                "O lugar onde você se sente mais esquecido é onde o seu chamado começa..."
            ]
            ganchos_motivacionais = [
                "A disciplina vai te levar até lugares onde a motivação sozinha não consegue...",
                "Não compare o seu começo com o momento de sucesso de outra pessoa...",
                "A tempestade não veio para te parar, veio para testar a força da sua raiz..."
            ]
            
            gancho_escolhido = random.choice(ganchos_biblicos if nicho == "Histórias Bíblicas" else ganchos_motivacionais)
            
            st.success("Roteiro Gerado com Sucesso!")
            st.markdown(f"**📌 Gancho de Abertura (0-3s):** `{gancho_escolhido}`")
            st.markdown("**🗣️ Narração Principal (3-15s):**\n*Mantenha os olhos no seu propósito e não se distraia com as críticas do caminho. Cada esforço feito no silêncio gerará um resultado público abundante.*")
            st.markdown("**📢 Chamada para Ação (CTA 15-18s):**\n*Digite AMÉM e compartilhe este vídeo com alguém que precisa dessa palavra hoje!*")
            st.markdown("**🎨 Prompt para Imagem/Vídeo em IA:**\n`Cinematic photorealistic portrait of an ancient prophet standing on a mountain peak at golden sunrise, 8k, aspect ratio 9:16`")

# -------------------------------------------------------------------
# ABA 2: PROMPTS DE IMAGEM IA
# -------------------------------------------------------------------
with tab2:
    st.header("🖼️ Gerador de Prompts Cinematográficos para IA")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        personagem = st.text_input("Personagem ou Tema", "Davi e Golias no Vale")
        formato = st.radio("Proporção", ["1:1 (Feed Facebook/Insta)", "9:16 (Stories/Reels)"])
        estilo_visual = st.selectbox("Estilo Visual", ["Cinematográfico Fotorrealista", "Pintura Clássica Barroca", "Ilustração 3D Épica"])
        btn_prompt = st.button("🎨 Criar Prompt")
        
    with col2:
        if btn_prompt:
            aspect = "1:1" if "1:1" in formato else "9:16"
            prompt_en = f"A cinematic photorealistic portrait of {personagem}, dramatic volumetric golden lighting, highly detailed robes, soft dust particles floating in the air, masterpiece, 8k, aspect ratio {aspect}"
            
            st.subheader("Prompt Gerado (Copiar para Bing/Midjourney/Leonardo AI):")
            st.code(prompt_en, language="text")
            st.info("💡 Cole este código em inglês nos geradores de imagem para obter a melhor qualidade visual.")

# -------------------------------------------------------------------
# ABA 3: POSTS & LEGENDAS
# -------------------------------------------------------------------
with tab3:
    st.header("📝 Banco de Posts e Legendas Virais")
    categoria_post = st.selectbox("Categoria de Post", [
        "Promessas & Conforto", 
        "Superação de Batalhas", 
        "Milagres & Provisão", 
        "Motivação & Foco"
    ])
    
    if st.button("🎲 Gerar Modelo de Post Pronto"):
        st.subheader("📌 Título da Arte (Texto em Destaque na Imagem):")
        st.code("DEUS OUVIU O SEU CHORO EM SILÊNCIO ONTEM À NOITE.", language="text")
        
        st.subheader("💬 Legenda Completa para o Facebook/Instagram:")
        legenda_texto = """Quando o mundo não vê as suas lágrimas, Deus escuta o seu coração no segredo. A sua resposta já está a caminho!

Digite AMÉM se você crê e compartilhe essa mensagem de esperança com alguém!

#fe #deus #oracao #mensagemdeesperanca #biblia #motivacaocristao #paz"""
        st.text_area("Copiar Legenda:", legenda_texto, height=150)

# -------------------------------------------------------------------
# ABA 4: DEVOCIONAIS & E-BOOKS
# -------------------------------------------------------------------
with tab4:
    st.header("📘 Gerador de Capítulos para Devocionais de 30 Dias")
    dia_num = st.number_input("Número do Dia", 1, 30, 1)
    tema_devocional = st.text_input("Tema do Dia", "A Oração de Ana e a Persistência")
    
    if st.button("📖 Gerar Estrutura do Capítulo"):
        st.markdown(f"### 📖 Dia {dia_num}: {tema_devocional}")
        st.markdown("**Versículo Chave:** *1 Samuel 1:10 - 'Ela, pois, com amargura de alma, orou ao Senhor, e chorou abundantemente.'*")
        st.markdown("**Reflexão Prática:** Ana enfrentou anos de provocação e silêncio, mas não abandonou o altar. A sua perseverança gerou o profeta Samuel.")
        st.markdown("**Oração do Dia:** *Senhor, fortalece o meu coração nos dias em que a resposta parecer demorar. Eu entrego minhas causas nas Tuas mãos. Amém.*")

# -------------------------------------------------------------------
# ABA 5: DISPAROS WHATSAPP & TELEGRAM
# -------------------------------------------------------------------
with tab5:
    st.header("📲 Mensagens Acolhedoras para Grupos e Transmissão")
    st.write("Mensagens curtas variadas para evitar filtros de spam ao enviar em grupos do WhatsApp/Telegram.")
    
    link_video = st.text_input("Seu Link do Vídeo/Post", "https://www.facebook.com/share/v/1C8dhnShhE/")
    
    if st.button("🚀 Gerar Variações de Mensagem"):
        st.markdown("**Variação 1:**")
        msg1 = f"Deus mandou te dizer isso hoje... 🙏✨\nSe você precisa de uma palavra de paz, assista por 20 segundos:\n👇\n{link_video}\n\nDigite AMÉM!"
        st.code(msg1, language="text")
        
        st.markdown("**Variação 2:**")
        msg2 = f"Uma mensagem especial para abençoar o seu dia! ❤️\nClique no link para assistir:\n👇\n{link_video}\n\nCompartilhe com quem você ama!"
        st.code(msg2, language="text")

# -------------------------------------------------------------------
# ABA 6: MONETIZAÇÃO & PIX
# -------------------------------------------------------------------
with tab6:
    st.header("💛 Configuração de Doações & Apoio Voluntário")
    st.write("Mensagem de agradecimento configurada para rodar ao final dos seus e-books e PDFs.")
    
    chave_pix = st.text_input("Chave PIX Cadastrada", "maosamigasrelogiofinal@gmail.com")
    
    st.info(f"""
    **🤝 Apoie o Nosso Projeto Mãos Amigas**
    
    Se este conteúdo abençoou a sua vida e você deseja nos ajudar a manter este trabalho ativo e agregar mais valor às pessoas, faça uma contribuição voluntária de qualquer valor.
    
    **Chave PIX:** `{chave_pix}`
    
    *'Cada um contribua segundo propôs no seu coração... porque Deus ama ao que dá com alegria.' (2 Coríntios 9:7)*
    """)
