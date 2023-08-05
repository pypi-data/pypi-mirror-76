# remapdict

Really simple Python function for arbitrarily remapping dictionary keys value pairs with arbitrary transformations and convenience configuration like passthrough and error handling.

## Documentation

Example usage:

```python
user = {
  'email': 'email@email.com',
  'firstName': 'Foo',
  'lastName': 'Bar',
  'status': 'active',
  'type': 'administrator',
  'tenantId': 1,
}

payload = remap_dict(user,
  const={'password': 'password'},
  passthrough={
    'email',
    'status',
    'type',
  },
  mapper={
    'first_name': 'firstName',
    'last_name': 'lastName',
    'tenant_id': 'tenantId',
  },
  transformer={
    'full_name': lambda x: f'{x["firstName"]} {x["lastName"]}'
  }
)

>>> payload
{
  'status': 'active',
  'email': 'email@email.com',
  'type': 'administrator',
  'password': 'password',
  'first_name': 'Foo',
  'last_name': 'Bar',
  'tenant_id': 1,
  'full_name': 'Foo Bar'
}
```
