## Alembic Guide

### Initialize Alembic

```bash
alembic init migrations
```

### Create a Migration

```bash
alembic revision --autogenerate -m "Initial migration"
```

### Apply Migrations

```bash
alembic upgrade head
```
### Check Current Migration

```bash
alembic current
```

### Check History

```bash
alembic history
```

### Downgrade Migrations

```bash
alembic downgrade -1
```
