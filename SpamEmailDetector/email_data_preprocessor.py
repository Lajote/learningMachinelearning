# -*- coding: utf-8 -*-
#Regresion logística
#Esta clase facilita el preprocesamiento de correos electrónicos que poseen código HTML
from html.parser import HTMLParser
import email
import string
import nltk

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []
    def  handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

#Esta función se encarga de eliminar los tags HTML que se encuentren en el texto del correo

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()



class Parser:
    def __init__(self):
        self.stemmer = nltk.PorterStemmer()
        self.stopwords = set(nltk.corpus.stopwords.words('english'))
        self.punctuation = list(string.punctuation)
    
    def parse(self, email_path):
        """Parse an email. """
        with open(email_path, errors="ignore") as e:
            msg = email.message_from_file(e)
        return None if not msg else self.get_email_content(msg)
    def get_email_content(self, msg):
        """Extract the email content. """
        subject = self.tokenize(msg["Subject"]) if msg["Subject"] else []
        body = self.get_email_body(msg.get_payload(),
                                   msg.get_content_type())
        content_type = msg.get_content_type()
        #Returning the content of the email
        return {"subject": subject,
                "body": body,
                "Content_type": content_type}
    
    def get_email_body(self, payload, content_type):
        """Extract the body of the email. """
        body = []
        if type(payload) is str and content_type == "text/plain":
            return self.tokenize(payload)
        elif type(payload) is str and content_type == "text/html":
            return self.tokenize(strip_tags(payload))
        elif type(payload) is list:
            for p in payload:
                body += self.get_email_body(p.get_payload(),
                                            p.get_content_type())
        return body
    def tokenize(self, text):
        """Transform a text string in tokens. Perform two main actions,
        clean the punctuation symbols and do stemming of the text."""
        for c in self.punctuation:
            text = text.replace(c, "")
        text = text.replace("\t", " ")
        text = text.replace("\n", " ")
        tokens = list(filter(None, text.split(" ")))
        #Stemming of the tokens
        return [self.stemmer.stem(w) for w in tokens if w not in self.stopwords]