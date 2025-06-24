# 🎥 Downloader de Vídeos e Áudios com Interface Gráfica

Este projeto foi criado para oferecer uma solução **gratuita** e **acessível** para baixar vídeos e áudios de diversas plataformas, como **YouTube** e **redes sociais**.  
Ideal para quem deseja salvar conteúdos para **estudo**, **trabalho** ou **lazer**, sem depender de ferramentas pagas ou com anúncios.

## 🔧 Tecnologias Utilizadas

- **[yt_dlp](https://github.com/yt-dlp/yt-dlp)** – Biblioteca poderosa para download de vídeos e áudios de múltiplas plataformas.  
- **[PySimpleGUI](https://pysimplegui.readthedocs.io/)** – Interface gráfica simples, leve e intuitiva.  
- **os** – Manipulação de arquivos e diretórios no sistema operacional.

## 📌 Como Funciona

1. O usuário insere o **link** do conteúdo desejado.
2. Escolhe o **formato** de saída: vídeo completo ou apenas áudio.
3. Escolhe a qualidade do vídeo, se não a melhor será baixada por padrão.
4. Define a **pasta de destino** onde o conteúdo será salvo.
5. Com um clique, o sistema realiza o **download automático** e salva o arquivo.

## 🎬 Demonstração do Projeto (Vídeo)

[![Assista à apresentação no YouTube](https://img.youtube.com/vi/5T__ed89DhM/maxresdefault.jpg)](https://www.youtube.com/watch?v=5T__ed89DhM)

## 🔄 Em Desenvolvimento Contínuo

- Suporte a mais plataformas  
- Melhoria na verificação e validação de links  
- Mais opções de formatos e qualidades de saída  
- Interface cada vez mais amigável e responsiva
- Build para criar um App Executável

## 🚀 Como Executar o Projeto

1. **Clone este repositório**:

```bash
git clone https://github.com/vmellozk/midia-downloader.git
cd midia-downloader
```

2. Crie um ambiente virtual (opcional, mas recomendado):

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Ativar o ambiente virtual:

```bash
./venv/scripts/activate
```

4. Instale as dependências:

```bash
pip install -r requirements.txt
```

5. Execute o script principal:

```bash
python main.py #Windows
python3 main.py #Linux e macOS
```

## 📦 Requisitos
Python 3.7+

yt_dlp

PySimpleGUI

## ℹ️ Requisitos adicionais por sistema operacional

#### 🔵 Windows

O executável do `ffmpeg` já está incluído na pasta `ffmpeg/bin` do projeto.  
Não é necessário instalar ou configurar nada adicionalmente — tudo já está pronto para uso.

---

#### 🐧 Linux

Para que o projeto funcione corretamente no Linux, é necessário que o `ffmpeg` esteja instalado no sistema.

##### 📥 Como instalar:

Execute no terminal:

```bash
sudo apt update
sudo apt install ffmpeg
```

🔎 Para verificar se está instalado corretamente:

```bash
which ffmpeg
which ffprobe
```

A saída deve ser algo como:
```text
/usr/bin/ffmpeg
/usr/bin/ffprobe
```

Se os caminhos forem exibidos, significa que está tudo certo para utilizar o projeto.

## 💡 Sobre o Projeto

Este é um projeto independente, com foco em:

- Praticidade  
- Eficiência  
- Liberdade de acesso ao conteúdo  

Sinta-se à vontade para contribuir, sugerir melhorias ou relatar problemas.

## 🤝 Contribuindo

1. Faça um **fork** do projeto

2. Crie uma **branch**:  
```bash
git checkout -b nova-funcionalidade
```

3. Faça o commit das suas alterações:

```bash
git commit -m 'Adiciona nova funcionalidade'
```

4. Faça o push para a branch:

```bash
git push origin nova-funcionalidade
```

5. Abra um Pull Request

## 📄 Licença
Este projeto está sob a licença MIT. O arquivo 'LICENSE' será adicionado para mais detalhes.
