"""Retrieve LinkedIn profile details with the Datablist API using requests.

This standalone example submits a small list of profile URLs, waits for the
background task to finish, and reads all pages of results.
HTTP calls and three-second polling pauses block until they finish.

The API returns available profile, employment, and education fields. The payload
requests three work experiences and one education entry. These settings are
strings; edit them in the payload to request more history.

Set DATABLIST_API_KEY and run: python sync_requests.py
Edit profile_urls at the bottom to try your own LinkedIn profiles. This example
submits one task of up to 10,000 profiles. Calls consume account credits.
"""

import os
import time
import uuid

import requests


def scrape_profiles(profile_urls: list[str], api_key: str) -> list[dict]:
    """Submit one task, wait for it to finish, and return its results."""
    tasks_url = "https://api.datablist.com/v1/enrichments/tasks"
    headers = {"X-API-Key": api_key}
    inputs = [
        {"inputId": f"row-{index}", "data": {"profileUrl": profile_url}}
        for index, profile_url in enumerate(profile_urls, start=1)
    ]

    # 1. Submit the profile URLs.
    payload = {
        "enrichmentId": "linkedin-profile-scraper",
        "uniqueId": str(uuid.uuid4()),
        "settings": {"experiencesNb": "3", "educationsNb": "1"},
        "inputs": inputs,
    }
    response = requests.post(tasks_url, headers=headers, json=payload)
    response.raise_for_status()
    task = response.json()
    task_id = task["@id"]
    task_url = f"{tasks_url}/{task_id}"

    # 2. Wait for the background task to finish.
    while task["status"] not in ("completed", "failed", "stopped"):
        time.sleep(3)
        response = requests.get(task_url, headers=headers)
        response.raise_for_status()
        task = response.json()

    if task["status"] != "completed":
        raise RuntimeError(f"Task {task_id} {task['status']}: {task.get('error')}")

    # 3. Read the results, following pagination when needed.
    results = []
    results_url = f"{task_url}/results"
    params = {"limit": 100}
    while True:
        response = requests.get(results_url, headers=headers, params=params)
        response.raise_for_status()
        page = response.json()
        results.extend(page["results"])
        next_cursor = page["nextCursor"]
        if next_cursor is None:
            break
        params["cursor"] = next_cursor

    return results


if __name__ == "__main__":
    api_key = os.environ["DATABLIST_API_KEY"]
    profile_urls = [
        "https://www.linkedin.com/in/satyanadella/",
        "https://www.linkedin.com/in/reidhoffman/",
    ]

    results = scrape_profiles(profile_urls, api_key)
    for result in results:
        print(result)
