from payments.models import *
from django.utils.timezone import  timedelta
import pytz
from django.utils import timezone
import datetime
from django.db.models import Sum

class SortUserBalance:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not '/admin/' in request.path:
            now = timezone.now()
            expired_date = now.astimezone() - timedelta(hours=24)
            model_list = Crypto.objects.all().filter(created_at__lt=expired_date, user=request.user)    
            for model_item in model_list:
                if model_item.status == "Accepted" and model_item.plan == 'BASIC PLAN':
                    # self.handle_investment(request,model_item)
                    model_item.status = "Completed"
                    model_item.save()
    
            now = timezone.now()
            expired_date = now.astimezone() - timedelta(hours=24)
            model_list = Crypto.objects.all().filter(created_at__lt=expired_date, user=request.user)    
            for model_item in model_list:
                if model_item.status == "Accepted" and model_item.plan == 'STANDARD PLAN':
                    # self.handle_investment(request,model_item)
                    model_item.status = "Completed"
                    model_item.save()
        
            now = timezone.now()
            expired_date = now.astimezone() - timedelta(hours=24)
            model_list = Crypto.objects.all().filter(created_at__lt=expired_date, user=request.user)    
            for model_item in model_list:
                if model_item.status == "Accepted" and model_item.plan == 'ULTRA PLAN':
                    # self.handle_investment(request,model_item)
                    model_item.status = "Completed"
                    model_item.save()

            now = timezone.now()
            expired_date = now.astimezone() - timedelta(hours=24)
            model_list = Crypto.objects.all().filter(created_at__lt=expired_date, user=request.user)    
            for model_item in model_list:
                if model_item.status == "Accepted" and model_item.plan == 'PROFESSIONAL PLAN':
                    # self.handle_investment(request,model_item)
                    model_item.status = "Completed"
                    model_item.save()
            
            now = timezone.now()
            expired_date = now.astimezone() - timedelta(hours=24)
            model_list = Crypto.objects.all().filter(created_at__lt=expired_date, user=request.user)    
            for model_item in model_list:
                if model_item.status == "Accepted" and model_item.plan == 'MEGA PLAN':
                    # self.handle_investment(request,model_item)
                    model_item.status = "Completed"
                    model_item.save()

            now = timezone.now()
            expired_date = now.astimezone() - timedelta(hours=24)
            model_list = Crypto.objects.all().filter(created_at__lt=expired_date, user=request.user)    
            for model_item in model_list:
                if model_item.status == "Accepted" and model_item.plan == 'COMPOUNDING PLAN':
                    # self.handle_investment(request,model_item)
                    model_item.status = "Completed"
                    model_item.save()
                    
            
            total = 0
            w = 0
            percent = 0
            roi = 0
            f = Crypto_Withdrawal_Request.objects.filter(user=request.user, status='Paid', remove_from_balance=False)
            if f.exists():
                w = sum([i.amount for i in f])
                f.update(remove_from_balance=True)
                
            d = Crypto.objects.filter(user=request.user, status='Completed', added_to_balance=False).order_by("-created_at")
            if d.exists():
                total = sum([b.amount for b in d])
                for b in d:
                    total += int(b.amount) 
                    
                    
                    if d.filter(plan = "BASIC PLAN").exists():
                        percent += (0.05 * (int(b.amount))) + (int(b.amount))
                        roi += (0.05 * (int(b.amount)))
                    if d.filter(plan = "STANDARD PLAN").exists():
                        percent += (0.07 * (int(b.amount))) + (int(b.amount))
                        roi += (0.07 * (int(b.amount)))
                    if d.filter(plan = "ULTRA PLAN").exists():
                        percent += (0.06 * (int(b.amount))) + (int(b.amount))
                        roi += (0.06 * (int(b.amount)))
                    if d.filter(plan = "PROFESSIONAL PLAN").exists():
                        percent += (0.08 * (int(b.amount))) + (int(b.amount))
                        roi += (0.08 * (int(b.amount)))
                    if d.filter(plan = "MEGA PLAN").exists():
                        percent += (0.12 * (int(b.amount))) + (int(b.amount))
                        roi += (0.12 * (int(b.amount)))
                    if d.filter(plan = "COMPOUNDING PLAN").exists():
                        percent += (0.18 * (int(b.amount))) + (int(b.amount))
                        roi += (0.18 * (int(b.amount)))
                    
                d.update(added_to_balance=True)
                
            if total > 0:
                bb = (w) + (percent)
                request.user.crypto_balance = request.user.crypto_balance + int(roi)
                request.user.total_earned = request.user.total_earned + int(roi)
                request.user.invested_total = request.user.invested_total + int(roi)
                request.user.save()
            if w > 0:
                request.user.crypto_balance = request.user.crypto_balance - int(w)
                request.user.save()
        response = self.get_response(request)

        return response
        
    # def handle_investment(self,  request,crypto_object):
    #     if crypto_object.investment_type == "Payment Account":
    #         # Remove amount from crypto balance
    #         request.user.crypto_balance -= crypto_object.amount
    #         request.user.save()

    #         # Add amount to invested total
    #         request.user.invested_total += crypto_object.amount
    #         request.user.save()

    #         # Calculate and add ROI after the specified duration
    #         # if (timezone.now() - crypto_object.created_at).total_seconds() >= crypto_object.duration_in_hours * 3600:
    #         #     # Your ROI calculation logic here
    #         #     roi_amount = calculate_roi(crypto_object.amount, crypto_object.plan)

    #         #     # Add ROI to total earned
    #         #     request.user.total_earned += roi_amount
    #         #     request.user.save()

    #         #     # Add the original invested amount plus ROI back to crypto balance
    #         #     request.user.crypto_balance += crypto_object.amount + roi_amount
    #         #     request.user.save()

    #         # # Mark the investment as completed
    #         # crypto_object.status = "Completed"
    #         crypto_object.save()

    def calculate_roi(self, amount, plan):
        # Your ROI calculation logic based on the plan
        # Example: Replace this with your actual ROI calculation
        if plan == "BASIC PLAN":
            return 0.05 * amount
        elif plan == "STANDARD PLAN":
            return 0.07 * amount
        elif plan == "ULTRA PLAN":
            return 0.06 * amount
        elif plan == "ULTRA PLAN":
            return 0.08 * amount
        elif plan == "ULTRA PLAN":
            return 0.12 * amount
        elif plan == "ULTRA PLAN":
            return 0.18 * amount
        else:
            return 0.0
