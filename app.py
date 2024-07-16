from flask import Flask, request, jsonify, render_template
from newsapi import NewsApiClient
import os
import traceback

app = Flask(__name__)

# Initialize News API client
newsapi = NewsApiClient(api_key="a5e6")


def is_related_to_padres(article):
    """Check if the article is related to San Diego Padres"""
    keywords = ["san diego padres", "padres", "mlb", "baseball"]
    title = article["title"].lower() if article["title"] else ""
    description = article["description"].lower() if article["description"] else ""
    return any(keyword in title or keyword in description for keyword in keywords)


@app.route("/")
def home():
    # Fetch articles for the default keyword
    default_keyword = "San Diego Padres"
    try:
        articles = newsapi.get_everything(
            q=default_keyword, language="en", sort_by="publishedAt"
        )

        if articles["status"] != "ok":
            return render_template(
                "index.html", articles=[], error="Error fetching news articles"
            )

        filtered_articles = [
            article for article in articles["articles"] if is_related_to_padres(article)
        ]

        return render_template("index.html", articles=filtered_articles)
    except Exception as e:
        print("An error occurred:")
        traceback.print_exc()
        return render_template("index.html", articles=[], error=str(e))


@app.route("/search_news", methods=["GET"])
def search_news():
    keyword = request.args.get("keyword", "San Diego Padres")
    try:
        print(f"Keyword: {keyword}")

        articles = newsapi.get_everything(
            q=keyword, language="en", sort_by="publishedAt"
        )  # Sort by date

        if articles["status"] != "ok":
            return jsonify({"error": "Error fetching news articles"}), 500

        filtered_articles = [
            article for article in articles["articles"] if is_related_to_padres(article)
        ]

        return jsonify({"articles": filtered_articles})
    except Exception as e:
        print("An error occurred:")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    server_port = os.environ.get("PORT", "8080")
    app.run(debug=True, port=server_port, host="0.0.0.0")
