# LinkedIn Profile Scraper API — Python examples

Retrieve profile, employment, and education details from LinkedIn profile URLs.
Each file shows all the HTTP calls in one place.

## Setup

Use Python 3.12 or newer. From this `python` folder:

```sh
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
export DATABLIST_API_KEY='your-personal-api-key'
```

Create your key on the [Datablist API page](https://app.datablist.com/account/api).
Calls use credits; see the current
[credit cost and limits](https://platform.datablist.com/docs/enrichments/tools/linkedin-profile-scraper#credits-and-limits)
and [pricing](https://www.datablist.com/pricing).

## Run an example

**Synchronous, using Requests:**

```sh
python sync_requests.py
```

**Asynchronous, using HTTPX:**

```sh
python async_httpx.py
```

Edit `profile_urls` at the bottom of either file. Both scripts submit a
background task, poll every three seconds, and read all result pages. Requests
uses blocking calls. HTTPX uses `await` and `asyncio.sleep`.

## Customize the example

The payload requests three work experiences and one education entry:

```python
"settings": {"experiencesNb": "3", "educationsNb": "1"}
```

Use `"3"`, `"5"`, or `"10"` for work experiences, and `"1"`, `"3"`, or `"5"`
for education entries. Keep these values as strings.

Add `"acceptCachedProfiles": True` to use cached profiles when available.
For `includeUrn` or `includePictures`, set `acceptCachedProfiles` to `False`.
The [API reference](https://platform.datablist.com/docs/enrichments/tools/linkedin-profile-scraper#settings)
describes these settings.

## Results and limits

Each script prints full results, including `inputId`, `status`, `outputs`,
`creditsUsed`, and `error`. Match results to submitted profiles through `inputId`.
Outputs can include `profileUrl`, `fullName`, `linkedInHeadline`,
`linkedInSummary`, `linkedInCity`, `linkedInState`, `linkedInCountryCode`,
`linkedInCountryName`, `linkedInLocation`, employment, and education details.
Additional history uses numbered fields such as `linkedIn2ExpTitle`.
`linkedInProfilePicture` is available when `includePictures` is enabled and
cached profiles are disabled. See the [production schema](https://api.datablist.com/v1/enrichments/linkedin-profile-scraper)
for all output fields and types.

Each script submits one task with up to 10,000 profiles, within the API's request
size limits. These examples do not batch larger lists.

See the [complete output example](../README.md#input-and-output) for all 48
production output fields, including optional identifiers and pictures.

## When something fails

HTTP errors raise the library's normal exception. A failed or stopped task
raises an exception with its task ID. A completed task can still have individual
errors or missing fields; check each result's `status`.

If you stop a script, the submitted task continues on the server. List your
[tasks](https://platform.datablist.com/docs/enrichments/tasks) to check its status
before creating another task.
