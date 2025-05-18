from enum import Enum


class AppEnv(Enum):
    DEV = "dev"
    PROD = "prod"


class AppMode(Enum):
    TIMELINE = "timeline"
    ARTICLE_SEARCH = "article_search"


class TimelineMode(Enum):
    TIMELINEVOL = "timelinevol"  # Volume of articles by day
    TIMELINEVOLRAW = "timelinevolraw"  # Volume of articles by day (raw)
    TIMELINETONE = "timelinetone"  # Tone of articles by day
    TIMELINELANG = "timelinelang"  # Language of articles by day
    TIMELINESOURCECOUNTRY = "timelinesourcecountry"  # Source country of articles by day


class ArticleSearchMode(Enum):
    ARTICLE_SEARCH = "article_search"  # Search for articles by keyword
