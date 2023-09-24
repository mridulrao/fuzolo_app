import razorpay

client = razorpay.Client(auth=("rzp_test_MUFWJzfALmtlEZ", "2InpKrmuuTFeCxYzlAfRU9Np"))

def get_payment_details(amount):
    amount = int(amount + "00")

    DATA = {
    "amount": amount,
    "currency": "INR",
    "receipt": "receipt#1",
    "notes": {
        "key1": "value3",
        "key2": "value2"
        }
    }
    order = client.order.create(data=DATA)

    payment_details = {
        'order_id' : order['id'],
        'amount' : str(amount)
    }

    return payment_details

def verify_payment_status(payment_details):
    flag = client.utility.verify_payment_signature({'razorpay_order_id': payment_details['order_id'],
                                                    'razorpay_payment_id': payment_details['payment_id'],
                                                    'razorpay_signature': payment_details['signature'] })

    return flag