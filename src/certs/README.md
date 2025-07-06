## Генерация ключей
Удостоверьтесь в наличии установленной программы openssl, в случае отсутствия установите: https://slproweb.com/products/Win32OpenSSL.html

Перейдите в директорию ./NullReceiver-server/src/certs

```shell
# Чтобы сгенерировать приватный ключ RSA, размером 2048
openssl genrsa -out jwt_private.pem 2048
```

```shell
# Чтобы сгенерировать публичный ключ RSA на основе приватного
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt_public.pem
```