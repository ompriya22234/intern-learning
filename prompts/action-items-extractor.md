# Action Item Extractor

Extract tasks from meeting notes.

Return JSON:

{
"action_items":[
{
"task":"",
"owner":"",
"due_date":""
}
]
}

Use null if missing.

## User Template

Meeting Notes:
{notes}

## Example Output

{
"action_items":[
{
"task":"Update API docs",
"owner":"Priya",
"due_date":"2026-07-01"
}
]
}
