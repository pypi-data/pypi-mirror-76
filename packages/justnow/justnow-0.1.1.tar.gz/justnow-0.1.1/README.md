# justnow

`justnow` is a systemd.timer inspired event parser in pure Python. The library consists of a [lark](https://github.com/lark-parser/lark) grammar definition and some code to parse and generate datetimes.

## Usage

Below is a snippet of the basic usage.

```python
import datetime

from justnow.parser import EventParser

reference_date = datetime.datetime(2020, 1, 1)

# "sat *-*-* 14:00:00" => Generate all Saturdays at 14:00:00
parser = EventParser("sat *-*-* 14:00:00", reference_date=reference_date)

next(parser)  # datetime.datetime(2020, 1, 4, 14, 0)

# "sat *-02-29" => Generate all Saturdays which occur on a leap year
parser = EventParser("sat *-02-29", reference_date=reference_date)

list(parser.get_next_n(limit=2))  # [datetime.datetime(2020, 2, 29, 0, 0), datetime.datetime(2048, 2, 29, 0, 0)]
```

The `justnow` grammar defines a `time event` and is made of up 3 sections:

### Weekday section

This section allows for a comma separated list of weekday names and weekday ranges.

#### Weekday names

The following are valid tokens for the weekday section:

- mon
- tue
- wed
- thu
- fri
- Mon
- Tue
- Wed
- Thu
- Fri
- monday
- tuesday
- wednesday
- thursday
- friday

#### Weekday ranges

A weekday range consists of two day names separated by two full stops.

For example  `mon..wed` will evaluate into mon, tue and wed.

### Date section

The date section is made up of 3 sub sections, namely:

- A year section
- A month section
- A day section

Each of the above sub sections can be either:

- One of more fixed length strings made up of integers separated by a comma. The length is 4 for years and 2 for months and days.
- A wildcard `*`

### Time section

The time section is made up of 3 sub sections, namely:

- A hour section
- A minute section
- A second section

Each of the above sub sections can be either:

- One of more strings made up of 2 integers separated by a comma.
- A wildcard `*`

### Named Events

`justnow` also supports a set of built in named events including:

- `@minutely`
- `@hourly`
- `@daily`
- `@monthly`
- `@weekly`
- `@yearly`
- `@quarterly`
- `@semiannually`
- `@annually`