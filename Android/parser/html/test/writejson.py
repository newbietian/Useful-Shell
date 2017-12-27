import json
import os

data = {
  "head_title":"Android Log Analysis Tool",
  "chart_title": "Pengtian Chart 2015",
  "chart_data": [
    {
      "name": "Java Crash",
      "y": 100,
      "link": "HTML_tutorial_output.html"
    },
        {
      "name": "ANR",
      "y": 10,
      "link": "HTML_tutorial_output.html"
    },
    {
      "name": "Native Crash",
      "y": 20,
      "link": "HTML_tutorial_output.html"
    },
        {
      "name": "Other1",
      "y": 67,
      "link": "HTML_tutorial_output.html"
    },    {
      "name": "Other2",
      "y": 35,
      "link": "HTML_tutorial_output.html"
    }
  ]
}

print os.getcwd()
with open(os.getcwd() + "../tmp/record.json", "w") as f:
    json.dump(data, f, sort_keys=True, indent=2)
    f.close()

