#modulos de python
import os
import re
import requests
#modulos de terceros
import PyPDF2
from bs4 import BeautifulSoup

def Buscar_URLs(s):
	pattern = "http:\/\/link\.springer\.com\/openurl\?genre\=book\&isbn\=\d+-\d+-\d+\d+-\d+-\d+"
	urls = re.findall(pattern, s)
	return urls

def main():
	ruta_origen = open('/home/diego/Downloads/Telegram Desktop/Springer Ebooks.pdf','rb')

	PDF = PyPDF2.PdfFileReader(ruta_origen)
	pages = PDF.getNumPages()

	for page in range(pages):
		#texto de pag
		pageSliced = PDF.getPage(page)
		pageObject = pageSliced.getObject()
		text = pageObject.extractText()

		#urls en pag
		urls = Buscar_URLs(text)

		for url in urls:
			#peticion
			r = requests.get(url)
			la_sopita = BeautifulSoup(r.content, 'html.parser')

			#contenido
			titulo = la_sopita.select('h1')[0].text.strip()
			auths = la_sopita.findAll("span", {"class" : "authors__name"})

			#revisar descarga gratuita
			if la_sopita.find("a", {"class" : "test-bookpdf-link"}):
				download_pdf = "https://link.springer.com" + la_sopita.find("a", {"class" : "test-bookpdf-link"})['href']

				#nombre de autor(es)
				autor = ""
				for i in range(len(auths)):
					a = auths[i]
					if len(auths) == 1:
						autor += a.text.strip()
					else:
						autor += a.text.strip() + ", "
						if i == (len(auths) - 1):
							autor += a.text.strip()

				file_name = titulo + ": " + autor + ".pdf"

				#caracter que rompen el nombre de archivo
				if '/' in file_name: file_name = file_name.replace("/", ", ")

				#mostrar info al usuario
				print(file_name)
				print(url)

				#descargar pdf
				myfile = requests.get(download_pdf, allow_redirects=True)
				open(file_name, 'wb').write(myfile.content)

if __name__ == '__main__':
	main()
