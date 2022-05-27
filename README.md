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
- Copy some images under  data/images/
- Start the docker instance
- Open the URL in http://localhost:$EXPOSE

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
