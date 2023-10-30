from operator import truediv
import razorpay

from fuzolo_pickup.settings import RZP_ACCOUNT_ID, RZP_KEY

client = razorpay.Client(auth=(RZP_ACCOUNT_ID, RZP_KEY))

#database entry
from .models import UserAddPoints

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


def user_rzp_transactions(user, payment_details, amount):
    comment = ''
    points = 0
    if amount == '300':
        comment = 'No plan'
        points = 300
    else:
        comment = 'Basic Plan'
        points = 3000

    try:
        entry = UserAddPoints.objects.create(name = user['name'],
                                            email = user['email'],
                                            phone_number = user['phone_number'],
                                            points = points,
                                            amount = amount,
                                            razorpay_id = payment_details['order_id'],
                                            comment = comment)
        
        return True
    except:
        print("UserAddPoints object not created")

    return False


def verify_user_rzp_transactions(order_id):
    try:
        entry = UserAddPoints.objects.get(razorpay_id = order_id)
        amount = entry.points
        entry.paid = True
        entry.save()

        return True, amount
    except:
        print("Payment cannot be verified")

    return False, '0'

    
