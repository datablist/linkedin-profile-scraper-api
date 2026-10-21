# LinkedIn Profile Scraper API — TypeScript example

Retrieve profile details using async/await and the standard `fetch` API.
All HTTP calls are in [one standalone file](example.ts).

## Setup and run

From the repository root:

```sh
export DATABLIST_API_KEY='your-personal-api-key'
npx tsx typescript/example.ts
```

With Node.js 24.3 or newer, no runner package is needed:

```sh
node typescript/example.ts
```

From this `typescript` folder, use `npx tsx example.ts` or `node example.ts`.
Create your key on the [Datablist API page](https://app.datablist.com/account/api).
Calls use credits; see the current
[credit cost and limits](https://platform.datablist.com/docs/enrichments/tools/linkedin-profile-scraper#credits-and-limits)
and [pricing](https://www.datablist.com/pricing).

## Customize the example

Edit `profileUrls` at the bottom. The payload uses the default history settings:

```typescript
settings: { experiencesNb: "3", educationsNb: "1" }
```

Use `"3"`, `"5"`, or `"10"` work experiences, and `"1"`, `"3"`, or `"5"`
education entries. Send these counts as strings.

Add `acceptCachedProfiles: true` to use cached profiles when available.
For `includeUrn` or `includePictures`, set `acceptCachedProfiles: false`.
See the [API settings](https://platform.datablist.com/docs/enrichments/tools/linkedin-profile-scraper#settings).

## How it works

The script submits one task, polls every three seconds, and reads result pages
until `nextCursor` is `null`. It uses `fetch`, `crypto.randomUUID()`, and
`setTimeout`, with no imports. The example reads your key from the environment.

Each profile gets its own `inputId`, including repeated URLs. Full results are
printed as JSON, including statuses, outputs, credits used, and errors. Available
fields include `profileUrl`, `fullName`, `linkedInHeadline`, `linkedInSummary`,
`linkedInCity`, `linkedInState`, `linkedInCountryCode`, `linkedInCountryName`,
`linkedInLocation`, employment, and education details. Additional history uses
flat, numbered fields. `linkedInProfilePicture` is available when `includePictures`
is enabled and cached profiles are disabled. See the
[production schema](https://api.datablist.com/v1/enrichments/linkedin-profile-scraper)
for all output fields and types.

Each run submits one task with up to 10,000 profiles, within the API's request
size limits. This example does not batch larger lists.

See the [complete output example](../README.md#input-and-output) for all 48
production output fields, including optional identifiers and pictures.

## When something fails

HTTP errors and network failures stop the script. A failed or stopped task
throws an error with its task ID. A completed task can still contain individual
errors or missing fields; check each result's `status`.

If you stop the script, the submitted task continues on the server. List your
[tasks](https://platform.datablist.com/docs/enrichments/tasks) to check its status
before creating another task.
