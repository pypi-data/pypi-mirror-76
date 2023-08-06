# Lollygag

Lollygag is a CLI based Task Manager.

## Core Concepts

### Tasks

Tasks are the core construct of Lollygag. A task has the following fields:

* __id__ - auto incrementing int
* __title__ - String
* __due__ - DateTime
* __description__ - String
* __priority__ - Integer corresponding to a priority value:
    * 0 - "low"
    * 1 - "medium"
    * 2 - "high"
    * 3 - "critical"
* __status__ = Integer corresponding to a status value:
    * 0 - "Open"
    * 1 - "In Progress"
    * 2 - "Blocked"
    * 3 - "Complete"

To add a task, ensure the tasks box has focus (tab / shift-tab to switch focus) and press `ctrl+a`.  To delete a task, press ctrl+d

### Views

to organize how you navigate your tasks, a user can create arbitrary views that are built using SQL.  To create a view, ensure the views box has focus, then press `ctrl+a`.  There are three fields to fill out:

* __Title__: The title for this view
* __Query__: The sql query to perform
* __Sort Order__: An integer used to sort the order of your views. (lower numbers are sorted higher, i.e. 1 is higher on the list than 2, )

#### View SQL Queries

Basic View SQL queries should take the form of:
```sql
select * from tasks where {your criteria}
```

Using the available fields from a Task listed above, we can craft a query to filter all open critical priority items due today:

```sql
# Open Critical tasks due today (sqlite)
select * from tasks where priority = 3 and date(due) = date('now') and status = 0
```

### Other shortcuts

* To save a task or view without needing to tab to ok, `ctrl+s`
* to abandon editing or creating a view or task, `ctrl+w`
* `ctrl+c` to quit