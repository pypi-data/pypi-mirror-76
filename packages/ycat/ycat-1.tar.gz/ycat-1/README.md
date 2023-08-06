# Install

`pip install ycat`

# example

```
~$ cat /tmp/test2.yml
---
mappings:
  templates:
  - fields:
      mapping:
        norms: false
        type: text
        fields:
          keyword:
            ignore_above: 256
            type: keyword

~$ ycat
USAGE:
        cat some.yaml | ycat
        ycat some.yaml

~$ ycat /tmp/test2.yml
.mappings.templates[0].fields.mapping.norms = False
.mappings.templates[0].fields.mapping.type = "text"
.mappings.templates[0].fields.mapping.fields.keyword.ignore_above = 256
.mappings.templates[0].fields.mapping.fields.keyword.type = "keyword"
```
