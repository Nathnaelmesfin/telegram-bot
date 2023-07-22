import requests
from bs4 import BeautifulSoup

# Telegram bot token (replace 'YOUR_TELEGRAM_BOT_TOKEN' with your bot token)
telegram_bot_token = '6354155159:AAEXGFU9Y3pH4dRdcDLL99pPDZ-c5FsAYh0'

telegram_channel_username = '@amharic_Boo'

url = 'https://www.ethiobookreview.com/amharic'
response = requests.get(url)
content2 = response.content


def scrape_data(html_code):
    soup = BeautifulSoup(html_code, "lxml")
    books = []

    items = soup.find_all("div", class_="product")
    for item in items:
        # Image URL
        image_url = item.find("img")["src"] if item.find(
            "img") else "Image URL not found"

        # Author
        author_tag = item.find("h5")
        author = author_tag.text.strip() if author_tag else "Author not found"

        # Category
        category_tag = item.find("h6")
        category = category_tag.text.strip() if category_tag else "Category not found"

        # Price
        price_tag = item.find("h5", style="color:red; padding-top:5px;")
        price = price_tag.text.strip() if price_tag else "Price not found"

        books.append({
            "Image URL": image_url,
            "Author": author,
            "Category": category,
            "Price": price
        })

    return books


def send_message_to_telegram(message):
    send_message_url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    data = {
        "chat_id": telegram_channel_username,
        "text": message,
        "parse_mode": "HTML"
    }
    response = requests.post(send_message_url, data=data)
    if response.status_code != 200:
        print("Failed to send message to Telegram channel.")


books_data = scrape_data(content2)

# Prepare the message with extracted book data
message = "<b>New Book Releases:</b>\n\n"
for book in books_data:
    message += f"<b>Author:</b> {book['Author']}\n"
    message += f"<b>Category:</b> {book['Category']}\n"
    message += f"<b>Price:</b> {book['Price']}\n"
    message += f"<a href='{book['Image URL']}'>View Image</a>\n"
    message += "\n"

# Send the message to the Telegram channel
send_message_to_telegram(message)
