
-------
account
-------

- account:count id 
- account:userlist set(id)
- account:email:[email] id

- account:[id]: hash

  - email string
  - password string // md5(password..salt)
  - sex string
  - age string
  - desc string
  - image string
  - status enum(open/close/delete)
  - mobile string

- account:[id]:lastlogin hash

  - ip string
  - time string

- account:[id]:avatars set(id)

