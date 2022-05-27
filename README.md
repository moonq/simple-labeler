Simle Image Labeler

For trainig machine learning algorithms.

Setup:

- Copy `example.env` as `.env`
- Start the docker instance
- Write a data/config.json:

```
{ "title": "My Labeler",
"labels": [
    {
    "type": "checkbox", "name": "my_check", "value": "off"},
            {"type": "text", "name": "my_text", "value": "1.0"},
            {
                "type": "range",
                "name": "my_slider",
                "value": "75",
                "min": "0",
                "max": "100",
            }
        ]
}

```
