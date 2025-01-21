# INE5454 - Special Topics in Data Management

This application is a web crawler that extracts data from the following Wikipedia pages:

- [List of municipalities in São Paulo](https://pt.wikipedia.org/wiki/Lista_de_munic%C3%ADpios_de_S%C3%A3o_Paulo)  
- [List of municipalities in Rio de Janeiro](https://pt.wikipedia.org/wiki/Lista_de_munic%C3%ADpios_do_Rio_de_Janeiro)  
- [List of municipalities in Minas Gerais](https://pt.wikipedia.org/wiki/Lista_de_munic%C3%ADpios_de_Minas_Gerais)  

As a result of the spider's execution, the following files are generated containing information about the municipalities of each state:

- `minas_gerais.csv` and `minas_gerais.json`  
- `rio_de_janeiro.csv` and `rio_de_janeiro.json`  
- `sao_paulo.csv` and `sao_paulo.json`  

---

## How to Run the Application

### 1. Create a Virtual Environment

Run the commands below to create and activate a virtual environment:

```bash
sudo apt-get install python3-venv
python3 -m venv webscraping
source webscraping/bin/activate
```

### 2. Install Dependencies

Install the required dependencies using the following command:
```
make install
```
### 3. Run the Spider

To execute the spider and start data collection, use one of the commands below:
```
make run
```

or run it directly with Scrapy:
```
scrapy crawl cities
```