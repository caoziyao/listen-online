# orm

```python
import orm 

db = orm.Database('postgres://...')
rows = db.query('select * from tb_user') 

rows[0]

for r in rows:
    print(r.id, r.username)
    
rows.all()

rows.first()

```
