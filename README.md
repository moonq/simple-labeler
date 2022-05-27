# Simple Image Labeler

For trainig machine learning algorithms.

Setup:

- Copy `example.env` as `.env`
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
      "title": "Click to enable",
      "default": "on"
    },
    {
      "type": "info",
      "title": "Piece of text shown here."
    },
    {
      "type": "number",
      "name": "my_number",
      "default": "1.0",
      "title": "Only numbers allowed."
    },
    {
      "type": "text",
      "name": "my_text",
      "title": "Any text here",
      "default": "some text"
    },
    {
      "type": "range",
      "name": "my_slider",
      "title": "Slide away!",
      "default": "75",
      "min": "0",
      "max": "100"
    },
    {
      "type": "select",
      "title": "Select any from these",
      "name": "my_selection",
      "default": "select2",
      "options": [
        "option1",
        "select2",
        "select4",
        "select5",
        "select9"
      ]
    }
  ]
}

```
- Copy some images under  data/images/
- Start the docker instance
- Open the URL in http://localhost:$EXPOSE

## Label types

Label entries require "type" and "name". All labels can include
a "title" field, which is added as a hover-on text, and "default" for
the default value.

In some cases more fields required.

- checkbox: If "default": "on", checkbox is selected. Otherwise it is unselected.
- text: Any string, if no default: ""
- number: Any number entry, if no default: ""
- range: Requires  "min" and "max" values. if no default, default = min.
- select: Requires a list of "options".
- info: Not a selection. Add "title" field to show text instead.

## With nginx:

```
location /labeler/ {
         proxy_pass http://localhost:8088/;
         proxy_set_header Host $host;
         proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
         proxy_set_header X-Scheme $scheme;
         proxy_set_header X-Script-Name /labeler;
    }
```
