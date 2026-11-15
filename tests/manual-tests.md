| User story | Acceptance criterion | Tester | Date | Result | Notes |
| --- | --- | --- | --- | --- | --- |
| US1 | 2: duplicate email rejected | Name | 99/99/26 | passed |  |
| US5 | Deletion of a listing succeeded when there was >1 reservation on the listing | Artemis | 11/6/2026 | Failed | ... |
| US5 | Deletion of a listing succeeded when there was >1 reservation on the listing | Artemis | 11/6/2026 | Passed | I had to make it loop through reservations |
| US8 | 1: Given I am on the listings page, when I select one or more dietary tags, then only listings that have all selected tags are shown. | Faye | 11/14/2026 | Passed | Tested Vegetarian, Vegan, Halal + Gluten-free, and Vegetarian + Vegan. The empty-state message appeared when no listings matched. |
| US8 | 2: When I select a campus location, then only listings at that location are shown; filters can be combined with dietary tags. | Faye | 11/14/2026 | Partial | Tested pickup location filtering using Tivoli Cafe. Combining a location filter with dietary tags has not yet been tested. |
| US8 | 3: When I click "Clear filters", then all available listings are shown again. | Faye | 11/14/2026 | Passed | Clear Filters restored all available listings. |