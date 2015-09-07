# Policy Control

Policy Control is a kind of simple script used to make flow control easier,
especially when your transaction contains asynchronous procedure. This little
script can help you construct long and complicated but mostly sequenced
transaction policy.

There isn't a context manager for you so you have to implement it by yourself.
The `context` provided `__getstate__` and `__setstate__` method so it's very
handy to store it in persistent interface using `pickle` library.

## How to use it

A policy is such a file having syntax like this, assumed `example.policy`:

```
load!: policy_test
assert!: is_authenticated

await: modify_email -> address
apply: send_verf_email(address)

await: verf_email_recv
apply: save_current_user_info(address)
```

And there is a thing called **context** to record the state the policy
transaction is running in. You have to store it in your own way to ensure the
policy transaction to run normally.

When you want to run the policy file anew:

```
p = policy.load(file("example.policy"))
p.provide("modify_email", "john@example.com")
p.resume()

c = p.context
db.store(pickle.dumps(c))
```

A few days later finally you discovered a verification email in you mailbox:

```
p = policy.load(file("example.policy"))
# equivalent: p.load_context(db.retrieve())
p.context = db.retrieve()
p.provide("verf_email_recv")
p.resume()
```

And that's it. For more information about policy, read test samples in
`/tests/policy_test.py`.

## Todos

I don't have many plans. Depending on my mood, maybe I will or will not:

* implement flow control command like `if`/`for` (Under consideration)
* implement some operators to complete simple operations (Never)
* make the policy script Turing complete and generic (Never)
* fix bugs (Sure)

