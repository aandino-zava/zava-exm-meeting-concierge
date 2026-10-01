# Zava ExM Meeting Concierge Microsoft Graph tools

| Operation | Use | Boundary |
| --- | --- | --- |
| GET /v1.0/me/events/{encodedEventId} | Authoritative target event | Agent reads and flow independently reads |
| GET /v1.0/me/calendar/calendarView | Expanded occurrences and busy intervals | Agent searches all pages; flow rejects incomplete current-conflict results |
| PATCH /v1.0/me/events/{encodedEventId} | Start and end update | Only inside Gatekeeper permitted branch |

The actual connector is Office 365 Outlook HttpRequest. The agent read action has Method fixed to GET. The Gatekeeper URL is assembled from the event ID, and its PATCH body sets start/end dateTime and timeZone UTC. Its header is `If-Match` with the authoritative event's `@odata.etag`.

Conflict means `other.start < target.end AND other.end > target.start`, with a different event ID, isCancelled false, and showAs not free. Touching endpoints do not overlap. Recurring occurrences are inspected through calendarView; series masters are not movable through the flow.

A fixed POST getSchedule setup tool is present but was recorded as disabled because its exposed file-body input was unsuitable. A preauthorized Entra GET tool is also retained from setup after unsuccessful reads. Neither is presented as a working-hours capability. The implemented fallback is Monday–Friday 09:00–17:00 in originalStartTimeZone.

[Read action](../../solution/unpacked/botcomponents/cr9b0_ZavaCalendarGovernanceAgent.action.Office365Outlook-SendanHTTPrequest/data) · [Notification action](../../solution/unpacked/botcomponents/cr9b0_ZavaCalendarGovernanceAgent.action.Office365Outlook-SendanemailV2/data)
