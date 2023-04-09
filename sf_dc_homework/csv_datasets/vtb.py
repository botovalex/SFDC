from datetime import datetime, timedelta

now = datetime.strptime("2021-11-19 15:05", "%Y-%m-%d %H:%M")
end_period_1 = datetime.strptime("2021-12-02 23:59", "%Y-%m-%d %H:%M")
start_period_2 = end_period_1 + timedelta(hours=7)
end_period_2 = datetime.strptime("2021-12-16 23:59", "%Y-%m-%d %H:%M")
# start_period_3 = end_period_2 + timedelta(hours=7)
# end_period_3 = datetime.strptime("2021-12-13 23:59", "%Y-%m-%d %H:%M")

test_period_1 = end_period_1 - timedelta(days=2, hours=12)
test_period_2 = end_period_2 - timedelta(days=2, hours=12)
course_period_2 = start_period_2 + timedelta(hours=6)
# test_period_3 = end_period_3 - timedelta(days=2, hours=12)
# course_period_3 = start_period_3 + timedelta(hours=6)

print('time_now:', now)
print('назначить тесты периода_1:', round((test_period_1 - now).total_seconds() / 3600 ))
print('назначить курсы периода_2:', round((start_period_2 - now).total_seconds() / 3600 ))
print('назначить тесты периода_2:', round((test_period_2 - now).total_seconds() / 3600 ))
# print('назначить курсы периода_3:', round((start_period_3 - now).total_seconds() / 3600 ))
# print('назначить тесты периода_3:', round((test_period_3 - now).total_seconds() / 3600 ))
