# from datetime import datetime, timedelta

# from django.conf import settings
# from django.db.models import Q

# from rakamin_test.api.response import ErrorResponse, error_response

# from rest_framework import request, status
# from rest_framework.response import Response
# from rest_framework.views import APIView

# from rakamin_test.apps.users.model import User
# from rakamin_test.core.utils import PaginatorPage


# class IndexTransaction(APIView):
#     '''
#     url: /api/transactions?page=1&limit=5&acc_number=405811371&type=Deposit&start=2022-12-15&end=2022-12-19\
#     :param page: Number of page
#     :param limit: Limit data per page
#     :param acc_number: account number user, delete param is true
#     :param type: type of transaction (Deposit/Withdraw), delete param is true
#     :param start: Start date (Format YYYY-MM-DD), delete param is true
#     :param end: End date (Format YYYY-MM-DD), delete param is true
#     default param if just page and limit is 1 month back
#     '''

#     def get(self, request: request) -> Response:
#         transaction_list = []
#         transactions = None
#         acc_number = request.GET.get('acc_number')
#         limit = int(request.GET.get('limit', 1))
#         page = request.GET.get('page', 1)
#         types = request.GET.get('type')
#         if types:
#             types = [value for value, name in TransactionLog.STATUS if name == types][0]
#         start = request.GET.get('start')
#         end = request.GET.get('end')

#         if start and end:
#             is_date_valid, message, dates = self.check_date_filter(start, end)
#             if not is_date_valid:
#                 return error_response(message)
#             start = dates['start']
#             end = dates['end']
#         else:
#             start = datetime.now() - timedelta(days=30)
#             end = datetime.now()

#         if acc_number:
#             filters = Q(from_user__account_number=acc_number) | Q(status=types) | Q(created__range=[start, end])
#         elif types:
#             filters = Q(status=types) | Q(created__range=[start, end])
#         elif start and end:
#             filters = Q(created__range=[start, end])
#         else:
#             filters = Q(created__range=[start, end])

#         # default value is 1 month back
#         transactions = TransactionLog.objects.select_related('from_user').filter(filters)
#         paginator = PaginatorPage(transactions, page, step=limit)
#         for transaction in paginator.objects:
#             transaction_list.append(self.serialize_data(transaction))

#         data = {
#             'limit': limit,
#             'paginator': {
#                 'next': paginator.next,
#                 'previous': paginator.previous
#             },
#             'data': transaction_list
#         }

#         return Response(data=data, status=status.HTTP_200_OK)

#     def check_date_filter(self, start: str, end: str):
#         date_format = "%Y-%m-%d %H:%M:%S"
#         start = f'{start} 00:00:00'
#         end = f'{end} 23:59:59'
#         start = datetime.strptime(start, date_format)
#         end = datetime.strptime(end, date_format)
#         delta = end - start
#         day_count = delta.days
#         dates = {
#             'start': start,
#             'end': end,
#         }
#         message = None
#         print(day_count)
#         if day_count > settings.MAXIMAL_DAYS_FILTER_TRANSACTION:
#             message = 'Tidak bisa filter lebih dari 3 bulan'
#             return False, message, dates
        
#         if end > (datetime.now() + timedelta(days=1)):
#             message = f'Tidak bisa filter lebih dari {datetime.now()}'
#             return False, message, dates

#         return True, message, dates

#     def serialize_data(self, transaction: TransactionLog) -> dict:
#         user = transaction.from_user
#         data = {
#             "name": user.name,
#             "account_number": user.account_number,
#             "transaction_number": transaction.transaction_number,
#             "charge": transaction.charge,
#             "previous_balance": transaction.previous_balance,
#             "amount": transaction.amount,
#             "after_balance": transaction.after_balance,
#             "created": transaction.created,
#             "type": transaction.get_status_display(),

#         }
#         return data


# class Deposit(APIView):
#     '''
#     Payload:
#         {
#             "user_id": 1,
#             "amount": 2000
#         }
#     Response:
#     {
#         "messages": "Proses deposit berhasil",
#         "is_success": true,
#         "data": {
#             "user_id": 1,
#             "name": "aden",
#             "email": "aden3@gmail.com",
#             "account_number": "405811371",
#             "previous_balance": 10000,
#             "amount": 2000,
#             "after_balance": 12000,
#             "transaction_number": "PR7056CP1"
#         }
#     }
#     '''

#     def post(self, request: request) -> Response:
#         form = DepositForm(data=request.data or None)
#         if form.is_valid():
#             user, transaction_log = form.save()
#             data ={
#                 'messages': f'Proses deposit berhasil',
#                 'is_success': True
#             }
#             data['data'] = self.serialize_data(user, transaction_log)
#             return Response(data=data, status=status.HTTP_200_OK)
#         return ErrorResponse(form=form)

#     def serialize_data(self, user: User, transaction_log: TransactionLog) -> dict:
#         data = {
#             "user_id": user.id,
#             "name": user.name,
#             "email": user.email,
#             "account_number": user.account_number,
#             "previous_balance": transaction_log.previous_balance,
#             "amount": transaction_log.amount,
#             "after_balance": transaction_log.after_balance,
#             "transaction_number": transaction_log.transaction_number,
#         }

#         return data


# class Withdraw(APIView):

#     def post(self, request: request) -> Response:
#         form = WithdrawForm(data=request.data or None)
#         if form.is_valid():
#             user, transaction_log = form.save()
#             data ={
#                 'messages': f'Proses withdraw berhasil',
#                 'is_success': True
#             }
#             data['data'] = self.serialize_data(user, transaction_log)
#             return Response(data=data, status=status.HTTP_200_OK)
#         return ErrorResponse(form=form)

#     def serialize_data(self, user: User, transaction_log: TransactionLog) -> dict:
#         data = {
#             "user_id": user.id,
#             "name": user.name,
#             "email": user.email,
#             "account_number": user.account_number,
#             "previous_balance": transaction_log.previous_balance,
#             "amount": transaction_log.amount,
#             "charge": transaction_log.charge,
#             "after_balance": transaction_log.after_balance,
#             "transaction_number": transaction_log.transaction_number,
#         }

#         return data