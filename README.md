# gbpwd

A simple and modern way of creating passwords.

## About

gbpwd comes from a problem: secure passwords requires **complexity** (due to entropy), **uniqueness** (due to database breaches that occurs every year) and **ease of storage** or remember (due to the need of reusing your password to login each time). To do it manually is exaustitng and requires some effort.

With gbpwd you can create very complex passwords (including upper and lower case letters, numbers and special characters), unique password for each account by setting a human-readable public token and easy-to-retrieve passwords that you can generate again by using your secret master key (password or file) and your token.

## What is the master key?

The master key is your secret that will really make the password creating a secure process. The master key can either be a **password** or a **file**. 

## What about the token? How can it really be public?

To create the passwords gbpwd uses KDF (key derivation function) algorithms that use a public (not secret) data called salt to derive your final password based on your master key. The supported functions are secure and cryptographically tested for many years. This makes it possible to create secure passwords based on a secret data part and a public too.

