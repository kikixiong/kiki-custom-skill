# arXiv API Reference

## API Endpoint

```
http://export.arxiv.org/api/query
```

## Query Parameters

- `search_query`: Search query string
- `start`: Start index (0-based)
- `max_results`: Maximum results to return
- `sortBy`: Sort field (`relevance`, `lastUpdatedDate`, `submittedDate`)
- `sortOrder`: Sort order (`ascending`, `descending`)

## Query Syntax

### By Category

```
cat:cs.AI
```

### By Date Range

```
submittedDate:[20260301 TO 20260318]
```

### Combined Query

```
cat:cs.AI AND submittedDate:[20260301 TO 20260318]
```

### Boolean Operators

- `AND`: Both terms must match
- `OR`: Either term must match
- `ANDNOT`: Exclude term

## Response Format

XML (Atom feed) with entries containing:

- `id`: arXiv URL
- `title`: Paper title
- `summary`: Abstract
- `author`: Author list
- `category`: Category tags
- `published`: Original submission date
- `updated`: Latest version date
- `link`: HTML and PDF links

## Rate Limiting

- Be respectful: ~1 request every 3 seconds
- Use `time.sleep()` between requests
- Consider caching results

## Categories

### Computer Science
- `cs.AI` - Artificial Intelligence
- `cs.LG` - Machine Learning
- `cs.CL` - Computation and Language
- `cs.CV` - Computer Vision
- `cs.MA` - Multiagent Systems

### Quantitative Biology
- `q-bio.GN` - Genomics
- `q-bio.MN` - Molecular Networks
- `q-bio.QM` - Quantitative Methods

### Statistics
- `stat.ML` - Machine Learning

## Examples

### Recent CS.AI papers

```
http://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=50
```

### Papers with keyword

```
http://export.arxiv.org/api/query?search_query=all:graph+neural+network&max_results=20
```

## Python Example

```python
import urllib.request
import xml.etree.ElementTree as ET

url = "http://export.arxiv.org/api/query?search_query=cat:cs.AI&max_results=10"

with urllib.request.urlopen(url) as response:
    data = response.read()

root = ET.fromstring(data)
ns = {"atom": "http://www.w3.org/2005/Atom"}

for entry in root.findall("atom:entry", ns):
    title = entry.find("atom:title", ns).text
    arxiv_id = entry.find("atom:id", ns).text
    print(f"{arxiv_id}: {title}")
```

## References

- [Official API Documentation](https://arxiv.org/help/api/index)
- [User Manual](https://arxiv.org/help/api/user-manual)
