# LinkedIn Profile Scraper API

Retrieve LinkedIn profile details from a profile URL with the
[Datablist](https://www.datablist.com/) LinkedIn Profile Scraper API.

Send LinkedIn profile URLs as JSON and get available names, headlines,
locations, work experiences, education, and company details. Use the results to
update CRM contacts, enrich candidate records, or build a company research
workflow in your own application.

Already have a name but need the profile URL? Start with the
[LinkedIn Profile Finder API](https://github.com/datablist/linkedin-profile-finder-api).

## Get started

Choose [Python](python/README.md) or [TypeScript](typescript/README.md).
Create a [Personal API Key](https://app.datablist.com/account/api), then run an
example from this repository's root.

**Python:**

```sh
cd python
python -m pip install -r requirements.txt
export DATABLIST_API_KEY='your-personal-api-key'
python sync_requests.py
```

**TypeScript:**

```sh
export DATABLIST_API_KEY='your-personal-api-key'
npx tsx typescript/example.ts
```

With Node.js 24.3 or newer, you can also run `node typescript/example.ts` directly.
Run each command block from the repository root.

Calls use account credits. Fresh and cached profiles have different costs;
see the current
[credit cost and limits](https://platform.datablist.com/docs/enrichments/tools/linkedin-profile-scraper#credits-and-limits)
and [pricing](https://www.datablist.com/pricing). Each result reports its actual
`creditsUsed`.

## Input and output

Send profile URLs to `POST https://api.datablist.com/v1/enrichments/tasks`, with
your key in the `X-API-Key` header:

```json
{
  "enrichmentId": "linkedin-profile-scraper",
  "uniqueId": "linkedin-profile-scraper-example-001",
  "settings": {
    "experiencesNb": "3",
    "educationsNb": "1",
    "includeUrn": true,
    "includePictures": true,
    "acceptCachedProfiles": false
  },
  "inputs": [
    {
      "inputId": "row-1",
      "data": {
        "profileUrl": "https://www.linkedin.com/in/example-person/"
      }
    }
  ]
}
```

Use a new `uniqueId` for each new task. Give each profile its own `inputId` to
match it to its result, including when URLs repeat. Standard LinkedIn profile
URLs and Sales Navigator URLs are supported.

The API returns `202 Accepted` with a task ID in `@id`. Check the task status,
then retrieve its results. This complete response example includes all 48 output
fields from the production schema (sample data):

```json
{
  "taskId": "00000000000040008000000000000001",
  "results": [
    {
      "inputId": "row-1",
      "status": "success",
      "outputs": {
        "linkedInInternalIdentifier": "ACoAAAExamplePerson",
        "profileUrl": "https://www.linkedin.com/in/example-person/",
        "firstName": "Example",
        "lastName": "Person",
        "fullName": "Example Person",
        "linkedInHeadline": "Software engineer",
        "linkedInSummary": "I build data tools and backend services.",
        "linkedInCity": "San Francisco",
        "linkedInState": "California",
        "linkedInCountryCode": "US",
        "linkedInCountryName": "United States",
        "linkedInLocation": "San Francisco, California, United States",
        "linkedInProfilePicture": "https://example.com/images/profile.jpg",
        "linkedInlastExpTitle": "Senior Software Engineer",
        "linkedInlastExpEmploymentType": "Full-time",
        "linkedInlastExpDescription": "Built data pipelines and backend services.",
        "linkedInlastExpStartsAt": "2022-01-01",
        "linkedInlastExpEndsAt": "2025-12-31",
        "linkedInlastExpLocation": "San Francisco, California, United States",
        "linkedInlastExpCompany": "Example Company",
        "linkedInlastExpCompanyPage": "https://www.linkedin.com/company/example-company/",
        "linkedInlastExpCompanyWebsite": "https://example.com",
        "linkedInlastExpCompanyDescription": "Data software for business teams.",
        "linkedInlastExpCompanyIndustry": "Software Development",
        "linkedInlastExpCompanyRange": "51-200",
        "linkedInlastExpCompanyLogo": "https://example.com/images/company-logo.png",
        "linkedIn2ExpTitle": "Software Engineer",
        "linkedIn2ExpEmploymentType": "Full-time",
        "linkedIn2ExpDescription": "Developed APIs and internal applications.",
        "linkedIn2ExpStartsAt": "2019-07-01",
        "linkedIn2ExpEndsAt": "2021-12-31",
        "linkedIn2ExpCompanyName": "Example Analytics",
        "linkedIn2ExpLogo": "https://example.com/images/analytics-logo.png",
        "linkedIn3ExpTitle": "Junior Software Engineer",
        "linkedIn3ExpEmploymentType": "Full-time",
        "linkedIn3ExpDescription": "Built web applications and reporting tools.",
        "linkedIn3ExpStartsAt": "2017-07-01",
        "linkedIn3ExpEndsAt": "2019-06-30",
        "linkedIn3ExpCompanyName": "Example Studio",
        "linkedIn3ExpLogo": "https://example.com/images/studio-logo.png",
        "linkedInlastEduSchool": "Example University",
        "linkedInlastEduDegree": "Bachelor of Science",
        "linkedInlastEduField": "Computer Science",
        "linkedInlastEduStartsAt": "2013-09-01",
        "linkedInlastEduEndsAt": "2017-06-30",
        "linkedInlastEduLogo": "https://example.com/images/university-logo.png",
        "linkedInLanguages": "English, French",
        "linkedInConnections": "500+"
      },
      "creditsUsed": "25",
      "error": null
    }
  ],
  "nextCursor": null
}
```

The request above enables `includeUrn` and `includePictures`, with cached
profiles disabled, so the example can show the optional identifier and image
fields too. Available values depend on the profile. Work and education history
use flat, numbered fields. The scripts print complete result objects.

The [production schema](https://api.datablist.com/v1/enrichments/linkedin-profile-scraper)
lists the types and conditions for every output field.

## Settings

- `experiencesNb`: `"3"`, `"5"`, or `"10"` work experiences. Default: `"3"`.
- `educationsNb`: `"1"`, `"3"`, or `"5"` education entries. Default: `"1"`.
- `acceptCachedProfiles`: set to `true` to use cached profiles when available.
  The default requests fresh data.
- `includeUrn` and `includePictures`: optional LinkedIn identifiers and image
  URLs. Set `acceptCachedProfiles` to `false` when using either. Image URLs can
  expire.

Send the history counts as strings, as shown in the request above.

## Try with cURL

Set your key, then submit a profile:

```sh
export DATABLIST_API_KEY='your-personal-api-key'

curl --request POST 'https://api.datablist.com/v1/enrichments/tasks' \
  --header "X-API-Key: $DATABLIST_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "enrichmentId": "linkedin-profile-scraper",
    "uniqueId": "linkedin-profile-scraper-curl-001",
    "settings": {"experiencesNb": "3", "educationsNb": "1"},
    "inputs": [
      {"inputId": "row-1", "data": {"profileUrl": "https://www.linkedin.com/in/satyanadella/"}}
    ]
  }'
```

Copy the returned `@id` into `TASK_ID`. Use a new `uniqueId` for a new task.

```sh
TASK_ID='paste-returned-task-id'

curl "https://api.datablist.com/v1/enrichments/tasks/$TASK_ID" \
  --header "X-API-Key: $DATABLIST_API_KEY"
```

Repeat the status command every few seconds until `status` is `completed`,
`failed`, or `stopped`. Then retrieve the results:

```sh
curl "https://api.datablist.com/v1/enrichments/tasks/$TASK_ID/results" \
  --header "X-API-Key: $DATABLIST_API_KEY"
```

If `nextCursor` is not `null`, pass it as `cursor` to fetch the next page.
The Python and TypeScript examples read every page for you.

## Code examples

| Example | What it shows |
| --- | --- |
| [Synchronous Requests](python/sync_requests.py) | Retrieve profiles with blocking HTTP calls. |
| [Asynchronous HTTPX](python/async_httpx.py) | Use `async` and `await` for the same API workflow. |
| [TypeScript](typescript/example.ts) | Use async/await, standard `fetch`, and no imports. |

Each script is self-contained: submit URLs, wait for the background task, and
read the results. The API processes tasks in the background for all three clients.

## Documentation

- [LinkedIn Profile Scraper API](https://platform.datablist.com/docs/enrichments/tools/linkedin-profile-scraper)
- [Enrichments API quickstart](https://platform.datablist.com/docs/enrichments/quickstart)
- [Task lifecycle](https://platform.datablist.com/docs/enrichments/tasks)

## Other Datablist API examples

- [Company Name to Domain API](https://github.com/datablist/company-name-to-domain-api): find company websites from names.
- [Company Name Cleaner API](https://github.com/datablist/company-name-cleaner-api): clean and standardize company names.
- [LinkedIn Profile Finder API](https://github.com/datablist/linkedin-profile-finder-api): find profiles from names and company keywords.
- [LinkedIn Company Scraper API](https://github.com/datablist/linkedin-company-scraper-api): retrieve company details from LinkedIn company pages.
- [Impressum Scraper API](https://github.com/datablist/impressum-scraper-api): extract business details from website Impressum pages.
- [Waterfall Email Finder API](https://github.com/datablist/waterfall-email-finder-api): find work emails from names and companies or LinkedIn URLs.
