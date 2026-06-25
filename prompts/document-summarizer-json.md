# Document Summarizer JSON

Summarize the document.

Return ONLY:

{
"title":"",
"summary":"",
"key_points":[]
}

Rules:

* Valid JSON only
* 3-5 key points
* No markdown

## User Template

Document:
{document}

## Example Output

{
"title":"AI in Healthcare",
"summary":"AI improves diagnosis and patient care.",
"key_points":[
"Faster diagnosis",
"Better treatment plans",
"Reduced costs"
]
}

## v1 vs v2

v1: Summarize as JSON.
Issue: Extra text appeared.

v2: Added schema and 'JSON only'.
Result: Parseable output across runs.
