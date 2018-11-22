# orm

```python
import records

db = records.Database('postgres://...')
rows = db.query('select * from active_users')    # or db.query_file('sqls/active-users.sql')

rows[0]

for r in rows:
    print(r.name, r.user_email)
    
rows.all()

rows.first()

```