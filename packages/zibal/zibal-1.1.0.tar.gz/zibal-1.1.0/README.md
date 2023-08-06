# Zibal Payment Gateway

[![N|Zibal](https://github.com/zibalco/zibal-opencart-v2.3/raw/master/admin/view/image/payment/zibal.png)](https://github.com/zibalco/zibal-opencart-v2.3/raw/master/admin/view/image/payment/zibal.png)



### Installation

Zibal Payment pacakge requires [Requests](https://pypi.org/project/requests/) to run.

Install the package using pip

```sh
$ pip install zibal
```

For upgrading to newer versions

```sh
$ pip install zibal --upgrade
```

### Usage

You can send a request and verify your payment using this package. Also you can use this package to translate the result codes to printable messages
Pass your merchant_id and callback url while creating a zibal instance

```python
import zibal.zibal as zibal

merchant_id = 'Your merchant id, use zibal for testing'
callback_url = 'https://yourdomain.com/callbackUrl'

zb = zibal.zibal(merchant_id, callback_url)
amount = 30000 # IRR
request_to_zibal = zb.request(amount)
```

Now you can access the parameters using
```python
track_id = request_to_zibal['trackId']
request_result_code = request_to_zibal['result']
```
Pass the result code to the translator function "requeset_result(result_code)" to create printable output
Python3 example:
```python
print(zb.request_result(request_result_code))
```
Verify the payment using the verify function
```python
verify_zibal = zb.verify(track_id)
verify_result = verify_zibal['result']
```
Now you can access the parameters using
```python
ref_number = verify_zibal['refNumber']
verify_result_code = verify_zibal['result']
```
Pass the result code to the translator function "verify_result(result_code)" to create printable output
Python3 example:
```python
print(zb.verify_result(verify_result_code))
```
