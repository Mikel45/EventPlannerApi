# EventPlannerApi
Api for planning events. It made with flask and sqlalchemy.

## Running
Clone this repository:

```bash
git clone https://github.com/Mikel45/EventPlannerApi.git
```

Run the app:
```bash
cd EventPlannerApi
python app.py
```

| Route | Description |
| --- | --- |
| `/event` | There are 2 methods get and post. With post method you need to specify event and date(YYYY-MM-DD). With get you can get all events if no start_date or end_date specified.|
| `/event/today` | There is get method, which return all events today.|
| `/event/event_id` | There are get and delete methods. With get you can get specific event with known id. With delete you can delete specific event with known id.|