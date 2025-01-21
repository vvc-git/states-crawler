# Define a regra para executar o spider
run:
	scrapy crawl cities

# Define a regra para instalar o Scrapy globalmente
install:
	sudo apt update && sudo apt install -y python3 python3-pip && python3 -m pip install --break-system-packages Scrapy
