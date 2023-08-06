# jcat

Python implementation of [catj](https://github.com/soheilpro/catj)

Origin: https://git.osuv.de/m/jcat  
Mirror: https://gitlab.com/markuman/jcat

# Install

`pip install jcat`

# example

```
~$ cat /tmp/test2.json
{
  "mappings": {
    "templates": [
      {
        "fields": {
          "mapping": {
            "norms": false,
            "type": "text",
            "fields": {
              "keyword": {
                "ignore_above": 256,
                "type": "keyword"
              }
            }
          }
        }
      }
    ]
  }
}
~$ jcat
USAGE:
        cat some.json | jcat
        jcat some.json

~$ jcat /tmp/test2.json
.mappings.templates[0].fields.mapping.norms = False
.mappings.templates[0].fields.mapping.type = "text"
.mappings.templates[0].fields.mapping.fields.keyword.ignore_above = 256
.mappings.templates[0].fields.mapping.fields.keyword.type = "keyword"
```
