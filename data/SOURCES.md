# Data provenance

The analysis uses a local snapshot of the OpenFootball World Cup 2026 match dataset:

- Dataset page: https://github.com/openfootball/worldcup.json/tree/master/2026
- Raw file: https://raw.githubusercontent.com/openfootball/worldcup.json/master/2026/worldcup.json
- Retrieved: 6 August 2026
- Records: 104 matches
- SHA-256: `0ae2c18109b5aa86bc11928b43586ca430c234804d5bbf808d2c3bf2051ecfca`

Used the official FIFA tournament pages to spot-check the snapshot before submission:

- Statistics: https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/statistics
- Fixtures and results: https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/articles/match-schedule-fixtures-results-teams-stadiums


The snapshot contains the tournament stage, date, teams, score at half-time and full-time, extra-time and penalty scores where applicable, venue, and named goal events. The acquisition script validates the record count and required fields before replacing the local snapshot.
The OpenFootball project describes these files as free public-domain football data.

