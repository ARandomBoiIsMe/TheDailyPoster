import re
from lxml import html

from .database import retrieve_article

def is_article_new(connection, article):
    if retrieve_article(connection, article):
        return False

    return True

def retrieve_article_data(article):
    title = article['title']
    date = _format_date_string(article['published_parsed'])
    podcast_link = article['links'][1]['href']
    unformatted_content = article['content'][0]['value']

    doc = html.fromstring(unformatted_content)

    paragraphs = doc.xpath('//p')

    guest_paragraph_index = -1 # Stores the location of the first guest mention.

    # Gets the text of the article.
    text_list = []
    for index, p in enumerate(paragraphs):
        if p.text is None:
            continue

        if "Guest:" in p.text:
            guest_paragraph_index = index
            break

        if "Background reading:" in p.text:
            break

        if "For more information on today's episode" in p.text:
            break

        text_list.append(p)

    # Gets the guests of the article (if there are any.)
    guest_list = []
    if guest_paragraph_index != -1:
        for i in range(guest_paragraph_index, len(paragraphs)):
            if paragraphs[i].text is None:
                continue

            if "Background reading:" in paragraphs[i].text:
                break

            if "For more information on today's episode" in paragraphs[i].text:
                break

            guest_list.append(paragraphs[i])

    background_readings = _format_background_readings(doc.xpath('//li'))
    text = _format_text_list(text_list)
    guests = _format_guest_list(guest_list)

    return {
        'title': title,
        'date': date,
        'podcast_link': podcast_link,
        'text': text,
        'guests': guests,
        'background_readings': background_readings
    }

def _format_background_readings(readings):
    if readings == []:
        return ""

    formatted_readings = []
    for reading in readings:
        reading = html.tostring(reading, pretty_print=True, encoding='unicode').strip()[4:-5].strip().replace('\n    ', ' ')

        if reading.find('<a ') == -1:
            formatted_readings.append(f"* {reading}")
            continue

        formatted_readings.append(f"* {_reformat_html_links(reading)}")

    return "\n\n".join(formatted_readings)

def _format_text_list(text_list):
    if text_list == []:
        return ""

    return '\n\n'.join([t.text for t in text_list])

def _format_guest_list(guest_list):
    if guest_list == []:
        return ""

    guests = []
    for guest in guest_list:
        guest = html.tostring(guest, pretty_print=True, encoding='unicode').strip()[4:-5].strip().replace('\n    ', ' ')

        if guest.find('<a ') == -1:
            guests.append(guest)
            continue

        guests.append(_reformat_html_links(guest))

    guests[0] = guests[0][5:]
    guests = [g.strip() for g in guests]

    return "\n\n".join(guests)

def _reformat_html_links(html_string):
    anchor_tag_pattern = r"<a href=\"(.*?)\">(.*?)</a>"

    def replace_func(match):
        # Extract link and text from the regex match
        link = match.group(1)
        text = match.group(2)

        return f"[{text}]({link})"

    # Replace anchor tags with formatted links
    formatted_text = re.sub(anchor_tag_pattern, replace_func, html_string)
    return formatted_text

def _format_date_string(publish_date_object):
    months = {
        1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
        7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
    }

    return f"{months[publish_date_object.tm_mon]} {publish_date_object.tm_mday}, {publish_date_object.tm_year}"

def generate_post_text(article_data):
    text = f"{article_data['date']}\n\n"

    text += f"{article_data['text']}\n\n"

    if article_data['guests'] != "":
        text += "**On today's episode:**\n\n"
        text += f"{article_data['guests']}\n\n"

    if article_data['background_readings'] != "":
        text += "**Background readings:**\n\n"
        text += f"{article_data['background_readings']}\n\n"

    text += "---\n\n"
    text += f"You can listen to the episode [here]({article_data['podcast_link']})."

    return text