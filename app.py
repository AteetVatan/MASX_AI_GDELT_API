from datetime import datetime, timedelta
from gdeltdoc import GdeltDoc, Filters


def main():

    gd = GdeltDoc()

    start_date = datetime.now() - timedelta(days=1)
    end_date = datetime.now()
    # http://192.168.0.235:5000/api/articles?keyword=FORCEPOSTURE;LEADER;FNCACT;FNCACT_PRESIDENT;USPEC_POLITICS_GENERAL1;CRIME_CARTELS;ORGANIZED_CRIME;WB_1743_ANTICARTEL_ENFORCEMENT;WB_1921_PRIVATE_SECTOR_DEVELOPMENT;
    # http://192.168.0.235:5000/api/timeline?mode=timelinevol&keyword=FORCEPOSTURE;LEADER;FNCACT;FNCACT_PRESIDENT;USPEC_POLITICS_GENERAL1;CRIME_CARTELS;ORGANIZED_CRIME;WB_1743_ANTICARTEL_ENFORCEMENT;WB_1921_PRIVATE_SECTOR_DEVELOPMENT;
    f = Filters(
        keyword="FORCEPOSTURE;LEADER;FNCACT;FNCACT_PRESIDENT;USPEC_POLITICS_GENERAL1;CRIME_CARTELS;ORGANIZED_CRIME;WB_1743_ANTICARTEL_ENFORCEMENT;WB_1921_PRIVATE_SECTOR_DEVELOPMENT;",
        start_date=start_date,
        end_date=end_date,
    )

    gd = GdeltDoc()

    # Search for articles matching the filters
    articles = gd.article_search(f)
    print(articles)
    # Get a timeline of the number of articles matching the filters
    timeline = gd.timeline_search("timelinevol", f)
    print("Hello, World!")


if __name__ == "__main__":
    main()
