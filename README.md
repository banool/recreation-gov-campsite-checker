
Table: Facility Configuration
    Primary Key: Facility-name
    base-url
    availability-endpoint
    main-page-endpoint

Table: Campsite Configurations
    Primary Key: Facility-name
    Secondary Key: campsite-name
    Sort Key: campsite-id

Table: Campsite Availabilities
    Primary Key: campsite-name
    campsite id
    Facility name
    availability dates

Table: User Configuration
    Primary Key: user-name
    campsite names: {
        "campsite 1",
        "campsite 2
    }
    availability preferences: {
        "sat",
        "sun",
        "mon",
        "teu",
        "wed",
        "thu",
        "fri"
    }


BASE_URL = "https://www.recreation.gov"
AVAILABILITY_ENDPOINT = "/api/camps/availability/campground/"
MAIN_PAGE_ENDPOINT = "/api/camps/campgrounds/"

INPUT_DATE_FORMAT = "%Y-%m-%d"

headers = {"User-Agent": UserAgent().random}

test
