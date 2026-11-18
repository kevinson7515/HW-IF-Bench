"""System-prompt suffixes used in the original run."""

S1 = (
    "Before your final answer, after successfully retrieving your evidence with web_fetch, use the write tool to save evidence_check.json in the workspace. "
    "The file must be a JSON array containing records for at least two distinct successfully retrieved public pages. "
    "Each record must contain exactly three nonempty string fields: url, role, and scope. "
    "The role explains what that page supports; the scope identifies the relevant version, time, region, model, or population as applicable. "
    "Use the URL you actually fetched. If the required evidence is inaccessible, report the limitation accurately. "
    "Keep the original question and its requested final answer format."
)
EXTRA = (
    " Before every web_fetch call, make sure its URL appears either in the original question or in a completed earlier web_search tool result. "
    "Use the exact returned link, allowing a trailing slash or URL fragment to differ; a search request alone is insufficient. "
    "If a new URL is needed, search for it before requesting the page."
)
POLICIES = {"S0": "", "S1": S1, "S2": S1 + EXTRA}
