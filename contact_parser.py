import re
import json
from datetime import datetime


SAMPLE_TEXT = """Иван Иванов, тел: +7 900 123-45-67, ivan@mail.ru
Анна Петрова - 8(495)555-22-11, a.petrova@company.com
Сергей Кондратьев, 89995632830, serkon@mail.com"""


class ContactParser:
    def __init__( self, text ):
        self.text = text
        self.contacts = []
        self.parsed_at = datetime.now().isoformat()

    def extract_phones(self,line):
        pattern =( r'(\+7[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}|8[\s\-]?'
		   r'\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}|8\d{10})')
        match = re.search(pattern, line)
        return match.group(0) if match else None

    def extract_emails(self,line):
        pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
        match = re.search(pattern, line)
        return match.group(0) if match else None

    def extract_name(self,line):
        match = re.match(r'([А-ЯЁ][а-яё]+\s[А-ЯЁ][а-яё]+)', line)
        return match.group(0) if match else None

    def parse(self):
        for line in self.text.strip().split('\n'):
            name=self.extract_name(line)
            phone=self.extract_phones(line)
            email=self.extract_emails(line)
            if name or phone or email:
                self.contacts.append({'name':name,'phone':phone,'email':email})
        print(f"Найдено контактов: {len(self.contacts)}")
        return self.contacts

    def to_json(self,output_file='contacts.json'):
        result = {'parsed_at': self.parsed_at,'total': len(self.contacts),'contacts': self.contacts}
        with open(output_file,'w',encoding='utf-8') as f:
            json.dump(result,f,ensure_ascii=False,indent=2)
        print(f"Сохранено в {output_file}")

    def print_table(self):
        print("\n{:<20} {:<20} {:<30}".format('Имя','Телефон','Email'))
        print("-"*70)
        for c in self.contacts:
            name=c['name'] or '—'
            phone=c['phone'] or '—'
            email=c['email'] or '—'
            print("{:<20} {:<20} {:<30}".format(name,phone,email))


def main():
    parser = ContactParser(SAMPLE_TEXT)
    parser.parse()
    parser.print_table()
    parser.to_json()


if __name__ == '__main__':
    main()
