# Security

Reads `data/notes.csv` from disk. No model client.

| Field | Kept in the audit event? |
| --- | --- |
| Note id | yes |
| Route | yes |
| Citation count | yes |
| Note text | no |
| Patient token | no |

A blocked note's rendered decision does not include the body. Urgent notes cite the one sentence that tripped the word list, because the nurse has to see why the phone should ring.

Rollback is stopping the process. Nothing is written to the chart.
