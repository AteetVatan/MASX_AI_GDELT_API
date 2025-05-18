from datetime import datetime, timedelta
from typing import Optional, Tuple
from fastapi import HTTPException


class Validators:
    """The Validators Class"""

    @staticmethod
    def get_and_validate_date_range(
        start_date_str: Optional[str], end_date_str: Optional[str]
    ) -> Tuple[datetime, datetime]:
        """Function to Validate dates if given else return default."""
        try:
            start_date = (
                datetime.strptime(start_date_str, "%Y-%m-%d")
                if start_date_str
                else datetime.now() - timedelta(days=1)
            )
            end_date = (
                datetime.strptime(end_date_str, "%Y-%m-%d")
                if end_date_str
                else datetime.now()
            )
            return start_date, end_date
        except ValueError:
            raise HTTPException(
                status_code=400, detail="Invalid date format. Use YYYY-MM-DD"
            )
