from flask import Flask, request, jsonify
from datetime import datetime, timedelta
from gdeltdoc import GdeltDoc, Filters

app = Flask(__name__)
gdelt_client = GdeltDoc()


@app.route("/api/articles", methods=["POST"])
def search_articles():
    """
    Search for articles based on provided filters.

    Query Parameters:
    - keyword: Search keyword
    - start_date: Start date (YYYY-MM-DD)
    - end_date: End date (YYYY-MM-DD)
    - domain: Optional domain filter
    - country: Optional country filter
    - language: Optional language filter

    Returns:
    - JSON array of matching articles
    """
    try:
        # Extract query parameters
        # Extract them from post parameters
        data = request.get_json()

        if data is None:
            return jsonify({"error": "Invalid or missing JSON body"}), 400

        keyword = data.get("keyword") if data else None
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        domain = data.get("domain")
        country = data.get("country")
        language = data.get("language")

        # Validate required parameters
        if not keyword:
            return jsonify({"error": "Missing required parameters: keyword"}), 400

        # Use helper
        date_result = validate_date_range(start_date, end_date)
        if len(date_result) == 3:  # error case (None, jsonify, 400)
            return date_result[1], date_result[2]
        start_date, end_date = date_result

        # Create filters
        filters = Filters(
            keyword=keyword,
            start_date=start_date,
            end_date=end_date,
            domain=domain,
            country=country,
            language=language,
        )

        # Search articles
        articles = gdelt_client.article_search(filters)
        return jsonify(articles)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/timeline", methods=["POST"])
def search_timeline():
    """
    Get timeline data based on provided filters and mode.

    Query Parameters:
    - mode: Timeline mode (timelinevol, timelinevolraw, timelinetone, timelinelang, timelinesourcecountry)
    - keyword: Search keyword
    - start_date: Start date (YYYY-MM-DD)
    - end_date: End date (YYYY-MM-DD)
    - domain: Optional domain filter
    - country: Optional country filter
    - language: Optional language filter

    Returns:
    - JSON object containing timeline data
    """
    try:
        data = request.get_json()

        if data is None:
            return jsonify({"error": "Invalid or missing JSON body"}), 400

        mode = data.get("mode")
        keyword = data.get("keyword")
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        domain = data.get("domain")
        country = data.get("country")
        language = data.get("language")

        # Validate required parameters
        if not all([mode, keyword]):
            return (
                jsonify(
                    {
                        "error": "Missing required parameters: mode, keyword, start_date, and end_date are required"
                    }
                ),
                400,
            )

        # Validate mode
        valid_modes = [
            "timelinevol",
            "timelinevolraw",
            "timelinetone",
            "timelinelang",
            "timelinesourcecountry",
        ]
        if mode not in valid_modes:
            return (
                jsonify(
                    {"error": f'Invalid mode. Must be one of: {", ".join(valid_modes)}'}
                ),
                400,
            )

        # Use helper
        date_result = validate_date_range(start_date, end_date)
        if len(date_result) == 3:  # error case (None, jsonify, 400)
            return date_result[1], date_result[2]
        start_date, end_date = date_result

        # Create filters
        filters = Filters(
            keyword=keyword,
            start_date=start_date,
            end_date=end_date,
            domain=domain,
            country=country,
            language=language,
        )

        # Get timeline data
        timeline_data = gdelt_client.timeline_search(mode, filters)

        # Convert DataFrame to JSON
        if timeline_data.empty:
            return jsonify([])

        timeline_data["datetime"] = timeline_data["datetime"].dt.strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        return jsonify(timeline_data.to_dict(orient="records"))

    except Exception as e:
        return jsonify({"error": str(e)}), 500


from datetime import datetime, timedelta
from flask import jsonify


def validate_date_range(start_date_str, end_date_str):
    """
    Validate and parse start_date and end_date strings.

    Args:
    - start_date_str: str or None
    - end_date_str: str or None

    Returns:
    - tuple: (start_date: datetime, end_date: datetime)
    - tuple: (None, jsonify error response) on failure
    """
    try:
        if start_date_str:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        else:
            start_date = datetime.now() - timedelta(days=1)

        if end_date_str:
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        else:
            end_date = datetime.now()

        return start_date, end_date

    except ValueError:
        return None, jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
