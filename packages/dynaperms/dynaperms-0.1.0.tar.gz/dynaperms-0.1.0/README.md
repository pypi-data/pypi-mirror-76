# Django Dynaperms

Django's [permissions](https://docs.djangoproject.com/en/3.0/topics/auth/default/#permissions-and-authorization) are very useful,
but sometimes authorizations to certain system features can rapidly change based on different needs or need a way to allow
easily expand the number of different ways to check if access should be granted.

Rather than creating/updating/deleting database records, let's just run a function to see if the return value is True or False.


## Example


In `debit_card.perms`, you define a function like below:
``` 

def have_valid_card(user: User) -> bool:
    # Check some API or something

```



In your `settings.py` file
```

AUTHENTICATION_BACKENDS = (
    ...
    'dynaperms.backends.DynamicBackend'
)

...

DYNA_PERMS = {
    'active_payment_method': [
        'credit_card.perms.have_valid_card',
        'debit_card.perms.have_valid_card',
    ]
}
```

And elsewhere in your code, you can simply call:
```
if request.user.has_perm('active_payment_method'):
    # Do something for authorized users.
else:
    # Do something for authenticated users.
```
