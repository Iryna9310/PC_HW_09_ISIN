import json
from mongoengine import connect
from models import Author, Quote

# Підключення до бази даних MongoDB
connect("my_database", host="mongodb+srv://MYNAME:PASSWORD@cluster0.ct1p0gg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# Завантаження даних з файлів JSON та збереження їх у базі даних
def load_authors_from_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        authors_data = json.load(file)
        for author_data in authors_data:
            author = Author(**author_data)
            author.save()

def load_quotes_from_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        quotes_data = json.load(file)
        for quote_data in quotes_data:
            author_name = quote_data.pop('author')
            author = Author.objects(fullname=author_name).first()
            if author:
                quote_data['author'] = author
                quote = Quote(**quote_data)
                quote.save()

def print_quotes(quotes):
    unique_quotes = set()
    if quotes:
        for quote in quotes:
            if quote.quote not in unique_quotes:
                print(quote.quote)
                unique_quotes.add(quote.quote)
    else:
        print("No quotes found!")

def search_quotes():
    while True:
        command = input("Enter command (name:<author_name>, tag:<tag>, tags:<tag1>,<tag2>, exit to quit): ").strip()
        if command.lower() == "exit":
            break
        command_parts = command.split(":")
        if len(command_parts) != 2:
            print("Invalid command format!")
            continue

        search_type, value = command_parts
        value = value.strip()

        if search_type == "name":
            author = Author.objects(fullname=value).first()
            if author:
                quotes = Quote.objects(author=author)
                print_quotes(quotes)
            else:
                print("Author not found!")
        elif search_type == "tag":
            quotes = Quote.objects(tags=value)
            print_quotes(quotes)
        elif search_type == "tags":
            tags = value.split(",")
            quotes = Quote.objects(tags__in=tags)
            print_quotes(quotes)
        else:
            print("Invalid command format!")

# Основний код
if __name__ == "__main__":
    load_authors_from_json('authors.json')
    load_quotes_from_json('quotes.json')
    search_quotes()