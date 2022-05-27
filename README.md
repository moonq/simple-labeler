Simle Image Labeler

For trainig machine learning algorithms.

Setup:

- Copy `example.env` as `.env`
- Start the docker instance
- Write a data/config.json:

```
{
  "title": "My Labeler",
  "users": [
    "user1",
    "name2"
  ],
  "labels": [
    {
      "type": "checkbox",
      "name": "my_check",
      "default": "off"
    },
    {
      "type": "number",
      "name": "my_number",
      "default": "1.0"
    },
    {
      "type": "text",
      "name": "my_text",
      "default": "some text"
    },
    {
      "type": "range",
      "name": "my_slider",
      "default": "75",
      "min": "0",
      "max": "100"
    },
    {
      "type": "select",
      "name": "my_selection",
      "default": "select2",
      "options": [
        "option1",
        "select2"
      ]
    }
  ]
}
```
