import PyPDF2
import requests
from bs4 import BeautifulSoup
import os

PDFFile = open('/home/diego/Downloads/Telegram Desktop/Springer Ebooks.pdf','rb')

PDF = PyPDF2.PdfFileReader(PDFFile)
pages = PDF.getNumPages()
key = '/Annots'
uri = '/URI'
ank = '/A'

for page in range(pages):
	pageSliced = PDF.getPage(page)
	pageObject = pageSliced.getObject()
	if key in pageObject.keys():
		ann = pageObject[key]
		for a in ann:
			u = a.getObject()
			if uri in u[ank].keys():
				url = u[ank][uri]
				print(url)
				r = requests.get(url)
				contenido = r.content
				la_sopita = BeautifulSoup(contenido, 'html.parser')
				titulo = la_sopita.select('h1')[0].text.strip()
				auths = la_sopita.findAll("span", {"class" : "authors__name"})
				download_pdf = "https://link.springer.com" + la_sopita.find("a", {"class" : "test-bookpdf-link"})['href']
				autor = ""
				
				print(download_pdf)
				#exit()

				for i in range(len(auths)):
					a = auths[i]
					if len(auths) == 1:
						autor += a.text.strip()
					else:
						autor += a.text.strip() + ", "
						if i == (len(auths) - 1):
							autor += a.text.strip()

				file_name = titulo + ": " + autor + ".pdf"
				print(file_name)
				
				myfile = requests.get(download_pdf, allow_redirects=True)
				open(file_name, 'wb').write(myfile.content)
