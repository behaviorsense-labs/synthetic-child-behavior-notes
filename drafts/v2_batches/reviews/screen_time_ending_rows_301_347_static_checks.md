# Static Validation Report

Source file: `drafts/v2_batches/screen_time_ending_rows_301_347.csv`

Total rows: 47

## Schema Compliance

- Row 332 | `setting` = 'public-playground' — not in allowed values: ['daycare', 'home', 'other-public', 'outdoor', 'public-restaurant', 'public-store', 'public-transport', 'relative-home', 'school-classroom', 'school-playground']
- Row 305 | `consequence_present` = 'ending screen time' — not in allowed values: ['no', 'yes']
- Row 311 | `consequence_present` = 'desire for a snack after watching' — not in allowed values: ['no', 'yes']
- Row 319 | `consequence_present` = 'end of playtime' — not in allowed values: ['no', 'yes']
- Row 305 | `risk_level` = 'easy' — not in allowed values: ['high', 'low', 'moderate']
- Row 311 | `risk_level` = 'easy' — not in allowed values: ['high', 'low', 'moderate']
- Row 319 | `risk_level` = 'easy' — not in allowed values: ['high', 'low', 'moderate']
- Row 341 | `risk_level` = 'medium' — not in allowed values: ['high', 'low', 'moderate']
- Row 342 | `risk_level` = 'medium' — not in allowed values: ['high', 'low', 'moderate']
- Row 343 | `risk_level` = 'medium' — not in allowed values: ['high', 'low', 'moderate']
- Row 344 | `risk_level` = 'easy' — not in allowed values: ['high', 'low', 'moderate']
- Row 345 | `risk_level` = 'medium' — not in allowed values: ['high', 'low', 'moderate']
- Row 346 | `risk_level` = 'complex' — not in allowed values: ['high', 'low', 'moderate']
- Row 347 | `risk_level` = 'medium' — not in allowed values: ['high', 'low', 'moderate']
- Row 305 | `difficulty_level` = 'low' — not in allowed values: ['complex', 'easy', 'medium']
- Row 311 | `difficulty_level` = 'low' — not in allowed values: ['complex', 'easy', 'medium']
- Row 319 | `difficulty_level` = 'low' — not in allowed values: ['complex', 'easy', 'medium']
- Row 343 | `difficulty_level` = 'low' — not in allowed values: ['complex', 'easy', 'medium']
- Row 344 | `difficulty_level` = 'low' — not in allowed values: ['complex', 'easy', 'medium']
- Row 346 | `difficulty_level` = 'high' — not in allowed values: ['complex', 'easy', 'medium']
- Row 305 | `ambiguity_level` = 'train' — not in allowed values: ['high', 'low', 'medium']
- Row 311 | `ambiguity_level` = 'train' — not in allowed values: ['high', 'low', 'medium']
- Row 319 | `ambiguity_level` = 'test' — not in allowed values: ['high', 'low', 'medium']
- Row 341 | `ambiguity_level` = 'train' — not in allowed values: ['high', 'low', 'medium']
- Row 342 | `ambiguity_level` = 'train' — not in allowed values: ['high', 'low', 'medium']
- Row 343 | `ambiguity_level` = 'train' — not in allowed values: ['high', 'low', 'medium']
- Row 344 | `ambiguity_level` = 'train' — not in allowed values: ['high', 'low', 'medium']
- Row 345 | `ambiguity_level` = 'validation' — not in allowed values: ['high', 'low', 'medium']
- Row 346 | `ambiguity_level` = 'test' — not in allowed values: ['high', 'low', 'medium']
- Row 347 | `ambiguity_level` = 'test' — not in allowed values: ['high', 'low', 'medium']
- Row 305 | `split` = 'yes' — not in allowed values: ['test', 'train', 'validation']
- Row 311 | `split` = 'yes' — not in allowed values: ['test', 'train', 'validation']
- Row 319 | `split` = 'yes' — not in allowed values: ['test', 'train', 'validation']
- Row 341 | `split` = 'yes' — not in allowed values: ['test', 'train', 'validation']
- Row 342 | `split` = 'yes' — not in allowed values: ['test', 'train', 'validation']
- Row 343 | `split` = 'yes' — not in allowed values: ['test', 'train', 'validation']
- Row 344 | `split` = 'yes' — not in allowed values: ['test', 'train', 'validation']
- Row 345 | `split` = 'yes' — not in allowed values: ['test', 'train', 'validation']
- Row 346 | `split` = 'yes' — not in allowed values: ['test', 'train', 'validation']
- Row 347 | `split` = 'yes' — not in allowed values: ['test', 'train', 'validation']
- Row 305 | `synthetic_flag` = 'draft' — not in allowed values: ['yes']
- Row 311 | `synthetic_flag` = 'draft' — not in allowed values: ['yes']
- Row 319 | `synthetic_flag` = 'draft' — not in allowed values: ['yes']
- Row 341 | `synthetic_flag` = 'draft' — not in allowed values: ['yes']
- Row 342 | `synthetic_flag` = 'draft' — not in allowed values: ['yes']
- Row 343 | `synthetic_flag` = 'draft' — not in allowed values: ['yes']
- Row 344 | `synthetic_flag` = 'draft' — not in allowed values: ['yes']
- Row 345 | `synthetic_flag` = 'draft' — not in allowed values: ['yes']
- Row 346 | `synthetic_flag` = 'draft' — not in allowed values: ['yes']
- Row 347 | `synthetic_flag` = 'draft' — not in allowed values: ['yes']
- Row 305 | `review_status` = '' — not in allowed values: ['draft']
- Row 311 | `review_status` = '' — not in allowed values: ['draft']
- Row 319 | `review_status` = '' — not in allowed values: ['draft']
- Row 341 | `review_status` = '' — not in allowed values: ['draft']
- Row 342 | `review_status` = '' — not in allowed values: ['draft']
- Row 343 | `review_status` = '' — not in allowed values: ['draft']
- Row 344 | `review_status` = '' — not in allowed values: ['draft']
- Row 345 | `review_status` = '' — not in allowed values: ['draft']
- Row 346 | `review_status` = '' — not in allowed values: ['draft']
- Row 347 | `review_status` = '' — not in allowed values: ['draft']

## Consequence Field Check

- Row 301 | consequence_present=yes but consequence is vague or empty: 'Child eventually agreed and turned off the screen after a brief discussion.'
- Row 302 | consequence_present=yes but consequence is vague or empty: 'Sibling picked up the controller and suggested playing a different game together.'
- Row 304 | consequence_present=yes but consequence is vague or empty: 'Child paused the game after being offered a snack break.'
- Row 307 | consequence_present=yes but consequence is vague or empty: 'Caregiver safely helped the child down and put the tablet away.'
- Row 308 | consequence_present=yes but consequence is vague or empty: 'Caregiver offered a comforting toy and sang a song to distract them.'
- Row 310 | consequence_present=yes but consequence is vague or empty: 'Child finally calmed down and helped clean up after a discussion.'
- Row 312 | consequence_present=yes but consequence is vague or empty: 'Caregiver calmly unlocked the door and discussed sharing space with family.'
- Row 313 | consequence_present=yes but consequence is vague or empty: 'Caregiver turned off the console and redirected to board games.'
- Row 314 | consequence_present=yes but consequence is vague or empty: 'Caregiver reassured the child and suggested singing a song together.'
- Row 315 | consequence_present=yes but consequence is vague or empty: 'Caregiver reminded about the rules and suggested reading instead.'
- Row 317 | consequence_present=yes but consequence is vague or empty: 'Child later joined the family activity after a gentle nudge.'
- Row 318 | consequence_present=yes but consequence is vague or empty: 'Caregiver safely intervened and explained why they shouldn't climb.'
- Row 320 | consequence_present=yes but consequence is vague or empty: 'Child began to participate in group discussion after a timeout.'
- Row 323 | consequence_present=yes but consequence is vague or empty: 'Child sat silently in the corner after throwing the remote.'
- Row 325 | consequence_present=yes but consequence is vague or empty: 'Child picked up toys willingly after being reminded of the next activity.'
- Row 326 | consequence_present=yes but consequence is vague or empty: 'Child finally turned it off and joined the group activity after a few reminders.'
- Row 327 | consequence_present=yes but consequence is vague or empty: 'Caregiver quickly redirected them to sit down safely.'
- Row 328 | consequence_present=yes but consequence is vague or empty: 'Child reluctantly started picking up after being asked again.'
- Row 329 | consequence_present=yes but consequence is vague or empty: 'Child calmed down after the caregiver offered to read a book.'
- Row 330 | consequence_present=yes but consequence is vague or empty: 'Child picked up speed after seeing a friend join them.'
- Row 331 | consequence_present=yes but consequence is vague or empty: 'Child eventually took a deep breath and sat down at the table.'
- Row 332 | consequence_present=yes but consequence is vague or empty: 'Caregiver found them and brought them to the car after a search.'
- Row 333 | consequence_present=yes but consequence is vague or empty: 'Child apologized after being redirected by the caregiver.'
- Row 335 | consequence_present=yes but consequence is vague or empty: 'Child sat up and turned off the TV after a gentle reminder.'
- Row 336 | consequence_present=yes but consequence is vague or empty: 'Caregiver caught them and reminded about the rules, leading to a discussion.'
- Row 337 | consequence_present=yes but consequence is vague or empty: 'Child finally agreed to help carry the groceries as a distraction.'
- Row 338 | consequence_present=yes but consequence is vague or empty: 'Child eventually joined for dinner after the caregiver offered dessert later.'
- Row 339 | consequence_present=yes but consequence is vague or empty: 'Child calmed down after the caregiver offered to play their favorite game next.'
- Row 340 | consequence_present=yes but consequence is vague or empty: 'Child picked up their toy and joined the caregiver after a brief talk.'
- Row 341 | consequence_present=yes but consequence is vague or empty: 'Child finally put the tablet down and joined for dinner after caregiver showed the food.'
- Row 342 | consequence_present=yes but consequence is vague or empty: 'Child eventually turned off the device and started eating lunch.'
- Row 343 | consequence_present=yes but consequence is vague or empty: 'Child turned off the game and greeted friends after a short negotiation.'
- Row 344 | consequence_present=yes but consequence is vague or empty: 'Child picked up their shoes and left with the family after a countdown.'
- Row 345 | consequence_present=yes but consequence is vague or empty: 'Child eventually turned off the TV and went to bed after a timer went off.'
- Row 346 | consequence_present=yes but consequence is vague or empty: 'Child came inside after caregiver gently called them and explained dinner was ready.'
- Row 347 | consequence_present=yes but consequence is vague or empty: 'Child eventually turned off the TV and joined the family after caregiver offered to play their favorite game.'

## Distribution Check

- `risk_level=low` is 29.8% (14 rows) — below target minimum of 50%
- `difficulty_level=easy` is 14.9% (7 rows) — below target minimum of 15%
- `difficulty_level=complex` is 14.9% (7 rows) — below target minimum of 15%
- `ambiguity_level=low` is 27.7% (13 rows) — below target minimum of 30%
- `consequence_present=yes` is 76.6% (36 rows) — above target maximum of 40%
- `consequence_present=no` is 17.0% (8 rows) — below target minimum of 60%

## Near-Duplicate Check

No issues found.

