from django.urls import path

from myBoard.myboard_utest.views import MyBoardUtestPaymentsAPI
from myBoard.myboard_utest.views import MyBoardUtestProfileAPI
from myBoard.myboard_utest.views import MyBoardUtestBugsInTestCycleAPI
from myBoard.myboard_utest.views import MyBoardUtestTestcasesInTestCycleAPI
from myBoard.myboard_utest.views import MyBoardUtestPreApprovePaymentAPI
from myBoard.myboard_utest.views import MyBoardUtestActivityAPI

urlpatterns = [
    path('myboard_utest/payments/', MyBoardUtestPaymentsAPI.as_view(), name='utest_payments'),
    path('myboard_utest/profile/', MyBoardUtestProfileAPI.as_view(), name='utest_payments'),
    path('myboard_utest/bugsInCycle/', MyBoardUtestBugsInTestCycleAPI.as_view(), name='utest_bugs_in_cycles'),
    path('myboard_utest/testcasesInCycle/', MyBoardUtestTestcasesInTestCycleAPI.as_view(), name='utest_testcase_in_cycles'),
    path('myboard_utest/preapprovePayment/', MyBoardUtestPreApprovePaymentAPI.as_view(), name='utest_pre_approve_payment'),
    path('myboard_utest/activity/', MyBoardUtestActivityAPI.as_view(), name='utest_pre_approve_payment'),
]
