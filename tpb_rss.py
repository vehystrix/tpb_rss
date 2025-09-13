from flask import Flask, Response, request
import requests
import xml.etree.ElementTree as ET
from xml.dom import minidom
from typing import List, Dict
from datetime import datetime, timezone  # Updated import to include timezone
import argparse  # Added import for argparse


TITLE = "The pirate bay search results"
LINK = "https://thepiratebay.org"

app = Flask(__name__)


def fetch_data(user_query: str) -> List[Dict]:
    url = f"https://apibay.org/q.php?{user_query}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def create_rss_feed(data: List[Dict], user_query: str) -> str:
    rss = ET.Element(
        "rss", version="2.0", attrib={"xmlns:dc": "http://purl.org/dc/elements/1.1/"}
    )
    channel = ET.SubElement(rss, "channel")

    ET.SubElement(channel, "title").text = f"{TITLE} - {user_query}"
    ET.SubElement(
        channel, "link"
    ).text = f"{LINK}/search.php?{user_query}"  # Update link with the query
    ET.SubElement(channel, "language").text = "en"

    for item in data:
        rss_item = ET.SubElement(channel, "item")
        ET.SubElement(rss_item, "title").text = item["name"]
        magnet_link = f"magnet:?xt=urn:btih:{item['info_hash']}&dn={item['name'].replace(' ', '+')}"
        magnet_link += "&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337"
        magnet_link += "&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce"
        magnet_link += "&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce"
        magnet_link += "&tr=udp%3A%2F%2Ftracker.bittor.pw%3A1337%2Fannounce"
        magnet_link += "&tr=udp%3A%2F%2Fpublic.popcorn-tracker.org%3A6969%2Fannounce"
        magnet_link += "&tr=udp%3A%2F%2Ftracker.dler.org%3A6969%2Fannounce"
        magnet_link += "&tr=udp%3A%2F%2Fexodus.desync.com%3A6969"
        magnet_link += "&tr=udp%3A%2F%2Fopen.demonii.com%3A1337%2Fannounce"
        ET.SubElement(rss_item, "link").text = magnet_link
        formatted_date = datetime.fromtimestamp(
            int(item["added"]), tz=timezone.utc
        ).strftime("%a, %d %b %Y %H:%M:%S +0000")  # Updated date format
        ET.SubElement(rss_item, "pubDate").text = formatted_date
        ET.SubElement(
            rss_item, "category", domain="https://tpb.party/browse/205"
        ).text = "Video / TV shows"
        ET.SubElement(rss_item, "dc:creator").text = item["username"]
        ET.SubElement(
            rss_item, "guid"
        ).text = f"https://tpb.party/torrent/{item['id']}/"

    return minidom.parseString(ET.tostring(rss)).toprettyxml(indent="  ")


@app.route("/rss")
def serve_rss() -> Response:
    try:
        user_query = request.query_string.decode("utf-8")
        data = fetch_data(user_query)
        rss_feed = create_rss_feed(
            data, user_query
        )  # Pass the query to the RSS feed generator
        return Response(rss_feed, mimetype="application/rss+xml")
    except Exception as e:
        return Response(f"An error occurred: {e}", status=500)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Pirate Bay RSS server.")
    parser.add_argument("--host", default="127.0.0.1", help="Host to run the server on (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=5000, help="Port to run the server on (default: 5000)")
    args = parser.parse_args()

    app.run(host=args.host, port=args.port)
